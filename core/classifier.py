"""
Ticket Classifier — v3.0 Cascade Architecture

Classification cascade:
  1. Embed ticket
  2. Novelty check: if best-match similarity < NOVELTY_SIMILARITY_THRESHOLD → NOVEL_TICKET
  3. Centroid + search blending → adjusted_confidence
  4. High confidence (>0.75): fast centroid path, no LLM call
  5. Low confidence (<0.40): direct escalation, no LLM call
  6. Medium confidence (0.40–0.75): LLM judge re-classifies via Groq/Ollama
"""
import os
import sys
import json
import requests
import numpy as np
from collections import defaultdict

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from core.embeddings import get_embedding_model, get_chroma_collection


class TicketClassifier:
    """Classifies tickets using a confidence-based cascade architecture."""

    def __init__(self):
        self.model = get_embedding_model()
        self.collection = get_chroma_collection()
        self.centroids = {}
        self._build_centroids()

    def _build_centroids(self):
        """Compute average embedding per category from stored tickets."""
        all_data = self.collection.get(include=["embeddings", "metadatas"])

        if not all_data["ids"]:
            print("⚠ No tickets in vector store. Run embeddings.py first.")
            return

        category_embeddings = defaultdict(list)
        for emb, meta in zip(all_data["embeddings"], all_data["metadatas"]):
            cat = meta.get("category", "Unknown")
            category_embeddings[cat].append(emb)

        for cat, embs in category_embeddings.items():
            self.centroids[cat] = np.mean(embs, axis=0)

        print(f"✓ Built centroids for {len(self.centroids)} categories: {list(self.centroids.keys())}")

    def _cosine_similarity(self, a, b):
        """Compute cosine similarity between two vectors."""
        a, b = np.array(a), np.array(b)
        dot = np.dot(a, b)
        norm = np.linalg.norm(a) * np.linalg.norm(b)
        return dot / norm if norm > 0 else 0.0

    # ------------------------------------------------------------------
    # LLM Judge — called only for medium-confidence tickets (0.40–0.75)
    # ------------------------------------------------------------------
    def _llm_judge_classify(self, title: str, description: str, centroid_guess: str, confidence: float) -> dict:
        """
        Ask an LLM to re-classify a ticket when vector similarity is uncertain.

        Returns dict with 'category' and 'rationale', or None on failure.
        """
        categories_str = ", ".join(config.CATEGORIES)
        prompt = f"""You are an IT ticket classification expert. A vector-similarity classifier
assigned this ticket to "{centroid_guess}" with only {confidence:.0%} confidence.

Re-classify the ticket into exactly ONE of these categories:
{categories_str}

Ticket Title: {title}
Ticket Description: {description}

Reply ONLY with valid JSON (no markdown, no explanation):
{{"category": "<chosen category>", "rationale": "<one sentence why>"}}"""

        try:
            if config.USE_GROQ and config.GROQ_API_KEY:
                return self._call_groq(prompt)
            else:
                return self._call_ollama(prompt)
        except Exception as e:
            print(f"  ⚠ LLM judge failed ({e}), falling back to centroid guess")
            return None

    def _call_groq(self, prompt: str) -> dict | None:
        """Call Groq free-tier API for classification."""
        resp = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {config.GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": config.GROQ_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.1,
                "max_tokens": 150,
            },
            timeout=15,
        )
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"].strip()
        # Strip markdown fences if present
        if content.startswith("```"):
            content = content.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        return json.loads(content)

    def _call_ollama(self, prompt: str) -> dict | None:
        """Call local Ollama for classification."""
        resp = requests.post(
            f"{config.OLLAMA_BASE_URL}/api/generate",
            json={
                "model": config.OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "format": "json",
            },
            timeout=30,
        )
        resp.raise_for_status()
        content = resp.json()["response"].strip()
        return json.loads(content)

    # ------------------------------------------------------------------
    # Main classification cascade
    # ------------------------------------------------------------------
    def classify(self, title: str, description: str) -> dict:
        """
        Classify a ticket through the confidence cascade.

        Returns dict with keys:
            category, department, confidence, priority_suggestion,
            similar_tickets, all_scores, method, is_novel, escalate,
            llm_rationale (when method=llm_judge)
        """
        text = f"{title} {description}"
        embedding = self.model.encode(text).tolist()

        # ── Step 1: Centroid similarity scores ──
        scores = {}
        for cat, centroid in self.centroids.items():
            scores[cat] = self._cosine_similarity(embedding, centroid)

        best_category = max(scores, key=scores.get)
        best_score = scores[best_category]

        # ── Step 2: ChromaDB nearest-neighbour search ──
        search_results = self.collection.query(
            query_embeddings=[embedding],
            n_results=5,
            include=["documents", "metadatas", "distances"],
        )

        similar_tickets = []
        top_categories_from_search = []
        best_match_similarity = 0.0

        if search_results["ids"][0]:
            for doc, meta, dist in zip(
                search_results["documents"][0],
                search_results["metadatas"][0],
                search_results["distances"][0],
            ):
                similarity = 1 - dist  # ChromaDB cosine distance = 1 - sim
                if similarity > best_match_similarity:
                    best_match_similarity = similarity

                similar_tickets.append({
                    "document": doc[:150],
                    "category": meta.get("category", "Unknown"),
                    "priority": meta.get("priority", "Unknown"),
                    "resolution": meta.get("resolution", "")[:200],
                    "department": meta.get("department", "Unknown"),
                    "similarity": round(similarity, 4),
                })
                top_categories_from_search.append(meta.get("category", "Unknown"))

        # ── Step 3: Novelty detection (CASC-04) ──
        is_novel = best_match_similarity < config.NOVELTY_SIMILARITY_THRESHOLD

        if is_novel:
            return {
                "category": "Unknown",
                "department": config.ROUTING["Unknown"],
                "confidence": round(best_match_similarity, 4),
                "priority_suggestion": "P2 High",  # novel → escalate with urgency
                "similar_tickets": similar_tickets,
                "all_scores": {k: round(v, 4) for k, v in sorted(scores.items(), key=lambda x: -x[1])},
                "method": "novel_ticket",
                "is_novel": True,
                "escalate": True,
                "llm_rationale": None,
            }

        # ── Step 4: Confidence blending ──
        if top_categories_from_search:
            search_agreement = (
                sum(1 for c in top_categories_from_search[:3] if c == best_category)
                / min(3, len(top_categories_from_search))
            )
            adjusted_confidence = (best_score * 0.6) + (search_agreement * 0.4)
        else:
            adjusted_confidence = best_score

        # ── Step 5: Priority suggestion ──
        priority_counts = defaultdict(int)
        for t in similar_tickets[:3]:
            priority_counts[t["priority"]] += 1
        suggested_priority = max(priority_counts, key=priority_counts.get) if priority_counts else "P3 Medium"

        # ── Step 6: Department routing ──
        department = config.ROUTING.get(best_category, config.ROUTING["Unknown"])

        # ── Step 7: Cascade decision ──
        method = "centroid"
        escalate = False
        llm_rationale = None

        if adjusted_confidence >= config.CONFIDENCE_THRESHOLD:
            # HIGH confidence → fast path, no LLM (CASC-01)
            method = "centroid"

        elif adjusted_confidence < config.MEDIUM_CONFIDENCE_THRESHOLD:
            # LOW confidence → direct escalation, no LLM (CASC-03)
            method = "escalated"
            escalate = True
            # Still use best guess from search if available
            if top_categories_from_search:
                best_category = top_categories_from_search[0]
                department = config.ROUTING.get(best_category, config.ROUTING["Unknown"])

        else:
            # MEDIUM confidence (0.40–0.75) → LLM judge (CASC-02)
            llm_result = self._llm_judge_classify(title, description, best_category, adjusted_confidence)
            if llm_result and llm_result.get("category") in config.CATEGORIES:
                best_category = llm_result["category"]
                department = config.ROUTING.get(best_category, config.ROUTING["Unknown"])
                llm_rationale = llm_result.get("rationale", "")
                method = "llm_judge"
            else:
                # LLM failed or returned invalid category — fall back to search
                if top_categories_from_search:
                    best_category = top_categories_from_search[0]
                    department = config.ROUTING.get(best_category, config.ROUTING["Unknown"])
                method = "similarity_search"

        return {
            "category": best_category,
            "department": department,
            "confidence": round(adjusted_confidence, 4),
            "priority_suggestion": suggested_priority,
            "similar_tickets": similar_tickets,
            "all_scores": {k: round(v, 4) for k, v in sorted(scores.items(), key=lambda x: -x[1])},
            "method": method,
            "is_novel": False,
            "escalate": escalate,
            "llm_rationale": llm_rationale,
        }

    def find_repeats(self, title: str, description: str) -> list:
        """Find potentially recurring/duplicate tickets."""
        text = f"{title} {description}"
        embedding = self.model.encode(text).tolist()

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=10,
            include=["documents", "metadatas", "distances"],
        )

        repeats = []
        if results["ids"][0]:
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            ):
                similarity = 1 - dist
                if similarity >= config.SIMILARITY_THRESHOLD:
                    repeats.append({
                        "document": doc[:150],
                        "category": meta.get("category"),
                        "resolution": meta.get("resolution", "")[:300],
                        "similarity": round(similarity, 4),
                    })

        return repeats


