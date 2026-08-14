# romeo-crt-engine

Evidence-driven research, validation, and execution platform for translating Romeo / @Romeotpt's publicly demonstrated CRT methodology into deterministic, testable, risk-controlled trading systems.

> **Status:** Phases 0–6 are complete for the first deterministic candidate. `CRT-C3-D1-H1-M1-BEAR-v0.1` finished Phase 6 with **`INSUFFICIENT_EVIDENCE`** because the preregistered four-year DEV window produced only 4 closed trades against a required minimum of 30. OOS and final-confirmatory windows remain unopened. Paper, shadow and live trading are not authorized.

## Progress to Paper Trading

This is the executive gate view of the project. The bars represent **milestone/gate maturity**, not trading performance, probability of success, or a forecast. A bar advances only when the corresponding canonical gate materially changes.

```text
FIRST-PARTY EVIDENCE
████████████████░░░░   good corpus; predicates incomplete

DETERMINISTIC CANDIDATE
░░░░░░░░░░░░░░░░░░░░   BLOCKED — no candidate-ready predicate

ACTIVITY VALIDATION
░░░░░░░░░░░░░░░░░░░░   not authorized — candidate not frozen

PERFORMANCE VALIDATION
░░░░░░░░░░░░░░░░░░░░   not authorized — activity gate not reached

OOS
░░░░░░░░░░░░░░░░░░░░   unopened

CONFIRM
░░░░░░░░░░░░░░░░░░░░   unopened

PAPER TRADING
░░░░░░░░░░░░░░░░░░░░   BLOCKED — requires PROMOTE_TO_PAPER_CANDIDATE
```

**Current bottleneck:** direct first-party evidence must close at least one held deterministic predicate before a new candidate can be selected and preregistered. See [`STATUS.md`](STATUS.md) for the canonical evidence/authorization state and [GitHub Issues](../../issues) for the autonomous execution queue.

## Start here

1. Read [`PROJECT_BIBLE.md`](PROJECT_BIBLE.md) — canonical governance and phase definitions.
2. Read [`STATUS.md`](STATUS.md) — current candidate disposition and promotion state.
3. Read [`AGENTS.md`](AGENTS.md) — operating contract for AI/coding agents.
4. Read [`strategy/CRT_V0.1_SPEC.md`](strategy/CRT_V0.1_SPEC.md) and its freeze manifest before touching v0.1 strategy semantics.
5. Read [`docs/MARKET_DATA.md`](docs/MARKET_DATA.md) before touching data semantics.
6. Read [`docs/DETECTOR.md`](docs/DETECTOR.md) before touching detector semantics.
7. Read [`docs/BACKTESTER.md`](docs/BACKTESTER.md) before touching simulator semantics.
8. Read [`experiments/phase6/P6_VALIDATION_PROTOCOL_V1.md`](experiments/phase6/P6_VALIDATION_PROTOCOL_V1.md) and [`docs/PHASE_6_COMPLETION_REPORT.md`](docs/PHASE_6_COMPLETION_REPORT.md) before interpreting historical performance.
9. Follow [`docs/ROADMAP.md`](docs/ROADMAP.md) and the Project Bible for ordered gates.
10. Use [`research/romeo/VIDEO_ANALYSIS_TEMPLATE.md`](research/romeo/VIDEO_ANALYSIS_TEMPLATE.md) for new strategy-source research.

## First candidate validation chain

```text
strategy   CRT-C3-D1-H1-M1-BEAR-v0.1
detector   CRT-DETECTOR-v0.1
simulator  CRT-BACKTEST-v0.1.1
DEV data   3e8a39fec1062ef902e8a1ad
result     INSUFFICIENT_EVIDENCE
```

`CRT-BACKTEST-v0.1.1` is a data-gap compatibility patch to the v0.1 simulator; it does not change entry, stop, target, sizing or friction semantics.

The strategy active route is deliberately narrow: bearish-only New-York D1 parent context with H1 Model #1 execution. Broader CRT doctrine remains deferred/versioned rather than silently mixed into v0.1.

## Phase-6 DEV result

The validation protocol was frozen before results. DEV was opened only after its trusted dataset was sealed and independently reproduced. OOS and CONFIRM were not opened.

```text
DEV window                   2019-01-01 .. 2022-12-31
trusted M1                   2,074,680
trusted H1                      34,578
complete New-York D1             1,418
rolling detector candidates      1,416
valid TradePlans / trades            4
required DEV minimum                30
result             INSUFFICIENT_DEV_SAMPLE
Phase-6 disposition INSUFFICIENT_EVIDENCE
```

All four preregistered cost scenarios were preserved, but four observations are insufficient for robust expectancy claims. No parameter optimization, walk-forward inference, Monte Carlo inference, OOS test, or final-confirmatory test was performed after the sample gate failed.

See:

- [`experiments/phase6/P6_DEV_RESULT_001.md`](experiments/phase6/P6_DEV_RESULT_001.md)
- [`experiments/phase6/P6_DEV_RESULT_001.json`](experiments/phase6/P6_DEV_RESULT_001.json)
- [`docs/reviews/PHASE_6_GATE_REVIEW.md`](docs/reviews/PHASE_6_GATE_REVIEW.md)

## Trusted data baseline

Phase 3's compact integration dataset remains:

```text
dataset_version = ee1300f0da50e4debcbbc3b7
provider        = Binance Public Data
venue           = Binance Spot
symbol          = BTCUSDT
```

Phase 6 used a separate four-year trusted DEV dataset. Provider-authenticated anomalies were handled before outcome access: one independently evidenced venue closure was modeled explicitly and 20 other incomplete/malformed UTC daily archives were excluded whole without synthesizing prices.

## Core principle

We do **not** optimize for a beautiful backtest. We optimize for an evidence-grounded, reproducible and explainable hypothesis, and we preserve negative or insufficient results rather than changing rules until the historical result improves.

The first candidate did **not** pass the evidence gate. That is a successful use of the validation process, not permission to skip it.

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
Frozen deterministic CRT detector
        |
        v
Event-driven backtester
        |
        v
Preregistered validation
        |
        +--> insufficient evidence -> preserve candidate -> new research/version
        |
        +--> pass -> independent risk -> paper -> shadow -> controlled live
```

## Current project direction

Do **not** start Phase 7 from v0.1.

The next legitimate track is to return to the public-source evidence and unresolved/deferred CRT doctrine, define **one new evidence-backed strategy candidate/version** (for example v0.2), create new deterministic fixtures/tests, and then repeat the gated validation lifecycle.

The v0.1 OOS and CONFIRM windows remain unconsumed and must not be casually inspected.

## Safety boundary

AI may research, classify, explain, propose, score, and generate candidate models. AI must never bypass deterministic strategy rules, independent hard risk controls, strategy-version promotion gates, or the emergency kill switch.

```text
PAPER_TRADING_AUTHORIZED=false
SHADOW_TRADING_AUTHORIZED=false
LIVE_TRADING_AUTHORIZED=false
```
