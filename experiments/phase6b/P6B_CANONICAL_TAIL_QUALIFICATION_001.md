# Phase 6B Canonical Tail Qualification 001

**Status:** **PASS — CANONICAL BOUNDARY QUALIFIED 4/4**  
**Date:** 2026-08-14  
**Provider:** OANDA v20 practice  
**Workflow:** OANDA Canonical Tail Qualification run #1 (`31797839483`)  
**Evidence commit:** `4c6af48f0f1cea1b83a02f9bf1734679d5db8c5f`  
**Coverage policy:** `P6B_CANONICAL_COVERAGE_V1`  
**Observation policy:** `P6B_OANDA_OBSERVATION_POLICY_V2`  
**Detector activity counts:** **UNOPENED**  
**P&L outcome access:** **PROHIBITED**

## Purpose

Seal the exact UTC-boundary correction required to preserve the preregistered Phase-6B DEV interval in `America/New_York` calendar time.

The activity protocol freezes the DEV interval as 2019-01-01 00:00 New York through the end of 2022-12-31 New York. The correct operational UTC interval is therefore:

```text
2019-01-01T05:00:00Z
through
2023-01-01T05:00:00Z exclusive
```

The earlier raw qualification pass ended at `2023-01-01T00:00:00Z`. This record qualifies exactly the missing five-hour tail and no later data:

```text
2023-01-01T00:00:00Z .. 2023-01-01T05:00:00Z exclusive
```

This is a coverage correction only. It does not expand the frozen local DEV period and it does not authorize any detector or performance outcome surface.

## Result

All four frozen instruments returned the same provider-observation result for the exact tail:

```text
primary M1 observations                0
independent refetch M1 observations    0
missing intervals                      1
missing minutes                      300
NO_PRICE_OBSERVATION intervals         1
NO_PRICE_OBSERVATION minutes          300
UNRESOLVED_PROVIDER_GAP intervals      0
UNRESOLVED_PROVIDER_GAP minutes        0
refetch status          EXACT_PROVIDER_EMPTY_MATCH
```

Per instrument:

| Instrument | M1 observations | Missing gaps | Missing minutes | No-price gaps | Unresolved gaps | Refetch |
|---|---:|---:|---:|---:|---:|---|
| `EUR_USD` | 0 | 1 | 300 | 1 | 0 | `EXACT_PROVIDER_EMPTY_MATCH` |
| `XAU_USD` | 0 | 1 | 300 | 1 | 0 | `EXACT_PROVIDER_EMPTY_MATCH` |
| `NAS100_USD` | 0 | 1 | 300 | 1 | 0 | `EXACT_PROVIDER_EMPTY_MATCH` |
| `SPX500_USD` | 0 | 1 | 300 | 1 | 0 | `EXACT_PROVIDER_EMPTY_MATCH` |

The exact five-hour tail is therefore a provider-confirmed no-price interval for every frozen market under the finer S5 observation check. No holiday/calendar assumption is required.

## Artifact inventory

All artifacts are from run `31797839483` and evidence commit `4c6af48f0f1cea1b83a02f9bf1734679d5db8c5f`.

| Instrument | Artifact ID | Artifact SHA-256 |
|---|---:|---|
| `EUR_USD` | 9218059952 | `e93c6b4e784ebe423dc16f46a302302135e8ae57ee84e0c73e5ea5cf027b85ee` |
| `XAU_USD` | 9218068363 | `680351d76851df81cfad8053738ee959c2301b8310dfcd2c0344f4a962c5e616` |
| `NAS100_USD` | 9218078313 | `54d6aef046f0053bf3e86eb767c30bdf54f6642fe1c0583cf131fcd92c670018` |
| `SPX500_USD` | 9218086609 | `57cc4aaf6ca13c9fa7f64a083a6b95c49245956fb678adc680b0a4c50c01652d` |

Raw/local evidence was deleted after the credential-safe evidence artifacts were uploaded.

## Decision

```text
CANONICAL_BOUNDARY_QUALIFICATION = PASS 4/4
```

The full preregistered New-York DEV boundary is now provider-qualified without changing the local research window.

This pass is still not equivalent to a detector-facing trusted dataset. The next hard gate remains deterministic reconstruction and freeze of complete canonical MID/M1, H1, and New-York-midnight D1 datasets with one `P6B_CANONICAL_PRICE_DATASET_V2` identity per instrument and `quality_status = TRUSTED` only after all checks pass.

## Safety boundary

```text
V0_1_MUTATION_AUTHORIZED               = false
V0_1_OOS_OUTCOME_ACCESS_AUTHORIZED     = false
V0_1_CONFIRM_OUTCOME_ACCESS_AUTHORIZED = false
PARAMETER_OPTIMIZATION_AUTHORIZED      = false
DETECTOR_ACTIVITY_COUNTS_AUTHORIZED    = false
BACKTEST_AUTHORIZED                    = false
MULTI_MARKET_PNL_OUTCOME_ACCESS        = false
PAPER_TRADING_AUTHORIZED               = false
SHADOW_TRADING_AUTHORIZED              = false
LIVE_TRADING_AUTHORIZED                = false
```
