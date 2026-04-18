# Phase 2 Validation Document (02-VALIDATION.md)

## Nyquist Validation Framework for Frontend Scaffolding

This document outlines the validation framework for the frontend decoupling phase (Phase 2), ensuring that the elite React frontend adheres to quality and performance standards.

## Domain Boundaries

| Domain | Description | Responsibility |
|--------|-------------|----------------|
| **Vite & Infrastructure** | Project scaffolding, dependency management, and build pipeline. | Phase 2, Wave 1 |
| **Glassmorphism Layout** | The Aurora background, Glass panels, and responsive grid. | Phase 2, Wave 2 |
| **Realtime Infrastructure** | The SSE hook and EventSource lifecycle management. | Phase 2, Wave 3 |
| **Metrics & HealthPulse** | The Recharts-based monitoring and classification confidence displays. | Phase 2, Wave 4 |

## Invariants

The following invariants MUST be maintained throughout Phase 2 implementation:

- **SSE-INV-01 (SSE Lifecycle):** The SSE connection MUST explicitly close on component unmount to prevent memory leaks and dangling connections (Mitigation for T-02-04).
- **AUR-INV-01 (Aurora Performance):** The Aurora background effect MUST use `will-change: transform` and GPU-accelerated CSS properties to ensure smooth 60fps performance on target hardware.
- **HP-INV-01 (HealthPulse Library):** All metrics and trend charts in the HealthPulse component MUST use Recharts for consistent data visualization.
- **API-INV-01 (Type Safety):** All API interactions MUST use types generated from the backend `openapi.json` to ensure contract synchronization.

## Verification Dimensions

### D4: Realtime Behavior (SSE)
- **Goal:** Verify that the frontend correctly consumes and displays the backend event stream.
- **Method:** Automated tests for the SSE hook, mocking the EventSource API.
- **Success Criteria:** Data is updated in React state within 100ms of the SSE event arriving.

### D8: Glassmorphism Standard
- **Goal:** Ensure the UI adheres to the "Zenith Elite" aesthetic.
- **Method:** Visual review and automated CSS property checks.
- **Success Criteria:** All panels use `backdrop-filter: blur(20px)` and semi-transparent backgrounds (`bg-white/5`).

### D9: Motion Choreography
- **Goal:** Validate that UI transitions are fluid and non-blocking.
- **Method:** Manual verification of Framer Motion transitions.
- **Success Criteria:** No frame drops during panel transitions or data updates.

## Threat Register Tracking

- **T-02-01 (API Proxy):** Proxy only targets `localhost:8000`.
- **T-02-02 (Dependency Security):** `npm audit` should be run regularly.
- **T-02-03 (XSS):** React's built-in sanitization used for all dynamic content.
- **T-02-04 (SSE Leak):** Connection cleanup implemented in `useEffect`.
