# Phase 6B OANDA History Collection Gate 001

**Date:** 2026-08-13  
**Status:** READY FOR COMPLETE RAW COLLECTION / NOT YET COMPLETE  
**Detector activity counts:** NOT AUTHORIZED  
**P&L:** NOT AUTHORIZED

## Completed prerequisites

```text
practice account qualified               yes
exact four-symbol universe frozen        yes
MID / M1 signal-source contract frozen   yes
provider price quantum frozen            yes
historical endpoint contract verified    yes
4500-minute page contract frozen         yes
empty-page provenance tested             yes
raw missing-interval enumeration tested  yes
independent value-refetch logic tested   yes
historical session regime fully frozen   no
```

## Runtime smoke

The fixed `2019-03-12T14:00:00Z .. 15:00:00Z` historical smoke passed through the real qualified OANDA practice account for:

```text
EUR_USD       60 / 60 complete M1
XAU_USD       60 / 60 complete M1
NAS100_USD    60 / 60 complete M1
SPX500_USD    60 / 60 complete M1
```

Canonical evidence:

- `experiments/phase6b/P6B_OANDA_HISTORY_SMOKE_001.md`

## Frozen complete-collection protocol

Canonical protocol:

- `experiments/phase6b/P6B_OANDA_HISTORY_QUALIFICATION_PROTOCOL_V1.md`

Required raw interval:

```text
2019-01-01T00:00:00Z .. 2023-01-01T00:00:00Z exclusive
```

The complete collection must preserve page-level request/raw-response provenance and leave every missing interval `UNRECONCILED` until a date-valid availability rule is proven.

## Historical-session warning

A dated OANDA notice proves the US Nas 100 / US SPX 500 session changed inside DEV on `2021-06-28`. Current hours also differ by one minute from the dated post-change schedule.

Therefore the trusted-data gate explicitly prohibits applying one current recurring schedule to the entire 2019-2022 interval.

Canonical source evidence:

- `experiments/phase6b/P6B_OANDA_HISTORICAL_SESSION_EVIDENCE_001.md`
- `research/romeo/phase6b/PRIMARY_SOURCE_PASS_003.md`

## Promotion rule

Complete raw provider history is **not** itself enough for detector access.

Before any detector count is opened, each promoted instrument must have:

1. complete raw value/provenance artifacts;
2. all four frozen independent re-fetch samples equal by provider value;
3. every missing interval reconciled to an approved date-valid closure/session/holiday category;
4. no `UNKNOWN_GAP` / `PROVIDER_MISSING` / `UNRECONCILED` interval remaining;
5. deterministic H1 and New-York-midnight D1;
6. a frozen `P6B_CANONICAL_PRICE_DATASET_V2` identity with `quality_status=TRUSTED`.

If fewer than two instruments meet the trusted-data gate, stop as `INSUFFICIENT_ELIGIBLE_UNIVERSE` before running the detector.

## Authorization

```text
DETECTOR_EXECUTION_AUTHORIZED           = false
TRADEPLAN_COUNT_ACCESS_AUTHORIZED       = false
BACKTESTER_AUTHORIZED                   = false
PNL_OUTCOME_ACCESS_AUTHORIZED           = false
V0_1_OOS_ACCESS_AUTHORIZED              = false
V0_1_CONFIRM_ACCESS_AUTHORIZED          = false
PAPER_TRADING_AUTHORIZED                = false
SHADOW_TRADING_AUTHORIZED               = false
LIVE_TRADING_AUTHORIZED                 = false
```
