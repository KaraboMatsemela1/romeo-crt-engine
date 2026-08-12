# Roadmap

The canonical phase definitions and exit gates are in `PROJECT_BIBLE.md`. This document is the execution-oriented view.

## Work order

1. Phase 0 foundation
2. Phase 1 corpus
3. Phase 2 formal spec
4. Phase 3 data
5. Phase 4 detector
6. Phase 5 backtester
7. Phase 6 validation
8. Phase 7 paper
9. Phase 8 learning
10. Phase 9 shadow
11. Phase 10 controlled live

Never skip from a promising backtest directly to live execution.

## Milestones

### M0 — Reproducible repository
CI, tests, formatting, typed package scaffold, config conventions, ADRs and docs.

### M1 — Romeo CRT Strategy Reproduction
Evidence-backed frozen spec and deterministic reproduction of known valid/invalid examples.

### M2 — Historical Simulation Integrity
Trusted data + event-driven simulator + execution costs + no-lookahead regression suite.

### M3 — Edge Validation
Candidate passes/fails explicit OOS, walk-forward, stress, Monte Carlo and regime review.

### M4 — Realtime Paper Reliability
Signals, risk, state persistence, reconciliation, alerts and paper executions operate reliably.

### M5 — Learning Layer
A candidate setup-ranking model adds validated OOS value without overriding core validity/risk.

### M6 — Production Readiness
Shadow environment proves operational behavior and kill/reconciliation controls.

### M7 — Controlled Live Canary
Explicitly authorized tiny-capital live test with pre-defined stop and scale criteria.
