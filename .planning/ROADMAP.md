# Roadmap: Nexus AI v3.0 — Enterprise Intelligence (Free Stack)

**Milestone:** v3.0
**Phases:** 6
**Requirements:** 25
**Estimated timeline:** ~2 weeks

---

## Phase 1: Calibration & Feedback Foundation

**Goal:** Validate classifier confidence thresholds and establish the feedback capture table before building any v3 logic.

**Requirements:** CALIB-01, FDBK-01

**Rationale:** If confidence bands are uncalibrated, the cascade thresholds (0.75, 0.40) will be meaningless and every downstream agent decision will be wrong. The feedback table enables the learning loop for v4.

**Depends on:** Existing v1 classifier + 150 tickets in ChromaDB

**Success criteria:**
1. Calibration script runs against all 150 tickets and outputs accuracy per confidence band (high >0.75, medium 0.40-0.75, low <0.40)
2. High confidence band shows ≥80% accuracy (or thresholds are adjusted to achieve this)
3. SQLite feedback table created with correct schema and successfully stores test pipeline runs
4. Feedback table write confirmed via SQL query returning inserted rows

---

## Phase 2: Classification Cascade + Novelty Detection

**Goal:** Replace the single-method classifier with a cascade: fast centroid → LLM judge → escalate, plus a novelty detector for unprecedented tickets.

**Requirements:** CASC-01, CASC-02, CASC-03, CASC-04

**Rationale:** The cascade saves LLM tokens on easy tickets (majority) and routes truly hard/novel cases differently. This is the core intelligence upgrade.

**Depends on:** Phase 1 (calibrated thresholds)

**Success criteria:**
1. High-confidence tickets (>0.75) route directly without LLM call — verified by absence of Groq/Ollama API call in logs
2. Medium-confidence tickets (0.40-0.75) trigger LLM judge call and return reclassification result
3. Low-confidence tickets (<0.40) escalate immediately without LLM call
4. Novel tickets (embedding distance > threshold from all centroids) are flagged as `NOVEL_TICKET` with distinct handling
5. Cascade tested against 10+ diverse test tickets covering all 4 paths

---

## Phase 3: Enhanced RAG — Context Ranking + Multi-Hop

**Goal:** Upgrade RAG from raw ChromaDB results to ranked, multi-hop retrieval that considers recency and resolution outcomes.

**Requirements:** RANK-01, RANK-02, MHOP-01, MHOP-02

**Rationale:** Current RAG returns raw similarity order. Context ranking ensures fresher, successfully-resolved tickets rank higher. Multi-hop chains tickets to KB articles for richer context.

**Depends on:** Phase 2 (cascade classification provides category for multi-hop metadata filter)

**Success criteria:**
1. `rank_retrieved_chunks()` returns chunks scored on 3 axes: semantic (60%), recency (20%), outcome (20%)
2. Ranked results differ from raw ChromaDB order in at least 1 test case (proving ranking works)
3. Multi-hop query uses `where={"category": predicted_category}` to fetch linked KB articles on second query
4. LLM resolution uses combined 2-hop context and produces visibly richer answers than single-hop

---

## Phase 4: Agentic Workflows — Triage, Resolution, AutomationDiscovery

**Goal:** Build three decoupled agent classes that form the decision pipeline: classify → triage → resolve → discover.

**Requirements:** TRIAGE-01, TRIAGE-02, RESOLVE-01, RESOLVE-02, AUTODISC-01, AUTODISC-02

**Rationale:** The current agent.py mixes escalation and repeat detection in one class. v3 separates concerns into specialized agents with clear inputs/outputs.

**Depends on:** Phase 3 (ranked RAG chunks feed ResolutionAgent)

**Success criteria:**
1. `TriageAgent.run(ticket, classification) → AgentResult` with routing decision and rationale
2. `ResolutionAgent.run(ticket, ranked_chunks) → AgentResult` with structured steps and confidence
3. `AutomationDiscoveryAgent.run(resolved_ticket) → AgentResult` fires only post-resolution
4. AutomationDiscovery correctly identifies 3+ tickets with same category + root-cause combination
5. All 3 agents tested independently with mock inputs

---

## Phase 5: LLM-as-Judge Evaluation Framework

**Goal:** Build the rubric-based resolution evaluator with a safety hard-gate that blocks unsafe auto-resolutions.

**Requirements:** JUDGE-01, JUDGE-02, JUDGE-03, JUDGE-04

