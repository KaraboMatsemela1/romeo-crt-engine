# romeo-crt-engine

Evidence-driven research, validation, and execution platform for translating Romeo / @Romeotpt's publicly demonstrated CRT methodology into deterministic, testable, risk-controlled trading systems.

> **Status:** Phase 2 complete. `CRT-C3-D1-H1-M1-BEAR-v0.1` is frozen for validation. Profitability is not established; paper, shadow and live trading are not authorized.

## Start here

1. Read [`PROJECT_BIBLE.md`](PROJECT_BIBLE.md) — canonical source of truth.
2. Read [`STATUS.md`](STATUS.md) — current phase and promotion state.
3. Read [`AGENTS.md`](AGENTS.md) — operating contract for AI/coding agents.
4. Read [`strategy/CRT_V0.1_SPEC.md`](strategy/CRT_V0.1_SPEC.md) and its freeze manifest before touching strategy semantics.
5. Follow [`docs/ROADMAP.md`](docs/ROADMAP.md) — ordered phases and gates.
6. Use [`research/romeo/VIDEO_ANALYSIS_TEMPLATE.md`](research/romeo/VIDEO_ANALYSIS_TEMPLATE.md) for new strategy-source research.

## Frozen candidate

```text
CRT-C3-D1-H1-M1-BEAR-v0.1
lifecycle = FROZEN_FOR_VALIDATION
```

The frozen active route is deliberately narrow: bearish-only New-York D1 parent context with H1 Model #1 execution. Broader CRT doctrine remains explicitly deferred/versioned rather than silently mixed into this candidate.

## Core principle

We do **not** optimize for a beautiful backtest. We optimize for a reproducible, explainable strategy hypothesis that survives trusted-data checks, out-of-sample testing, realistic trading costs, walk-forward analysis, stress tests, and paper trading before any live capital is exposed.

## Architecture

```text
Public research sources
        |
        v
Research / provenance layer
        |
        v
Frozen CRT strategy specification
        |
        v
Trusted market-data layer
        |
        v
Deterministic signal engine
        |
        +----> Backtest / validation
        |
        v
Independent risk engine
        |
        v
Paper / shadow execution
        |
        v
Controlled live execution (future, gated)
        |
        v
Journal + learning / candidate-model pipeline
```

## Safety boundary

AI may research, classify, explain, propose, score, and generate candidate models. AI must never bypass deterministic strategy rules, independent hard risk controls, strategy-version promotion gates, or the emergency kill switch.

`LIVE_TRADING_AUTHORIZED=false` remains the repository-safe default.

## Project phases

0. Engineering foundation — complete
1. Romeo corpus acquisition/reconciliation — complete
2. Formal strategy specification — complete; frozen for validation
3. Trusted market-data layer — next
4. CRT detection primitives
5. Event-driven backtester
6. Robust strategy validation
7. Paper trading
8. Learning and setup-quality models
9. Shadow trading
10. Controlled live deployment

See the project bible for full exit criteria and `STATUS.md` for the current gate.
