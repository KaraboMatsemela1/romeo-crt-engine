# P6 DEV Data Freeze 001

Status: **SEALED BEFORE DEV DETECTOR / P&L ACCESS**  
Protocol: `P6-VALIDATION-PROTOCOL-v1`  
Window: `P6-DEV-001` (`2019-01-01` through `2022-12-31`)  
Source workflow: run `31681313574`, job `94387156400`

## Decision

The DEV trusted-data gate is complete. The detector and backtester steps in the source workflow were skipped because:

```text
P6_DEV_OUTCOME_ACCESS_AUTHORIZED = false
```

Therefore the facts below were sealed before any new Phase-6 DEV candidate count, TradePlan count, trade result, P&L, expectancy, drawdown, or cost-scenario result was observed.

## Frozen trusted-data identity

```text
dataset_version                 3e8a39fec1062ef902e8a1ad
manifest_sha256                 761b561885f94cdb440be02d3a84169549d7bafd8e820bb9654c77ed8aed9e97
normalized_sha256               46682c2d793dbdd0a0939862f444d19b4817559c8989a7fde031598d52cb29f5
market_data_code_sha256         2c2e6ff7505e2a427b4a2209ddf59c05caa0f48380e33bbce8f9f76489009829
dependency_lock_sha256          13653ec2f358aa078fb3a4189299cc8e1f4b71e930cdc3141a8e044de14effa5
instrument_metadata_version     6dde8c5617697745
instrument_metadata_observed_at 2026-08-13T08:16:25.815237+00:00
```

The metadata observation timestamp is now a frozen reconstruction input for `P6-DEV-001`. Acquisition/retrieval timestamps may differ on later reproductions, but the canonical manifest must remain byte-identical before outcome access.

## Frozen shape

```text
requested raw UTC daily archives  1,461
excluded whole UTC archives          20
accepted normalized M1         2,074,680
accepted canonical H1             34,578
complete New-York D1               1,418
```

Provider verification:

```text
REST_KLINE_EXACT_MATCH_V1       48
PROVIDER_SHA256_CHECKSUM_V1   1,413
```

The 48 REST records are one strict-parser-eligible archive per UTC calendar month across the four-year DEV window. Every raw archive has exactly one verification record.

## Data-quality amendments

The canonical DEV dataset applies:

- `P6-DATA-QUALITY-AMENDMENT-001` — independently evidenced Binance venue closure on `2019-03-12 02:00–08:00 UTC`; only that exact interval is treated as an exchange closure.
- `P6-DATA-QUALITY-AMENDMENT-002` — 20 checksum-authenticated but incomplete/malformed UTC daily archives are excluded whole from normalization without claiming an operational cause.

Archive exclusion ledger:

```text
schema                 P6_ARCHIVE_EXCLUSIONS_V1
policy                 P6-DATA-QUALITY-AMENDMENT-002
excluded_archive_count 20
ledger_sha256           fe6ef14eedd4340c0fa6157fb1b44e17684a1bbdfcef7e9c82b3276755fcb5aa
```

The exact dates, source hashes and parser failure classes are frozen in `P6_DEV_DATA_FREEZE_001.json`.

No missing observation was interpolated, forward-filled, back-filled or synthesized. H1 is built only from actual 60-minute groups, and any New-York parent intersecting an excluded interval is omitted. The frozen strategy's consecutive-D1 requirement prevents detector sequences from bridging those gaps.

## Reproduction gate before outcome access

Before setting `P6_DEV_OUTCOME_ACCESS_AUTHORIZED=true`, a fresh provider retrieval must reproduce all of the following exactly:

```text
dataset_version          3e8a39fec1062ef902e8a1ad
manifest_sha256          761b561885f94cdb440be02d3a84169549d7bafd8e820bb9654c77ed8aed9e97
normalized_sha256        46682c2d793dbdd0a0939862f444d19b4817559c8989a7fde031598d52cb29f5
exclusion_ledger_sha256  fe6ef14eedd4340c0fa6157fb1b44e17684a1bbdfcef7e9c82b3276755fcb5aa
M1/H1/D1                 2074680 / 34578 / 1418
excluded archives        20
REST/checksum evidence   48 / 1413
metadata version         6dde8c5617697745
metadata observed_at     2026-08-13T08:16:25.815237+00:00
```

A mismatch stops DEV outcome access. It is investigated as new data/provider evidence, not patched around after seeing trading results.

## Safety

```text
PAPER_TRADING_AUTHORIZED = false
LIVE_TRADING_AUTHORIZED  = false
```

This is a data-integrity freeze only. It contains no strategy-performance evidence.
