# Requirements: Nexus AI Ticket Intelligence Platform

**Defined:** 2026-04-08
**Core Value:** Every ticket gets classified, routed, and resolved with transparent confidence scoring and safety gates

## v3.0 Requirements

Requirements for milestone v3.0. Each maps to roadmap phases.

### Calibration & Feedback

- [x] **CALIB-01**: System validates classifier confidence bands against existing 50 tickets (high/medium/low accuracy per band) — ✅ 100% accuracy all bands
- [x] **FDBK-01**: System stores every pipeline run in SQLite feedback table (ticket_id, category, confidence, resolution, judge_scores, agent_action, human_override, outcome, created_at) — ✅ Schema verified

### Classification Cascade

- [ ] **CASC-01**: System routes tickets through fast centroid path (>0.75 confidence → direct route, no LLM call)
- [ ] **CASC-02**: System escalates medium-confidence tickets (0.40–0.75) to LLM judge for re-classification
- [ ] **CASC-03**: System escalates low-confidence tickets (<0.40) directly without wasting LLM tokens
- [ ] **CASC-04**: System detects novel tickets (embedding distance from ALL training examples above threshold) and flags as `NOVEL_TICKET` before classification

### Enhanced RAG

- [ ] **RANK-01**: System scores retrieved chunks on 3 axes: semantic similarity (60%), recency (20%), outcome success (20%)
- [ ] **RANK-02**: System returns ranked results instead of raw ChromaDB order
- [ ] **MHOP-01**: System performs second ChromaDB query using category/metadata from initial retrieval to fetch linked KB articles
- [ ] **MHOP-02**: System feeds both retrieval hops as combined context to LLM for resolution generation

### Agentic Workflows

- [ ] **TRIAGE-01**: TriageAgent class accepts ticket + classification → outputs routing decision with rationale
- [ ] **TRIAGE-02**: TriageAgent applies confidence gates + sentiment check for escalation decisions
- [ ] **RESOLVE-01**: ResolutionAgent class accepts ticket + ranked RAG chunks → outputs structured resolution steps
- [ ] **RESOLVE-02**: ResolutionAgent exposes confidence score for its generated resolution
- [ ] **AUTODISC-01**: AutomationDiscoveryAgent runs as post-resolution hook (not during triage)
- [ ] **AUTODISC-02**: AutomationDiscoveryAgent checks ChromaDB for 3+ tickets with same category + root-cause → suggests automation

### Evaluation (LLM-as-Judge)

- [ ] **JUDGE-01**: System evaluates resolutions on 4 rubric axes: correctness (1-5), completeness (1-5), safety (1-5), clarity (1-5)
- [ ] **JUDGE-02**: System returns structured JSON with per-axis scores, overall score, and critique
- [ ] **JUDGE-03**: Safety hard-gate blocks resolutions with safety < 3 from auto-resolve path
- [ ] **JUDGE-04**: System uses Groq free tier for judge calls (separate from resolution LLM)

### Unified UI

- [ ] **UI-01**: Tab 1 (🎫 Submit Ticket) provides form input for title and description
- [ ] **UI-02**: Tab 2 (🧠 Classification) shows cascade result, confidence score, novelty flag
- [ ] **UI-03**: Tab 3 (🔍 RAG Evidence) displays ranked chunks with multi-hop results and individual scores
- [ ] **UI-04**: Tab 4 (🤖 Agent Decisions) shows which agent fired, its decision, and rationale
- [ ] **UI-05**: Tab 5 (⚖️ Resolution + Judge) shows resolution steps, rubric scores, safety gate status

## v4.0 Requirements (Deferred)

### Learning Loop
- **LEARN-01**: System retrains classification centroids from feedback table corrections
- **LEARN-02**: System adjusts confidence thresholds based on override patterns
- **LEARN-03**: System performs active learning — surfaces uncertain tickets for human labeling

### Enterprise Integration
- **INTEG-01**: System ingests tickets from ServiceNow API
- **INTEG-02**: System ingests tickets from Jira Service Management API
- **INTEG-03**: System writes resolutions back to ITSM tools via API

### Advanced Agents
- **AIOPS-01**: AIOps agent correlates tickets with observability signals
- **SELFHEAL-01**: Self-healing agent applies known remediations automatically

## Out of Scope

| Feature | Reason |
|---------|--------|
| Microservices architecture | Zero budget — prove intelligence in monolith first |
| Kafka/Pulsar message bus | Single-process pipeline, no inter-service comms |
| Managed vector DBs (Pinecone, Weaviate) | ChromaDB is free and sufficient |
| gRPC/REST service mesh | No distributed services |
| Multi-tenant deployment | Single demo instance |
| Paid API tiers | Must stay $0.00 |
| PII detection/masking | Not handling real user data |
| Mobile/native app | Streamlit web-only |
| OAuth/SSO authentication | Internal demo tool |
| Real-time streaming inference | Batch/request-response sufficient |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| CALIB-01 | Phase 1 | Complete |
| FDBK-01 | Phase 1 | Complete |
| CASC-01 | Phase 2 | Pending |
| CASC-02 | Phase 2 | Pending |
| CASC-03 | Phase 2 | Pending |
| CASC-04 | Phase 2 | Pending |
| RANK-01 | Phase 3 | Pending |
| RANK-02 | Phase 3 | Pending |
| MHOP-01 | Phase 3 | Pending |
| MHOP-02 | Phase 3 | Pending |
| TRIAGE-01 | Phase 4 | Pending |
| TRIAGE-02 | Phase 4 | Pending |
| RESOLVE-01 | Phase 4 | Pending |
| RESOLVE-02 | Phase 4 | Pending |
| AUTODISC-01 | Phase 4 | Pending |
| AUTODISC-02 | Phase 4 | Pending |
| JUDGE-01 | Phase 5 | Pending |
| JUDGE-02 | Phase 5 | Pending |
| JUDGE-03 | Phase 5 | Pending |
| JUDGE-04 | Phase 5 | Pending |
| UI-01 | Phase 6 | Pending |
| UI-02 | Phase 6 | Pending |
| UI-03 | Phase 6 | Pending |
| UI-04 | Phase 6 | Pending |
| UI-05 | Phase 6 | Pending |

**Coverage:**
- v3.0 requirements: 25 total
- Mapped to phases: 25
- Unmapped: 0 ✓

---
*Requirements defined: 2026-04-08*
*Last updated: 2026-04-08 after milestone v3.0 initialization*
