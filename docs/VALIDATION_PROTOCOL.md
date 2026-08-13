# Phase 6 Validation Protocol — CRT v0.1

**Registered:** 2026-08-13  
**Status:** PREREGISTERED — NEW HISTORICAL RESULTS NOT YET OBSERVED  
**Strategy:** `CRT-C3-D1-H1-M1-BEAR-v0.1`  
**Detector:** `CRT-DETECTOR-v0.1`  
**Simulator:** `CRT-BACKTEST-v0.1`  
**Live trading:** **NOT AUTHORIZED**

## 1. Purpose

Phase 6 asks two questions in order:

1. **Does the frozen strategy generate enough independent TradePlans to support meaningful statistical inference?**
2. **If sample size is adequate, does the frozen edge survive historical holdout data, realistic friction and robustness tests?**

The first question is deliberately answered before looking at P&L.

A low-frequency result is not a bug to optimize away. `INSUFFICIENT_EVIDENCE` is a valid Phase-6 decision.

## 2. Frozen baseline

No Phase-6 historical result may silently change:

```text
strategy   CRT-C3-D1-H1-M1-BEAR-v0.1
detector   CRT-DETECTOR-v0.1
simulator  CRT-BACKTEST-v0.1
```

Frozen strategy parameters remain:

```text
P2-PARAM-M1-THICK-050 = body/full_range >= 0.50
P2-PARAM-STOP-1TICK   = structural high + one instrument tick
```

Parameter sensitivity may later evaluate separately versioned hypothetical alternatives, but those runs may not overwrite the frozen baseline.

## 3. Historical contamination policy

The public Romeo corpus used to derive the strategy begins in 2024 and includes 2024–2025 source material/chart examples.

Therefore Phase 6 distinguishes:

```text
2019–2023  PRE-CORPUS historical validation universe
2024–2025  SOURCE-EXPOSED robustness only; never called clean OOS
2026-08-13 onward  TRUE FORWARD post-freeze observations
```

Historical validation cannot substitute for true forward evidence, but using years before the source corpus materially reduces direct chart-example contamination risk.

## 4. Preregistered historical split

The split is fixed **before new Phase-6 detector output is observed**.

### Development / frequency pool

```text
2019-01-01 through 2021-12-31 UTC archive days
```

Purpose:

- validate scaled data ingestion;
- measure frozen candidate/TradePlan frequency;
- debug validation analytics only;
- if frequency is sufficient, permit exploratory performance analysis.

The strategy/detector/simulator themselves remain frozen. Development does **not** permit tuning their rules in place.

### Historical OOS

```text
2022-01-01 through 2022-12-31 UTC archive days
```

This window remains unopened for P&L until development-stage analysis and performance gates are frozen.

### Historical confirmatory

```text
2023-01-01 through 2023-12-31 UTC archive days
```

This is the final pre-corpus confirmatory year. It remains untouched until development and OOS decisions are complete and no further baseline rule/cost-gate choices will be made from historical results.

### Source-exposed robustness — optional later

```text
2024-01-01 through 2025-12-31
```

These years may later test operational robustness, but because the Romeo research corpus itself contains 2024–2025 material, they must be labeled `SOURCE_EXPOSED_ROBUSTNESS` and may not be represented as clean OOS confirmation.

### True forward confirmation

```text
start = 2026-08-13
```

Any post-freeze forward observations are separate from historical Phase-6 inference. Future paper/forward testing must accumulate without retrospective relabeling.

## 5. Stage 6A — frequency gate before P&L

Phase 6 first runs the frozen detector and records only:

- trusted dataset identities;
- D1/H1 coverage;
- rolling candidate count;
- reason-code distribution;
- valid TradePlan count;
- TradePlan timestamps/count by calendar period;
- detector-run SHA.

Stage 6A must **not** report trade outcomes, equity, expectancy, profit factor or parameter comparisons.

### Project sample-sufficiency policy

These are governance thresholds, not universal statistical laws.

For the complete 2019–2021 development pool:

```text
valid TradePlans < 30
    -> INSUFFICIENT_FREQUENCY
    -> stop edge inference for CRT v0.1
    -> do not consume OOS/confirmatory P&L merely to hunt for trades

30 <= valid TradePlans < 100
    -> LIMITED_SAMPLE
    -> exploratory development analysis allowed
    -> no historical-only paper promotion

valid TradePlans >= 100
    -> ADEQUATE_FOR_FULL_HISTORICAL_VALIDATION
    -> proceed to preregistered performance Stage 6B
```

If annual datasets are processed separately, year-boundary C1/C2/C3 candidates must be handled explicitly or excluded deterministically; they may not be recovered selectively based on outcome.

## 6. Stage 6B — performance gates

