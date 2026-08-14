# Phase 6B Canonical Coverage Amendment 001

**Status:** **FROZEN — PRE-DETECTOR DATA-BOUNDARY CORRECTION**  
**Date:** 2026-08-14  
**Parent protocol:** `P6B-MULTI-MARKET-ACTIVITY-PROTOCOL-v1`  
**Coverage policy:** `P6B_CANONICAL_COVERAGE_V1`  
**Detector activity counts:** **UNOPENED**  
**P&L outcome access:** **PROHIBITED**

## Reason for this amendment

The activity protocol froze its DEV window in New-York wall-clock time:

```text
2019-01-01 00:00:00 America/New_York
through
2022-12-31 23:59:59.999... America/New_York
```

It also requires provider manifests to represent operational bounds in UTC while preserving New-York-midnight D1 construction.

At both endpoints New York is UTC-05:00. Therefore the exact operational UTC interval for the already-frozen local DEV window is:

```text
2019-01-01T05:00:00Z
through
2023-01-01T05:00:00Z exclusive
```

The raw yearly qualification pass was intentionally frozen earlier as:

```text
2019-01-01T00:00:00Z
through
2023-01-01T00:00:00Z exclusive
```

That raw pass contains five hours before the detector window begins, but it stops five hours before the frozen 2022-12-31 New-York D1 candle ends.

Shrinking the activity period to fit the earlier UTC collection would violate the preregistered activity protocol. Extending beyond `2023-01-01T05:00:00Z` would also violate it. The only valid correction is therefore to qualify exactly the missing five-hour UTC tail.

## Frozen canonical bounds

```text
canonical_start_utc       2019-01-01T05:00:00Z
canonical_end_utc         2023-01-01T05:00:00Z exclusive
previous_raw_end_utc      2023-01-01T00:00:00Z
additional_tail_start_utc 2023-01-01T00:00:00Z
additional_tail_end_utc   2023-01-01T05:00:00Z exclusive
additional_tail_duration  5 hours
```

No data after `2023-01-01T05:00:00Z` may be fetched or used by the canonical DEV construction under this amendment.

## Eligibility semantics for New-York D1

A New-York local date is eligible for canonical D1 construction only when the qualified provider M1 stream contains at least one price observation whose open belongs to that local date.

This rule is data-geometric and pre-outcome:

- it does not guess weekends or holidays;
- it does not fabricate a Daily candle for a date with zero provider observations;
- it does not inspect detector signals, TradePlans, or performance;
- once a date is eligible, every absent minute inside its New-York-midnight window must still be covered by approved gap evidence or aggregation fails closed.

Implementation: `src/romeo_crt_engine/market_data/canonical_coverage_v2.py`.

## Tail qualification requirement

Before any instrument can become `TRUSTED`, the exact five-hour tail must be qualified with the same principles as the core raw window:

```text
provider                     OANDA_V20 practice
price component              MID
granularity                  M1
smoothing                    false
interval                     2023-01-01T00:00:00Z .. 2023-01-01T05:00:00Z
independent provider refetch required
missing intervals            enumerated exactly
finer evidence               MID/S5, exact tail only
synthetic prices             prohibited
forward fill                 prohibited
unresolved provider gaps     fail closed
```

The tail is provider-data qualification only. It does not authorize detector access to any date outside the frozen DEV interval and it does not open the v0.1 OOS result surface.

## Authorization boundary

```text
V0_1_MUTATION_AUTHORIZED               = false
V0_1_OOS_OUTCOME_ACCESS_AUTHORIZED     = false
V0_1_CONFIRM_OUTCOME_ACCESS_AUTHORIZED = false
DETECTOR_ACTIVITY_COUNTS_AUTHORIZED    = false
BACKTEST_AUTHORIZED                    = false
MULTI_MARKET_PNL_OUTCOME_ACCESS        = false
PAPER_TRADING_AUTHORIZED               = false
SHADOW_TRADING_AUTHORIZED              = false
LIVE_TRADING_AUTHORIZED                = false
```
