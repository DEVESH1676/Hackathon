# State

## Current Position

Phase: 1 — Calibration & Feedback Foundation
Plan: 01-PLAN.md
Status: COMPLETE
Last activity: 2026-04-08 — Phase 1 executed (both tasks passed)

## Project Reference

See: .planning/PROJECT.md (updated 2026-04-08)

**Core value:** Every ticket gets classified, routed, and resolved with transparent confidence scoring and safety gates
**Current focus:** Milestone v3.0 — Enterprise Intelligence on Free Stack

## Accumulated Context

### From Hackathon MVP (v1.0)
- All 4 original phases COMPLETE (Data → Classification → RAG → Agent+UI)
- 50 synthetic tickets in ChromaDB (6 categories, 4 priority levels)
- Classifier achieves 100% on 6 manual test cases (untested at scale)
- RAG uses direct Ollama REST calls (LangChain bypassed due to stability issues)
- Agent layer detects low-confidence + repeat patterns
- Streamlit 3-tab dashboard functional

### From Phase 1: Calibration & Feedback (v3.0)
- **Calibration result:** 100% accuracy across ALL confidence bands on 50 tickets
- **Band distribution:** 12 high (>0.75), 37 medium (0.40-0.75), 1 low (<0.40)
- **Insight:** Only 24% of tickets land in high-confidence band — cascade will route 76% to LLM judge
- **Thresholds validated:** 0.75 / 0.40 confirmed as valid cascade boundaries
- **Feedback table:** SQLite `data/feedback.db` with `resolutions` schema operational
- **Data correction:** ChromaDB has 50 tickets (not 150 as previously noted)

### Known Technical Debt
- `sys.path.append` hacks in every core module
- app.py references `synthetic_tickets.csv` but file is `synthetic_tickets_merged.csv`
- Ollama IP hardcoded to `192.168.137.1`
- No automated tests, no evaluation framework
- Three separate embedding calls per ticket (classifier + agent + RAG)
- Agent repeat detection ignores `created_at` dates
