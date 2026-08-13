# Phase 5 Completion Report — Event-Driven Backtester

**Project:** `romeo-crt-engine`  
**Date:** 2026-08-13  
**Phase:** 5 — Event-driven backtester  
**Status:** **COMPLETE**  
**Strategy:** `CRT-C3-D1-H1-M1-BEAR-v0.1` — unchanged  
**Detector:** `CRT-DETECTOR-v0.1` — unchanged  
**Simulator:** `CRT-BACKTEST-v0.1`  
**Profitability:** **NOT ESTABLISHED**  
**Paper / shadow / live trading:** **NOT AUTHORIZED**

## Completion decision

Phase 5 is complete as a deterministic simulation engine.

The project can now take immutable `TradePlan` outputs from the frozen detector and evolve them through a causal H1 event clock with explicit position sizing, transaction-cost assumptions, stop/target sequencing, gap handling, censoring, journaling, realized-equity bookkeeping and deterministic result identity.

This phase proves **simulator integrity**. It does not prove that the strategy has positive expectancy.

## Frozen handoff

```text
strategy   CRT-C3-D1-H1-M1-BEAR-v0.1
detector   CRT-DETECTOR-v0.1
simulator  CRT-BACKTEST-v0.1
```

Machine-readable freeze:

```text
strategy/CRT_V0.1_BACKTEST_FREEZE_MANIFEST.json
```

## Event-order invariant

For every H1 bar:

```text
bar opens
 -> manage positions already open before the bar
 -> observe completed bar path envelope
 -> bar closes
 -> activate TradePlans confirmed at that close
```

A plan confirmed at a close cannot be stopped or targeted by the earlier high/low of its own confirmation candle.

## Entry integrity

A TradePlan activates only when:

- detector/data identity matches;
- entry timestamp equals a canonical H1 close;
- direction is supported by the frozen simulator route;
- entry reference exactly equals the canonical confirmation close;
- capacity/conflict policy permits activation;
- risk sizing produces a positive permitted quantity.

`ENTRY_REFERENCE_MISMATCH` fails closed rather than silently choosing one price.

## Simultaneous-plan policy

Overlapping detector parents can create more than one plan at the same timestamp.

If an already-open position uses all capacity, new plans are rejected as `POSITION_LIMIT`.

If there is positive capacity but the simultaneous group is larger than available slots, the entire group is rejected as `SIMULTANEOUS_PLAN_CONFLICT`.

The simulator never chooses an arbitrary candidate by hash ordering or later P&L.

## Synthetic short boundary

The first trusted observation route is Binance BTCUSDT **Spot**, while the frozen strategy is bearish-only.

Phase 5 therefore labels execution:

```text
SYNTHETIC_LINEAR_SHORT_RESEARCH_V1
```

This permits deterministic research of short stop/target/cost mechanics, but it is **not** a claim that the modeled naked short is directly executable on Binance Spot.

Before paper/live relevance the project requires a separately governed executable short venue/instrument contract, including margin/funding/liquidation and venue-specific execution semantics where material.

## Transaction-cost presets

The following are project research assumptions, not historical Binance claims:

| Scenario | Fee / side | Half-spread / side | Slippage / side |
|---|---:|---:|---:|
| IDEAL | 0 bps | 0 bps | 0 bps |
| BASE | 10 bps | 1 bp | 2 bps |
| STRESSED | 15 bps | 3 bps | 5 bps |
| SEVERE | 20 bps | 5 bps | 10 bps |

Adverse price adjustment is applied to both entry and exit and fees are charged on simulated fill notional.

## Risk sizing

Research sizing uses realized equity:

```text
risk_budget = realized_equity * risk_fraction
```

The frozen Phase-5 research control is `0.5%` for the first historical integration run.

For a bearish plan, quantity is calculated against the estimated adverse stop loss including entry/exit costs and rounded **down** to the allowed quantity step.

Normal modeled stop execution therefore does not exceed the declared budget because of rounding. A gap through the stop may exceed the intended risk and is reported rather than clipped.

## Stop / target / gap semantics

### Same-bar ambiguity

If an already-open position's H1 has both:

```text
high >= stop
low <= target
```

