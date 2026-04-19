# Phase 3: Frontend Robustness & State Sync

## Goal
Harden the React frontend against validation errors and fix state synchronization bugs in the Intelligence Feed.

## Tasks

### 3.1 The Validation "Wall" (UI-04)
- **Problem:** FastAPI Pydantic models reject short inputs (Title < 3, Desc < 10) with 422 errors, causing the SSE stream to fail before it starts.
- **Action:** Update `TicketForm.tsx` to disable the "Launch" button and show visual feedback when inputs are invalid.
- **Verification:** "Launch" button should be unclickable until both fields meet length requirements.

### 3.2 Fix "Completed but Empty" State Bug (UI-05)
- **Problem:** Intelligence Feed shows checkmarks (success) but cards remain empty (no data displayed).
- **Subtask 3.2.1: State Persistence**
    - Ensure the `SET_RESULT` action in the `usePipeline` reducer correctly saves the `payload` into `state.results`.
- **Subtask 3.2.2: Prop Passing**
    - Update `IntelligenceFeed.tsx` to pass the specific result data from `state.results[stage.id]` to the `StageCard` component.
- **Subtask 3.2.3: Data Reveal Animation**
    - Update `StageCard.tsx` to conditionally render the AI payload with a Framer Motion reveal animation once `data` is present.

## Verification
- **Automated:** Run `vitest` for the reducer logic.
- **Manual:** Submit a valid ticket and verify every card expands and shows actual AI content (Category, Rationale, Resolution steps, etc.).
