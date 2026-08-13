# ADR-008 — Multi-Market Detector Compatibility Without Alpha Mutation

**Status:** Accepted for implementation / parity gate pending CI  
**Date:** 2026-08-13  
**Phase:** 6B  
**Active research candidate:** `CRT-C3-D1-H1-M1-BEAR-v0.2-MULTI-MARKET-RESEARCH`

## Context

Phase 6B selected a multi-market successor after the bullish direction-expansion path failed its primary-source evidence gate.

The active successor is intentionally unusual from a versioning perspective:

- the **research candidate** is new because the market universe, provider/data contracts, execution evidence, and validation protocol will be new;
- the **alpha rules** are not new: they remain the frozen `CRT-C3-D1-H1-M1-BEAR-v0.1` strategy semantics;
- the **data schema** is new: `P6B_CANONICAL_PRICE_DATASET_V2`;
- the **detector compatibility layer** must therefore be separately versioned without implying that the v0.1 alpha was rewritten.

## Decision

Use three explicit identities:

```text
candidate_version       CRT-C3-D1-H1-M1-BEAR-v0.2-MULTI-MARKET-RESEARCH
alpha_strategy_version  CRT-C3-D1-H1-M1-BEAR-v0.1
detector_version        CRT-DETECTOR-v0.2-MULTI-MARKET
```

Every Phase-6B detector candidate/run must retain all three.

Any emitted `TradePlan` must continue to carry:

```text
strategy_version = CRT-C3-D1-H1-M1-BEAR-v0.1
```

because `evaluate_bearish_c3` and its frozen parameters remain the source of signal validity.

## Why the candidate version changes

The multi-market research program creates a materially new validation hypothesis even when alpha logic is unchanged.

New dimensions include:

- instrument universe;
- provider and regulatory/account scope;
- price component;
- session/holiday gap policy;
- price quantum contract;
- bid/ask execution/friction model;
- dataset identity/provenance;
- cross-instrument pooling and validation gates.

These changes require independent validation and must not be reported as if they were the previously validated BTCUSDT candidate.

## Why the alpha version does not change

The project is explicitly trying to answer:

> Does the already frozen bearish D1 -> H1 Model #1 hypothesis remain observable and sufficiently frequent/robust across an ex-ante source-relevant market universe?

Changing the entry/stop/target/parent rules at the same time would destroy attribution and reopen the post-outcome tuning problem.

Therefore the compatibility detector must call the existing frozen strategy evaluator rather than reimplementing the rules.

## Data contract

The v2 detector consumes only trusted:

```text
PriceDatasetIdentityV2
CanonicalPriceBarV2 H1
CanonicalPriceBarV2 D1
```

The active candidate further requires:

```text
price_component = MID
quality_status  = TRUSTED
price_quantum   > 0 and pre-frozen
```

The detector verifies:

- provider/venue/instrument identity;
- price component;
- session-policy version;
- H1/D1 row counts;
- strict chronological uniqueness;
- normalized v2 price-data digest.

No activity/volume measure participates in alpha validity.

## Compatibility transformation

Only the following semantically equivalent fields may cross the data -> alpha boundary:

```text
timeframe
open_time
close_time
open
high
low
close
price_quantum
```

The detector must not pass or reinterpret:

- OANDA `PRICE_COUNT` as trade volume;
- provider metadata as directional context;
- session labels as alpha filters unless a future strategy version explicitly says so;
- bid/ask spread as Model #1 candle geometry when the signal component is frozen to MID;
- future D1 OHLC into the C3-open eligibility state.

## Parity gate

Before any provider-backed Phase-6B strategy outcome may be opened, `CRT-DETECTOR-v0.2-MULTI-MARKET` must reproduce the frozen Phase-2/v0.1 fixtures exactly on semantically identical OHLC/time inputs.

Required parity dimensions:

```text
DecisionState
ReasonCode
rule trace
evidence IDs
causal input digest
TradePlan fields
```

Candidate IDs and run hashes are intentionally allowed to differ because the candidate/detector/dataset identity has changed.

## Price quantum boundary

The v2 detector passes `PriceDatasetIdentityV2.price_quantum` into the frozen evaluator's `tick_size` argument.

This is safe only after the instrument's price quantum has been frozen from a documented source before outcomes.

Until then, real provider-backed data may not become detector-facing `TRUSTED` data.

Fixture parity may use an explicit test quantum because the purpose of the fixture is semantic compatibility, not provider-contract validation.

## Outcome independence

The detector layer may inspect:

- trusted market data;
- frozen dataset identity;
- frozen alpha parameters.

It may not inspect:

- P&L;
- backtest outcome metrics;
- future candidate success/failure labels;
- instrument profitability ranking.

The detector must emit candidates/TradePlans before the backtester computes outcomes.

## Legacy preservation

`src/romeo_crt_engine/crt/detector.py` and `CRT-DETECTOR-v0.1` remain the historical v0.1 detector chain.

Phase 6B adds `detector_v2.py` rather than changing legacy detector semantics or legacy manifest requirements.

## Gate result

This ADR becomes implementation-complete only when:

1. the v2 detector has a native v2 dataset/candidate/run identity;
2. the v2 detector calls the frozen v0.1 evaluator;
3. all frozen v0.1 fixtures achieve exact alpha parity;
4. non-MID signal data fail closed for this candidate;
5. trusted-dataset digest mismatches fail closed;
6. insufficient D1 history produces no candidate;
7. legacy v0.1 detector/regression tests remain green;
8. CI and preserved Backtest Smoke are green.

Even after this gate passes, provider-backed outcome access remains blocked until the OANDA runtime/data universe is frozen and the new validation protocol is preregistered.
