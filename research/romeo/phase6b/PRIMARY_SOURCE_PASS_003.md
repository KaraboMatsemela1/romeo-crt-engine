# Phase 6B Primary Source Pass 003 — OANDA Historical Data Boundary

**Date:** 2026-08-13  
**Scope:** historical provider/data semantics only  
**Strategy outcomes:** NOT OPENED

## Direct first-party findings

### OANDA v20 historical candle contract

OANDA's official v20 instrument endpoint defines account-scoped historical candles at:

```text
GET /v3/accounts/{accountID}/instruments/{instrument}/candles
```

Relevant contract fields for Phase 6B:

```text
granularity = M1
price       = M
from / to   supported
smooth      = false by default
count       = maximum 5000 candles
```

Official sources:

- https://developer.oanda.com/rest-live-v20/instrument-ep/
- https://developer.oanda.com/rest-live-v20/api-comparison/

Conclusion: the project account-scoped OANDA history adapter is using the correct current v20 endpoint and the frozen 4500-minute page width is below the provider maximum.

### OANDA connection-rate evidence

OANDA's v20 best-practices page recommends at most two new connections per second; its development guide describes the two-new-connections-per-second limit. Established persistent connections may sustain a much higher request rate.

Official sources:

- https://developer.oanda.com/rest-live-v20/best-practices/
- https://developer.oanda.com/rest-live-v20/development-guide/

Conclusion: long-running raw-history acquisition must be rate-aware. Provider limits are a data-acquisition constraint, not a strategy parameter.

### Historical US index schedule boundary inside DEV

OANDA published a dated notice on **2021-06-28** changing US Nas 100 and US SPX 500 hours:

```text
before  Sunday-Friday 17:00-16:00
after   Sunday-Friday 17:00-15:59
```

Official source:

- https://www.oanda.com/bvi-ft/lab-education/info/20210628-1/

OANDA's current hours page now lists both index CFDs as `17:01-15:59` Chicago time, creating evidence that another later schedule regime may exist.

Official current reference:

- https://www.oanda.com/bvi-en/cfds/hours-of-operation/

Conclusion: current session hours cannot be projected backward across the complete 2019-2022 DEV window. Historical reconciliation must be date-segmented and driven by the raw missing-interval inventory.

### Current reference constraints

OANDA currently publishes:

```text
All FX      New York  Sunday-Friday 17:05-16:59
XAU/USD     New York  Sunday-Friday 18:05-16:59
US Nas 100  Chicago   Sunday-Friday 17:01-15:59
US SPX 500  Chicago   Sunday-Friday 17:01-15:59
```

OANDA also states hours can change for daylight saving time and public holidays.

These are useful as present-day reference constraints only; they are not sufficient historical evidence for every missing minute between 2019 and 2022.

## Runtime confirmation already obtained

The fixed 2019-03-12 14:00-15:00 UTC MID/M1 smoke passed for all four frozen symbols with 60/60 complete M1 candles each. Only counts and cryptographic hashes were preserved in repo evidence.

Canonical runtime record:

- `experiments/phase6b/P6B_OANDA_HISTORY_SMOKE_001.md`

## Gate state after Pass 003

```text
OANDA_HISTORICAL_ENDPOINT_VERIFIED      = true
M1_MID_ACCESS_SMOKE_4_OF_4              = true
PAGING_PROVENANCE_MECHANICS             = implemented_and_tested
RAW_GAP_ENUMERATION_MECHANICS           = implemented_and_tested
HISTORICAL_SESSION_CALENDAR_FROZEN      = false
FULL_2019_2022_RAW_COLLECTION_COMPLETE  = false
DETECTOR_ACTIVITY_COUNTS_AUTHORIZED     = false
PNL_OUTCOME_ACCESS_AUTHORIZED           = false
```

The next admissible provider-data evidence is the complete raw DEV missing-interval inventory. No alpha or detector rule change is justified by this source pass.