OHLC cannot reveal which occurred first.

Frozen policy:

```text
STOP_FIRST_CONSERVATIVE
```

### Stop gap

```text
bar.open >= stop
 -> stop at worse bar open
```

### Favorable target gap

```text
bar.open <= target
 -> target at declared target reference
```

No favorable price improvement is granted in v0.1.

### Dataset end

The frozen strategy has no time exit, so historical data ending cannot invent one.

Positions still open at the final H1 are recorded as `POSITION_OPEN_AT_END`, marked for audit and excluded from closed-trade expectancy/win-rate statistics.

## Deterministic provenance

Every result binds:

```text
strategy version
detector version
detector-run SHA
dataset version + manifest SHA
simulator version
simulator-code SHA
quantity step
backtest-config SHA
backtest-run SHA
```

`simulator_code_sha256` hashes the Phase-5 Python source package. Quantity step is included because changing permitted quantity granularity can change size and P&L even when the TradePlan is identical.

## Simulator-integrity regressions

The test suite covers:

- target exit only after confirmation;
- structural stop;
- same-bar stop+target ambiguity;
- adverse stop gap;
- no favorable target-gap improvement;
- censored open-at-end position;
- adverse fee/spread/slippage effects;
- risk sizing and quantity-step rounding;
- entry-reference mismatch;
- simultaneous-plan conflict;
- deterministic identical-input run hash;
- different quantity step => different run identity.

These tests exercise the actual simulator lifecycle independently of whether a real historical month produces a valid CRT TradePlan.

## Preregistered historical integration — P5-SIM-001

Before observing detector or P&L results, Phase 5 preregistered the full UTC calendar month:

```text
BTCUSDT
2025-09-01 through 2025-09-30
```

The month was selected mechanically around the already-established September Phase-3 source dates, not because of observed performance.

Trusted canonical shape:

```text
43,200 M1
720 H1
29 complete New-York D1
27 rolling C1/C2/C3 candidates
```

### Observed frozen-strategy result

```text
detector candidates  27
valid TradePlans      0
completed trades      0
```

All four cost scenarios therefore correctly produced:

```text
realized equity  100000
net P&L          0
expectancy R     undefined / no closed sample
```

This is preserved as a **negative/zero-activity result**.

The project did not switch months, relax the detector or change the strategy to manufacture trades.

Canonical result record:

```text
experiments/phase5/P5_SIMULATION_WINDOW_001_RESULTS.json
```

## Final quality evidence

Exact simulator source head used for the final engineering gate:

```text
dbd29ae17ed067511d4c256398bc088903577691
```

Deterministic CI:

```text
workflow run  31670117944
job           94352804983
result        SUCCESS
locked install PASS
Ruff           PASS
strict MyPy    PASS
pytest         PASS
```

Provider-backed preregistered replay:

```text
workflow run  31670117938
job           94352804834
result        SUCCESS
```

The replay rebuilt the complete September trusted dataset and reproduced the same 27-candidate / zero-TradePlan result across all four cost configurations.

## What Phase 5 completion does NOT mean

Phase 5 does not establish:

- positive expectancy;
- a sufficient trade count;
- out-of-sample robustness;
- walk-forward stability;
- optimal strategy parameters;
- historical spread accuracy;
- a production-executable short venue;
- margin/funding/liquidation realism;
- paper readiness;
- live readiness.

The September result contains no realized strategy trades and therefore cannot answer whether the strategy is profitable.

## Phase-6 handoff

Phase 6 may begin **validation design and dataset preregistration**, not profitability marketing.

It must:

1. preserve the frozen strategy/detector/simulator triple;
2. preregister substantially larger trusted historical windows before observing results;
3. separate development, OOS and confirmatory data;
4. build enough trusted history to establish whether the frozen strategy generates a meaningful sample at all;
5. run the four cost scenarios plus sensitivity tests;
6. perform walk-forward, sequence/Monte-Carlo and regime breakdowns only if trade count supports them;
7. report zero/low trade frequency as a result rather than loosening rules;
8. treat the synthetic-short route as research-only until an executable instrument/venue is formally selected.

`LIVE_TRADING_AUTHORIZED=false` remains unchanged.
