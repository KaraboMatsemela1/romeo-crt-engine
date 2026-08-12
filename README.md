# romeo-crt-engine

Evidence-driven research, validation, and execution platform for translating Romeo / @Romeotpt's publicly demonstrated CRT methodology into deterministic, testable, risk-controlled trading systems.

> **Status:** Phases 0–3 complete. `CRT-C3-D1-H1-M1-BEAR-v0.1` is frozen for validation and trusted dataset `ee1300f0da50e4debcbbc3b7` is frozen for Phase-4 detector reproduction. Profitability is not established; paper, shadow and live trading are not authorized.

## Start here

1. Read [`PROJECT_BIBLE.md`](PROJECT_BIBLE.md) — canonical governance and phase definitions.
2. Read [`STATUS.md`](STATUS.md) — current phase and promotion state.
3. Read [`AGENTS.md`](AGENTS.md) — operating contract for AI/coding agents.
4. Read [`strategy/CRT_V0.1_SPEC.md`](strategy/CRT_V0.1_SPEC.md) and its freeze manifest before touching strategy semantics.
5. Read [`docs/MARKET_DATA.md`](docs/MARKET_DATA.md) and the Phase-3 completion report before touching data semantics.
6. Follow [`docs/ROADMAP.md`](docs/ROADMAP.md) — ordered phases and gates.
7. Use [`research/romeo/VIDEO_ANALYSIS_TEMPLATE.md`](research/romeo/VIDEO_ANALYSIS_TEMPLATE.md) for new strategy-source research.

`STATUS.md` is the live project-state record; phase descriptions and governance remain defined by the Project Bible.

## Frozen strategy candidate

```text
CRT-C3-D1-H1-M1-BEAR-v0.1
lifecycle = FROZEN_FOR_VALIDATION
```

The frozen active route is deliberately narrow: bearish-only New-York D1 parent context with H1 Model #1 execution. Broader CRT doctrine remains explicitly deferred/versioned rather than silently mixed into this candidate.

## Frozen Phase-4 reproduction dataset

```text
dataset_version = ee1300f0da50e4debcbbc3b7
provider        = Binance Public Data
venue           = Binance Spot
symbol          = BTCUSDT
raw             = daily 1m archives
canonical       = UTC H1 + America/New_York D1
```

This is a compact trusted detector-integration dataset, **not** the final historical/OOS validation sample.

Canonical records:

- [`data/manifests/PHASE3_BTCUSDT_EE1300F0DA50E4DEBCBBC3B7.json`](data/manifests/PHASE3_BTCUSDT_EE1300F0DA50E4DEBCBBC3B7.json)
- [`data/manifests/PHASE3_BTCUSDT_EE1300F0DA50E4DEBCBBC3B7_EVIDENCE.json`](data/manifests/PHASE3_BTCUSDT_EE1300F0DA50E4DEBCBBC3B7_EVIDENCE.json)

## Core principle

We do **not** optimize for a beautiful backtest. We optimize for a reproducible, explainable strategy hypothesis that survives trusted-data checks, detector-reproduction checks, out-of-sample testing, realistic trading costs, walk-forward analysis, stress tests, and paper trading before any live capital is exposed.

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
Deterministic CRT detector
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
3. Trusted market-data layer — complete; provider-backed dataset frozen
4. CRT detection primitives — next
5. Event-driven backtester
6. Robust strategy validation
7. Paper trading
8. Learning and setup-quality models
9. Shadow trading
10. Controlled live deployment

See the Project Bible for phase definitions/exit criteria and `STATUS.md` for the live current gate.
