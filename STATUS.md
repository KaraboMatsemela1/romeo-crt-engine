# Project Status

Updated: 2026-08-14

| Phase | Status | Primary exit condition |
|---|---|---|
| 0 — Engineering foundation | **COMPLETE** | Reproducible dev + CI + logging/storage/experiment contracts |
| 1 — Romeo corpus / reconciliation | **COMPLETE** | Evidence-indexed corpus + explicit evidence debts |
| 2 — Formal CRT spec | **COMPLETE — v0.1 FROZEN** | Deterministic v0.1 order path |
| 3 — Market data | **COMPLETE FOR BINANCE/BTCUSDT v0.1 ROUTE** | Trusted/reproducible D1/H1 dataset |
| 4 — CRT detector | **COMPLETE FOR v0.1** | Frozen deterministic detector |
| 5 — Backtester | **COMPLETE FOR v0.1** | Deterministic cost-aware simulator |
| 6 — Validation | **COMPLETE — INSUFFICIENT_EVIDENCE** | Terminal preregistered DEV decision |
| 6B — Candidate revision | **IN PROGRESS — ALL-GAP DATA CLASSIFICATION** | Trusted multi-market DEV datasets + detector-only activity decision |
| 7 — Paper trading | **BLOCKED** | Requires future validated paper promotion |
| 8 — Learning engine | Not started | Requires sufficient deterministic labels |
| 9 — Shadow trading | Not started | Requires paper readiness |
| 10 — Controlled live | **NOT AUTHORIZED** | Explicit future approval + canary gates |

## Frozen v0.1 result

```text
strategy   CRT-C3-D1-H1-M1-BEAR-v0.1
detector   CRT-DETECTOR-v0.1
simulator  CRT-BACKTEST-v0.1.1
DEV        2019-01-01 .. 2022-12-31
candidates 1,416
TradePlans 4
required   30
decision   INSUFFICIENT_EVIDENCE
```

The Phase-6 v0.1 result is historical evidence and is not overwritten by Phase 6B. v0.1 OOS and CONFIRM remain unopened. Parameter optimization and paper/shadow/live promotion remain unauthorized.

## Active Phase 6B route

```text
candidate_version      CRT-C3-D1-H1-M1-BEAR-v0.2-MULTI-MARKET-RESEARCH
alpha_strategy_version CRT-C3-D1-H1-M1-BEAR-v0.1
detector_version       CRT-DETECTOR-v0.2-MULTI-MARKET
signal_component       MID
alpha changes          NONE AUTHORIZED
```

Frozen OANDA universe:

```text
EUR_USD
XAU_USD
NAS100_USD
SPX500_USD
```

Historical qualification is governed by `P6B-OANDA-HISTORY-QUALIFICATION-V1` and the corrected observation contract `P6B_OANDA_OBSERVATION_POLICY_V2`.

## Historical collection and integrity state

All 16 preregistered instrument/year MID/M1 shards for 2019-2022 have been collected through OANDA practice, independently re-fetched, validated and reduced to credential-free reconciliation evidence. Raw price artifacts remain ephemeral and are deleted after validation.

Sealed inventory:

```text
complete M1 candles       5,529,393
missing intervals           122,626
missing minutes           2,885,967
V2 evidence shards            16/16
independent refetch       PASS 4/4 per instrument
raw price artifacts       EPHEMERAL / DELETED
```

Per instrument:

```text
EUR_USD      1,428,155 complete M1 | 37,770 gaps | 675,685 missing minutes
XAU_USD      1,394,064 complete M1 | 17,967 gaps | 709,776 missing minutes
NAS100_USD   1,392,496 complete M1 | 11,111 gaps | 711,344 missing minutes
SPX500_USD   1,314,678 complete M1 | 55,778 gaps | 789,162 missing minutes
```

Every shard passed its frozen independent provider-value re-fetch. This proves deterministic provider retrieval for the observed values; it does not by itself prove that every omitted M1 observation is an acceptable market closure.

## Gap-classification state

The V2 contract allows only these terminal classifications:

```text
EXPECTED_MARKET_CLOSURE
NO_PRICE_OBSERVATION
```

Any interval that cannot be supported by date-valid market evidence or finer-granularity provider evidence remains:

```text
UNRESOLVED_PROVIDER_GAP
```

