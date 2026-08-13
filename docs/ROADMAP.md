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
8. **If validation does not promote the candidate: preserve it and loop back to evidence-backed candidate research/versioning**
9. Phase 7 paper — only for a promoted candidate
10. Phase 8 learning — only when sufficient labeled evidence exists
11. Phase 9 shadow
12. Phase 10 controlled live

Never skip from a promising backtest directly to live execution, and never interpret completion of a phase as automatic promotion to the next phase.

## Current branch in the roadmap

`CRT-C3-D1-H1-M1-BEAR-v0.1` completed Phase 6 with:

```text
INSUFFICIENT_EVIDENCE
```

The preregistered 2019–2022 DEV window produced only 4 closed trades against a required minimum of 30. Therefore:

```text
Phase 7 paper    BLOCKED FOR v0.1
OOS              UNOPENED
CONFIRM          UNOPENED
live             NOT AUTHORIZED
```

The active track returns to source-backed candidate research. Any successor must use a new strategy version and repeat the relevant freeze/detector/backtest/validation gates.

## Milestones

### M0 — Reproducible repository
CI, tests, formatting, typed package scaffold, config conventions, ADRs and docs.

**Status:** complete.

### M1 — Romeo CRT Strategy Reproduction
Evidence-backed frozen spec and deterministic reproduction of known valid/invalid examples.

**Status:** complete for v0.1.

### M2 — Historical Simulation Integrity
Trusted data + event-driven simulator + execution costs + no-lookahead regression suite.

**Status:** complete for the v0.1 research chain.

### M3 — Edge Validation
Candidate passes/fails explicit preregistered validation and receives a written disposition.

**v0.1 status:** complete with `INSUFFICIENT_EVIDENCE`; not promoted.

### M4 — Realtime Paper Reliability
Signals, risk, state persistence, reconciliation, alerts and paper executions operate reliably.

**Status:** blocked until a future candidate is promoted from validation.

### M5 — Learning Layer
A candidate setup-ranking model adds validated OOS value without overriding core validity/risk.

**Status:** not started; v0.1 produced too few valid setups for meaningful model work.

### M6 — Production Readiness
Shadow environment proves operational behavior and kill/reconciliation controls.

### M7 — Controlled Live Canary
Explicitly authorized tiny-capital live test with pre-defined stop and scale criteria.

`LIVE_TRADING_AUTHORIZED=false` remains mandatory until all intervening gates are explicitly passed.
