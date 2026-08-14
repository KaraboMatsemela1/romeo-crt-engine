# ADR-006 — OANDA v20 for Multi-Market Provider Qualification

**Status:** Proposed / Phase-6B qualification  
**Date:** 2026-08-13  
**Applies to:** Phase 6B multi-market research route  
**Alpha strategy impact:** none

## Context

`CRT-C3-D1-H1-M1-BEAR-v0.1` completed its preregistered BTCUSDT DEV gate with only four closed trades and therefore `INSUFFICIENT_EVIDENCE`.

ADR-005 deliberately selected Binance BTCUSDT as the first data-engine route because 24/7 trading reduced venue/session ambiguity. ADR-005 also explicitly prohibits generalizing that route's results to forex, indices, metals or other instruments.

Phase 6B now needs a provider capable of qualifying additional source-relevant markets without changing the frozen strategy predicates.

## Decision

Qualify the OANDA v20 REST API as the first non-Binance multi-market provider candidate.

This ADR does **not** yet mark OANDA data `TRUSTED` and does not authorize any historical strategy outcome access.

## Why OANDA v20

Current official OANDA v20 documentation provides:

- account-specific tradeable-instrument discovery;
- historical candlestick endpoints;
- M1 and H1 granularities;
- bid, ask and midpoint candle components;
- instrument precision/pip/trade-size metadata;
- explicit complete-candle state;
- historical pricing described by OANDA as available back to 2005;
- configurable daily alignment timezone/hour.

Primary documentation:

- `https://developer.oanda.com/rest-live-v20/introduction/`
- `https://developer.oanda.com/rest-live-v20/account-ep/`
- `https://developer.oanda.com/rest-live-v20/pricing-ep/`
- `https://developer.oanda.com/rest-live-v20/instrument-df/`
- `https://developer.oanda.com/rest-live-v20/primitives-df/`

## Critical calendar mismatch

OANDA's documented default for daily-aligned candles is:

```text
dailyAlignment    = 17
alignmentTimezone = America/New_York
```

The frozen CRT strategy calendar is:

```text
D1 = [00:00 America/New_York, next 00:00 America/New_York)
```

Therefore OANDA default D candles are **not strategy-canonical D1 bars**.

The provider must not silently redefine the strategy calendar.

Required canonical path:

```text
OANDA M1/H1 provider observations
        ↓
UTC raw chronology
        ↓
session/closure classification
        ↓
project-controlled New-York-midnight D1 aggregation
```

Provider-native daily candles may only be used as a separately configured cross-check after alignment has been made explicit and verified.

## Account/division dependency

OANDA documents that the instrument list is account/regulatory-division dependent.

Therefore code must:

1. query `/v3/accounts/{accountID}/instruments`;
2. record the returned instrument universe and metadata snapshot;
3. intersect it with the preregistered source-relevant market whitelist;
4. freeze exact API symbols before outcome access.

Hardcoding that every account exposes a specific CFD is prohibited.

## Initial source-relevant market families

Subject to exact account availability:

```text
US NAS 100 / NQ proxy
US SPX 500 / ES proxy
EUR/USD
Gold/USD
```

The existence of NQ/ES, EUR/USD-DXY and Gold-Silver in Romeo's first-party material motivates universe selection but does not activate SMT rules.

SMT remains a separately versioned feature.

## Price component decision

OANDA can return:

```text
M = midpoint
B = bid
A = ask
```

No component is automatically the universal truth for both signal generation and execution simulation.

The Phase-6B route must freeze:

- signal-detection component;
- execution/friction component usage;
- re-fetch/cross-check policy;

before strategy outcomes are calculated.

The initial adapter therefore preserves OANDA candles as provider-specific `OandaPriceCandle` objects instead of coercing them into Binance `MinuteBar` volume semantics.

## Volume/activity semantics

OANDA documents candle `volume` as the **number of prices created during the candle**.

It must not be represented as:

- exchange base volume;
- quote volume;
- actual trade count.

The adapter stores it as `price_count` until the provider-neutral data model explicitly supports heterogeneous activity semantics.

## Instrument tick-size caution

The OANDA instrument schema exposes fields such as `displayPrecision` and `pipLocation`.

Phase 6B must not automatically claim that `10^-displayPrecision` is the exact historical executable tick size used by the strategy's one-tick stop-buffer policy.

The adapter therefore captures provider metadata without populating the existing `InstrumentMetadata.price_tick_size` contract.

Tick/execution quantum is a blocking provider-contract decision before validation.

## Session gaps

The Binance route could initially expect continuous 24/7 minute chronology apart from explicitly evidenced exceptional closures.

OANDA markets require a broader gap taxonomy:

```text
MARKET_CLOSED
SESSION_BREAK
HOLIDAY_OR_EARLY_CLOSE
PROVIDER_MISSING
UNKNOWN_GAP
```

The project must not synthesize prices across any gap.

A gap may be accepted only when its provider/venue/session cause is documented by a versioned calendar/policy. Unknown required gaps fail closed.

## Authentication and secret handling

OANDA personal access tokens are credentials and must be treated as passwords.

Requirements:

- token only from environment/local/managed secret storage;
- never commit token or account ID values;
- never log Authorization headers;
- never include token in provenance hashes;
- practice and live environment URLs explicit;
- provider qualification defaults to practice;
- live trading remains independently disabled.

`.env.example` contains variable names only.

## Provenance model

Unlike Binance public archives, this route does not currently rely on provider-published file SHA-256 records.

Trusted-data qualification must therefore seal the API retrieval itself:

```text
request path + non-secret parameters fingerprint
retrieved_at UTC
raw response SHA-256
instrument metadata response SHA-256
normalized output SHA-256
code SHA-256
dependency-lock SHA-256
row counts / coverage
provider re-fetch comparison evidence
```

A later provider correction creates a new dataset version.

## Validation boundary

This ADR authorizes only provider/data engineering.

It does not authorize:

- mutating v0.1 alpha rules;
- using preliminary strategy P&L to select instruments;
- opening v0.1 OOS or CONFIRM;
- paper trading;
- shadow trading;
- live trading.

## Exit criteria

ADR status may move from `Proposed` to `Accepted for validation data` only after:

1. provider parser tests pass;
2. account-specific instrument discovery is reproduced;
3. M1/H1 chronology is reproduced;
4. session-gap policy is frozen;
5. canonical NY-midnight D1 reconstruction is tested;
6. price-component policy is frozen;
7. tick/execution-quantum policy is resolved;
8. raw-response/re-fetch provenance is implemented;
9. initial instrument universe is frozen before outcome access;
10. independent data-gate review passes.
