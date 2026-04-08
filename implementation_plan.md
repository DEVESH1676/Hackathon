# Milestone v3.0: Enterprise Intelligence on a Free/Local Stack

## Strategy Overview
Evolve the existing ticket routing and resolution prototype into a sophisticated, agentic AI platform that implements advanced classification, enhanced RAG, and automated resolution intelligence, while maintaining a zero-cost, local-first infrastructure (Ollama/Groq Hybrid).

## Week 1: Core Intelligence
**Phase 1: Data & Setup**
  └─ 1.1: Environment configuration
  └─ 1.2: Confidence Calibration check (Run against existing tickets to calibrate the 0.75 threshold)
  └─ 1.3: Initialize Feedback Capture SQLite table (`feedback.db` for resolutions & overrides)

**Phase 2: Classification Core**
  └─ 2.1: Establish category centroids
  └─ 2.2: Implement Novelty detector (Flag `NOVEL_TICKET` BEFORE LLM if distance is too high)
  └─ 2.3: Build similarity matcher & LLM Judge fallback for uncertain tickets

**Phase 3: RAG & Resolution**
  └─ 3.1: Context ranking (Rank chunks across semantic, recency, and outcome axes)
  └─ 3.2: Multi-hop retrieval (Retrieve similar -> Extract runbook/category -> Retrieve KB/articles)

## Week 2: Agents & UI
**Phase 4: Agentic Layer & UI**
  └─ 4.1: TriageAgent (Routing decision + rationale + novelty handling)
  └─ 4.2: ResolutionAgent (Multi-hop RAG -> LLM structured generation)
  └─ 4.3: AutomationDiscoveryAgent (Runs POST-resolution, flags pattern repeats)
  └─ 4.4: LLM-as-Judge Evaluation (Groq-based rubric scoring with a Safety hard-gate)
  └─ 4.5: Streamlit dashboard implementation (5-tab progressive disclosure UI)

---
*Note: This plan has been locked in by the user.*
