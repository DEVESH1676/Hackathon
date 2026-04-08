# Nexus AI Ticket Intelligence Platform — Project Context

## Project Overview
Nexus AI is an enterprise-grade IT ticket routing and resolution system. It automates the helpdesk pipeline by classifying incoming tickets, retrieving relevant historical context via RAG, generating resolutions, and applying agentic reasoning for triage and automation discovery.

### Core Stack
- **Frontend/Dashboard:** Streamlit (v1.x)
- **Language:** Python 3.14+
- **Vector Database:** ChromaDB (Local Persistent)
- **Embeddings:** `all-MiniLM-L6-v2` (Sentence-Transformers)
- **LLM Orchestration:** Direct REST calls to Ollama (local) and Groq API (cloud free tier)
- **Data Storage:** SQLite (for feedback and resolution tracking)

### Key Architectural Patterns
1. **Confidence-Based Cascade:** Tickets are routed through a 4-tier cascade:
   - **Novelty Check:** Distance-based detection for unprecedented issues.
   - **Fast Path (High Confidence):** Centroid-based routing, bypassing LLMs.
   - **LLM Judge (Medium Confidence):** Groq/Ollama re-classification with rationale.
   - **Direct Escalation (Low Confidence):** Immediate routing to human triage.
2. **Modular Intelligence:**
   - `core/classifier.py`: Cascade logic and category centroids.
   - `core/rag.py`: Multi-hop retrieval and context ranking.
   - `core/agent.py`: Specialized agents (Triage, Resolution, Discovery).
   - `core/feedback.py`: Persistent storage of pipeline outcomes and scores.

---

## Building and Running

### Prerequisites
- Python 3.14+
- Local Ollama instance (running `qwen2.5-gpu:latest`)
- Groq API Key (in `.env`)

### Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Data Initialization
If the vector database is empty, run:
```bash
python core/embeddings.py
```

### Running the Application
```bash
streamlit run app.py
```

### Testing and Utilities
- **Cascade Test:** `python scripts/test_cascade.py`
- **Calibration Check:** `python scripts/calibrate.py`
- **Feedback Test:** `python scripts/test_feedback.py`

---

## Development Conventions

### Code Structure
- **`core/`**: Foundational logic. Keep these modules decoupled and focused on single responsibilities.
- **`scripts/`**: One-off utilities, calibration tools, and verification scripts.
- **`.planning/`**: Structured project documentation using the GSD (Get Shit Done) framework.
- **`data/`**: Persistent databases (SQLite, CSVs) and synthetic data generators.

### Guidelines
- **Bypass LangChain for LLM Calls:** Use direct `requests` to Ollama/Groq to avoid stability issues with cloud-routed models.
- **Atomic Commits:** Prefer small, focused commits that map to specific planning tasks.
- **Validation-First:** Use `scripts/` to verify logic (like cascade thresholds) before integrating into the main UI.
- **Configuration:** All sensitive keys and model names must reside in `config.py` and `.env`.

---

## Current Status (Milestone v3.0)
- **Phase 1 (Calibration & Feedback):** COMPLETE
- **Phase 2 (Classification Cascade):** COMPLETE
- **Phase 3 (Enhanced RAG):** PLANNED / NEXT

*Refer to `tillnow.md` for a detailed log of recent changes and `ROADMAP.md` for upcoming features.*
