# romeo-crt-engine

Evidence-driven research, validation, and execution platform for translating Romeo / @Romeotpt's publicly demonstrated CRT methodology into deterministic, testable, risk-controlled trading systems.

> **Status:** Research foundation. No strategy is considered verified or production-ready yet.

## Start here

1. Read [`PROJECT_BIBLE.md`](PROJECT_BIBLE.md) — canonical source of truth.
2. Read [`AGENTS.md`](AGENTS.md) — operating contract for AI/coding agents.
3. Follow [`docs/ROADMAP.md`](docs/ROADMAP.md) — ordered phases and gates.
4. Use [`research/romeo/VIDEO_ANALYSIS_TEMPLATE.md`](research/romeo/VIDEO_ANALYSIS_TEMPLATE.md) for every source.
5. Promote only evidence-backed rules into [`strategy/CRT_V0.1_SPEC.md`](strategy/CRT_V0.1_SPEC.md).

## Core principle

We do **not** optimize for a beautiful backtest. We optimize for a reproducible, explainable strategy hypothesis that survives out-of-sample testing, realistic trading costs, walk-forward analysis, stress tests, and paper trading before any live capital is exposed.

## Architecture

```text
Public research sources
        |
        v
Research / provenance layer
        |
        v
Formal CRT strategy specification
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

## Project phases

0. Engineering foundation
1. Romeo corpus acquisition
2. Formal strategy specification
3. Trusted market-data layer
4. CRT detection primitives
5. Event-driven backtester
6. Robust strategy validation
7. Paper trading
8. Learning and setup-quality models
9. Shadow trading
10. Controlled live deployment

See the project bible for full checklists and exit criteria.
