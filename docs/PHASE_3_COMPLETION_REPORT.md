# Phase 3 Completion Report — Trusted Market Data

**Project:** `romeo-crt-engine`  
**Date:** 2026-08-12  
**Phase:** 3 — Trusted market-data engine  
**Status:** **COMPLETE**  
**Frozen strategy:** `CRT-C3-D1-H1-M1-BEAR-v0.1` — unchanged  
**Phase-4 dataset:** `ee1300f0da50e4debcbbc3b7`  
**Paper / shadow / live trading:** **NOT AUTHORIZED**

## Completion decision

Phase 3 is complete for the first approved market-data route.

The project can now reproduce a historical BTCUSDT Spot window from provider-published raw archives through deterministic validation, normalization, H1 aggregation, New-York D1 aggregation, immutable storage and versioned provenance without using strategy outcomes to repair data.

This phase establishes a trusted **data-engine route**, not a profitability dataset and not evidence that the frozen CRT strategy has an edge.

## First approved route

```text
Provider      Binance Public Data
Venue         Binance Spot
Instrument    BTCUSDT
Raw interval  1 minute
Raw archive   DAILY files only
Internal time UTC
Analysis time America/New_York
Output        H1 + D1
```

Monthly archive bundles are not eligible for trusted promotion in this route. Provider checksum verification is mandatory but not sufficient: every daily archive also requires exact REST-kline cross-check evidence before a `TRUSTED` manifest can be created.

## Exit criteria

| Exit criterion | Result |
|---|---|
| Concrete provider/instrument/venue selected | PASS |
| Provider capabilities and limitations documented | PASS |
| Provider-neutral contracts retained | PASS |
| Immutable raw bytes retained with SHA-256 | PASS |
| Concrete local `ArtifactStore` implemented | PASS |
| Millisecond and microsecond provider timestamp eras supported | PASS |
| UTC normalized M1 chronology | PASS |
| Duplicate/out-of-order/gap/future rejection | PASS |
| Impossible OHLC rejection | PASS |
| Exact H1 aggregation | PASS |
| New-York local-midnight D1 aggregation | PASS |
| Spring DST 23-hour D1 regression | PASS |
| Fall DST 25-hour D1 regression | PASS |
| Partial-edge/incomplete-interior policy deterministic | PASS |
| Provider cross-check evidence required per raw artifact | PASS |
| Dataset manifest deterministic and integrity hashed | PASS |
| Acquisition receipt separated from canonical dataset identity | PASS |
| Dependency environment resolved and locked | PASS |
| Dataset writer immutable/idempotent | PASS |
| `DatasetRef` derivable from receipt | PASS |
| Deterministic CI green | PASS |
| Real provider-backed historical window reproduced | PASS |
| Frozen dataset record committed | PASS |
| Independent Phase-3 review | PASS — `docs/reviews/PHASE_3_GATE_REVIEW.md` |
| Strategy semantics changed | **NO — prohibited** |
| Profitability established | **NO — not a Phase-3 criterion** |

## Frozen provider-backed dataset

Canonical manifest record:

```text
data/manifests/PHASE3_BTCUSDT_EE1300F0DA50E4DEBCBBC3B7.json
```

Evidence record:

```text
data/manifests/PHASE3_BTCUSDT_EE1300F0DA50E4DEBCBBC3B7_EVIDENCE.json
```

### Identity

```text
dataset_version             ee1300f0da50e4debcbbc3b7
manifest_sha256              eaf828ee3acc8adf9e3b931cc6a55d385b0be61b58ae72f01205b3f6034a2141
normalized_sha256            86f6f69176e68655032f3d12910572214de2fa04266c5615146ae03e9f414fc2
market_data_code_sha256      8fbcbb435ce47a405f3500a66935f633136669750cfbe2e014ce1649d4b6140d
dependency_lock_sha256       13653ec2f358aa078fb3a4189299cc8e1f4b71e930cdc3141a8e044de14effa5
normalizer_version            NY_D1_H1_FROM_UTC_M1_V1
```

The committed canonical manifest is the byte-for-byte compact JSON payload produced by the provider smoke; its SHA-256 equals the recorded `manifest_sha256` above.

### Raw source artifacts