# --- CLI Test ---
if __name__ == "__main__":
    print("Initializing classifier...")
    clf = TicketClassifier()

    test_cases = [
        ("VPN not working", "Multiple users cannot connect to VPN. Getting error 619. Remote team is affected."),
        ("Cannot access SharePoint", "Getting access denied when trying to open the project site in SharePoint."),
        ("Database slow", "PROD-DB-02 queries are taking 30+ seconds. Application is timing out."),
        ("Suspicious email received", "Got a phishing email pretending to be from HR. Contains a suspicious link."),
        ("Kubernetes pods crashing", "Payment service pods keep getting OOMKilled in the production cluster."),
        ("Need new service account", "DevOps needs a service account with S3 access for the backup automation."),
    ]

    print(f"\n{'='*70}")
    print(f"  Testing cascade classifier on {len(test_cases)} tickets")
    print(f"{'='*70}")

    for title, desc in test_cases:
        result = clf.classify(title, desc)
        novel_tag = " 🆕 NOVEL" if result.get("is_novel") else ""
        esc_tag = " ⚠ ESCALATE" if result.get("escalate") else ""
        print(f"\n  📝 \"{title}\"{novel_tag}{esc_tag}")
        print(f"     Category:   {result['category']} (via {result['method']})")
        print(f"     Department: {result['department']}")
        print(f"     Confidence: {result['confidence']:.1%}")
        print(f"     Priority:   {result['priority_suggestion']}")
        if result.get("llm_rationale"):
            print(f"     LLM Judge:  {result['llm_rationale']}")
        print(f"     Top scores: {result['all_scores']}")
