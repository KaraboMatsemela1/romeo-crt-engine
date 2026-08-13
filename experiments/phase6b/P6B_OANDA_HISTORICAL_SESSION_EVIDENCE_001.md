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

OANDA's table states:

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

## Evidence E2 — current OANDA schedules are current-reference only

OANDA's current hours-of-operation page presently lists:

```text
US Nas 100  — Chicago — Sunday-Friday 17:01-15:59
US SPX 500  — Chicago — Sunday-Friday 17:01-15:59
```

First-party source:

- OANDA Global Markets, `Trading Times | Forex Market Hours`
- https://www.oanda.com/bvi-en/cfds/hours-of-operation/

This differs by one minute from the 2021 change notice's stated post-change `17:00-15:59`. Therefore even post-2021 current rules must not be silently assumed for all historical data without raw-gap confirmation or another dated OANDA change notice.

## Evidence E3 — FX weekly closure / special-day caveat

OANDA's own FX educational material states that FX is ordinarily available on weekdays but not on weekends and identifies New Year's Day as a non-trading day; it also notes daylight-saving effects.

First-party source:

- OANDA Lab, `外匯交易最佳時段與交易時段解析`
- https://www.oanda.com/bvi-ft/lab-education/forex/aboutfx-time/

This is useful as a broad availability constraint for `EUR_USD`, but it is not sufficiently precise to classify every minute of the 2019-2022 provider stream.

## Evidence E4 — dated exceptional closures exist

OANDA published dated trading notices for exceptional closures. For example, on **2022-06-10**, OANDA announced a temporary trading suspension for AU200 related to an Australian holiday, and on **2022-05-31** OANDA announced market closures affecting some financial instruments for UK public holidays.

First-party sources:

- https://www.oanda.com/bvi-ft/lab-education/info/20220610-4/
- https://www.oanda.com/bvi-ft/lab-education/info/20220531-1/

These notices establish that historical exceptional closures must be treated as dated evidence, not inferred from today's recurring schedule.

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

After the sealed raw M1 pull, use the actual missing-interval inventory to search OANDA's dated archive efficiently. This prevents us from manufacturing a broad holiday calendar that may not match the provider's historical instrument availability.
