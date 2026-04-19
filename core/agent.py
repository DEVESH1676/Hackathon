"""
Agentic Layer v3.0 — Decoupled Agent Architecture

Three specialized agents form the decision pipeline:
  1. TriageAgent:              classify → route/escalate with rationale
  2. ResolutionAgent:          ticket + ranked RAG chunks → structured resolution
  3. AutomationDiscoveryAgent: post-resolution hook → detect repeating patterns

Each agent returns an AgentResult dict with a consistent contract.
"""
import os
import sys
import json
import requests
from datetime import datetime, timedelta
from collections import Counter

import config
from core.embeddings import get_chroma_collection, get_embedding_model


# ──────────────────────────────────────────────────────────────
# Agent 1: TriageAgent (TRIAGE-01, TRIAGE-02)
# ──────────────────────────────────────────────────────────────
class TriageAgent:
    """
    Accepts a ticket + classification result and produces a routing
    decision with rationale. Applies confidence gates and sentiment
    urgency detection.

    Input:  ticket_dict  = {"title": str, "description": str}
            classification = dict from TicketClassifier.classify()
    Output: AgentResult  = {"decision": str, "rationale": str,
                            "route_to": str, "escalate": bool,
                            "urgency_boost": bool}
    """

    URGENCY_KEYWORDS = [
        "urgent", "critical", "down", "outage", "blocked",
        "emergency", "asap", "crashed", "unresponsive", "production",
        "p1", "sev1", "major incident",
    ]

    def run(self, ticket_dict: dict, classification: dict) -> dict:
        """Execute triage logic and return routing decision."""
        title = ticket_dict.get("title", "")
        description = ticket_dict.get("description", "")
        text = f"{title} {description}".lower()

        confidence = classification.get("confidence", 0.0)
        method = classification.get("method", "centroid")
        is_novel = classification.get("is_novel", False)
        category = classification.get("category", "Unknown")
        department = classification.get("department", config.ROUTING.get("Unknown", "General Support L1"))

        # ── Sentiment / Urgency check (TRIAGE-02) ──
        urgency_hits = [kw for kw in self.URGENCY_KEYWORDS if kw in text]
        urgency_boost = len(urgency_hits) > 0

        # ── Confidence-gated routing (TRIAGE-01) ──
        if is_novel:
            decision = "ESCALATE_NOVEL"
            rationale = (
                f"Ticket has no precedent in the knowledge base (novel detection). "
                f"Cannot auto-route safely."
            )
            escalate = True
            route_to = config.ROUTING.get("Unknown", "General Support L1")

        elif confidence < config.MEDIUM_CONFIDENCE_THRESHOLD:
            decision = "ESCALATE_LOW_CONFIDENCE"
            rationale = (
                f"Classification confidence ({confidence:.0%}) is critically low "
                f"(below {config.MEDIUM_CONFIDENCE_THRESHOLD:.0%}). "
                f"Routing to human triage to prevent misclassification."
            )
            escalate = True
            route_to = config.ROUTING.get("Unknown", "General Support L1")

        elif confidence < config.CONFIDENCE_THRESHOLD:
            decision = "ROUTE_WITH_LLM_ASSIST"
            rationale = (
                f"Medium confidence ({confidence:.0%}) — LLM judge re-classified "
                f"as '{category}'. Routing with advisory flag."
            )
            escalate = False
            route_to = department

        else:
            decision = "AUTO_ROUTE"
            rationale = (
                f"High confidence ({confidence:.0%}) via fast centroid path. "
                f"Auto-routing to {department}."
            )
            escalate = False
            route_to = department

        # Urgency override: boost priority language in rationale
        if urgency_boost and not escalate:
            rationale += (
                f" ⚠ Urgency keywords detected ({', '.join(urgency_hits[:3])}). "
                f"Flagging for priority handling."
            )

        return {
            "decision": decision,
            "rationale": rationale,
            "route_to": route_to,
            "escalate": escalate,
            "urgency_boost": urgency_boost,
            "urgency_keywords": urgency_hits,
        }


