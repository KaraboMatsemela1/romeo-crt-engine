# Trusted Market-Data Contract

## Purpose

Phase 3 produces reproducible market observations for the frozen strategy without changing strategy semantics to match a data vendor.

The first route is defined by ADR-005:

```text
Binance Public Data -> BTCUSDT Spot -> daily 1m archives
```

## Provider capability matrix

| Capability | First Phase-3 route |
|---|---|
| Provider | Binance Public Data |
| Venue | Binance Spot |
| Instrument | BTCUSDT |
| Asset class | Crypto spot |
| Authentication | Not required for approved public market-data endpoints |
| Raw historical granularity | 1-minute daily kline archives |
| Provider SHA-256 | Available and mandatory |
| REST historical comparison | Available; first/middle/last M1 samples per archive are exact-matched |
| OHLC | Available |
| Base volume | Available |
| Quote volume | Available |
| Trade count | Available |
| Bid/ask | Not available in this archive route |
| Spread | Not available in this archive route |
| Venue closures | Market is expected to operate 24/7; missing minutes are rejected, never fabricated |
| Historical exchange-filter metadata | Not provided by this route; `exchangeInfo` is a snapshot at ingestion |
| Monthly archives | Explicitly not eligible for trusted promotion in v1 |

The absence of bid/ask/spread means this route is sufficient for trusted bar construction and Phase-4 detector reproduction, but not sufficient by itself for later realistic execution-cost validation.

## Trust states

Raw data is not trusted merely because it downloaded successfully.

A Phase-3 dataset may be labeled `TRUSTED` only after:

1. provider source is on the approved provider policy;
2. raw artifact has a provider-published SHA-256 that matches the retained bytes;
3. archive schema is valid;
4. the daily crypto archive contains exactly 1,440 consecutive UTC minutes;
5. selected rows match the provider's public REST kline endpoint;
6. provider-verification evidence exists for every raw artifact;
7. normalized minute chronology is unique, ordered and gapless;
8. OHLC and numeric invariants pass;
9. H1 aggregation is exactly one elapsed hour;
10. D1 aggregation uses New-York local-midnight boundaries;
11. only complete D1 bars are emitted;
12. dependency, market-data-code, metadata and source versions are captured;
13. normalized content and manifest digests are computed.

Any failure means the dataset is rejected rather than repaired silently.

## Layers

### Raw

Raw zip bytes are retained through the provider-neutral `ArtifactStore` boundary. The first implementation is `LocalArtifactStore`.

```text
data/raw/<provider>/<venue>/<symbol>/1m/<utc-day>-<sha256>.zip
```

Paths are immutable: rewriting the same key with different bytes fails. Reads verify SHA-256 and size.

If a provider later changes history, the replacement is a different raw artifact. The original retained artifact is not overwritten.

Provider-native timestamps remain in the immutable raw zip. The normalized layer converts them explicitly to UTC.

### Normalized

The current canonical on-disk format is deterministic JSON Lines so Phase 3 does not need a columnar dependency merely to establish trust semantics.

```text
data/normalized/<dataset-version>/H1.jsonl
data/normalized/<dataset-version>/D1.jsonl
data/normalized/<dataset-version>/manifest.json
```

A later Parquet representation may be added as another storage representation, but it may not alter bar semantics or silently mutate an existing dataset version.

### Ingestion receipt

Acquisition-time provenance is deliberately separate from canonical dataset identity:

```text
data/receipts/<dataset-version>/<receipt-sha256>.json
```

The receipt records:

- dataset ID/version;
- canonical manifest SHA-256;
- retrieval timestamp;
- full Git revision used by the ingestion run;
- raw artifact hashes;
- provider cross-check evidence digests.

The receipt can produce a Phase-0 `DatasetRef`. Multiple retrievals of the same canonical dataset may therefore have different receipts without pretending the market dataset itself changed.

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

A partial first or last local day caused solely by the requested archive window is omitted. An incomplete interior local day is a data-quality failure.

Provider-native H1/D1 bars are not treated as equivalent by default. The canonical route is built from trusted M1 observations.

## Binance timestamp units

The Binance public-data repository documents that Spot archive timestamps from 2025 onward are in microseconds. Older archive rows use milliseconds.

The adapter detects and normalizes the two supported timestamp magnitudes explicitly. Unknown magnitudes fail closed.

## Instrument metadata

The provider adapter captures current Spot `exchangeInfo` values including:

- `PRICE_FILTER.tickSize`;
- `LOT_SIZE.stepSize`.

Metadata is labeled `SNAPSHOT_AT_INGESTION`. It is not assumed to reconstruct historical exchange filters. If point-in-time tick/lot rules become material to later execution validation, a separate historical metadata source or explicit approximation policy will be required.

## Dataset identity

`dataset_version` is content/configuration derived from:

- manifest schema version;
- provider, venue and symbol;
- instrument metadata version and observation timestamp;
- analytical timezone;
- normalizer version;
- SHA-256 fingerprint of the market-data implementation files;
- dependency-lock SHA-256;
- normalized H1/D1 SHA-256;
- ordered raw artifact SHA-256 values;
- provider-verification evidence digests.

It is intentionally **not** derived from the full repository Git revision or retrieval timestamp. A README-only commit does not create a fake new market dataset. Full Git revision and retrieval time belong to the ingestion receipt.

## Corrections

Never edit a trusted dataset in place.

```text
provider correction
   -> different raw SHA-256
   -> rebuild
   -> different dataset version
   -> preserve previous version and receipts
```

No forward-fill, interpolation or silent provider-history repair is allowed in the trusted layer.

## Dependency lock

`requirements.lock` is the resolved Python 3.12 validation/ingestion environment for the current phase. CI installs this lock first and installs the project with dependency resolution disabled.

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

The command requires provider checksum verification and REST cross-checking before it writes a `TRUSTED` dataset.

## Provider corrections and maintenance gaps

BTCUSDT is treated as a 24/7 route for this phase. Therefore a missing M1 observation is a quality failure, including a provider/venue maintenance gap; the engine does not synthesize a price for the missing minute.

A valid provider checksum is necessary but not sufficient. The project deliberately cross-checks selected daily-archive rows against the public REST kline API because a provider may republish corrected history.

## What Phase 3 does not do

Phase 3 does not:

- choose profitable dates;
- change the frozen CRT rules;
- detect CRT setups;
- backtest trades;
- infer missing candles;
- forward-fill prices;
- silently repair provider history;
- claim provider-native H1/D1 equivalence;
- supply bid/ask or spread that the chosen route does not contain;
- reconstruct historical exchange filters from a current snapshot;
- authorize paper, shadow or live execution.
