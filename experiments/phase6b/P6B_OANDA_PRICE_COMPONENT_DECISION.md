# P6B OANDA Price-Component Decision

**Decision ID:** `P6B-OANDA-PRICE-COMPONENT-001`  
**Date:** 2026-08-13  
**Status:** **FROZEN BEFORE STRATEGY OUTCOME ACCESS**  
**Applies to:** `CRT-C3-D1-H1-M1-BEAR-v0.2-MULTI-MARKET-RESEARCH`  
**Strategy outcome access:** **NOT AUTHORIZED**

## Decision

For the OANDA Phase-6B qualification route:

```text
SIGNAL / PATTERN OHLC COMPONENT = MID
OANDA API PRICE PARAMETER        = M
CANDLE SMOOTHING                 = false
SOURCE GRANULARITY               = M1 for canonical reconstruction
```

Bid/ask data are **not** replaced by midpoint for execution modeling. They remain a separate execution/friction input.

## Primary provider semantics

OANDA v20 defines the historical candle pricing components as:

```text
M = midpoint candles
B = bid candles
A = ask candles
```

Official documentation also currently defaults the instrument-candle `price` parameter to `M`.

Primary sources:

- `https://developer.oanda.com/rest-live-v20/primitives-df/`
- `https://developer.oanda.com/rest-live-v20/pricing-ep/`
- `https://developer.oanda.com/rest-live-v20/instrument-df/`

## Why MID is frozen for signal detection

The strategy's deterministic validity predicates operate on candle geometry and relative price relationships:

- parent high/low/midpoint;
- sweep/reclaim;
- Model #1 candle geometry;
- close confirmation;
- structural stop reference;
- target geometry.

Using midpoint as the canonical signal observation:

1. gives one provider-defined symmetric price series rather than selecting bid or ask based on trade direction;
2. keeps spread/executable-side effects out of the alpha pattern definition;
3. allows bid/ask to be modeled independently as execution friction;
4. is selected before any Phase-6B strategy result exists;
5. prevents later switching among M/B/A based on which produces better trade count or P&L.

This is a project market-data parameter, not a claimed Romeo rule.

## Execution boundary

OANDA's execution/pricing model exposes bid and ask prices separately. Phase 6B must therefore later define a cost/execution contract such as:

```text
signal geometry             MID
short entry executable side BID / provider execution model
short stop/cover side       ASK / provider execution model
spread                      derived from contemporaneous B/A evidence
slippage                    separately frozen stress assumption
```

The exact historical fill model is **not frozen by this document**. It requires its own preregistered execution/friction decision before backtesting.

The detector may never use future bid/ask information to alter a previously established MID signal.

## No native-D1 shortcut

This decision does not authorize using OANDA default Daily candles.

The strategy D1 remains:

```text
[00:00 America/New_York, next 00:00 America/New_York)
```

OANDA's documented default daily alignment is 17:00 New York, so Phase 6B must continue to reconstruct canonical D1 from lower-timeframe observations under the frozen session/gap policy.

## Dataset identity effect

`price_component = MID` is part of the new `P6B_CANONICAL_PRICE_DATASET_V2` identity and normalized digest.

A BID- or ASK-derived dataset is therefore a distinct dataset and cannot silently replace MID data under the same dataset version.

## Anti-selection-bias rule

After this decision:

```text
switch MID -> BID because more trades appear      PROHIBITED
switch MID -> ASK because P&L improves             PROHIBITED
choose per-instrument M/B/A from historical result PROHIBITED
```

A future non-MID signal experiment requires a new candidate/data version and its own pre-outcome justification.

## Current authorization

```text
OANDA_SIGNAL_PRICE_COMPONENT          = MID
OANDA_SIGNAL_COMPONENT_FROZEN         = true
OANDA_EXECUTION_MODEL_FROZEN          = false
MULTI_MARKET_OUTCOME_ACCESS_AUTHORIZED= false
PAPER_TRADING_AUTHORIZED              = false
LIVE_TRADING_AUTHORIZED               = false
```
