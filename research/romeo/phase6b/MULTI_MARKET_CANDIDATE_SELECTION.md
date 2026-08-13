# Phase 6B — Multi-Market Successor Selection

**Date:** 2026-08-13  
**Status:** **SELECTED / PROVIDER-DATA GATE OPEN**  
**Predecessor:** `CRT-C3-D1-H1-M1-BEAR-v0.1`  
**Research candidate:** `CRT-C3-D1-H1-M1-BEAR-v0.2-MULTI-MARKET-RESEARCH`  
**Alpha-rule changes:** **NONE AUTHORIZED**  
**Historical strategy outcome access:** **NOT AUTHORIZED**

## Purpose

The first Phase-6B successor hypothesis attempted to add the bullish D1 -> H1 Model #1 direction. That path closed with `EVIDENCE_INSUFFICIENT` before any outcome access because several bullish order-path predicates could not be primary-source verified.

The next successor therefore takes the lower-ambiguity route:

> preserve the already frozen bearish D1 -> H1 Model #1 strategy semantics and test whether the hypothesis is observable across additional Romeo-relevant market families using separately trusted provider data.

This is a market-universe revision, not an alpha relaxation.

## Why this is independently justified

### 1. The v0.1 Phase-6 conclusion is instrument-route specific

ADR-005 states that BTCUSDT was chosen as the **first engineering/validation route** because its 24/7 venue simplified data-quality and DST work. The ADR explicitly says BTCUSDT results must not be generalized to Forex, index futures, metals, or other instruments.

The Phase-6 result therefore establishes:

```text
frozen bearish CRT v0.1
+ BTCUSDT Binance Spot observation route
= insufficient sample for statistical validation
```

It does not establish that the same frozen strategy semantics are necessarily too sparse on every source-relevant market.

### 2. Romeo's first-party corpus is multi-market

The existing evidence record includes first-party examples/references involving:

- NQ / Nasdaq context;
- NQ - ES as a basic related-market pair;
- EUR/USD - DXY as a basic related-market pair;
- Gold - Silver as a basic related-market pair;
- BTC - ETH as a basic related-market pair.

The bearish `old CRTH` clarification that motivated the v0.1 one-sided reference subtype was itself recorded from an NQ example.

This makes a non-crypto validation route independently motivated by the source corpus rather than by the four-trade BTC result.

### 3. No strategy predicate needs to be weakened

The candidate does **not** authorize changing:

- D1 parent enumeration;
- bearish C2 sweep/reclaim rules;
- midpoint consumption;
- H1 Model #1 geometry;
- 0.50 body/range project parameter;
- confirmation rule;
- target;
- structural stop;
- one-tick execution buffer policy;
- Candle-3 expiry;
- risk fraction;
- cost model merely to improve results.

If provider/instrument mechanics require an execution-policy difference, that difference must be versioned separately from alpha validity.

## Candidate provider — OANDA v20 REST API

OANDA v20 is selected for provider qualification, not yet as trusted validation data.

Official documentation establishes that the API can:

- enumerate instruments available to the user's account/division;
- retrieve historical candlestick pricing;
- provide M1 and H1 granularities;
- expose bid, ask and midpoint price components;
- expose instrument precision/pip/type metadata;
- configure candle alignment timezone and daily alignment;
- return complete-candle state;
- provide historical pricing reaching back to 2005 according to OANDA's current introduction documentation.

Canonical documentation:

- `https://developer.oanda.com/rest-live-v20/introduction/`
- `https://developer.oanda.com/rest-live-v20/account-ep/`
- `https://developer.oanda.com/rest-live-v20/pricing-ep/`
- `https://developer.oanda.com/rest-live-v20/instrument-df/`
- `https://developer.oanda.com/rest-live-v20/primitives-df/`

## Critical provider-calendar rule

OANDA's default daily alignment is **17:00 America/New_York**.

That is **not** the frozen strategy D1 calendar, which is New-York local midnight.

Therefore the project must not request default OANDA D candles and silently treat them as Romeo CRT Daily candles.

Required route:

```text
OANDA M1/H1 observations
        ↓
UTC-normalized raw chronology
        ↓
explicit venue/session-gap model
        ↓
project-owned H1 chronology
        ↓
America/New_York 00:00 -> 00:00 D1 aggregation
        ↓
frozen CRT strategy
```

Provider-native D1 is permitted only as a cross-check if explicitly requested with alignment matching the strategy calendar and independently verified against project aggregation.

## Candidate observation universe

The exact instrument list cannot be frozen until the user's OANDA account/division is queried because OANDA documents that tradeable instruments are division-dependent.

The initial priority universe is therefore a source-backed **family whitelist**, not assumed API symbols:

```text
1. US NAS 100 / NQ proxy
2. US SPX 500 / ES proxy
3. EUR/USD
4. Gold/USD
```

