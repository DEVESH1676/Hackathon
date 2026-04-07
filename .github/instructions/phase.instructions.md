---
trigger: always_on
---

# Phase-Driven Development Protocol

## Work in Phases - No Skipping

Work **strictly** in phases as defined in `implementation_plan.md`:

```
Phase 1: Data & Setup
  └─ 1.1: Environment configuration
  └─ 1.2: Synthetic data generation
  └─ 1.3: Vector database ingestion

Phase 2: Classification Core
  └─ 2.1: Establish category centroids
  └─ 2.2: Build similarity matcher
  └─ 2.3: Test classification accuracy

Phase 3: RAG & Resolution
  └─ 3.1: Build semantic retrieval mechanism
  └─ 3.2: Implement LLM resolution generation

Phase 4: Agentic Layer & UI
  └─ 4.1: Escalation logic rules
  └─ 4.2: Repeat detection (automation playbook suggestion)
  └─ 4.3: Streamlit dashboard implementation
```

## Phase Completion Checklist

Before marking a phase COMPLETE:
- [ ] All required code for the phase in `implementation_plan.md` is functioning and tested.
- [ ] `tillnow.md` is updated with completion status.
- [ ] Next phase steps are noted.

## Blockers Protocol

If blocked (e.g., LLM timeouts, missing dependencies):
1. Document in `tillnow.md` under "Next Steps".
2. List what the user needs to provide or decide on.
3. Note an alternative approach (e.g., fallback scripts) for once unblocked.

## Never Skip Documentation

Even failed attempts must be documented in `tillnow.md`:
- What was attempted
- Why it failed
- What to try next

**"No documentation = no progress tracking = phase never completes."**

---
### **Changelog**
- **2026-03-31:** Adapted from Pentest protocol to AI Ticket Agent Hackathon development structure.
