# ADR-009 — OANDA Execution Evidence Boundary Before Multi-Market Simulation

**Status:** Accepted boundary / full execution model remains blocked  
**Date:** 2026-08-13  
**Phase:** 6B  
**Strategy outcome access:** **NOT AUTHORIZED**

## Context

Phase 6B has now frozen:

- the multi-market research candidate identity;
- the unchanged bearish v0.1 alpha semantics;
- MID as the OANDA signal component;
- provider-neutral price data v2;
- session-aware H1/D1 aggregation mechanics;
- the `CRT-DETECTOR-v0.2-MULTI-MARKET` compatibility baseline.

The next architectural temptation would be to adapt the v0.1 synthetic-linear backtester immediately to OANDA.

That would be premature.

The original simulator assumes one linear price/quantity P&L model and generic basis-point costs. OANDA's actual execution contract includes account/instrument-specific unit precision, minimum/maximum sizes, commission structures, home-currency conversion factors, bid/ask execution prices and potentially financing/other instrument rules.

Those semantics must be resolved before a provider-backed simulator is allowed to produce performance metrics.

## Primary provider facts accepted

Official OANDA v20 documentation establishes the following provider semantics.

### Direction / units

A long order buys units; a short order sells units.

OANDA's market-order example sells EUR/USD with negative units:

```text
units = -100
```

Therefore the provider execution adapter may treat:

```text
positive units -> long/buy
negative units -> short/sell
```

This is provider semantics, not a strategy rule.

### Unit precision and minimum size

OANDA instrument metadata defines:

```text
tradeUnitsPrecision
minimumTradeSize
maximumOrderUnits
maximumPositionSize
```

`tradeUnitsPrecision` is the number of decimal places allowed when specifying units. The provider-order unit quantum implied by that formatting rule is:

```text
provider_unit_precision_step = 10 ^ (-tradeUnitsPrecision)
```

This is an order-quantity precision contract, not the instrument's price tick.

A future sizing adapter must additionally enforce `minimumTradeSize` and account/instrument maximums.

### Price components / natural order side

OANDA exposes MID, BID and ASK price components.

Its order definitions describe the default/natural trigger side as:

```text
long / buy  -> ASK
short / sell -> BID
```

and state that orders are filled using their default price component.

For the active bearish candidate the research architecture is therefore:

```text
signal geometry     MID
short entry side    SELL / natural BID-side execution evidence
short close side    BUY / natural ASK-side execution evidence
```

The exact bar-level historical fill algorithm is **not yet frozen** by this ADR.

### Instrument commission

OANDA's instrument schema includes an account/instrument commission structure containing:

```text
commission
unitsTraded
minimumCommission
```

with commission amounts represented in the account's home currency.

Therefore a generic hardcoded commission percentage must not silently replace the actual account/instrument contract for the eventual OANDA base scenario.

Stress scenarios may later add separately preregistered slippage/friction assumptions, but the provider-base model must first be grounded in the discovered account contract.

### Home-currency conversion

OANDA defines `HomeConversionFactors` for converting realized gains/losses from instrument base/quote currency into the account home currency.

This matters for:

- cross-instrument position sizing;
- pooled absolute P&L;
- commission effects;
- account-level risk limits.

The original BTCUSDT linear simulator does not provide this multi-currency/account conversion contract.

## Decisions frozen now

The following may be implemented before provider-backed outcomes:

```text
OANDA direction sign:
  buy/long  = positive units
  sell/short = negative units

provider quantity precision:
  unit step = 10 ^ (-tradeUnitsPrecision)

minimum provider quantity:
  minimumTradeSize from account instrument metadata

signal component:
  MID (already frozen by P6B-OANDA-PRICE-COMPONENT-001)

execution-side evidence:
  short open is sell/BID-side
  short close is buy/ASK-side
```

These decisions may not be changed because a later historical result looks better.

## Decisions explicitly not frozen yet

Provider-backed simulation remains blocked on:

1. exact accepted instrument API symbols;
2. exact account/division instrument metadata;
3. maximum order/position constraints;
4. account/instrument commission structure;
5. account home currency;
6. historical home-conversion methodology;
7. contemporaneous BID/ASK retrieval and synchronization with MID signals;
8. exact stop/target trigger/fill treatment on BID/ASK bars;
9. slippage model and stress scenarios;
10. financing treatment for positions crossing financing timestamps;
11. CFD/metal contract-value behavior where applicable;
12. account-specific guaranteed-stop requirements if relevant;
13. provider-backed quantity/risk sizing and portfolio aggregation.

## Why the old simulator cannot simply be reused

`CRT-BACKTEST-v0.1.1` remains valid historical evidence for its frozen BTCUSDT research route.

Using it unchanged for OANDA would silently assume:

- one universal linear contract value;
- the same quantity semantics across currencies, indices and metals;
- a generic percentage spread instead of actual bid/ask evidence;
- no account-home-currency conversion problem;
- no provider commission/minimum commission contract.

Those assumptions would be convenient but not sufficiently auditable for multi-market validation.

## Sequencing decision

Phase 6B uses this order:

```text
1. provider/account instrument discovery
2. exact universe freeze
3. session + price-quantum + quantity metadata freeze
4. trusted MID/BID/ASK data retrieval/provenance
5. detector-only activity gate may be preregistered/run without P&L
6. if sample is sufficient, freeze provider-backed execution/cost/conversion model
7. create separately versioned simulator compatibility baseline
8. only then authorize P&L/expectancy validation
```

This sequence avoids spending credibility on a detailed simulator before knowing whether the frozen strategy generates enough multi-market TradePlans to support statistical inference.

The detector-only activity gate still counts no P&L outcome and may not be used to alter alpha rules or the ex-ante instrument universe.

## Provider documentation

Primary documentation used by this decision:

- `https://developer.oanda.com/rest-live-v20/primitives-df/`
- `https://developer.oanda.com/rest-live-v20/order-df/`
- `https://developer.oanda.com/rest-live-v20/order-ep/`
- `https://developer.oanda.com/rest-live-v20/transaction-df/`
- `https://developer.oanda.com/rest-live-v20/account-ep/`

## Authorization boundary

```text
OANDA_DIRECTION_UNIT_SIGN_FROZEN       = true
OANDA_QUANTITY_PRECISION_RULE_FROZEN   = true
OANDA_SIGNAL_COMPONENT_FROZEN          = true
OANDA_EXECUTION_SIDE_EVIDENCE_FROZEN   = true
OANDA_FULL_EXECUTION_MODEL_FROZEN      = false
MULTI_MARKET_SIMULATOR_AUTHORIZED      = false
MULTI_MARKET_PNL_OUTCOME_ACCESS        = false
PAPER_TRADING_AUTHORIZED               = false
LIVE_TRADING_AUTHORIZED                = false
```
