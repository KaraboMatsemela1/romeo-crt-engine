# Phase 3 Gate Review — Trusted Market Data

**Date:** 2026-08-12  
**Review role:** independent data/reliability review  
**Strategy:** `CRT-C3-D1-H1-M1-BEAR-v0.1`  
**Candidate dataset:** `ee1300f0da50e4debcbbc3b7`  
**Decision:** **PASS — eligible for Phase-4 detector work**

## Review mandate

Challenge the Phase-3 implementation for data leakage, provider coupling, silent correction, irreproducibility, timezone/DST errors and strategy contamination before allowing the dataset into Phase 4.

## Findings

### 1. Strategy/data boundary

**PASS.**

The market-data package contains no CRT outcome logic and does not select dates/bars based on strategy performance. The provider route constructs M1/H1/D1 observations independently of whether the frozen strategy later emits a signal.

No strategy parameter was changed in Phase 3.

### 2. Provider-neutral boundary

**PASS.**

Binance parsing/fetching lives under `market_data/providers`. Canonical bar, verification-evidence, manifest and storage contracts remain provider-neutral.

A provider-specific type is not imported into the canonical dataset layer.

### 3. Raw immutability and corrections

**PASS.**

Raw provider zip bytes are keyed by source date and SHA-256 through the `ArtifactStore` boundary. Reusing a key with different bytes fails.

Provider correction policy is version-on-change, not in-place mutation.

### 4. Trust proof

**PASS.**

Checksum validity alone cannot produce a trusted dataset. The pipeline requires one provider-verification evidence record for each raw SHA-256, and the evidence identity must match provider/venue/symbol metadata.

The approved Binance adapter exact-matches first/middle/last archive rows against the public REST kline endpoint.

### 5. Chronology and DST

**PASS.**

Internal chronology is UTC and elapsed-time based. H1 requires exact 3,600-second buckets assembled from 60 gapless M1 observations.

D1 is New-York local midnight to next local midnight. Tests demonstrate 23-hour spring DST and 25-hour fall DST days.

No provider-native D1 boundary is silently substituted.

### 6. Missing observations

**PASS / deliberately strict.**

For the first 24/7 crypto route, any missing M1 is rejected. The engine does not forward-fill or synthesize a maintenance/halt candle.

This policy will need a venue-aware closure calendar for future non-24/7 instruments; that is not a defect in the BTCUSDT route.

### 7. Dataset identity

**PASS.**

Canonical dataset identity contains source/content/configuration that affects data semantics:

- raw SHA-256 values;
- provider verification evidence;
- normalized content digest;
- metadata snapshot identity;
- normalizer version;
- market-data code fingerprint;
- dependency-lock fingerprint.

Retrieval timestamp and full Git revision are separated into an ingestion receipt so non-semantic repository changes do not manufacture new market datasets.

### 8. Reproduction and storage

**PASS.**

Identical canonical inputs produce the same dataset version/manifest. The writer is idempotent for identical bytes and refuses conflicting mutation.

The ingestion receipt can produce a `DatasetRef` for downstream experiment provenance.

### 9. Dependency reproducibility

**PASS for Phase 3.**

CI and provider smoke install from the exact `requirements.lock`, and project installation disables dependency resolution. Build backend is pinned.

Future dependency updates must be deliberate and will change the lock digest recorded by a new dataset build.

### 10. Real-provider evidence

**PASS.**

The final provider smoke succeeded on the real public Binance route and generated:

```text
dataset_version  ee1300f0da50e4debcbbc3b7
manifest SHA     eaf828ee3acc8adf9e3b931cc6a55d385b0be61b58ae72f01205b3f6034a2141
M1               2,880
H1               48
D1               1 complete New-York day
```

The two provider archive hashes and six sampled REST observations are frozen in the committed manifest/evidence records.

## Non-blocking limitations

These are explicitly accepted rather than hidden:

- BTCUSDT Spot only;
- no bid/ask/spread history in this route;
- current exchange-filter metadata is an ingestion snapshot, not point-in-time history;
- compact Phase-4 reproduction window only, not a full OOS sample;
- non-24/7 venues will require a different closure/session quality policy;
- real-provider smoke depends on external provider availability and should not be a permanent automatic merge gate.

## Rejected shortcuts

The review confirms the implementation does not:

- use monthly Binance archive bundles for trusted promotion;
- accept checksum-only trust;
- forward-fill missing observations;
- accept provider-native Daily bars as canonical by convenience;
- change the CRT strategy because of provider data layout;
- embed ingestion wall-clock time into canonical dataset identity;
- infer historical tick-size rules from a current metadata snapshot;
- claim the compact reproduction dataset proves profitability.

## Decision

```text
Phase 3 data-engine gate         PASS
Dataset ee1300...                TRUSTED REPRODUCTION DATASET
Eligible next phase             Phase 4 detector implementation
Backtest profitability claims   NOT AUTHORIZED
Paper trading                   NOT AUTHORIZED
Shadow/live                     NOT AUTHORIZED
```

Any future modification to raw parsing, chronology, H1/D1 construction, manifest identity or correction policy must create/review a new market-data code fingerprint and rebuild affected dataset versions.
