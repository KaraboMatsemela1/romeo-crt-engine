# Phase 6B OANDA Runtime Qualification 002

**Date:** 2026-08-13  
**Environment:** OANDA practice  
**Research candidate:** `CRT-C3-D1-H1-M1-BEAR-v0.2-MULTI-MARKET-RESEARCH`  
**Strategy outcome access:** PROHIBITED  
**P&L access:** PROHIBITED

## Purpose

Repeat the credentialed OANDA qualification after the runtime account secret was changed, preserving the same redaction and outcome-lock controls used by the prior gate.

## Runtime evidence

GitHub Actions run `31696424928`, attempt `2`, job `94438165028` completed successfully.

Observed:

```text
authorized_account_count=5
configured_account_authorized=true
account_summary_available=true
account_home_currency=USD
available_instrument_count=123
source_family_matches=4/4
OANDA_QUALIFICATION_ARTIFACT_SAFE=true
```

No account identifier, bearer token, balance or NAV was persisted in the qualification result.

## Precommitted source-family intersection

All four ex-ante source families were available under their precommitted aliases:

| Source family | Frozen OANDA symbol | Type | Status |
|---|---|---|---|
| EUR/USD | `EUR_USD` | CURRENCY | MATCHED |
| Gold/USD | `XAU_USD` | METAL | MATCHED |
| US NAS 100 / NQ proxy | `NAS100_USD` | CFD | MATCHED |
| US SPX 500 / ES proxy | `SPX500_USD` | CFD | MATCHED |

The provider returned 123 instruments in total. Only the four precommitted source-family aliases were evaluated for this candidate; no additional instrument was selected after discovery.

Provider response identities:

```text
available_instrument_names_sha256 = 2e77a962f559c51d37120ebe842ba62cd0c42e07f50fe845ced04df7ad0755d2
raw_instrument_response_sha256    = e9ea9a83b2b0f66605f79a94e9c5ca6f21549dd1f1cbbe739077165fe604ea64
raw_account_summary_sha256        = 63cd8a2960941c199239250a12bd5954e7533113a9dfb8c9379236b4c42c9a22
```

## Decision

```text
P6B_OANDA_RUNTIME_QUALIFICATION_002 = ELIGIBLE_UNIVERSE_DISCOVERED
```

This clears the minimum eligible-universe requirement (`>=2`) and authorizes freezing the exact four-symbol research universe.

It does **not** authorize detector activity counts yet. Before activity access, the accepted instruments still require frozen session/holiday policy, explicit price quantum, sealed MID M1 DEV data, deterministic H1/New-York-D1 construction and trusted dataset identities.

## Authorization after this result

```text
INSTRUMENT_UNIVERSE_FREEZE_AUTHORIZED   = true
DETECTOR_ACTIVITY_COUNTS_AUTHORIZED     = false
MULTI_MARKET_PNL_OUTCOME_ACCESS         = false
V0_1_OOS_OUTCOME_ACCESS_AUTHORIZED      = false
V0_1_CONFIRM_OUTCOME_ACCESS_AUTHORIZED  = false
PAPER_TRADING_AUTHORIZED                = false
SHADOW_TRADING_AUTHORIZED               = false
LIVE_TRADING_AUTHORIZED                 = false
```
