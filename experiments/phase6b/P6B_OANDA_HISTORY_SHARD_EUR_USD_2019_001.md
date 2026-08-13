# Phase 6B OANDA Raw Historical Shard — EUR_USD / 2019 / 001

**Date:** 2026-08-13  
**Environment:** OANDA practice  
**Instrument:** `EUR_USD`  
**Year:** `2019`  
**Price:** MID / `M`  
**Granularity:** M1  
**Parent protocol:** `P6B-OANDA-HISTORY-QUALIFICATION-V1`  
**Shard execution:** `P6B-OANDA-HISTORY-SHARD-EXECUTION-V1`  
**Successful retained run:** `31714724701`  
**Successful retained job:** `94496399721`  
**Execution head:** `76e85ede9027fb2e4cddfbbae708c9a59d91369a`

## Decision

```text
P6B_OANDA_EUR_USD_2019_RAW_SHARD_001 = RAW_COLLECTION_PASS_RECONCILIATION_PENDING
```

The shard passed provider retrieval, frozen independent re-fetch equality, credential redaction, and the outcome-access firewall. It is **not** detector-facing `TRUSTED` because the raw missing-minute inventory remains unreconciled.

## Credential-free shard metrics

```text
page_count                           117
complete_candle_count               334841
missing_interval_count              23010
missing_minutes                     190759
refetch_complete_candle_count       60
refetch_status                      EXACT_PROVIDER_VALUE_MATCH
gap_reconciliation_status           UNRECONCILED
```

### Frozen digests

```text
retrieval_sha256                     90ecac09f426776a5cf10eb439d87068e1f77ee9fbec74d04663daa286407d37
normalized_provider_values_sha256    ddec49974155e460bed465f8952787d612325e089dc9a76d6f98850cbf20a66a
jsonl_content_sha256                 e9872da8bd440f675cda8729f179619eba7d55defad3be52cd4a1aa1b4c8d60b
missing_intervals_sha256             2abaa540528bc0a9f51be1e418ac7edd8d0956cf974fb723a6d970e80298bb39
refetch_provider_value_sha256        c63e78e912865988f5925d1cada0596e904f759151696a926e096641007b1ecc
```

The gzip container hash is deliberately not frozen as a canonical provider-value identity. The normalized provider-value digest and canonical JSONL-content digest are the stable raw-value identities.

## Raw absence profile — data-quality observation only

The raw timestamp inventory is materially more granular than weekends/known daily closures alone:

```text
1-minute missing intervals          15567
<=5-minute missing intervals        22390
minutes inside <=5-minute intervals 33191
>60-minute missing intervals        55
minutes inside >60-minute intervals 152914
```

Examples of small raw absences inside ordinary weekday daytime UTC periods include:

```text
2019-01-11T12:19Z .. 12:20Z   1 minute
2019-01-14T18:36Z .. 18:37Z   1 minute
2019-01-17T12:37Z .. 12:38Z   1 minute
2019-01-22T10:33Z .. 10:34Z   1 minute
2019-01-25T10:16Z .. 10:17Z   1 minute
```

These absences are **not** classified as `PROVIDER_MISSING`, `SESSION_BREAK`, `MARKET_CLOSED`, or any other approved category merely from their shape. They remain `UNRECONCILED`.

OANDA's first-party v20 definition states that candle `volume` is the number of prices created during the candle's time range, while OHLC fields are defined from the first/high/low/last price in that range. This creates a provider-semantics evidence question for a minute with no returned candlestick: whether it represents a legitimate no-price observation or missing provider history cannot be inferred from timestamps alone.

Primary contract reference:

- OANDA REST-v20 Instrument Definitions: `https://developer.oanda.com/rest-live-v20/instrument-df/`

The project therefore does **not** fill, forward-fill, smooth, or silently approve these minutes. Historical candle-absence semantics must be resolved/versioned before this shard can become `TRUSTED`.

## Credential / outcome safety

The retained runtime artifact passed an explicit serialized-manifest scan confirming absence of:

```text
account_id
api_token
authorization
bearer token
balance
NAV
```

Persisted account scope is only:

```text
REDACTED_RUNTIME_ACCOUNT
```

No raw M1 price file is committed to Git.

## Authorization after shard 1/16

```text
RAW_SHARDS_COLLECTED                   = 1 / 16
EUR_USD_REFETCH_WINDOWS_PASSED         = 1 / 4
EUR_USD_2019_RECONCILED                = false
EUR_USD_TRUSTED                        = false
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

## Next permitted actions

1. collect the frozen `EUR_USD` 2020, 2021 and 2022 shards without changing data rules;
2. compare the raw absence profile across years;
3. resolve OANDA's no-returned-candle semantics using primary/provider evidence before approving intra-session missing minutes;
4. reconcile only evidence-backed historical closures/absence semantics;
5. keep detector activity and all P&L closed.
