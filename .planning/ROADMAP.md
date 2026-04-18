# Roadmap

## Phase 1: Backend Extraction (API Bridge)

**Goal:** Create a FastAPI backend (`main.py`) that exposes the core ticket classification, RAG retrieval, and agent logic as RESTful endpoints, without immediately deleting the existing Streamlit app.

**Requirements:** API-01, API-02

**Rationale:** Establishing the API bridge allows the new React frontend to consume backend logic independently, laying the standard foundation for UI decoupling without breaking the existing monolithic setup during migration.

**Depends on:** Existing v3.0 core logic modules

**Success criteria:**
1. `main.py` created utilizing FastAPI framework.
2. Endpoint (e.g. `/api/ticket/process`) correctly triggers classification cascade and returns structured JSON output.
3. API is testable via Swagger UI/Docs or cURL without starting Streamlit.

---

## Phase 2: Frontend Scaffolding

**Goal:** Initialize the new UI architecture on the `frontend-v2` branch and establish the Vite/React/Tailwind foundation.

**Requirements:** UI-01, UI-02, UI-03

**Rationale:** Ensure base aesthetics, routing, and modern frontend tools (e.g., Tailwind CSS, Aceternity/Shadcn components) are structured properly before fully migrating functionality and hooking up API endpoints.

**Depends on:** Phase 1 (API Bridge) to test data endpoints

**Plans:** 4 plans
- [ ] 02-01-PLAN.md — Foundation & Project Setup
- [ ] 02-02-PLAN.md — Layout & Navigation
- [ ] 02-03-PLAN.md — Intelligence Feed & State
- [ ] 02-04-PLAN.md — Polish & Refinement

**Success criteria:**
1. React + Vite project initializes successfully.
2. Tailwind CSS is set up and functional.
3. Component rendering for ticket submission and dashboard dashboard states are mocked up and then mapped to Phase 1 APIs.

---

## Phase 3: The Purge

**Goal:** Systematically remove Streamlit-related code, dependencies, and legacy python-based UI injections across the codebase once the React interface takes over.

**Requirements:** PURGE-01, PURGE-02

**Rationale:** Complete the decoupling by removing UI responsibilities completely from Python logic, enforcing the API-only architecture.

**Depends on:** Phase 2 (Functional React app replacing Streamlit functionality)

**Success criteria:**
1. `app.py` Streamlit entrypoint removed/archived.
2. Direct styling injections (e.g., `st.markdown`) successfully scrubbed from core logic files.
3. Heavy unneeded dependencies (Streamlit, Altair, Watchdog) pruned from `requirements.txt`.

---

## Phase 4: Branch Convergence

**Goal:** Finalize the architectural change and stabilize the git repository with the 3-tier realm standard (`core`, `zenith`, `dao`/main).

**Requirements:** MERGE-01

**Rationale:** Integrate verified, decoupled changes from `frontend-v2` into the standard development stream, ensuring the multi-tier repo is ready for staging testing.

**Depends on:** Phase 3

**Success criteria:**
1. `frontend-v2` is successfully merged into the `core` branch.
2. Both Node/React app and FastAPI backend build/run commands are properly documented for developers working on the unified repository.

---

## Summary

| # | Phase | Goal | Requirements | Success Criteria |
|---|-------|------|--------------|------------------|
| 1 | Backend Extraction | Expose core logic as REST API | API-01, API-02 | 3 |
| 2 | Frontend Scaffolding | Build Vite/React/Tailwind Base UI | UI-01–03 | 3 |
| 3 | The Purge | Remove Streamlit + dependencies | PURGE-01–02 | 3 |
| 4 | Branch Convergence | Merge `frontend-v2` to `core` | MERGE-01 | 2 |

---
*Roadmap created: 2026-04-18*
*Milestone: v4.0 Architectural Decoupling & UI Modernization*