# ──────────────────────────────────────────────────────────────
# Agent 2: ResolutionAgent (RESOLVE-01, RESOLVE-02)
# ──────────────────────────────────────────────────────────────
class ResolutionAgent:
    """
    Accepts a ticket + pre-ranked RAG chunks and generates a structured
    step-by-step resolution via LLM, plus a confidence score.

    Input:  ticket_dict   = {"title": str, "description": str}
            ranked_chunks = list of dicts from rag._rank_retrieved_chunks()
    Output: AgentResult   = {"resolution_steps": list[str],
                             "confidence": float,
                             "source_ids": list[str],
                             "raw_text": str}
    """

    def run(self, ticket_dict: dict, ranked_chunks: list) -> dict:
        """Generate resolution from ranked evidence."""
        title = ticket_dict.get("title", "")
        description = ticket_dict.get("description", "")

        if not ranked_chunks:
            return {
                "resolution_steps": ["No similar tickets found. Manual investigation required."],
                "confidence": 0.0,
                "source_ids": [],
                "raw_text": "No evidence available for resolution generation.",
            }

        # Build context from ranked chunks
        context_parts = []
        source_ids = []
        for i, chunk in enumerate(ranked_chunks[:5]):
            source_ids.append(chunk["id"])
            context_parts.append(
                f"--- Evidence {i+1} (Score: {chunk['final_score']:.2f}) ---\n"
                f"Issue: {chunk['document'][:200]}\n"
                f"Resolution: {chunk['metadata'].get('resolution', 'N/A')}\n"
            )

        context = "\n".join(context_parts)

        # Build prompt for structured resolution
        prompt = f"""You are an Expert L3 IT Support Engineer.
Based on the ranked evidence below, generate a structured resolution for the new ticket.

## Ranked Evidence:
{context}

## New Ticket:
Title: {title}
Description: {description}

## Instructions:
Return ONLY a JSON object with this exact structure (no markdown fences):
{{"steps": ["Step 1: ...", "Step 2: ...", "Step 3: ..."], "summary": "One-line summary of the fix"}}
"""

        # Call LLM
        raw_text = self._call_llm(prompt)

        # Parse structured response
        steps = []
        try:
            clean = raw_text.strip()
            if clean.startswith("```"):
                clean = clean.split("\n", 1)[1].rsplit("```", 1)[0].strip()
            parsed = json.loads(clean)
            steps = parsed.get("steps", [])
        except (json.JSONDecodeError, Exception):
            # Fallback: treat raw text as the resolution
            steps = [line.strip() for line in raw_text.split("\n") if line.strip()]

        # Resolution confidence = average final_score of input chunks (RESOLVE-02)
        avg_score = sum(c["final_score"] for c in ranked_chunks[:5]) / len(ranked_chunks[:5])

        return {
            "resolution_steps": steps,
            "confidence": round(avg_score, 4),
            "source_ids": source_ids,
            "raw_text": raw_text,
        }

    def _call_llm(self, prompt: str) -> str:
        """Call Groq or Ollama for resolution generation."""
        try:
            if config.USE_GROQ and config.GROQ_API_KEY:
                resp = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {config.GROQ_API_KEY}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": config.GROQ_MODEL,
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.2,
                        "max_tokens": 500,
                    },
                    timeout=15,
                )
                resp.raise_for_status()
                return resp.json()["choices"][0]["message"]["content"].strip()
            else:
                resp = requests.post(
                    f"{config.OLLAMA_BASE_URL}/api/chat",
                    json={
                        "model": config.OLLAMA_MODEL,
                        "messages": [{"role": "user", "content": prompt}],
                        "stream": False,
                        "options": {"temperature": 0.2},
                    },
                    timeout=5,
                )
                if resp.status_code == 200:
                    return resp.json().get("message", {}).get("content", "").strip()
                return f"Error: Ollama returned HTTP {resp.status_code}"
        except Exception as e:
            return f"LLM call failed: {str(e)}"


# ──────────────────────────────────────────────────────────────
# Agent 3: AutomationDiscoveryAgent (AUTODISC-01, AUTODISC-02)
# ──────────────────────────────────────────────────────────────
class AutomationDiscoveryAgent:
    """
    Post-resolution hook that checks for repeating patterns.
    Only fires AFTER a resolution has been generated — never during triage.

    Input:  resolved_ticket = {"ticket_id": str, "category": str,
                               "title": str, "description": str,
                               "resolution": str}
    Output: AgentResult     = {"should_automate": bool,
                               "pattern_count": int,
                               "matching_ids": list[str],
                               "suggested_runbook": str}
    """

    def __init__(self):
        self.collection = get_chroma_collection()
        self.model = get_embedding_model()

    def run(self, resolved_ticket: dict) -> dict:
        """Check for automation-worthy patterns post-resolution."""
        title = resolved_ticket.get("title", "")
        description = resolved_ticket.get("description", "")
        category = resolved_ticket.get("category", "Unknown")
        resolution = resolved_ticket.get("resolution", "")

        ticket_text = f"{title} {description}"
        embedding = self.model.encode(ticket_text).tolist()

        # Query for similar tickets in the SAME category (AUTODISC-02)
        try:
            results = self.collection.query(
                query_embeddings=[embedding],
                n_results=10,
                where={"category": category},
                include=["documents", "metadatas", "distances"],
            )
        except Exception:
            # Fallback: query without category filter
            results = self.collection.query(
                query_embeddings=[embedding],
                n_results=10,
                include=["documents", "metadatas", "distances"],
            )

        matching_ids = []
        pattern_resolutions = []

        if results["ids"] and results["ids"][0]:
            for t_id, doc, meta, dist in zip(
                results["ids"][0],
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            ):
                similarity = 1 - dist
                if similarity >= config.SIMILARITY_THRESHOLD:
                    matching_ids.append(t_id)
                    pattern_resolutions.append(
                        meta.get("resolution", doc[:100])
                    )

        should_automate = len(matching_ids) >= config.REPEAT_THRESHOLD

        # Build suggested runbook summary from common resolution patterns
        suggested_runbook = ""
        if should_automate and pattern_resolutions:
            suggested_runbook = (
                f"[AUTO-RUNBOOK] {len(matching_ids)} similar '{category}' tickets detected. "
                f"Common resolution pattern: {pattern_resolutions[0][:200]}"
            )

        return {
            "should_automate": should_automate,
            "pattern_count": len(matching_ids),
            "matching_ids": matching_ids,
            "suggested_runbook": suggested_runbook,
        }


