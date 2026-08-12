# ADR-005 — Binance BTCUSDT as the First Trusted Market-Data Route

**Status:** Accepted  
**Date:** 2026-08-12  
**Applies to:** Phase 3 initial dataset route only  
**Strategy impact:** none

## Context

The frozen candidate `CRT-C3-D1-H1-M1-BEAR-v0.1` requires deterministic H1 and New-York Daily observations. Phase 3 needs one concrete provider/instrument route before generic provider abstractions can be proven against real provider semantics.

The first route should minimize authentication and venue-closure ambiguity while preserving the project's hard requirements for raw provenance, timestamp correctness, provider correction handling and deterministic resampling.

## Decision

Use:

```text
Provider/archive   Binance Public Data
Venue              Binance Spot
Instrument         BTCUSDT
Asset class        crypto spot
Raw interval       1 minute
Archive unit       DAILY files only
Internal time      UTC
Analytical time    America/New_York
Canonical output   H1 + D1
```

Official public sources:

- `https://github.com/binance/binance-public-data`
- `https://github.com/binance/binance-spot-api-docs`
- `https://data.binance.vision`
- `https://data-api.binance.vision`

Binance documents public market-data-only REST endpoints that do not require an API key. Its public-data repository publishes daily archive files and associated SHA-256 checksum files.

## Why daily archives only

A public Binance-data issue opened in 2026 documents historical cases where some monthly Spot kline archives disagree with daily archives and current API/UI kline responses. The reported daily values matched the API in the examined conflicts.

Therefore this project does not treat a monthly archive checksum as sufficient evidence that the file represents the provider's current canonical history.

Phase-3 trust policy:

```text
monthly archive -> NOT ELIGIBLE FOR TRUSTED DATASET

daily archive
  -> published checksum verification
  -> exact UTC-day / 1,440-minute validation
  -> selected REST API row cross-check
  -> provider-neutral normalization
  -> TRUSTED candidate
```

A provider correction produces a new raw artifact hash and therefore a new dataset version. Old raw bytes are never silently replaced.

## Why BTCUSDT first

BTCUSDT Spot provides a continuously traded 24/7 market. That removes weekend/holiday closure ambiguity from the first data-engine implementation while still forcing us to solve the harder analytical-time problem correctly:

- internal UTC chronology;
- New-York local Daily boundaries;
- spring DST 23-hour Daily candles;
- fall DST 25-hour Daily candles;
- repeated local wall-clock hours.

BTCUSDT is a first engineering/validation route. Results must not be generalized to Forex, index futures, metals or any other instrument.

## Provider-native bars

Provider-native H1 or D1 bars are not used as the canonical source of truth for v0.1.

The trusted route is:

```text
provider daily M1 archive
   -> normalized UTC M1
   -> exact elapsed-hour H1
   -> New-York local-midnight D1
```

This preserves the project's strategy calendar rather than adapting the strategy to provider convenience.

## Instrument metadata

`exchangeInfo` is captured at ingestion and records at minimum:

- price tick size;
- quantity step;
- observation timestamp;
- metadata version.

The metadata contract explicitly labels this as `SNAPSHOT_AT_INGESTION`. It is not represented as proof that the same exchange filter existed historically.

Point-in-time exchange-filter history remains a later validation/execution concern if a one-tick historical assumption becomes material.

## Reproducibility

Every trusted dataset manifest contains:

- provider / venue / symbol;
- instrument metadata version and observation timestamp;
- raw archive URLs and SHA-256 digests;
- normalizer version;
- git/code version;
- dependency-lock SHA-256;
- H1/D1 normalized content SHA-256;
- row counts and coverage;
- immutable dataset version;
- correction policy.

## Consequences

### Positive

- no API credential is needed for initial public data;
- raw source files and checksums are independently retainable;
- one-minute data lets the project own all analytical boundaries;
- 24/7 coverage makes missing-minute detection unambiguous;
- DST behavior can be tested without venue closure exceptions.

### Negative

- crypto evidence is not Forex/index evidence;
- current `exchangeInfo` is not a historical exchange-filter database;
- REST cross-checks add network dependency during ingestion;
- Binance archive corrections can create new dataset versions later.

## Governance

This ADR changes only Phase-3 market-data engineering. It does not authorize strategy changes, profitability claims, paper trading, shadow trading or live execution.
