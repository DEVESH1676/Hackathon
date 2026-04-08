# State

## Current Position

Phase: Not started (defining requirements)
Plan: —
Status: Defining requirements and roadmap
Last activity: 2026-04-08 — Milestone v3.0 started

## Project Reference

See: .planning/PROJECT.md (updated 2026-04-08)

**Core value:** Every ticket gets classified, routed, and resolved with transparent confidence scoring and safety gates
**Current focus:** Milestone v3.0 — Enterprise Intelligence on Free Stack

## Accumulated Context

### From Hackathon MVP (v1.0)
- All 4 original phases COMPLETE (Data → Classification → RAG → Agent+UI)
- 150 synthetic tickets in ChromaDB, 6 categories, 4 priority levels
- Classifier achieves 100% on 6 manual test cases (untested at scale)
- RAG uses direct Ollama REST calls (LangChain bypassed due to stability issues)
- Agent layer detects low-confidence + repeat patterns
- Streamlit 3-tab dashboard functional

### Known Technical Debt
- `sys.path.append` hacks in every core module
- app.py references `synthetic_tickets.csv` but file is `synthetic_tickets_merged.csv`
- Ollama IP hardcoded to `192.168.137.1`
- No automated tests, no evaluation framework
- Three separate embedding calls per ticket (classifier + agent + RAG)
- Agent repeat detection ignores `created_at` dates
