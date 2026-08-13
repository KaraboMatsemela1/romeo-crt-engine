# Event-Driven Backtester Contract

## Purpose

Phase 5 simulates the lifecycle of immutable `TradePlan` outputs from the frozen detector without changing strategy validity.

The first simulator route is:

```text
trusted canonical H1/D1
  -> CRT-DETECTOR-v0.1
  -> immutable TradePlan
  -> causal H1 event clock
  -> synthetic execution/cost model
  -> position lifecycle
  -> completed/censored trade record
  -> deterministic journal + metrics + run SHA
```

Frozen upstream identities:

```text
strategy  CRT-C3-D1-H1-M1-BEAR-v0.1
detector  CRT-DETECTOR-v0.1
```

Simulator identity:

```text
CRT-BACKTEST-v0.1
```

## Hard architecture boundary

The backtester does not decide whether a CRT setup is valid.

It consumes detector outputs and may only:

- reject a TradePlan for simulator/execution-state reasons;
- size a simulated position under declared research controls;
- apply declared friction assumptions;
- evolve open positions causally;
- record exits/censoring;
- calculate deterministic metrics.

It may not rewrite the parent, sweep, reclaim, Model-1, entry, stop or target predicates because a simulated result is unattractive.

## Event clock

For each canonical H1 bar, processing order is:

```text
1. bar opens
2. manage positions that were already open before this bar
3. observe the completed bar
4. bar closes
5. activate TradePlans whose confirmation timestamp equals this close
```

This ordering is critical.

A TradePlan confirmed at an H1 close did not exist during the earlier high/low path of that same H1 candle. Therefore the confirmation candle cannot retrospectively stop or target the newly created position.

## Entry integrity

Before a plan may activate:

1. its detector run must match the canonical dataset version, manifest and normalized digest;
2. its entry timestamp must equal an available canonical H1 close;
3. its direction must be supported by the frozen simulator route;
4. its entry reference must equal the canonical H1 confirmation close;
5. capacity/conflict rules must permit activation;
6. risk sizing must produce at least one permitted quantity step.

Failure is explicit and journaled.

### Entry-reference mismatch

If:

```text
TradePlan.entry_price != canonical confirmation H1 close
```

then:

```text
ENTRY_REFERENCE_MISMATCH
```

The backtester does not silently fill at either price.

## Simultaneous-plan policy

The frozen detector may produce overlapping parent candidates.

The simulator does not select among simultaneous plans using candidate hash order, P&L knowledge or any later outcome.

If there is positive capacity but a same-timestamp plan group is larger than the available position slots, all plans in that group are rejected as:

```text
SIMULTANEOUS_PLAN_CONFLICT
```

If no capacity is available because existing positions already occupy the limit, plans are rejected as:

```text
POSITION_LIMIT
```

This is intentionally fail-closed until a separately governed portfolio/ranking rule exists.

## First execution assumption

```text
SYNTHETIC_LINEAR_SHORT_RESEARCH_V1
```

This label is important.

The first trusted observation feed is Binance BTCUSDT **Spot**, while the frozen strategy is bearish-only and therefore requires short exposure.

The Phase-5 simulator models a linear synthetic short for research so that stop/target/cost mechanics can be tested. This does **not** claim that the modeled naked short is directly executable on Binance Spot.

Before live relevance, the project must establish an executable venue/instrument route whose contract, funding/margin/liquidation rules and costs match the intended short exposure.

## Position sizing

Research sizing is based on realized equity and estimated adverse stop loss.

```text
risk_budget = realized_equity * risk_fraction
```

For a bearish position, estimated loss per unit includes:

```text
adverse stop fill - adverse entry fill
+ entry fee
+ exit fee
```

Then:

```text
raw_quantity = risk_budget / estimated_loss_per_unit
quantity = floor(raw_quantity / quantity_step) * quantity_step
```

Quantity is rounded **down**, never up.

A normal stop under the declared fill assumptions therefore cannot exceed the budget merely because of quantity rounding. A market gap can exceed the budget and must be reported rather than clipped.

## Cost model

Each side may include:

```text
fee_bps
half_spread_bps
slippage_bps
```

For the synthetic bearish route:

```text
entry fill = reference * (1 - adverse_price_rate)
exit fill  = reference * (1 + adverse_price_rate)
```

where:

```text
adverse_price_rate = (half_spread_bps + slippage_bps) / 10,000
```

Fees are charged on simulated fill notional.