and fails closed.

S5 cross-granularity probes have already classified every XAU_USD M1 gap of 60 minutes or less for 2019-2022:

```text
XAU_USD short gaps classified          17,490
XAU_USD short-gap NO_PRICE_OBSERVATION 17,490
XAU_USD short-gap unresolved                0
XAU_USD no-price minutes classified    56,453
XAU_USD longer gaps still in scope        477
XAU_USD longer missing minutes        653,323
```

The short-gap evidence is strong but does **not** make XAU_USD `TRUSTED`: the remaining 477 longer gaps must still receive terminal evidence.

A fail-closed all-gap S5 probe path is now implemented in `scripts/probe_oanda_all_gaps_s5.py`. The first controlled all-gap pilot is XAU_USD/2022. Its validation requires the S5 evidence inventory to cover exactly the raw M1 missing-interval count; detector and P&L authorizations remain false regardless of the pilot result.

## Promotion rule

Before any Phase-6B detector activity count may be opened, each accepted instrument must have:

```text
complete frozen MID/M1 source history
independent provider-value re-fetch PASS
every raw missing interval terminally reconciled
zero unresolved/provider-missing intervals
deterministic trusted H1 derivation
deterministic New-York-midnight D1 derivation
frozen P6B_CANONICAL_PRICE_DATASET_V2 identity
quality_status = TRUSTED
```

At least two instruments must satisfy this gate. Otherwise the preregistered activity protocol terminates as `INSUFFICIENT_ELIGIBLE_UNIVERSE` without opening detector outcomes.

If at least two instruments become trusted, only detector activity counts may be opened under `P6B-MULTI-MARKET-ACTIVITY-PROTOCOL-v1`. P&L and the backtester remain prohibited.

## Current handoff

```text
Phase 6B                         IN PROGRESS — ALL-GAP DATA CLASSIFICATION
Alpha changes                    NONE AUTHORIZED
Frozen OANDA universe            4 SYMBOLS
Yearly raw validation            PASS 16/16
Independent refetch              PASS 4/4 PER INSTRUMENT
V2 reconciliation evidence       PASS 16/16
Exact missing-interval inventory PASS 122,626 INTERVALS
XAU short-gap S5 classification  PASS 17,490 / 17,490; 0 UNRESOLVED
All-gap S5 classification        CONTROLLED PILOT ACTIVE
Trusted H1 / NY-D1 datasets      PENDING
Detector activity counts         NOT OPENED
Multi-market P&L                 NOT AUTHORIZED
v0.1 OOS / CONFIRM               UNOPENED
Phase 7                          BLOCKED
Live trading                     NOT AUTHORIZED
```

Canonical detail:

- `docs/checklists/phase-6b.md`
- `experiments/phase6b/P6B_MULTI_MARKET_ACTIVITY_PROTOCOL_V1.md`
- `experiments/phase6b/P6B_OANDA_HISTORY_QUALIFICATION_PROTOCOL_V1.md`
- `experiments/phase6b/P6B_OANDA_HISTORY_SHARD_EXECUTION_V1.md`
- `experiments/phase6b/P6B_OANDA_HISTORICAL_SESSION_EVIDENCE_001.md`
- `experiments/phase6b/P6B_OANDA_HISTORY_COLLECTION_GATE_001.md`
- `src/romeo_crt_engine/market_data/gap_reconciliation_v2.py`
- `scripts/collect_oanda_history_shard.py`
- `scripts/probe_oanda_all_gaps_s5.py`

## Authorization

```text
V0_1_MUTATION_AUTHORIZED               = false
V0_1_OOS_OUTCOME_ACCESS_AUTHORIZED     = false
V0_1_CONFIRM_OUTCOME_ACCESS_AUTHORIZED = false
PARAMETER_OPTIMIZATION_AUTHORIZED      = false
FULL_RAW_HISTORY_COLLECTION_AUTHORIZED = true
ALL_GAP_PROVIDER_CLASSIFICATION        = true
MULTI_MARKET_ACTIVITY_COUNTS_OPENED    = false
MULTI_MARKET_PNL_OUTCOME_ACCESS        = false
PAPER_TRADING_AUTHORIZED               = false
SHADOW_TRADING_AUTHORIZED              = false
LIVE_TRADING_AUTHORIZED                = false
```
