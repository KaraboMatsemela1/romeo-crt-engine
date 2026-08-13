# Phase 6B OANDA Historical Collection Shard Execution v1

**Execution ID:** `P6B-OANDA-HISTORY-SHARD-EXECUTION-V1`  
**Date frozen:** 2026-08-13  
**Parent protocol:** `P6B-OANDA-HISTORY-QUALIFICATION-V1`  
**Detector / TradePlan / P&L access:** PROHIBITED

## Purpose

Freeze the operational sharding of the already-defined raw historical collection before the complete 2019-2022 provider pull is opened.

This is an execution detail only. It does not change the strategy, observation contract, trusted-data gate, missing-interval policy, or frozen four-symbol universe.

## Frozen shards

Each frozen instrument is collected in four non-overlapping UTC calendar-year shards:

```text
2019  2019-01-01T00:00:00Z .. 2020-01-01T00:00:00Z exclusive
2020  2020-01-01T00:00:00Z .. 2021-01-01T00:00:00Z exclusive
2021  2021-01-01T00:00:00Z .. 2022-01-01T00:00:00Z exclusive
2022  2022-01-01T00:00:00Z .. 2023-01-01T00:00:00Z exclusive
```

Frozen instruments:

```text
EUR_USD
XAU_USD
NAS100_USD
SPX500_USD
```

Total execution units: `4 instruments x 4 years = 16 shards`.

## Per-shard invariants

```text
provider          OANDA_V20
account           practice / runtime-only / redacted
price             MID / M
granularity       M1
smooth            false
page width        4500 minutes
synthetic prices  prohibited
initial gap class UNRECONCILED
```

Every shard must preserve:

- page request start/end;
- retrieval timestamp;
- secret/account-redacted request SHA-256;
- raw response SHA-256;
- page complete-candle count;
- normalized M1 provider-value SHA-256;
- complete raw missing-interval inventory;
- shard boundaries and identity.

Provider-confirmed empty pages remain valid provenance pages and never become synthetic candles.

## Frozen independent re-fetch mapping

The four parent-protocol re-fetch windows map one-to-one to the yearly shards:

```text
2019 -> 2019-03-12T14:00:00Z .. 15:00:00Z
2020 -> 2020-09-15T14:00:00Z .. 15:00:00Z
2021 -> 2021-04-13T14:00:00Z .. 15:00:00Z
2022 -> 2022-10-18T14:00:00Z .. 15:00:00Z
```

Each shard must independently re-request its mapped window after the primary shard retrieval and require exact provider-value equality.

After all four shards for an instrument exist, the parent gate is satisfied only if all four yearly re-fetch checks are exact matches.

## Consolidation rule

Yearly sharding does not create four detector datasets. Before detector access, the four shards must be consolidated in chronological order into one instrument-level 2019-2022 provider-value stream.

Consolidation must verify:

1. exact non-overlapping year boundaries;
2. no duplicate timestamp with conflicting values;
3. one deterministic combined normalized M1 digest;
4. union of all raw missing intervals;
5. 4/4 independent re-fetch matches;
6. all missing intervals reconciled under date-valid historical session/holiday evidence;
7. deterministic H1 and New-York-midnight D1 construction;
8. one final `P6B_CANONICAL_PRICE_DATASET_V2` identity per instrument.

No shard, yearly count, reason distribution, detector result, or P&L may be inspected for strategy selection.

## Failure policy

A failed transport/job may be rerun for the exact same frozen shard. The successful retrieval's provenance must be preserved. Shard boundaries, symbol, price component, page width and re-fetch window may not be changed in response to observed data.

If a shard cannot be retrieved or reconciled, the instrument remains `NOT_TRUSTED`. No symbol may be replaced based on this failure.

## Authorization

```text
FULL_RAW_HISTORY_COLLECTION_AUTHORIZED = true
DETECTOR_EXECUTION_AUTHORIZED          = false
TRADEPLAN_COUNT_ACCESS_AUTHORIZED      = false
BACKTESTER_AUTHORIZED                  = false
PNL_OUTCOME_ACCESS_AUTHORIZED          = false
V0_1_OOS_ACCESS_AUTHORIZED             = false
V0_1_CONFIRM_ACCESS_AUTHORIZED         = false
PAPER_TRADING_AUTHORIZED               = false
SHADOW_TRADING_AUTHORIZED              = false
LIVE_TRADING_AUTHORIZED                = false
```
