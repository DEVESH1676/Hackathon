# Phase 2 Validation Framework: Frontend Scaffolding

## Domain Boundaries
- **Foundation**: Vite, TypeScript, Vitest.
- **Visual Foundation**: Aurora Background, Glassmorphism System.
- **Reactive Layer**: SSE Pipeline Hook, React State Management.
- **Metric Layer**: HealthPulse (Recharts integration).

## Core Invariants
- **[INV-01] Realtime Reliability**: SSE connection MUST close on unmount to prevent memory leaks and zombie connections (T-02-04 mitigation).
- **[INV-02] Performance (GPU)**: Aurora background MUST use GPU acceleration (`will-change: transform`) to maintain 60FPS on high-density displays.
- **[INV-03] Visual Hierarchy**: Glassmorphism layers MUST follow the defined opacity/blur standards (bg-white/5, backdrop-blur-xl) for readability.
- **[INV-04] Observability**: HealthPulse MUST use Recharts for metrics to ensure consistent visual language with the bridge API.

## Verification Dimensions

### D4: Realtime Behavior (SSE)
- Validate connection handshake.
- Validate automatic reconnection logic.
- Validate proper cleanup on component unmount.

### D8: Glassmorphism Standard
- Verify backdrop filter support.
- Verify contrast ratios on frosted glass elements.
- Verify color bleed through transparent layers.

### D9: Motion Choreography
- Verify Framer Motion layout transitions.
- Verify "Liquid Entrance" animation for new ticket cards.
- Verify Staggered entry for metric pulses.

## Wave Validation Gates

### Wave 0: Infrastructure
- [ ] Vite project starts.
- [ ] Tailwind configured with Glass utility.
- [ ] Vitest environment active.

### Wave 1: Reactive Bridge
- [ ] SSE Hook successfully receives mock stream.
- [ ] Pipeline state updates correctly.

### Wave 2: Visual Elite
- [ ] Aurora component renders without layout thrashing.
- [ ] Shadcn components themed with Glassmorphism.
