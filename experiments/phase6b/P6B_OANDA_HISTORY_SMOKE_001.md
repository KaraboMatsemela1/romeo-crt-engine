# Phase 6B OANDA Historical M1 Smoke 001

**Date:** 2026-08-13  
**Environment:** OANDA practice  
**GitHub Actions run:** `31700603683`  
**Job:** `94448535449`  
**Execution head:** `cc3de1a2124349e304bcf297464d4a370ed158a1`  
**Current code baseline containing smoke capability:** `24f1d1e18a3c916a26fa7614450f5e48bfb0ca23`  
**Status:** `HISTORICAL_M1_ACCESS_CONFIRMED`

## Purpose

Verify the real qualified OANDA practice account can return a fixed historical MID/M1 interval for every already-frozen Phase-6B instrument through the actual account-scoped candle endpoint, parser and credential-redaction controls before the complete 2019-2022 pull.

The smoke interval was selected before provider-backed DEV activity access:

```text
2019-03-12T14:00:00Z .. 2019-03-12T15:00:00Z
price component MID / M
granularity M1
smooth false
```

## Result

All four frozen instruments returned exactly 60 complete one-minute candles spanning the complete selected interval.

| Instrument | Complete M1 | Request SHA-256 | Raw response SHA-256 | Normalized provider-value SHA-256 |
|---|---:|---|---|---|
| `EUR_USD` | 60 | `1a41c0fb4016084342071f085bac8dc32c6ec4d27d3e4c3ae75683e4fb0f1c9c` | `c8bf9a3cea6a1a6f8d5cd8a9ce4ff76c37efd8fdeb94074e3b7e95dffb04d316` | `870aa29d400b2fa9b0dd17bf2eaa147b36ee02b27f646affa753789988019fc1` |
| `XAU_USD` | 60 | `0ecc4aa2cbfe285ba5960903f25e39f6aec9283a3312195e703858628c7ce37e` | `4d18754a23e566586d45c81152300fb50189ef590bcf969c1c5d6118fd6accf8` | `8fabe08ede4242149251fbbaf9cecd486cb3416779ee07ec5b22d94e140bc688` |
| `NAS100_USD` | 60 | `cbeb846d0974a08660762e13c4a1e46041438d8cb4c4b10c098260b5020b0ccd` | `4d0728da8ffd798d8bddbcff7c8a32cb78cae39fa46f99fff1c5120ecf2b1614` | `651b95ab7d57571f93ced0c6c7f237b7329270ddb2727a9863a2a08b8759cea4` |
| `SPX500_USD` | 60 | `ff15698b7a0f31002652593fdf9b862fc037d3d7f8988cb218d05d6177ae96ed` | `b7c6a77ccc16332ab616aef6460dff802658003187ca4f7a2fac4b90c421c32f` | `81051373b95238c7cdf0e6ac54a31bdb16eda7ac92c87a6f777dd739461ec4f2` |

## Credential / outcome safety

The runtime verification passed:

```text
OANDA_QUALIFICATION_ARTIFACT_SAFE=true
OANDA_HISTORY_SMOKE_ARTIFACT_SAFE=true
```

No account ID, bearer token, balance or NAV was persisted in this record. No raw price values are committed here; only identity, counts and hashes are preserved.

The temporary branch/path-scoped trigger used to execute the smoke was subsequently removed from branch history; the canonical OANDA workflow is manual-only again.

## Interpretation

This establishes, without opening a strategy result, that:

- the configured practice account can access historical M1 data for all four frozen symbols;
- the account-scoped OANDA v20 candle endpoint works through the project adapter;
- the selected 2019 interval is available for each frozen symbol;
- MID/M1 parsing and complete-candle validation work on real provider responses;
- request/raw-response provenance and normalized provider-value hashing work.

It does **not** prove the full 2019-2022 stream is gap-free, that historical session/holiday rules are reconciled, or that any instrument is detector-facing `TRUSTED`.

## Authorization after smoke

```text
FULL_RAW_DEV_COLLECTION                 = NEXT DATA-QUALITY GATE
HISTORICAL_SESSION_CALENDAR_FROZEN      = false
DETECTOR_ACTIVITY_COUNTS_AUTHORIZED     = false
STRATEGY_OUTCOME_ACCESS_AUTHORIZED      = false
PNL_OUTCOME_ACCESS_AUTHORIZED           = false
BACKTESTER_AUTHORIZED                   = false
PAPER_TRADING_AUTHORIZED                = false
SHADOW_TRADING_AUTHORIZED               = false
LIVE_TRADING_AUTHORIZED                 = false
```

The next permitted action is the sealed raw 2019-2022 MID/M1 collection and missing-interval inventory under `P6B-OANDA-HISTORY-QUALIFICATION-V1`.