```text
2025-09-17
SHA-256  2f3e9a9d40275fa21c30d476f73dc73954e0fabc09b4726fd77fc8af0fb8be39
size     69,980 bytes

2025-09-18
SHA-256  c1edd3740bc8f861a817b3f7ee9205b1918e10f9cfd2225e759006bc94009489
size     69,502 bytes
```

Each raw artifact passed its provider-published checksum and exact first/middle/last REST-kline comparisons.

Provider verification evidence digests:

```text
17d286a7a50bcbeea7c97f0fd84f2ca27881cd31666781da5544bae7cbbdae17
ffae8a5ad70d505d3abbcdba411d955053c4475afc2899be6a11d2e4a1464f95
```

### Reproduced window

```text
raw M1 rows   2,880
canonical H1  48
canonical D1  1 complete New-York Daily candle
UTC coverage  2025-09-17T00:00:00Z -> 2025-09-19T00:00:00Z
```

The UTC coverage is larger than the single emitted New-York D1 because partial local edge days are deliberately omitted rather than emitted as incomplete D1 candles.

## Real-provider verification

The final provider smoke that established this freeze:

```text
workflow       Provider Smoke
workflow run   31642788087
job            94269168670
conclusion     success
Git revision   07b596ab7f5b55b238e67c9f2df13a7ad8afa6b6
receipt SHA    067845dd85e7b058a437ca5de0d7e95c1c71710fe3f5566d6fa4a43b7a964cef
```

The smoke fetched the real public daily archives, verified provider SHA-256 records, compared selected bars to the public REST API, built canonical H1/D1 and emitted the recorded manifest.

The final deterministic CI associated with this data-engine state also passed locked installation, Ruff, strict MyPy and the full test suite.

## Dataset identity versus acquisition identity

A key Phase-3 design decision is that canonical dataset identity and retrieval identity are separate.

`dataset_version` includes:

- provider/venue/symbol;
- instrument metadata snapshot identity;
- analytical timezone and normalizer version;
- market-data implementation SHA-256;
- dependency-lock SHA-256;
- normalized content SHA-256;
- ordered raw source SHA-256 values;
- provider verification evidence digests.

It does **not** include an arbitrary documentation-only Git change or the wall-clock time at which the same source was downloaded.

The separate ingestion receipt retains:

- retrieval timestamp;
- full Git revision;
- manifest SHA-256;
- raw source hashes;
- verification evidence hashes.

This allows true dataset reproducibility without losing acquisition auditability.

## Data-quality policy

The route fails closed on:

- checksum mismatch;
- unsupported provider schema/timestamp magnitude;
- wrong archive date coverage;
- archive count other than 1,440 M1 rows for a crypto UTC day;
- duplicate timestamps;
- out-of-order timestamps;
- any M1 gap;
- future observations relative to the ingestion `as_of`;
- illegal/non-finite OHLC;
- identity mismatch;
- incomplete H1;
- incomplete interior New-York D1;
- missing or mismatched provider cross-check evidence.

The trusted layer never forward-fills or fabricates a missing price.

## Explicit limitations carried forward

1. This first route is **BTCUSDT Spot only**. It is not evidence for Forex, index futures or metals.
2. The chosen archive route has no bid/ask or spread history. Later execution-cost validation requires additional data/assumptions.
3. `exchangeInfo` metadata is labeled `SNAPSHOT_AT_INGESTION`; it is not a historical exchange-filter database.
4. The frozen Phase-4 dataset is intentionally a compact reproduction window, not the eventual full historical validation sample.
5. Provider corrections can legitimately create a new dataset version later; old raw bytes/manifest records must remain preserved.
6. Provider-native H1/D1 bars are not trusted as substitutes for the canonical M1-derived calendar.
7. External provider smoke testing is an operational verification tool, not a replacement for deterministic unit/integration tests.

## Phase-4 handoff

Phase 4 may now integrate the frozen CRT detector against:

```text
strategy   CRT-C3-D1-H1-M1-BEAR-v0.1
dataset    ee1300f0da50e4debcbbc3b7
```

Phase 4 must not reinterpret strategy rules or data boundaries based on whether the example produces a trade.

The immediate Phase-4 objective is deterministic detector reproduction and explanation over canonical bars, followed by source-derived/negative fixtures. Historical profitability simulation remains a later phase.