# ──────────────────────────────────────────────────────────────
# CLI Test
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 70)
    print("  Agentic Layer v3.0 — Agent Self-Test")
    print("=" * 70)

    # Test TriageAgent
    print("\n── TriageAgent Tests ──")
    triage = TriageAgent()

    t1 = triage.run(
        {"title": "Printer toner low", "description": "Floor 3 printer needs cyan toner."},
        {"confidence": 0.88, "category": "Infrastructure", "method": "centroid",
         "is_novel": False, "department": "Cloud Platform Engineering"},
    )
    print(f"  [HIGH CONF]  Decision: {t1['decision']}, Escalate: {t1['escalate']}")

    t2 = triage.run(
        {"title": "Can't do my job", "description": "Everything is broken, production is DOWN and urgent."},
        {"confidence": 0.35, "category": "Application", "method": "escalated",
         "is_novel": False, "department": "Application Support Team"},
    )
    print(f"  [LOW CONF]   Decision: {t2['decision']}, Escalate: {t2['escalate']}, Urgency: {t2['urgency_boost']}")

    t3 = triage.run(
        {"title": "Mow my lawn", "description": "The grass is too long in the office courtyard."},
        {"confidence": 0.05, "category": "Unknown", "method": "novel_ticket",
         "is_novel": True, "department": "General Support L1"},
    )
    print(f"  [NOVEL]      Decision: {t3['decision']}, Escalate: {t3['escalate']}")

    # Test ResolutionAgent with mock chunks
    print("\n── ResolutionAgent Tests ──")
    resolver = ResolutionAgent()

    mock_chunks = [
        {
            "id": "TKT-MOCK-001", "document": "VPN connection fails for remote users",
            "metadata": {"resolution": "Restarted VPN concentrator and restored config from backup."},
            "semantic": 0.85, "recency": 0.6, "outcome": 1.0, "final_score": 0.83,
        },
        {
            "id": "TKT-MOCK-002", "document": "VPN timeout on Windows machines",
            "metadata": {"resolution": "Updated VPN client to latest version and adjusted session timeout."},
            "semantic": 0.70, "recency": 0.4, "outcome": 0.8, "final_score": 0.66,
        },
    ]

    r1 = resolver.run(
        {"title": "VPN keeps disconnecting", "description": "Users report VPN drops after 5 min."},
        mock_chunks,
    )
    print(f"  Steps: {len(r1['resolution_steps'])}, Confidence: {r1['confidence']:.2f}, Sources: {r1['source_ids']}")

    r2 = resolver.run({"title": "Mystery issue", "description": "Something broke."}, [])
    print(f"  [NO CHUNKS]  Steps: {r2['resolution_steps']}, Confidence: {r2['confidence']}")

    # Test AutomationDiscoveryAgent
    print("\n── AutomationDiscoveryAgent Tests ──")
    discovery = AutomationDiscoveryAgent()

    a1 = discovery.run({
        "title": "VPN connection fails for remote users",
        "description": "Users cannot connect to VPN, error 619.",
        "category": "Network",
        "resolution": "Restarted concentrator.",
    })
    print(f"  [NETWORK]    Automate: {a1['should_automate']}, Matches: {a1['pattern_count']}")

    a2 = discovery.run({
        "title": "Office plant needs watering",
        "description": "The ficus in room 201 is wilting.",
        "category": "Unknown",
        "resolution": "Watered the plant.",
    })
    print(f"  [UNKNOWN]    Automate: {a2['should_automate']}, Matches: {a2['pattern_count']}")

    print("\n" + "=" * 70)
    print("  All agent self-tests complete.")
    print("=" * 70)
