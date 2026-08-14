# Phase 6B All-Gap S5 Pilot 001

**Record:** `P6B-ALL-GAP-S5-PILOT-001`  
**Date:** 2026-08-14  
**Candidate:** `CRT-C3-D1-H1-M1-BEAR-v0.2-MULTI-MARKET-RESEARCH`  
**Alpha:** `CRT-C3-D1-H1-M1-BEAR-v0.1` — unchanged  
**Provider:** OANDA v20 practice  
**Instrument/year:** `XAU_USD / 2022`  
**Workflow:** `OANDA Provider Qualification` run `#26` / run id `31777768060`  
**Result:** `PASS — COMPLETE CROSS-GRANULARITY GAP CLASSIFICATION`  
**Detector activity:** `NOT_AUTHORIZED`  
**P&L access:** `NOT_AUTHORIZED`

## Purpose

Validate the fail-closed all-gap S5 method on one preregistered historical shard before expanding the same pre-outcome data-quality method to the complete frozen Phase-6B universe.

This is a provider/data-quality result only. It does not open detector outcomes, TradePlan counts, backtesting or P&L.

## Frozen method

The pilot reuses the already-validated yearly MID/M1 collector and S5 cross-granularity classifier. `scripts/probe_oanda_all_gaps_s5.py` removes only the prior `<=60 minute` eligibility filter; the underlying provider requests remain split into six-hour S5 buckets.

The pilot is valid only if:

```text
S5 eligible_gap_count == raw M1 missing_interval_count
S5 source_missing_intervals_sha256 == raw missing_intervals_sha256
S5 classified count == NO_PRICE_OBSERVATION + UNRESOLVED_PROVIDER_GAP
independent M1 refetch == EXACT_PROVIDER_VALUE_MATCH
all detector/P&L authorization flags == false
persisted evidence contains no credentials/account identifiers/raw-price path
```

No assertion forces `UNRESOLVED_PROVIDER_GAP == 0`; unresolved provider observations would be a legitimate fail-closed data outcome.

## Result

```text
history shard                    XAU_USD / 2022
complete M1 candles              352,677
M1 retrieval pages               117
raw missing intervals            827
raw missing minutes              172,923
S5 classified intervals          827
S5 NO_PRICE_OBSERVATION gaps     827
S5 NO_PRICE_OBSERVATION minutes  172,923
S5 UNRESOLVED_PROVIDER_GAP gaps  0
S5 unresolved minutes            0
independent refetch              EXACT_PROVIDER_VALUE_MATCH
manifest self-check              PASS
all-gap validation               PASS
```

Therefore every omitted M1 interval in the frozen XAU_USD/2022 shard is supported by finer-granularity OANDA evidence showing zero complete MID/S5 price observations inside the exact raw M1 gap coordinates.

This terminally classifies the XAU_USD/2022 raw omission inventory as `NO_PRICE_OBSERVATION` under `P6B_OANDA_OBSERVATION_POLICY_V2`.

## Evidence handling

Only credential-free reconciliation evidence was retained as the workflow artifact:

```text
artifact name  p6b-s5-all-gap-XAU_USD-2022
artifact id    9210773881
files          XAU_USD_2022_MID_M1.reconciliation-v2.json
               XAU_USD_2022_MID_M1.s5-gap-evidence-v1.json
```

Raw M1 history and the local evidence working directory were deleted after upload.

## Interpretation boundary

This pilot validates the all-gap classification method operationally for the frozen XAU_USD/2022 shard. It does **not** make the whole `XAU_USD` instrument detector-facing `TRUSTED`, because:

```text
XAU_USD 2019 all-gap classification  pending
XAU_USD 2020 all-gap classification  pending
XAU_USD 2021 all-gap classification  pending
trusted H1 derivation                 pending
trusted New-York-midnight D1          pending
P6B_CANONICAL_PRICE_DATASET_V2        pending
```

No result may be extrapolated from XAU_USD/2022 to other years or instruments. Each frozen instrument/year shard must be classified directly.

## Authorized next step

Expand the exact same all-gap S5 method to the complete frozen 16-shard universe using conservative sequential provider access. For each shard, preserve exact coverage accounting and report `UNRESOLVED_PROVIDER_GAP` rather than failing or relaxing the method.

Only instruments with all four years fully classified, zero unresolved intervals, deterministic H1/New-York-D1 derivation and a frozen trusted dataset identity may enter the preregistered detector-only activity gate.

## Authorization state

```text
V0_1_MUTATION_AUTHORIZED               = false
V0_1_OOS_OUTCOME_ACCESS_AUTHORIZED     = false
V0_1_CONFIRM_OUTCOME_ACCESS_AUTHORIZED = false
PARAMETER_OPTIMIZATION_AUTHORIZED      = false
ALL_GAP_PROVIDER_CLASSIFICATION        = true
DETECTOR_ACTIVITY_COUNTS_AUTHORIZED    = false
BACKTEST_AUTHORIZED                    = false
MULTI_MARKET_PNL_OUTCOME_ACCESS        = false
PAPER_TRADING_AUTHORIZED               = false
SHADOW_TRADING_AUTHORIZED              = false
LIVE_TRADING_AUTHORIZED                = false
```
