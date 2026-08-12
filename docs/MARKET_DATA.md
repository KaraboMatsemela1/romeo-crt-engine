# Trusted Market-Data Contract

## Purpose

Phase 3 produces reproducible market observations for the frozen strategy without changing strategy semantics to match a data vendor.

The first route is defined by ADR-005:

```text
Binance Public Data -> BTCUSDT Spot -> daily 1m archives
```

## Trust states

Raw data is not trusted merely because it downloaded successfully.

A Phase-3 dataset may be labeled `TRUSTED` only after:

1. provider source is on the approved provider policy;
2. raw artifact has a provider-published SHA-256 that matches the retained bytes;
3. archive schema is valid;
4. the daily crypto archive contains exactly 1,440 consecutive UTC minutes;
5. selected rows match the provider's public REST kline endpoint;
6. normalized minute chronology is unique, ordered and gapless;
7. OHLC and numeric invariants pass;
8. H1 aggregation is exactly one elapsed hour;
9. D1 aggregation uses New-York local midnight boundaries;
10. only complete D1 bars are emitted;
11. dependency, code, metadata and source versions are captured;
12. normalized content and manifest digests are computed.

Any failure means the dataset is rejected rather than repaired silently.

## Layers

### Raw

Raw zip bytes are retained content-addressed by SHA-256.

```text
data/raw/<provider>/<venue>/<symbol>/1m/<utc-day>-<sha256>.zip
```

If a provider later changes history, the replacement is a different raw artifact. The original retained artifact is not overwritten.

### Normalized

The current on-disk canonical format is deterministic JSON Lines to avoid introducing a columnar dependency before it is needed.

```text
data/normalized/<dataset-version>/H1.jsonl
data/normalized/<dataset-version>/D1.jsonl
data/normalized/<dataset-version>/manifest.json
```

A later Parquet representation may be added as a new storage representation, but it may not alter bar semantics or silently change an existing dataset version.

## Timestamp rules

### Internal chronology

All canonical bar endpoints are timezone-aware UTC timestamps.

Comparison and duration logic uses elapsed/absolute time, not naive wall-clock subtraction.

### H1

H1 is aggregated from exactly 60 gapless M1 observations and spans exactly 3,600 elapsed seconds.

This remains correct across New-York DST because UTC chronology is authoritative.

### D1

D1 is:

```text
[00:00 America/New_York, next 00:00 America/New_York)
```

A valid D1 therefore contains:

```text
23 H1 bars on spring DST transition
24 H1 bars normally
25 H1 bars on fall DST transition
```

A partial first or last local day caused solely by requested archive coverage is omitted. An incomplete interior local day is a data-quality failure.

## Binance timestamp units

The Binance public-data repository documents that Spot archive timestamps from 2025 onward are in microseconds. Older archive rows use milliseconds.

The adapter detects and normalizes the two supported archive timestamp magnitudes explicitly. Unknown magnitudes fail closed.

## Instrument metadata

The provider adapter captures current Spot `exchangeInfo` values including:

- `PRICE_FILTER.tickSize`;
- `LOT_SIZE.stepSize`.

Metadata is labeled `SNAPSHOT_AT_INGESTION`. It is not assumed to be a point-in-time reconstruction of historical exchange rules.

## Dataset identity

`dataset_version` is content/configuration derived from:

- manifest schema version;
- provider, venue and symbol;
- instrument metadata version;
- analytical timezone;
- normalizer version;
- git/code version;
- dependency-lock digest;
- normalized H1/D1 digest;
- ordered raw artifact digests.

Ingestion timestamp is recorded in the manifest but does not by itself change `dataset_version`.

## Corrections

Never edit a trusted dataset in place.

```text
provider correction
   -> different raw SHA-256
   -> rebuild
   -> different dataset version
   -> preserve previous version
```

## Dependency lock

`requirements.lock` is the resolved Python 3.12 validation/ingestion environment for the current phase. CI installs this file first and installs the project with dependency resolution disabled.

The SHA-256 of the exact lockfile used is stored in every trusted dataset manifest.

## Reproduction command

Example:

```bash
python scripts/ingest_binance_spot.py \
  --symbol BTCUSDT \
  --start-utc-day 2025-09-17 \
  --end-utc-day 2025-09-18
```

Two UTC archive days are normally needed to produce at least one complete New-York Daily candle because New-York midnight does not generally coincide with UTC midnight.

The command requires checksum verification and REST cross-checking before it writes a `TRUSTED` dataset.

## What Phase 3 does not do

Phase 3 does not:

- choose profitable dates;
- change the frozen CRT rules;
- detect CRT setups;
- backtest trades;
- infer missing candles;
- forward-fill prices;
- silently repair provider history;
- authorize paper or live execution.
