# Phase 2 Validation Framework: Frontend Scaffolding

## 1. Domain Boundaries

| Domain | Scope | Responsibility |
|--------|-------|----------------|
| Vite | Build & Tooling | Hot module replacement, asset bundling, API proxying |
| Layout | Shell & Navigation | Core UI scaffolding, Sidebar, Breadcrumbs, Glassmorphism foundations |
| SSE Hook | Real-time Data | Connection management, event parsing, state synchronization, clean-up |
| Aurora | Visual Aesthetics | Dynamic background, motion choreography, GPU-accelerated effects |

## 2. Invariants

| ID | Invariant | Mitigation/Requirement |
|----|-----------|-------------------------|
| INV-02-01 | SSE Lifecycle | SSE connection **MUST** close on component unmount (T-02-04 mitigation) |
| INV-02-02 | Performance | Aurora background **MUST** use GPU acceleration (via `will-change: transform/opacity`) |
| INV-02-03 | Metrics | HealthPulse component **MUST** use Recharts for metrics visualization |
| INV-02-04 | Safety | All API interactions **MUST** use Zod-validated TypeScript interfaces |

## 3. Verification Dimensions

### D4: Real-time Behavior (SSE)
- **Goal:** Robust event-driven state updates.
- **Verification:** Mock SSE server emitting multiple event types; verify UI updates without full re-render; verify memory leak absence on rapid mount/unmount.

### D8: Glassmorphism Standard
- **Goal:** Elite aesthetics across all containers.
- **Verification:** Visual check for `backdrop-blur-xl`, `bg-white/5`, and `border-white/10` on target components.

### D9: Motion Choreography
- **Goal:** Fluid, non-blocking transitions.
- **Verification:** Use Framer Motion for entry/exit animations; ensure no layout shifts during state transitions.

## 4. Wave Validation Gates

### Wave 0: Baseline
- [ ] Vite project starts
- [ ] Vitest executes successfully
- [ ] Tailwind Glass utilities functional

### Wave 1: Foundation
- [ ] SSE Hook unit tests pass
- [ ] Layout renders with Glassmorphism
- [ ] Zod schemas match backend OpenAPI spec
