# Phase 6 Validation Protocol v0.1

Status: PREREGISTERED DRAFT — no Phase-6 historical results observed under this protocol yet.

Frozen baseline:

```text
strategy   CRT-C3-D1-H1-M1-BEAR-v0.1
detector   CRT-DETECTOR-v0.1
simulator  CRT-BACKTEST-v0.1
```

This protocol exists to prevent outcome-driven window selection, rule changes, hidden tuning and over-interpretation of small samples.

## 1. Primary question

Does the frozen bearish D1/H1 CRT candidate generate enough causally valid TradePlans, and then enough closed trades, to support a credible robustness decision under realistic execution friction?

The first Phase-6 objective is therefore **sample sufficiency before profitability**.

## 2. Allowed decisions

Exactly one final disposition must be written for the frozen baseline:

```text
REJECT
REVISE_AS_NEW_VERSION
INSUFFICIENT_EVIDENCE
PROMOTE_TO_PAPER_CANDIDATE
```

`REVISE_AS_NEW_VERSION` creates a separately named candidate. It must not rewrite the frozen v0.1 baseline in place.

## 3. Predeclared historical partitions

BTCUSDT observation data is partitioned by complete UTC calendar months. The periods are selected mechanically and fixed before Phase-6 detector/backtest results are inspected.

### Development / diagnostic history

```text
2023-01-01 through 2024-12-31 UTC
```

Purpose:
- verify frequency and implementation behavior;
- inspect failure modes;
- run predeclared sensitivity and cost diagnostics;
- no final promotion claim.

### Out-of-sample validation history

```text
2025-01-01 through 2025-12-31 UTC
```

Purpose:
- evaluate the frozen baseline after all development diagnostics are defined;
- no parameter changes based on this period may be folded back into v0.1.

### Untouched confirmatory history

```text
2026-01-01 through 2026-06-30 UTC
```

Purpose:
- final confirmatory check only after the development and OOS reports are complete;
- must remain unopened for strategy outcome analysis until the confirmatory gate is explicitly reached.

The existing September 2025 Phase-5 smoke result remains preserved as prior integration evidence and is not discarded. Because that month has already been observed, Phase 6 must explicitly label September 2025 as previously exposed when interpreting the 2025 OOS partition.

## 4. Data requirements

Each partition must be built as a separately versioned trusted dataset using the Phase-3 ingestion/normalization contract.

Required before use:
- immutable provider receipts/hashes;
- trusted quality status;
- canonical M1/H1/New-York D1 reconstruction;
- dataset manifest SHA-256;
- market-data code SHA-256;
- exact UTC start/end dates;
- row-count and gap checks;
- explicit record of any provider unavailability or missing days.

No invalid dataset may be silently repaired by changing strategy logic.

## 5. Sample-size gates

The first question is whether enough trades exist for inference.

Predeclared handling:

```text
0–29 closed trades     => INSUFFICIENT_EVIDENCE for performance inference
30–99 closed trades    => exploratory only; no paper promotion
100–199 closed trades  => limited inference; robustness evidence must be especially strong
>=200 closed trades    => eligible for full statistical/Monte-Carlo robustness review
```

These thresholds are governance thresholds, not claims of universal statistical sufficiency.

TradePlan frequency and closed-trade frequency must both be reported. Zero or low frequency is a legitimate outcome and must not trigger rule loosening.

## 6. Frozen cost scenarios

Run all historical simulations under the existing Phase-5 assumptions:

```text
IDEAL
BASE
STRESSED
SEVERE
```

The cost model is a sensitivity envelope, not a claim that those values reproduce exact historical Binance execution costs.

Primary interpretation uses BASE. A candidate that only works under IDEAL cannot be promoted.

## 7. Primary metrics

For each partition and cost scenario report at least:
- detector candidate count;
- valid TradePlan count;
- completed trades;
- open-at-end count;
- wins/losses;
- win rate;
- average R;
- expectancy R;
- profit factor;
- net P&L;
- maximum realized drawdown;
- longest losing streak;
- time exposure where derivable;
- monthly trade frequency;
- yearly trade frequency.

CAGR/Sharpe/Sortino may only be reported if the sampling/exposure assumptions make them meaningful and their calculation contract is documented.

## 8. Robustness tests

Only after sample-size gates permit meaningful inference:

1. Cost stress across IDEAL/BASE/STRESSED/SEVERE.
2. Calendar subperiod stability by quarter and year.
3. Entry-time/session breakdown.
4. Volatility/regime breakdown using features derived without future information.
5. Parameter sensitivity around project-chosen thresholds without changing the frozen baseline.
6. Walk-forward analysis using chronologically ordered folds.
7. Monte Carlo resampling of realized R sequences, including trade-order permutation and predeclared execution perturbations.

No robustness test may select the final rule version by maximizing the untouched confirmatory period.

## 9. Parameter sensitivity policy

Frozen baseline parameters remain unchanged.

Sensitivity runs may vary one parameter at a time around the baseline solely to test fragility. They must be logged as diagnostics and cannot silently become v0.1.

If evidence supports a change, create a new candidate version and restart the appropriate validation lifecycle.

## 10. Leakage controls

- No future D1/H1 state may enter a decision.
- No parent or candidate may be selected retrospectively because it later succeeds.
- No confirmatory-period result may influence development or OOS tuning.
- No month may be removed because it performs poorly.
- Provider gaps and execution failures remain part of the record.
- The Phase-5 synthetic short assumption remains explicit.

## 11. Promotion gate

`PROMOTE_TO_PAPER_CANDIDATE` requires, at minimum:
- enough closed trades to clear the project sample gate;
- positive BASE expectancy in OOS and confirmatory history;
- no catastrophic dependence on IDEAL costs;
- acceptable drawdown and loss-streak behavior under the written risk policy;
- no obvious single-subperiod dependency;
- Monte Carlo robustness if sample size supports it;
- no unresolved leakage/data-integrity defect;
- a separately approved executable short-capable instrument/venue plan before actual paper execution claims;
- independent written Phase-6 review.

Failure to meet these conditions results in `REJECT`, `REVISE_AS_NEW_VERSION`, or `INSUFFICIENT_EVIDENCE`.

## 12. Safety

Phase 6 remains research-only.

```text
PAPER_TRADING_AUTHORIZED = false
SHADOW_TRADING_AUTHORIZED = false
LIVE_TRADING_AUTHORIZED = false
```