Stage 6B is activated only after Stage 6A frequency evidence is recorded and a separate `STAGE_6B_PERFORMANCE_PROTOCOL.md` is committed **before P&L is observed**.

That document must freeze:

- primary performance statistic;
- minimum OOS/confirmatory trade counts;
- cost-stress decision rules;
- drawdown/sequence criteria;
- parameter-sensitivity grid;
- walk-forward design;
- Monte-Carlo design;
- regime/session breakdowns;
- exact promotion/rejection criteria.

Until then, Phase 6 may not use historical P&L to choose thresholds after the fact.

## 7. Cost models carried from Phase 5

The frozen project research scenarios remain:

```text
IDEAL     fee 0 bps/side,  half-spread 0 bps/side, slippage 0 bps/side
BASE      fee 10 bps/side, half-spread 1 bp/side,  slippage 2 bps/side
STRESSED  fee 15 bps/side, half-spread 3 bps/side, slippage 5 bps/side
SEVERE    fee 20 bps/side, half-spread 5 bps/side, slippage 10 bps/side
```

They are project assumptions, not historical Binance fee/spread measurements.

Stage 6B may test additional sensitivity values only if preregistered before those outcomes are observed.

## 8. Execution realism limitation

The observation route remains Binance BTCUSDT Spot while the frozen strategy is bearish-only.

Phase-5 execution assumption:

```text
SYNTHETIC_LINEAR_SHORT_RESEARCH_V1
```

Historical strategy robustness under this assumption is research evidence only.

Before paper promotion, the project must choose and verify a short-capable executable instrument/venue contract and model material differences including, where relevant:

- fees;
- spread/slippage;
- margin;
- borrow/funding;
- liquidation;
- contract size/tick/quantity rules;
- trading/session constraints.

## 9. Data trust requirement

Every validation dataset must be separately versioned and satisfy the trusted-data contract.

Required provenance includes:

```text
provider
venue
symbol
coverage
raw hashes
provider verification evidence
canonical H1/D1 digest
dataset version
manifest SHA
market-data code SHA
dependency lock SHA
```

No historical candle may be repaired based on whether it creates or destroys a strategy signal.

## 10. Experiment registry

Phase-6 experiments use stable IDs:

```text
P6-FREQ-2019
P6-FREQ-2020
P6-FREQ-2021
P6-OOS-2022
P6-CONF-2023
```

If batching/technical constraints require multiple acquisition runs, sub-IDs are allowed but the calendar membership may not change after results.

## 11. Required reason-distribution evidence

Because a low TradePlan count may arise from a specific frozen gate, frequency reports preserve counts for at least:

- `NO_BEARISH_PARENT_SWEEP`
- double/opposite sweep rejection
- parent close not reclaimed
- T1 consumed in C2
- no Model-1 confirmation
- TradePlan
- any simulator/data rejection distinct from strategy validity

This helps diagnose rarity without turning diagnosis into post-hoc rule relaxation.

## 12. Decision vocabulary

Phase 6 may conclude:

```text
INSUFFICIENT_EVIDENCE
REJECT
REVISE_AS_NEW_VERSION
HISTORICAL_ROBUSTNESS_PASS_FORWARD_EVIDENCE_REQUIRED
PROMOTE_TO_PAPER_CANDIDATE
```

`REVISE_AS_NEW_VERSION` means the baseline remains preserved and a new research candidate begins from the research/spec gates. It does not mutate v0.1 in place.

## 13. Prohibited Phase-6 behavior

Do not:

- inspect OOS/confirmatory P&L before gates are frozen;
- replace a zero/losing calendar year with another year;
- loosen the strategy to increase trade count;
- tune project parameters on confirmatory data;
- label 2024–2025 source-exposed years as clean OOS;
- combine exploratory and confirmatory results without labels;
- report undefined metrics as zero/good/bad;
- run Monte Carlo on a tiny sample and imply statistical precision;
- claim the synthetic Spot-observation short model is production executable;
- promote directly to live trading.

## 14. Immediate execution order

```text
1. Freeze this protocol
2. Build/verify 2019 development dataset
3. Run frequency-only detector report
4. Build/verify 2020 development dataset
5. Run frequency-only detector report
6. Build/verify 2021 development dataset
7. Aggregate development frequency evidence
8. Apply the predeclared Stage-6A threshold
9. If <30 TradePlans: conclude INSUFFICIENT_FREQUENCY and preserve 2022/2023 untouched
10. If >=30: freeze Stage-6B performance protocol before any development P&L
11. Only then evaluate development performance and later unlock 2022 OOS per protocol
12. Keep 2023 confirmatory untouched until OOS gates are complete
```

This ordering makes it harder for attractive or disappointing results to influence which data becomes “test” data after the fact.
