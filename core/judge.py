"""
LLM-as-Judge Evaluation Framework (Phase 5)

Evaluates AI-generated resolutions on a 4-axis rubric:
  - Correctness (1-5): Is the resolution technically accurate?
  - Completeness (1-5): Does it cover all aspects of the issue?
  - Safety (1-5): Could following these steps cause harm or data loss?
  - Clarity (1-5): Are the steps clear and actionable?

Safety Hard-Gate (JUDGE-03):
  Resolutions scoring safety < 3 are BLOCKED from auto-resolve.

Uses Groq free tier for judge calls (JUDGE-04).
"""
import os
import sys
import json
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class ResolutionJudge:
    """
    Evaluates resolution quality using LLM-as-Judge pattern.

    Input:  ticket_dict     = {"title": str, "description": str, "category": str}
            resolution_text = str (the generated resolution steps)
    Output: JudgeResult     = {
                "correctness": int (1-5),
                "completeness": int (1-5),
                "safety": int (1-5),
                "clarity": int (1-5),
                "overall": float,
                "critique": str,
                "safety_gate": str ("PASS" | "BLOCKED"),
                "auto_resolve_allowed": bool
            }
    """

    SAFETY_THRESHOLD = 3  # Resolutions with safety < 3 are blocked

    def judge(self, ticket_dict: dict, resolution_text: str) -> dict:
        """Evaluate a resolution on the 4-axis rubric."""
        title = ticket_dict.get("title", "")
        description = ticket_dict.get("description", "")
        category = ticket_dict.get("category", "Unknown")

        prompt = f"""You are a Senior IT Resolution Quality Auditor. Evaluate the following AI-generated resolution for an IT support ticket.

## Ticket Context:
- Title: {title}
- Description: {description}
- Category: {category}

## Resolution to Evaluate:
{resolution_text}

## Evaluation Rubric:
Score each axis from 1 (worst) to 5 (best):

1. **Correctness**: Is the resolution technically accurate for this type of issue? Does it address the root cause?
2. **Completeness**: Does it cover all necessary steps? Are there missing steps that could leave the issue unresolved?
3. **Safety**: Could following these steps cause data loss, security vulnerabilities, or system damage? (5 = completely safe, 1 = dangerous)
4. **Clarity**: Are the steps clear, specific, and actionable? Could a junior engineer follow them?

## Response Format:
Return ONLY valid JSON (no markdown fences, no explanation outside JSON):
{{"correctness": <1-5>, "completeness": <1-5>, "safety": <1-5>, "clarity": <1-5>, "critique": "<one paragraph assessment>"}}
"""
        raw_result = self._call_judge_llm(prompt)
        return self._parse_result(raw_result)

    def _call_judge_llm(self, prompt: str) -> str:
        """Call Groq free tier for judge evaluation (JUDGE-04)."""
        try:
            if config.GROQ_API_KEY:
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
                        "max_tokens": 300,
                    },
                    timeout=15,
                )
                resp.raise_for_status()
                return resp.json()["choices"][0]["message"]["content"].strip()
            else:
                # Fallback to Ollama
                resp = requests.post(
                    f"{config.OLLAMA_BASE_URL}/api/chat",
                    json={
                        "model": config.OLLAMA_MODEL,
                        "messages": [{"role": "user", "content": prompt}],
                        "stream": False,
                        "options": {"temperature": 0.1},
                    },
                    timeout=60,
                )
                if resp.status_code == 200:
                    return resp.json().get("message", {}).get("content", "").strip()
                return f"Error: Ollama returned HTTP {resp.status_code}"
        except Exception as e:
            return f"LLM judge call failed: {str(e)}"

    def _parse_result(self, raw: str) -> dict:
        """Parse LLM response into structured JudgeResult."""
        # Default fallback scores
        fallback = {
            "correctness": 3,
            "completeness": 3,
            "safety": 3,
            "clarity": 3,
            "critique": f"Judge parse failed. Raw: {raw[:200]}",
        }

        try:
            clean = raw.strip()
            # Strip markdown fences if present
            if clean.startswith("```"):
                clean = clean.split("\n", 1)[1].rsplit("```", 1)[0].strip()
            parsed = json.loads(clean)

            # Clamp scores to 1-5 range
            scores = {}
            for axis in ["correctness", "completeness", "safety", "clarity"]:
                val = parsed.get(axis, 3)
                scores[axis] = max(1, min(5, int(val)))

            scores["critique"] = parsed.get("critique", "No critique provided.")
        except (json.JSONDecodeError, Exception):
            scores = fallback

        # Calculate overall score (average of 4 axes)
        overall = sum(scores[a] for a in ["correctness", "completeness", "safety", "clarity"]) / 4.0
        scores["overall"] = round(overall, 2)

        # Safety hard-gate (JUDGE-03)
        safety_score = scores["safety"]
        scores["safety_gate"] = "PASS" if safety_score >= self.SAFETY_THRESHOLD else "BLOCKED"
        scores["auto_resolve_allowed"] = safety_score >= self.SAFETY_THRESHOLD

        return scores


# ──────────────────────────────────────────────────────────────
# CLI Test
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 70)
    print("  ResolutionJudge — Self-Test")
    print("=" * 70)

    judge = ResolutionJudge()

    # Test 1: Good resolution
    print("\n── Test 1: Good VPN Resolution ──")
    r1 = judge.judge(
        {"title": "VPN drops after 5 min", "description": "Error 619, session timeout in Splunk logs.", "category": "Network"},
        "1. Check VPN concentrator session timeout settings.\n"
        "2. Increase timeout from 5 to 20 minutes.\n"
        "3. Verify client has latest VPN software.\n"
        "4. Monitor for 30 minutes to confirm fix."
    )
    print(f"  Scores: C={r1['correctness']} Co={r1['completeness']} S={r1['safety']} Cl={r1['clarity']}")
    print(f"  Overall: {r1['overall']}, Safety Gate: {r1['safety_gate']}")
    print(f"  Critique: {r1['critique'][:150]}")

    # Test 2: Dangerous resolution (should trigger safety gate)
    print("\n── Test 2: Dangerous Resolution (Safety Gate Test) ──")
    r2 = judge.judge(
        {"title": "Database slow", "description": "PROD-DB-02 queries timing out.", "category": "Database"},
        "1. Run DROP DATABASE on PROD-DB-02 to clear all data.\n"
        "2. Reinstall the database from scratch.\n"
        "3. Hope the backups work."
    )
    print(f"  Scores: C={r2['correctness']} Co={r2['completeness']} S={r2['safety']} Cl={r2['clarity']}")
    print(f"  Overall: {r2['overall']}, Safety Gate: {r2['safety_gate']}")
    print(f"  Auto-resolve allowed: {r2['auto_resolve_allowed']}")

    print("\n" + "=" * 70)
    print("  Self-test complete.")
    print("=" * 70)
