# Phase 6 Validation Protocol v1

Protocol ID: `P6-VALIDATION-PROTOCOL-v1`  
Status: **PREREGISTERED / NO NEW PHASE-6 OUTCOMES OBSERVED**  
Strategy: `CRT-C3-D1-H1-M1-BEAR-v0.1`  
Detector: `CRT-DETECTOR-v0.1`  
Simulator: `CRT-BACKTEST-v0.1`  
Live trading: **NOT AUTHORIZED**

## 1. Purpose

Phase 6 asks whether the already-frozen CRT v0.1 route has enough historical activity and enough out-of-sample robustness to justify promotion to a paper-trading candidate.

This protocol is frozen **before retrieving or inspecting any new Phase-6 historical outcomes**. The previously observed September 2025 engineering sample is explicitly quarantined from inferential validation.

The allowed final dispositions are:

```text
REJECT
REVISE_AS_NEW_VERSION
INSUFFICIENT_EVIDENCE
PROMOTE_TO_PAPER_CANDIDATE
```

No result can authorize live trading.

## 2. Frozen baseline

Phase 6 must consume the existing frozen chain unchanged:

```text
trusted market data
  -> CRT-DETECTOR-v0.1
  -> immutable TradePlan
  -> CRT-BACKTEST-v0.1
  -> validation analysis
```

Frozen strategy behavior must not be edited in place because of observed P&L or trade frequency.

Any proposed change to strategy validity, Model #1 geometry, Candle-3 eligibility, target, stop, timeframe, session, manipulation rule, entry model, or frozen parameters becomes a **new candidate version** and restarts validation with a newly reserved confirmatory set.

## 3. Observation instrument and execution boundary

Initial validation observation route:

```text
provider  BINANCE_PUBLIC_DATA
venue     BINANCE_SPOT
symbol    BTCUSDT
raw       DAILY 1m archives
D1 clock  America/New_York local midnight
H1 clock  exact elapsed UTC hour
```

The frozen strategy is bearish-only while the observation route is Spot. Backtest short execution therefore remains:

```text
SYNTHETIC_LINEAR_SHORT_RESEARCH_V1
```

This is a research abstraction. It is not evidence that Binance Spot can directly execute the modeled naked short. A real short-capable venue/instrument contract is a separate later gate.

## 4. Fixed simulation configuration

Unless a test is explicitly labeled a preregistered sensitivity diagnostic, the baseline configuration is:

```text
initial_equity            100000
risk_fraction             0.005
max_concurrent_positions  1
quantity_step             dataset instrument metadata
entry/stop/target         immutable detector TradePlan
finite-data-end           CENSOR_OPEN_POSITION
same-bar policy           STOP_FIRST_CONSERVATIVE
favorable target gap      NO PRICE IMPROVEMENT
adverse stop gap          WORSE BAR OPEN
```

Cost scenarios remain the Phase-5 preregistered assumptions:

```text
IDEAL     fee 0 bps/side,  half-spread 0 bps/side, slippage 0 bps/side
BASE      fee 10 bps/side, half-spread 1 bp/side,  slippage 2 bps/side
STRESSED  fee 15 bps/side, half-spread 3 bps/side, slippage 5 bps/side
SEVERE    fee 20 bps/side, half-spread 5 bps/side, slippage 10 bps/side
```

These are research assumptions, not historical Binance bid/ask claims.

## 5. Preregistered chronology

The date partitions are selected before outcome retrieval and must not be shifted because of results.

### DEV — development/frequency window

```text
2019-01-01 through 2022-12-31 UTC archive days
```

Purpose:
- verify multi-year signal frequency;
- detect implementation/data-quality defects;
- characterize descriptive behavior;
- run diagnostic sensitivity only if sample size permits.

DEV results may not be used to alter the frozen v0.1 rules. Any rule change creates a new version.

### OOS — independent validation window

```text
2023-01-01 through 2025-08-31 UTC archive days
```

Purpose:
- independent performance and robustness test of the unchanged frozen baseline.

The OOS result must not be inspected until the DEV evidence report is sealed.

### QUARANTINED — previously observed engineering window