## Predeclared research cost scenarios

These values are **project research assumptions**, not claims about exact historical Binance trading costs.

### IDEAL

```text
fee         0 bps / side
half spread 0 bps / side
slippage    0 bps / side
```

### BASE

```text
fee         10 bps / side
half spread  1 bp  / side
slippage     2 bps / side
```

### STRESSED

```text
fee         15 bps / side
half spread  3 bps / side
slippage     5 bps / side
```

### SEVERE

```text
fee         20 bps / side
half spread  5 bps / side
slippage    10 bps / side
```

Phase 6 must stress assumptions systematically; these presets are not optimized values.

## Stop and target sequencing

H1 OHLC does not reveal the exact intrabar path.

### Gap at bar open

For an already-open bearish position:

```text
bar.open >= stop
    -> STOP_GAP at bar.open
```

The worse opening reference is used; loss is not capped to intended 1R.

For a favorable target gap:

```text
bar.open <= target
    -> TARGET_GAP at target
```

The simulator deliberately does **not** grant favorable price improvement in v0.1.

### Both stop and target inside one H1

If:

```text
bar.high >= stop
and
bar.low <= target
```

exact ordering is unknowable from OHLC.

Policy:

```text
STOP_FIRST_CONSERVATIVE
```

Exit reason:

```text
STOP_SAME_BAR_AMBIGUITY
```

The simulator does not choose whichever ordering improves performance.

### Single-level hit

Otherwise:

```text
high >= stop -> STOP
low <= target -> TARGET
```

For intrabar H1 exits, the stored bar-close timestamp is an **audit timestamp for the bar in which the fill is assumed**, not a claim that the fill occurred exactly at the H1 close.

## Dataset end

The frozen strategy has no time exit.

Therefore the simulator may not invent one merely because historical data ends.

If a position is still open at the final canonical H1:

```text
POSITION_OPEN_AT_END
```

The position is marked for audit, but realized equity is unchanged and the trade is excluded from closed-trade expectancy/win-rate metrics.

Open-at-end observations are censored data, not wins or losses.

## Journal

Phase-5 journal events include:

```text
PLAN_REJECTED
ENTRY_FILLED
EXIT_FILLED
POSITION_OPEN_AT_END
```

Completed trade records retain:

- candidate ID;
- immutable TradePlan;
- entry reference/fill/quantity/fee;
- exit reference/fill/fee;
- exit reason;
- risk budget;
- gross P&L;
- total fees;
- net P&L;
- R multiple;
- realized equity after exit.

## Metrics

The first simulator integrity metrics are deliberately basic:

- closed trade count;
- wins/losses;
- win rate when defined;
- gross P&L;
- net P&L;
- total fees;
- average / expectancy R;
- profit factor when defined;
- maximum realized-equity drawdown.

Phase 6 owns broader validation metrics and statistical interpretation.

## Deterministic run identity

`BacktestConfig` has a deterministic SHA-256 over:

- simulator version;
- initial equity;
- risk fraction;
- maximum concurrent positions;
- execution assumption;
- same-bar/gap/end policies;
- cost-model version and values.

A backtest run SHA then binds:

```text
detector run SHA
+ backtest config SHA
+ completed trades
+ rejections
+ open-at-end records
+ final realized equity
```

Identical data, detector output and simulator configuration must reproduce the same run identity.

## Simulator-integrity fixture coverage

The deterministic regression suite covers:

- target exit after entry confirmation;
- structural stop exit;
- same-bar stop+target ambiguity;
- stop gap using worse open;
- target gap without favorable improvement;
- open position at dataset end;
- friction-adverse entry and exit;
- risk sizing under costs;
- quantity-step rounding;
- entry-reference mismatch;
- simultaneous-plan conflict;
- deterministic run hashing.

These fixtures validate execution semantics. They do not prove strategy profitability.

## First historical integration sample

`P5-SIM-001` was preregistered before results:

```text
BTCUSDT Spot observation data
2025-09-01 through 2025-09-30 UTC daily archives
entire calendar month
```

The window was chosen mechanically around the already-established September Phase-3 dates rather than by examining performance.

Its results must be preserved even if it has zero TradePlans or negative performance.

## What Phase 5 does not establish

Phase 5 does not establish:

- positive expectancy;
- out-of-sample robustness;
- walk-forward stability;
- optimal cost assumptions;
- an executable short venue;
- margin/funding/liquidation realism;
- paper readiness;
- live readiness.

Those remain later gates.
