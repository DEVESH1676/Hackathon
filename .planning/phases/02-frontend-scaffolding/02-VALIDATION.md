# Phase 2 Validation Framework: Elite Frontend Scaffolding

## Domain Boundaries

| Domain | Scope | Criticality |
|--------|-------|-------------|
| **Vite** | Build system, hot reload, bundling, proxy | High |
| **Layout** | Glassmorphism, Responsive Grid, Motion (Aurora) | Medium |
| **SSE Hook** | Real-time ticket pipeline connection | High |
| **Aurora** | Background motion choreography | Low (Visual) |

## Invariants (Correctness Requirements)

1.  **SSE Lifecycle:** SSE connection MUST close on unmount (T-02-04 mitigation).
2.  **Aurora GPU Acceleration:** Aurora background MUST use GPU acceleration (will-change).
3.  **HealthPulse Metrics:** HealthPulse MUST use Recharts for metrics.
4.  **Glass Material:** Glass components MUST use backdrop-blur-xl, bg-white/5, and border-white/10.

## Verification Dimensions (Nyquist-D)

| ID | Dimension | Target | Verification Method |
|----|-----------|--------|---------------------|
| **D4** | Realtime behavior | Server-Sent Events (SSE) | Automated: Mock SSE event flow |
| **D8** | Glassmorphism standard | Visual Material System | Inspection: Tailwind config & utility check |
| **D9** | Motion choreography | Framer Motion animations | Inspection: will-change application |

## Threat Register Mitigations

- **T-02-01 (Spoofing):** API Proxy only targets local loopback (localhost:8000).
- **T-02-02 (Tampering):** Use fixed versions or lockfile; npm audit in CI.
