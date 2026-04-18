# Phase 2 Validation: Frontend Scaffolding

## Domain Boundaries

| Boundary | Scope | Responsibilities |
|----------|-------|------------------|
| Vite Project | `frontend-v2/` | Build system, dev server, HMR, type generation. |
| Layout System | `src/components/shell/` | Responsive container, navbar, footer, feed skeleton. |
| SSE Hook | `src/hooks/use-pipeline.ts` | Real-time state management, connection lifecycle. |
| Aurora System | `src/components/ui/aurora.tsx` | GPU-accelerated background, motion choreography. |

## Invariants

- **I-01 (Connection Safety):** SSE connection MUST close on unmount.
- **I-02 (Performance):** Aurora background MUST use GPU acceleration (`will-change`).
- **I-03 (Visualization):** HealthPulse MUST use Recharts for metrics.
- **I-04 (Type Safety):** All API-derived types MUST be generated from the FastAPI OpenAPI schema.
- **I-05 (Accessibility):** All Shadcn UI components MUST maintain WCAG compliance.

## Verification Dimensions

### D4: Realtime Behavior (SSE)
- **Goal:** Validate stream consumption and state updates.
- **Checklist:**
  - [ ] `usePipeline` hook initializes with `EventSource`.
  - [ ] Progress values (0.0 - 1.0) correctly update the state.
  - [ ] Connection closes immediately when the component unmounts.
  - [ ] Errors in the stream are handled gracefully (reconnect or error state).

### D8: Glassmorphism Standard
- **Goal:** Ensure visual consistency across all surface materials.
- **Checklist:**
  - [ ] Backdrop blur is applied to cards (`backdrop-blur-xl`).
  - [ ] Background opacity is consistent (`bg-white/5` or equivalent).
  - [ ] Borders are subtle and semi-transparent (`border-white/10`).
  - [ ] No layout shift when applying glass effects.

### D9: Motion Choreography
- **Goal:** Verify animation fluidity and purpose.
- **Checklist:**
  - [ ] Stage reveals use Framer Motion transitions.
  - [ ] Aurora background remains at < 5% CPU usage during animation.
  - [ ] Hover states on pills and buttons are responsive and smooth.
  - [ ] Page-level entrance animations are unified.

## Success Criteria (Wave 1)

- [ ] Vite dev server starts without errors.
- [ ] `npm run test` passes (smoke + pipeline stubs).
- [ ] Tailwind configured with "Glass" material utility.
- [ ] Shadcn UI components can be imported and rendered.
