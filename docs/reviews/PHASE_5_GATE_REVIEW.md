# Phase 5 Gate Review — Event-Driven Backtester

**Date:** 2026-08-13  
**Strategy:** `CRT-C3-D1-H1-M1-BEAR-v0.1`  
**Detector:** `CRT-DETECTOR-v0.1`  
**Simulator:** `CRT-BACKTEST-v0.1`  
**Decision:** **PASS FOR PHASE-6 VALIDATION DESIGN**

## Review question

Can the project simulate frozen detector TradePlans causally and reproducibly without altering strategy validity, granting favorable OHLC sequencing, hiding gaps/censoring, or misrepresenting Binance Spot as an executable short venue?

## Findings

### Frozen upstream semantics

**PASS.** Phase 5 consumes detector outputs. It does not reimplement or modify the frozen CRT strategy predicates.

### Event-time causality

**PASS.** Existing positions are managed through an H1 bar before plans confirmed at that bar close are activated. The confirmation candle's earlier high/low cannot affect a newly created position.

### Entry-reference integrity

**PASS.** `TradePlan.entry_price` must equal the canonical H1 confirmation close or the plan is rejected as `ENTRY_REFERENCE_MISMATCH`.

### Same-bar ambiguity

**PASS.** If an already-open position's stop and target are both inside one H1 envelope, v0.1 resolves the ambiguity as `STOP_FIRST_CONSERVATIVE`.

### Gap realism

**PASS.** A stop gap uses the worse bar open and can exceed the intended risk budget. Favorable target-gap price improvement is deliberately disabled.

### Dataset-end censoring

**PASS.** The simulator does not invent a time exit. Open positions are marked `POSITION_OPEN_AT_END` and excluded from closed-trade expectancy/win-rate metrics.

### Risk sizing

**PASS.** Quantity uses realized equity, declared risk fraction, adverse stop-cost estimate and round-down quantity-step handling. No quantity is rounded upward to consume additional risk.

### Simultaneous candidate ambiguity

**PASS.** If a same-timestamp plan group is larger than available capacity, the group fails closed as `SIMULTANEOUS_PLAN_CONFLICT`. The simulator does not select a winner by hash order or future performance.

### Transaction-cost transparency

**PASS WITH LIMITATION.** Fee/spread/slippage presets are explicit project research assumptions. They are not represented as measured historical Binance costs.

### Execution venue realism

**PASS WITH MATERIAL LIMITATION.** The trusted observation route is BTCUSDT Spot while the frozen strategy is bearish-only. Simulation is explicitly labeled `SYNTHETIC_LINEAR_SHORT_RESEARCH_V1`. This is not production-execution evidence.

### Reproducibility

**PASS.** Run identity binds detector-run SHA, simulator source SHA, quantity step, configuration, outcomes/rejections/censoring and final realized equity.

### Simulator lifecycle coverage

**PASS.** Regressions cover target, stop, same-bar ambiguity, stop gap, target gap, cost adversity, sizing, entry-reference mismatch, simultaneous-plan conflict, open-at-end censoring and deterministic hashing.

### First real historical integration result

**PASS AS INTEGRATION, NOT PERFORMANCE EVIDENCE.** `P5-SIM-001` was preregistered before results. The complete September 2025 window produced 27 rolling detector candidates and zero valid TradePlans. All four cost scenarios therefore had zero completed trades and unchanged realized equity.

The project preserved the zero-activity result and did not change the month or relax rules.

## Adversarial checklist

| Risk | Result |
|---|---|
| Use confirmation bar's earlier high/low after entry | BLOCKED by event order |
| Favorable same-bar stop/target ordering | BLOCKED — stop first |
| Cap stop-gap loss at intended 1R | BLOCKED — worse open used |
| Grant favorable target gap fill | BLOCKED |
| Force-close at data end | BLOCKED |
| Fill at detector price despite canonical close mismatch | BLOCKED |
| Pick one simultaneous plan arbitrarily | BLOCKED |
| Hide zero-trade real month | NOT DONE |
| Change strategy/detector after seeing zero trades | NOT DONE |
| Treat Spot observation as executable naked short | NOT DONE |
| Present research cost presets as historical fact | NOT DONE |
| Omit quantity granularity from run identity | BLOCKED |
| Omit simulator implementation from run identity | BLOCKED |

## Accepted limitations carried to Phase 6

1. September 2025 contains no valid frozen-strategy TradePlans, so there is no real P&L sample yet.
2. A substantially larger preregistered trusted history is required to measure trade frequency and edge.
3. Historical bid/ask spread is unavailable from the current archive route.
4. Cost presets remain assumptions until a better historical/executable cost source is integrated.
5. The short model is synthetic; a real short-capable venue/instrument must be selected before paper/live relevance.
6. Margin, funding, borrow availability and liquidation are not modeled.
7. H1 OHLC cannot reveal exact intrabar order; conservative sequencing is a research approximation.
8. An intrabar stop/target record uses the bar boundary as an audit timestamp, not a claim of exact tick-level fill time.
9. Phase 6 must reject or report a strategy with insufficient trade frequency rather than weakening the frozen rules.

## Evidence

Final deterministic CI:

```text
run  31670117944
job  94352804983
PASS
```

Final provider-backed September replay:

```text
run  31670117938
job  94352804834
PASS
```

## Gate decision

**PASS.** `CRT-BACKTEST-v0.1` is suitable for Phase-6 validation integration under the stated limitations.

This is not approval for paper, shadow or live trading and is not evidence of profitability.
