# Phase 6B OANDA EUR_USD 2019–2022 Collection + Candle-Absence Probe 001

**Date:** 2026-08-13  
**Environment:** OANDA practice  
**Instrument:** `EUR_USD`  
**Price component:** MID  
**Primary granularity:** M1  
**Parent protocol:** `P6B-OANDA-HISTORY-QUALIFICATION-V1`  
**Strategy outcome access:** PROHIBITED

## Collection decision

```text
P6B_OANDA_EUR_USD_2019_2022_COLLECTION_001 = RAW_COLLECTION_PASS_RECONCILIATION_PENDING
```

All four frozen yearly raw shards completed successfully. All four preregistered independent one-hour re-fetches produced exact provider-value matches. No detector, TradePlan, backtester or P&L output was opened.

## Four-year raw shard summary

| Year | Pages | Complete M1 candles | Missing intervals | Missing minutes | Re-fetch |
|---:|---:|---:|---:|---:|---|
| 2019 | 117 | 334,841 | 23,010 | 190,759 | EXACT_PROVIDER_VALUE_MATCH |
| 2020 | 118 | 362,762 | 6,127 | 164,278 | EXACT_PROVIDER_VALUE_MATCH |
| 2021 | 117 | 362,338 | 6,292 | 163,262 | EXACT_PROVIDER_VALUE_MATCH |
| 2022 | 117 | 368,214 | 2,341 | 157,386 | EXACT_PROVIDER_VALUE_MATCH |

### Stable provider-value identities

```text
2019 normalized_provider_values_sha256 ddec49974155e460bed465f8952787d612325e089dc9a76d6f98850cbf20a66a
2020 normalized_provider_values_sha256 cb25199112ea0abd309485adfd206a189ba9bbc9642b15f31cbd81e065b80bba
2021 normalized_provider_values_sha256 bc2b98780991336e5fd909965c25abda5c383dd19804c69d32baa4bf48160ce6
2022 normalized_provider_values_sha256 da9625cf2d219444c3ec54a225d3070c7da6c9ef9388bf3c24f49b5db39b2f56

2019 missing_intervals_sha256 2abaa540528bc0a9f51be1e418ac7edd8d0956cf974fb723a6d970e80298bb39
2020 missing_intervals_sha256 032949de2d4cd293e04b792d9daa06f7701afc4afaf5e4759292bac4782df8d3
2021 missing_intervals_sha256 28d0e09d52f63bc10838ec9a03ae9ee72b0ba43dc9739a4c27d0cff1bef10676
2022 missing_intervals_sha256 dbc97e83b2415d7d93f6c7e24281bf512547257d3da7e3ecd4346d7376a14184
```

### Short-absence profile

| Year | 1-minute intervals | <=5-minute intervals | Minutes inside <=5-minute intervals | >60-minute intervals | Minutes inside >60-minute intervals |
|---:|---:|---:|---:|---:|---:|
| 2019 | 15,567 | 22,390 | 33,191 | 55 | 152,914 |
| 2020 | 3,840 | 5,790 | 9,090 | 54 | 152,742 |
| 2021 | 4,037 | 5,931 | 9,137 | 53 | 151,344 |
| 2022 | 1,452 | 2,244 | 3,761 | 54 | 153,247 |

This shows that raw absence density is materially higher in 2019 than later years. The project does not infer a strategy implication from that observation.

## Provider candle-absence probe

A separate practice-only read-only probe selected one ordinary raw one-minute absence from each year using only the already-opened gap inventory. For each probe, OANDA was queried over the surrounding three-minute window at both M1 and S5 MID granularity.

Probe run:

```text
GitHub Actions run 31717204184
schema             P6B_OANDA_CANDLE_ABSENCE_PROBE_V1
```

Results:

| Year | M1 missing minute | M1 candles inside minute | S5 candles inside minute | S5 prices created inside minute |
|---:|---|---:|---:|---:|
| 2019 | 2019-02-06T11:59Z | 0 | 0 | 0 |
| 2020 | 2020-02-05T18:26Z | 0 | 0 | 0 |
| 2021 | 2021-08-16T16:27Z | 0 | 0 | 0 |
| 2022 | 2022-02-01T03:16Z | 0 | 0 | 0 |

In all four samples, S5 prices existed immediately before and/or after the missing M1 minute, but OANDA returned **no S5 candle and zero S5 price observations inside the missing minute itself**.

## Evidence interpretation

OANDA's first-party REST-v20 `Candlestick` definition states that `volume` is the number of prices created during the time range represented by the candlestick. OHLC fields are defined from the first/high/low/last price in that range.

Primary source:

- `https://developer.oanda.com/rest-live-v20/instrument-df/`

The combined first-party contract + 4/4 cross-granularity probes supports the following limited conclusion:

```text
P6B_OANDA_M1_ABSENCE_PROBE_001 = SAMPLED_M1_ABSENCES_CONSISTENT_WITH_NO_PRICE_OBSERVATION
```

It does **not** authorize declaring every absent M1 minute harmless. It does establish that `absent M1 timestamp == provider data loss` is too strong: at least the sampled absences contain no underlying S5 price observation from which an M1 OHLC candle could be formed.

## Required protocol correction before TRUSTED status

The v1 historical qualification rule currently treats every absent M1 minute as a timestamp gap requiring a market/session/holiday classification. That rule is now known to conflate two different concepts:

1. **market-time absence** — closed market/session break/holiday;
2. **price-observation absence** — an open time bucket for which OANDA created no price observations and therefore returned no M1/S5 candle in the sampled cases.

This is a provider-data semantics issue discovered before detector execution and before P&L access. It must be corrected through a versioned data protocol/aggregation contract rather than by filling prices or relaxing rules in place.

Any successor protocol must preserve these principles:

- never synthesize or forward-fill missing prices;
- never classify an absence from timestamp shape alone;
- distinguish session closure from no-price observation;
- retain fail-closed handling for genuine provider-missing/unknown history;
- aggregate H1/D1 only from actual provider observations;
- freeze the corrected semantics before detector activity access.

`EUR_USD` therefore remains `NOT_TRUSTED` pending this provider-observation protocol correction and historical session reconciliation.

## Authorization

```text
RAW_SHARDS_COLLECTED                   = 4 / 16
EUR_USD_REFETCH_WINDOWS_PASSED         = 4 / 4
EUR_USD_RAW_COLLECTION_COMPLETE        = true
EUR_USD_GAP_RECONCILIATION_COMPLETE    = false
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
