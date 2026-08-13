# ADR-007 — Provider-Neutral Canonical Price Data for Phase 6B

**Status:** Accepted for implementation  
**Date:** 2026-08-13  
**Applies to:** Phase 6B multi-market provider/data qualification  
**Changes frozen v0.1 data schema:** **NO**

## Context

The existing Phase-3 trusted-data path was intentionally built around Binance public BTCUSDT archives. Its canonical `MinuteBar`, `CanonicalBar`, and `PHASE3_DATASET_MANIFEST_V1` records contain Binance-meaningful activity fields:

```text
base volume
quote volume
trade count
```

OANDA historical candles expose a different activity concept: the provider documents candle `volume` as the **number of prices created during the candle**.

Treating OANDA `price_count` as Binance base volume, quote volume, or exchange trade count would create false data semantics even if the OHLC values were correct.

At the same time, the frozen v0.1 detector converts canonical D1/H1 bars into strategy `ClosedCandle` objects using only:

```text
timeframe
open_time
close_time
open
high
low
close
```

The detector separately consumes an explicit positive price quantum/tick value from dataset identity for the one-quantum execution buffer. It does not use volume or trade counts in strategy validity.

Therefore provider activity semantics are not part of the current alpha hypothesis and should not block a clean price-only canonical contract.

## Decision

Introduce a new provider-neutral canonical price-data schema for Phase 6B rather than mutating or overloading the frozen Phase-3 schema.

Working schema/version names:

```text
P6B_CANONICAL_PRICE_DATASET_V2
P6B_CANONICAL_PRICE_NORMALIZER_V1
```

The existing:

```text
PHASE3_DATASET_MANIFEST_V1
NY_D1_H1_FROM_UTC_M1_V1
```

remain historical/frozen contracts for the Binance/BTCUSDT v0.1 evidence chain.

## Canonical price-bar contract

A Phase-6B canonical price bar must contain only fields that have the same meaning across providers:

```text
provider
venue
instrument
price_component
bar timeframe
open timestamp UTC
close timestamp UTC
open
high
low
close
source observation count
source digest
session/gap policy version
```

Activity data is optional metadata and is not required for a canonical price bar.

## Activity metadata contract

When provider activity is retained, it must be typed by meaning rather than squeezed into legacy fields.

Allowed Phase-6B activity semantics include:

```text
PRICE_COUNT
BASE_VOLUME
QUOTE_VOLUME
TRADE_COUNT
NONE
```

A provider may expose more than one activity measure. Each measure must keep its own semantic label.

Examples:

```text
Binance:
  base_volume   -> BASE_VOLUME
  quote_volume  -> QUOTE_VOLUME
  trade_count   -> TRADE_COUNT

OANDA:
  candle volume -> PRICE_COUNT
```

Prohibited:

```text
OANDA price_count -> base_volume
OANDA price_count -> trade_count
missing provider activity -> numeric zero pretending actual zero activity
```

Missing/unavailable activity is represented as unavailable, not zero.

## Price component becomes first-class

Provider-neutral price identity must include the exact price component used to build OHLC.

For OANDA this may be:

```text
MID
BID
ASK
```

For Binance Spot the native traded-price series may use:

```text
TRADED
```

A dataset built from MID is a different canonical dataset from one built from BID or ASK even when timestamps are identical.

The component must be frozen before strategy outcomes are opened.

## Price quantum is a separate instrument/execution contract

The frozen v0.1 strategy uses a one-instrument-quantum execution buffer. The legacy Binance route represented this through `price_tick_size` in the trusted manifest.

For Phase 6B, price quantum must be explicit but must not be inferred casually from unrelated display metadata.

The new instrument contract must record:

```text
price_quantum
price_quantum_source
price_quantum_observed_at
instrument metadata response digest
```

Permitted source classifications may include:

```text
PROVIDER_EXPLICIT
PROVIDER_PRICE_PRECISION_POLICY
VENUE_CONTRACT_SPECIFICATION
PROJECT_EXECUTION_PARAMETER
```

The exact classification and value must be frozen before detector/backtest outcome access.