**Rationale:** Without evaluation, resolution quality is unknown. The safety gate is the critical guardrail — no resolution with safety < 3 should ever auto-execute.

**Depends on:** Phase 4 (ResolutionAgent produces resolutions to judge)

**Success criteria:**
1. Judge returns JSON with correctness, completeness, safety, clarity scores (1-5) plus critique
2. Judge uses Groq free tier (not same model as resolution)
3. Resolution with safety < 3 is blocked from auto-resolve — verified with intentionally unsafe test resolution
4. Judge results are written to feedback table (FDBK-01 integration)

---

## Phase 6: Unified 5-Tab Streamlit UI

**Goal:** Rebuild the Streamlit interface from 3 tabs to 5 tabs with progressive disclosure of every pipeline stage.

**Requirements:** UI-01, UI-02, UI-03, UI-04, UI-05

**Rationale:** The current 3-tab UI hides the intelligence. The 5-tab layout makes classification cascade, RAG evidence, agent decisions, and judge scores visible and inspectable.

**Depends on:** Phase 5 (all pipeline components exist to display)

**Success criteria:**
1. Tab 1 (Submit) accepts title + description and triggers full pipeline
2. Tab 2 (Classification) shows cascade path taken, confidence, novelty flag
3. Tab 3 (RAG Evidence) displays ranked chunks with individual scores and multi-hop results
4. Tab 4 (Agent Decisions) shows which agent fired, decision, and written rationale
5. Tab 5 (Resolution + Judge) shows resolution steps, 4-axis rubric scores, safety gate status (PASS/BLOCKED)

---

## Phase 7: Premium Glassmorphism UI Transformation

**Goal:** Transform the Nexus AI dashboard from a functional Streamlit interface to a premium, futuristic SaaS-grade experience using Glassmorphism, dynamic motion, and floating tab navigation — rivaling tools like Linear and Vercel.

**Requirements:** GLASS-01, GLASS-02, GLASS-03, GLASS-04, GLASS-05

**Rationale:** The current UI (Phase 6) is functionally complete but visually utilitarian. A hackathon-winning demo requires a "wow factor" at first glance. Glassmorphism + animated backgrounds create an immersive intelligence-tool aesthetic that elevates the entire platform's perceived value.

**Depends on:** Phase 6 (all 5 tabs and pipeline rendering must exist before restyling)

**Success criteria:**
1. All primary containers (Ticket Form, Status Box, Top Tabs) render as frosted glass cards with `backdrop-filter: blur(20px)` and semi-transparent `rgba(255,255,255,0.03)` backgrounds
2. Tab navigation renders as individual floating glass islands — active tab lifts via `translateY(-5px)` with neon purple accent border
3. Background animates with a slow "Aurora Breathing" gradient cycling between `#0d0e17` and `#1a1c2c` using CSS keyframes
4. Sidebar collapse/expand button is always visible and clickable (fixed position, high z-index, glowing border) regardless of sidebar state
5. Text inputs use obsidian-dark backgrounds with glowing indigo border on focus
6. No visual regression — all 5 tabs continue to render pipeline data correctly
7. No GPU lag during pipeline execution (blur effects limited to top-level containers only)

---

## Summary

| # | Phase | Goal | Requirements | Success Criteria |
|---|-------|------|--------------|------------------|
| 1 | Calibration & Feedback | Validate thresholds + feedback table | CALIB-01, FDBK-01 | 4 |
| 2 | Classification Cascade | Centroid → LLM → Escalate + Novelty | CASC-01–04 | 5 |
| 3 | Enhanced RAG | Context ranking + multi-hop | RANK-01–02, MHOP-01–02 | 4 |
| 4 | Agentic Workflows | Triage + Resolution + AutomationDiscovery | TRIAGE-01–02, RESOLVE-01–02, AUTODISC-01–02 | 5 |
| 5 | LLM-as-Judge | Rubric scorer + safety gate | JUDGE-01–04 | 4 |
| 6 | Unified UI | 5-tab progressive disclosure | UI-01–05 | 5 |
| 7 | Premium Glassmorphism UI | Aurora + Glass Cards + Floating Tabs + Sidebar Fix | GLASS-01–05 | 7 |

**Total: 7 phases | 30 requirements | 34 success criteria**

---
*Roadmap created: 2026-04-08*
*Last updated: 2026-04-14 after Phase 7 (Glassmorphism UI) addition*
