# Till Now Progress

## Phase 1: Data & Setup
**Status:** COMPLETE

**What We Did Now:**
- [Environment configuration] - Setup Python venv with Streamlit, Langchain, ChromaDB, HuggingFace embeddings.
- [Synthetic data generation] - Built data generation scripts (`generate_standalone.py` and `generate_data.py`). Overcame Langchain/Ollama routing issues by using direct HTTP requests or MCP. Successfully generated 50 high-quality synthetic tickets covering 6 categories and 4 priority levels.
- [Vector database ingestion] - Built and executed `core/embeddings.py` to embed all 50 tickets using `all-MiniLM-L6-v2` and inserted them into a local ChromaDB instance to allow semantic search.

**Wrong Assumptions Corrected:**
- [LangChain ChatOllama Stability] - Initially assumed `langchain_community.chat_models.ChatOllama` would smoothly route nested cloud models (like deepseek-v3.2:cloud) through the local instance. Corrected by bypassing LangChain entirely for LLM calls and making direct REST POST requests using the `requests` library to the local Ollama API endpoint, achieving stability.

## Phase 2: Classification Core
**Status:** COMPLETE 

**What We Did Now:**
- [Establish category centroids] - Wrote logic in `core/classifier.py` to calculate mathematical centroids (the mean embedding vector) for each of the 6 IT categories based on the 50 ingested tickets.
- [Build similarity matcher] - Created a dual-pronged classifier combining Centroid Cosine Similarity with direct ChromaDB Nearest-Neighbor search for accuracy validation. Handled Department Routing logic automatically.
- [Test classification accuracy] - Passed 6 ambiguous mock tickets through the classifier, achieving a 100% correct classification hit rate.

## Phase 3: RAG & Resolution
**Status:** COMPLETE

**What We Did Now:**
- [Build semantic retrieval mechanism] - Created `core/rag.py` to query ChromaDB for the top 3 most similar past tickets to a new issue.
- [Implement LLM resolution generation] - Formatted a highly specific prompt containing context from past resolutions and queried Ollama via straight HTTP POST to output step-by-step technical fixes.

## Phase 4: Agentic Layer & UI
**Status:** COMPLETE

**What We Did Now:**
- [Escalation logic rules] - Created `core/agent.py` to identify tickets that the Classifier flags with < 75% confidence, marking them for Human L2 Escalation.
- [Repeat detection] - Built similarity-clustering logic into the Agent layer to identify if 3 or more highly-similar tickets occur (using a >0.85 similarity threshold), triggering an automated runbook suggestion.
- [Streamlit dashboard implementation] - Built `app.py` with a 3-tab layout: Ticket Submission (with real-time classification, RAG, and agent checks), Analytics Dashboard (with Plotly visualizations for ticket distributions), and Session History. The UI features a premium dark theme and responsive layout.

**Next Steps:**
- Present the Hackathon MVP. The full pipeline (Data -> Embeddings -> Classifier -> RAG -> Agent -> UI) is complete and functional.

**Files Created/Modified:**
- `app.py` - The main Streamlit dashboard application.
- `data/synthetic_tickets.csv` - The generated dataset.
- `core/embeddings.py` - Script for embedding and ChromaDB ingestion.
- `core/classifier.py` - Core logic for category matching and routing.
- `core/rag.py` - Core logic for retrieving similar tickets and generating resolutions.
- `core/agent.py` - Escalation and automation logic.
- `.agents/rules/*.md` - Refitted global agent rules from pentest workflow to Hackathon development protocol.