`displayPrecision` and `pipLocation` may be retained as provider metadata, but ADR-006 remains binding: neither field is silently relabeled as a historical executable tick size.

## Session and gap semantics become dataset identity

A provider-neutral D1/H1 series must not imply 24/7 continuity.

The dataset manifest must record the version of the session/gap policy used during normalization.

Required gap categories:

```text
MARKET_CLOSED
SESSION_BREAK
HOLIDAY_OR_EARLY_CLOSE
PROVIDER_MISSING
UNKNOWN_GAP
```

Only evidence-backed expected-closure categories may be approved for canonical chronology.

`PROVIDER_MISSING` and `UNKNOWN_GAP` fail closed unless a separately versioned data-quality decision explicitly resolves them.

No category authorizes synthetic prices.

## Canonical D1 remains strategy-owned

The strategy's D1 calendar remains:

```text
[00:00 America/New_York, next 00:00 America/New_York)
```

The provider-neutral normalizer builds this candle from actual observations after applying the versioned session/gap policy.

OANDA's default 17:00 New-York daily alignment is provider behavior, not permission to redefine strategy D1.

## Detector compatibility boundary

The current detector's alpha-facing transformation is price-only:

```text
canonical D1/H1 OHLC
        ↓
ClosedCandle / CandleWindow
        ↓
frozen v0.1 strategy evaluation
```

Phase 6B should therefore add an explicit adapter from the new provider-neutral trusted dataset into the frozen detector input contract.

The adapter may map only semantically equivalent fields.

It must not:

- invent activity values;
- alter OHLC;
- alter timestamps;
- change strategy parameters;
- select a price quantum from performance;
- conceal session/data gaps.

Compatibility must be fixture-tested before any historical outcome access.

## Manifest requirements

Minimum `P6B_CANONICAL_PRICE_DATASET_V2` identity includes:

```text
schema version
dataset version
provider
venue
instrument
asset class
price component
instrument metadata version/digest
price quantum + source classification
internal timezone UTC
analytical timezone America/New_York
normalizer version
session/gap policy version
market-data code digest
dependency lock digest
coverage start/end
source observation rows
H1 rows
D1 rows
normalized price-data digest
raw/provider retrieval manifests
provider re-fetch evidence
quality status
correction policy
```

Activity metadata may be included separately with explicit semantics but is not part of alpha validity unless a future strategy version deliberately consumes it.

## Provenance rule

Canonical price identity must be reproducible from source observations and code/config versions.

For OANDA API data this includes:

- secret-free request fingerprint;
- raw response SHA-256;
- retrieval timestamp;
- complete-candle checks;
- instrument metadata response SHA-256;
- independent re-fetch comparison evidence;
- normalization code SHA-256;
- session/gap policy version;
- normalized output SHA-256.

A provider correction creates a new data version; it does not overwrite historical evidence.

## Why not modify the existing `CanonicalBar`

The existing schema is already part of the frozen v0.1 evidence chain and its manifests/digests.

Changing field meaning or optionality in place would make historical code/data semantics harder to audit and could falsely imply that the original Phase-3 contract was provider-neutral when it was not.

Phase 6B therefore uses additive versioning:

```text
legacy Binance v0.1 data contracts -> preserved
new provider-neutral v2 contracts  -> additive
```

## Validation boundary

This ADR authorizes implementation of provider-neutral data contracts and compatibility tests only.

It does not authorize:

```text
strategy outcome access
instrument selection from P&L
v0.1 mutation
v0.1 OOS/CONFIRM access
paper trading
shadow trading
live trading
```

## Implementation exit criteria

Provider-neutral canonical price data is ready for the OANDA data gate only when:

1. v2 price/activity models are implemented and unit-tested;
2. OANDA observations can normalize without fabricated volume/trade semantics;
3. session/gap policy is explicit and versioned;
4. NY-midnight D1 aggregation is proven across DST and expected closures;
5. price component is frozen before outcomes;
6. price quantum contract is resolved before detector evaluation;
7. v2 dataset serialization/digests are deterministic;
8. a detector compatibility adapter is fixture-tested;
9. v0.1 legacy data tests remain unchanged and green;
10. independent provider/data gate review passes.
