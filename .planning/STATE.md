# State

## Current Position

Phase: 2 — Classification Cascade
Plan: 01-PLAN.md
Status: COMPLETE
Last activity: 2026-04-08 — Phase 2 executed (all 4 cascade paths verified)

## Project Reference

See: .planning/PROJECT.md (updated 2026-04-08)

**Core value:** Every ticket gets classified, routed, and resolved with transparent confidence scoring and safety gates
**Current focus:** Milestone v3.0 — Enterprise Intelligence on Free Stack

## Accumulated Context

### From Hackathon MVP (v1.0)
- All 4 original phases COMPLETE (Data → Classification → RAG → Agent+UI)
- 50 synthetic tickets in ChromaDB (6 categories, 4 priority levels)
- RAG uses direct Ollama REST calls (LangChain bypassed due to stability issues)
- Agent layer detects low-confidence + repeat patterns
- Streamlit 3-tab dashboard functional

### From Phase 1: Calibration & Feedback (v3.0)
- **Calibration result:** 100% accuracy in high-confidence band (12/12)
- **Band distribution:** 12 high (>0.75), 37 medium (0.40-0.75), 1 low (<0.40)
- **Feedback table:** SQLite `data/feedback.db` operational

### From Phase 2: Classification Cascade (v3.0)
- **Cascade implemented:** 4-tier routing (Novel → Escalated → LLM Judge → Fast Path)
- **Novelty Detection (CASC-04):** If best-match similarity < 0.20 → flagged as NOVEL_TICKET
- **Low-Confidence Escalation (CASC-03):** If confidence < 0.40 → direct escalation, no LLM tokens
- **LLM Judge (CASC-02):** If 0.40 ≤ confidence < 0.75 → Groq API re-classifies with rationale
- **Fast Path (CASC-01):** If confidence ≥ 0.75 → centroid routing, zero LLM cost
- **Test results:** 4/4 scenarios pass. LLM judge correctly classified VPN ticket as "Network"
- **Key insight:** With only 50 training tickets, most new tickets fall into medium band. Cascade LLM judge adds significant value.
- **UI updated:** Cascade path badges shown in classification results panel

### Known Technical Debt
- `sys.path.append` hacks in every core module
- app.py references `synthetic_tickets.csv` but file is `synthetic_tickets_merged.csv`
- Ollama IP hardcoded to `192.168.137.1`
- No automated tests, no evaluation framework
- Three separate embedding calls per ticket (classifier + agent + RAG)
- Agent repeat detection ignores `created_at` dates