```text
2025-09-01 through 2025-09-30 UTC archive days
```

September 2025 was already used by Phase 5 for provider-backed integration and produced 27 rolling C1/C2/C3 candidates with zero valid TradePlans.

It is excluded from Phase-6 inferential metrics, parameter sensitivity, OOS claims and final confirmation.

### CONFIRM — untouched final confirmatory window

```text
2025-10-01 through 2026-07-31 UTC archive days
```

Purpose:
- final untouched confirmation of the frozen baseline after DEV and OOS reports are sealed.

The CONFIRM data/results must not be inspected early. If Phase 6 is already classified `INSUFFICIENT_EVIDENCE` or `REJECT` before confirmation, the project may leave CONFIRM untouched for a future candidate rather than consume it unnecessarily.

## 6. Sequential access rule

The validation order is mandatory:

```text
freeze protocol
  -> build/analyze DEV
  -> seal DEV report
  -> build/analyze OOS
  -> seal OOS report
  -> decide whether CONFIRM should be consumed
  -> if eligible, build/analyze CONFIRM once
  -> final written decision
```

No OOS/CONFIRM result may be used to tune v0.1.

## 7. Data integrity gate

Every validation dataset must be separately versioned and `TRUSTED` before detector/backtest execution.

Required checks include:

- provider checksum/receipt where available;
- canonical manifest SHA-256;
- normalized content SHA-256;
- market-data code SHA-256;
- dependency-lock SHA-256;
- instrument metadata snapshot/version;
- exact row counts and coverage;
- duplicate/missing/out-of-order detection;
- canonical H1 construction;
- New-York D1 construction with DST correctness;
- no unfinished D1 passed as completed;
- detector/data identity binding.

A failed data gate stops the experiment. Data-quality repairs create a new dataset version and are documented before rerun.

## 8. Activity/sample-size gates

Trade frequency is evaluated before profitability interpretation.

### DEV activity gate

```text
closed trades < 30  -> INSUFFICIENT_DEV_SAMPLE
closed trades >= 30 -> descriptive robustness analysis permitted
```

If DEV has fewer than 30 closed trades across four years, no parameter optimization is permitted and the default Phase-6 disposition is `INSUFFICIENT_EVIDENCE` unless the issue is an independently demonstrated implementation/data defect.

### OOS activity gate

To consider consuming CONFIRM for promotion analysis:

```text
OOS closed trades >= 30
```

If OOS has fewer than 30 closed trades, v0.1 cannot be promoted to paper on statistical evidence from this route.

### Promotion sample floor

For `PROMOTE_TO_PAPER_CANDIDATE`, the independent OOS + CONFIRM sample must contain at least:

```text
60 closed trades total
20 closed trades in CONFIRM
```

These are governance floors, not claims that 60 trades guarantee statistical certainty.

## 9. Primary robustness gates

A paper-candidate promotion requires all of the following on the frozen baseline:

1. sample floors above are met;
2. BASE expectancy is positive in OOS;
3. BASE expectancy is positive in CONFIRM;
4. combined OOS + CONFIRM BASE expectancy is positive;
5. combined OOS + CONFIRM STRESSED expectancy is non-negative;
6. combined OOS + CONFIRM BASE profit factor is greater than `1.0`;
7. realized maximum drawdown at the fixed 0.5% risk configuration is no greater than `15%` in the combined independent sample;
8. no single closed trade contributes more than `25%` of positive total net P&L when total net P&L is positive;
9. the top five winning trades do not contribute more than `60%` of positive total net P&L when total net P&L is positive;
10. there is no discovered look-ahead, data leakage, retrospective parent selection, fill optimism or implementation/spec mismatch;
11. results remain reproducible from recorded code/data/config hashes.

Failure of a gate is reported; it is not repaired by moving dates or silently changing parameters.

SEVERE is a diagnostic survival scenario rather than a mandatory positive-expectancy gate. Its drawdown, expectancy and failure modes must still be reported.

## 10. Required metrics

For every eligible window and cost scenario report at least:

