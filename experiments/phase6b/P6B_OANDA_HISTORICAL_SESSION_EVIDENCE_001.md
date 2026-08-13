# Phase 6B OANDA Historical Session Evidence 001

**Status:** PARTIAL / RAW-GAP RECONCILIATION REQUIRED  
**Date:** 2026-08-13  
**Provider:** OANDA  
**Frozen instruments:** `EUR_USD`, `XAU_USD`, `NAS100_USD`, `SPX500_USD`  
**Strategy outcome access:** PROHIBITED

## Purpose

Record first-party OANDA evidence that constrains the historical availability model before any detector activity count is opened.

This document does **not** create the final executable 2019-2022 calendar. The final calendar must be derived by reconciling raw provider gaps against dated first-party evidence. Current published hours may not be projected backward when OANDA documents an historical schedule change.

## Evidence E1 — US index schedule changed during DEV

OANDA published **2021-06-28** that trading hours changed that day for, among other instruments, **US Nas 100** and **US SPX 500**.

OANDA's dated table states:

```text
before: Sunday-Friday 17:00-16:00
after:  Sunday-Friday 17:00-15:59
```

First-party source:

- OANDA Lab, `部分交易品種的交易時間變更`, 2021-06-28
- https://www.oanda.com/bvi-ft/lab-education/info/20210628-1/

### Consequence

A single present-day regular-session rule cannot be applied to the complete 2019-2022 DEV interval for `NAS100_USD` or `SPX500_USD`.

At minimum, index session reconciliation must treat **2021-06-28** as a dated policy boundary and confirm exact timestamp semantics against observed provider gaps.

## Evidence E2 — current OANDA schedules are reference constraints only

OANDA's current hours-of-operation material lists:

```text
All FX      New York  Sunday-Friday 17:05-16:59
XAU/USD     New York  Sunday-Friday 18:05-16:59
US Nas 100  Chicago   Sunday-Friday 17:01-15:59
US SPX 500  Chicago   Sunday-Friday 17:01-15:59
```

First-party source:

- OANDA Global Markets, `Trading Times | Forex Market Hours`
- https://www.oanda.com/bvi-en/cfds/hours-of-operation/

The current index reference differs by one minute from the 2021 dated post-change notice's `17:00-15:59`. Therefore another regime change may exist after 2021-06-28. The exact boundary must be identified from dated OANDA evidence plus observed provider gaps; it may not be guessed.

## Evidence E3 — hours vary for DST and public holidays

OANDA help material states that hours of operation are subject to change during daylight saving time and certain public holidays.

First-party source:

- OANDA Help, `Hours of operation in OANDA Global Markets`
- https://help.oanda.com/bvi/en/faqs/hours-of-operation.htm

### Consequence

Historical timestamp reconciliation must use the named source timezone and historical timezone rules. A familiar exchange holiday is not, by itself, enough to classify a missing OANDA interval.

## Evidence E4 — FX broad availability constraint

OANDA's FX educational material describes ordinary weekday availability, weekend closure, New Year's Day non-trading treatment, and daylight-saving effects.

First-party source:

- OANDA Lab, `外匯交易最佳時段與交易時段解析`
- https://www.oanda.com/bvi-ft/lab-education/forex/aboutfx-time/

This is useful as a broad availability constraint for `EUR_USD`, but it is not sufficiently precise to classify every minute of the 2019-2022 provider stream.

## Evidence E5 — dated exceptional closures exist

OANDA publishes dated notices for exceptional closures. Examples in the archive include:

- `2022-05-31`: notice that UK public holidays on June 2 and June 3 would close some financial-instrument markets;
- `2022-06-10`: notice of an Australian-holiday-related temporary closure for AU200.

First-party sources:

- https://www.oanda.com/bvi-ft/lab-education/info/20220531-1/
- https://www.oanda.com/bvi-ft/lab-education/info/20220610-4/

These examples are not automatically applicable to the four frozen instruments. They establish the evidence model: exceptional historical closures are dated provider events and must be reconciled instrument-by-instrument rather than generated from today's recurring schedule.

## Evidence E6 — historical API contract supports the raw observation route

OANDA v20's official instrument-candles endpoint is account scoped:

```text
GET /v3/accounts/{accountID}/instruments/{instrument}/candles
```

The official contract supports `M1`, `price=M`, `from`/`to`, unsmoothed candles and a maximum of 5,000 candles per response. OANDA's API comparison describes v20 instrument history as complete and supports M1.

First-party sources:

- https://developer.oanda.com/rest-live-v20/instrument-ep/
- https://developer.oanda.com/rest-live-v20/api-comparison/

This supports the project's frozen 4,500-minute paging contract without relying on provider-native Daily alignment.

## Evidence E7 — connection-rate constraint

OANDA's v20 best-practices material recommends no more than two new connections per second and up to 100 requests per second on an established persistent connection. The development guide describes the two-new-connections-per-second limit explicitly.

First-party sources:

- https://developer.oanda.com/rest-live-v20/best-practices/
- https://developer.oanda.com/rest-live-v20/development-guide/

Any complete historical collection job must therefore be rate-aware. Pagination may not be accelerated by violating the provider's documented connection limits.

## Historical-calendar rule

The Phase-6B trusted-data gate therefore uses this order:

1. retrieve the complete sealed provider M1 interval without synthesizing missing observations;
2. enumerate all missing intervals mechanically;
3. classify recurring session closures only when supported by a dated/current rule that is valid for that historical segment;
4. classify holidays/early closes only with dated evidence or an authoritative market-calendar contract proven to govern that OANDA instrument at the time;
5. leave any unresolved interval as `UNKNOWN_GAP` / fail closed;
6. do not build a detector-facing `TRUSTED` dataset until every removed expected observation is evidenced.

## Explicit non-decisions

```text
HISTORICAL_SESSION_CALENDAR_FROZEN      = false
HOLIDAY_EARLY_CLOSE_CALENDAR_FROZEN     = false
DETECTOR_ACTIVITY_COUNTS_AUTHORIZED     = false
STRATEGY_OUTCOME_ACCESS_AUTHORIZED      = false
PNL_OUTCOME_ACCESS_AUTHORIZED           = false
BACKTESTER_AUTHORIZED                   = false
PAPER_TRADING_AUTHORIZED                = false
LIVE_TRADING_AUTHORIZED                 = false
```

## Next evidence work

After the sealed raw M1 pull, use the actual missing-interval inventory to search OANDA's dated archive efficiently. This prevents manufacturing a broad holiday calendar that may not match the provider's historical instrument availability.