Secondary candidates may include Silver/USD and ETH/BTC routes where provider/data contracts permit, but they are not automatically part of the first validation basket.

### Instrument freeze rule

Before any strategy outcome is calculated:

1. query OANDA account instruments;
2. map source market family -> exact OANDA instrument;
3. record instrument type, display precision, pip location and minimum trade metadata;
4. verify historical coverage for the preregistered window;
5. verify session/closure semantics;
6. freeze the accepted instrument list in a machine-readable manifest;
7. only then authorize detector execution.

No instrument may be added or removed because its preliminary P&L looks favorable/unfavorable.

## Data trust model

Binance public archives provided published file checksums. OANDA is an API route, so its provenance contract must be different rather than pretending equivalent checksum evidence exists.

Minimum OANDA trusted-data record:

```text
provider                    OANDA_V20
account division            recorded without secrets
instrument                  exact API name
request URL template        canonicalized / token redacted
request parameters          exact
price component             frozen
retrieved_at                UTC
raw response SHA-256        recorded
row/candle count            recorded
first/last timestamp        recorded
complete flags              validated
instrument metadata         versioned snapshot
code SHA-256                recorded
dependency lock SHA-256     recorded
normalized content SHA-256  recorded
provider re-fetch policy    frozen
cross-check policy          frozen
```

### Re-fetch verification

Before a dataset is trusted, selected historical slices must be re-requested independently and compared to the sealed response/normalized values.

Any provider correction produces a new dataset version; historical bytes/results are not silently overwritten.

## Price component gate

OANDA supports midpoint (`M`), bid (`B`) and ask (`A`) candles.

The project must freeze the research price component before outcome access.

Recommended research architecture:

- use midpoint observations for strategy-pattern detection only if the choice is frozen and documented;
- retain bid/ask data where available for execution-friction validation;
- never use a price component selected after observing which one produces better signals/P&L.

The final choice requires an explicit provider-data ADR/gate decision.

## Venue/session gaps

Unlike BTCUSDT Spot, OANDA forex/index/metal instruments are not continuous 24/7 streams.

The project must therefore distinguish:

```text
KNOWN MARKET CLOSED
KNOWN MAINTENANCE / SESSION BREAK
PROVIDER MISSING DATA
UNKNOWN GAP
```

No synthetic price is permitted to bridge a closure or missing interval.

A canonical D1 may contain fewer absolute trading observations while still occupying its New-York wall-clock envelope.

The detector must fail closed where required observations are insufficient.

## Short execution improvement

The v0.1 BTCUSDT Spot backtest required `SYNTHETIC_LINEAR_SHORT_RESEARCH_V1` because Binance Spot cannot directly execute the modeled naked short.

OANDA's relevant FX/CFD instruments may support short positions depending on account/division/instrument contract. Provider qualification must record the actual short-capable execution boundary instead of assuming it.

Historical alpha detection remains separate from eventual broker execution semantics.

## Validation design boundary

This candidate is **not yet authorized to reuse the v0.1 DEV/OOS/CONFIRM partitions**.

A new protocol must decide:

- per-instrument history availability;
- development window;
- OOS window;
- final confirmatory window;
- cross-instrument pooling rules;
- minimum sample per instrument and pooled sample;
- whether one instrument may dominate the combined sample;
- friction assumptions by asset class;
- session/regime breakdowns;
- multiple-comparison controls.

All of those decisions must be frozen before strategy outcomes are opened.

## Anti-selection-bias rule

The project must never:

```text
run 50 instruments
-> keep only profitable ones
-> call that the candidate universe
```

The instrument universe must be selected from source relevance + provider/data eligibility before outcome retrieval.

If an instrument fails data-quality or execution-contract gates, the exclusion reason must be recorded before outcome access.

## Current state

```text
bullish v0.2 research path          EVIDENCE_INSUFFICIENT / PRESERVED
multi-market bearish successor      SELECTED
alpha semantics                     INHERIT FROZEN v0.1 / NO CHANGES
OANDA provider qualification        OPEN
instrument universe freeze          OPEN
new market datasets                 NOT TRUSTED YET
strategy outcome access             NOT AUTHORIZED
Phase 7                             BLOCKED
```

## Next gate

`Gate 6B-MM-1 — OANDA provider/data qualification`

Exit requires:

1. provider adapter contract;
2. account instrument discovery;
3. canonical M1/H1 retrieval;
4. project-owned New-York-midnight D1 aggregation;
5. price-component decision;
6. session-gap taxonomy;
7. provenance/re-fetch verification;
8. instrument metadata capture;
9. tests for DST, closures, duplicate/out-of-order/missing candles;
10. frozen pre-outcome instrument universe manifest.

Only after that may Phase 6B design a new validation protocol.