```text
candidate_count
TradePlan_count
closed_trade_count
open_at_end_count
win_rate
average_R
expectancy_R
gross_PnL
net_PnL
profit_factor
max_realized_drawdown
longest_losing_streak
exposure where available
entry-time distribution
result concentration
```

Metrics that are not statistically meaningful at the observed sample size must be labeled accordingly rather than forced.

## 11. Diagnostic parameter sensitivity

Sensitivity is allowed only after the DEV activity gate is met.

The frozen v0.1 baseline remains the reference. Predeclared diagnostic perturbations are:

### Model #1 thick-body threshold

```text
0.40
0.45
0.50  <- frozen baseline
0.55
0.60
```

### Structural stop buffer

```text
0 ticks
1 tick  <- frozen baseline
2 ticks
```

Sensitivity variants are **not** alternate versions of v0.1 and cannot be chosen post hoc for promotion. If a variant motivates a new strategy candidate, it receives a new version and new validation plan.

## 12. Rolling stability analysis

If at least 30 closed trades exist across the analysis history, report calendar-year and rolling 12-month descriptive slices.

No slice is dropped because it is unprofitable.

The baseline should not derive nearly all profit from one short period without that concentration being called out explicitly.

## 13. Monte Carlo protocol

Run only if at least 30 closed trades are available in the relevant sample.

Fixed random seed:

```text
20260813
```

Minimum iterations:

```text
10000
```

At minimum estimate distributions for:

- maximum drawdown;
- longest losing streak;
- final net P&L / cumulative R;
- sequence risk;
- 5% randomly missed trades;
- 10% randomly missed trades.

Monte Carlo does not replace chronological OOS/CONFIRM evidence.

## 14. Regime/session diagnostics

Only if sample size is adequate:

- entry New-York hour distribution;
- calendar year;
- month/quarter;
- causal trailing-volatility buckets if a versioned feature implementation is added;
- trend/range regime only if its classification is independently defined before observing outcome differences.

No regime filter may be retrofitted into v0.1 based on attractive subgroup performance.

## 15. Leakage/overfit review

Before any paper promotion, ReviewAgent or equivalent independent review must verify:

- no future D1/H1 information in detector inputs;
- no final Candle-3 D1 OHLC used before close;
- no retrospective parent/range selection;
- no result-driven date selection;
- no result-driven cost choice;
- no result-driven parameter replacement;
- no favorable same-bar fill assumption;
- exact detector/simulator/data version binding;
- quarantined September 2025 excluded from independent validation metrics.

## 16. Decision rules

### `INSUFFICIENT_EVIDENCE`
Use when sample frequency or data quality prevents a credible robustness conclusion without changing the frozen candidate.

### `REJECT`
Use when the frozen candidate has adequate sample but fails core independent robustness gates or is invalidated by leakage/spec mismatch.

### `REVISE_AS_NEW_VERSION`
Use when evidence motivates a specific rule/design change. The new candidate must not overwrite v0.1 and must receive fresh validation governance.

### `PROMOTE_TO_PAPER_CANDIDATE`
Use only when all mandatory sample, OOS, CONFIRM, cost, drawdown, concentration, reproducibility and leakage gates pass.

Promotion to paper is not live authorization.

## 17. Prohibited actions during Phase 6

- change a date window after seeing results;
- include September 2025 in independent evidence;
- optimize against CONFIRM;
- choose the best sensitivity variant and call it v0.1;
- weaken setup rules to increase trade count;
- change transaction costs because BASE results are unattractive;
- hide zero-trade or losing periods;
- drop outliers only because they hurt results;
- present simulated results as expected live returns;
- authorize paper/shadow/live automatically.

## 18. Phase-6 completion artifact

Phase 6 ends with a written decision report containing:

```text
protocol ID
frozen strategy/detector/simulator IDs
all dataset IDs + hashes
all experiment/run hashes
window-by-window activity
cost-scenario metrics
sensitivity diagnostics if eligible
Monte Carlo if eligible
leakage/overfit review
known limitations
final disposition
```

Until that report is completed and reviewed:

```text
PAPER_TRADING_AUTHORIZED = false
LIVE_TRADING_AUTHORIZED = false
```
