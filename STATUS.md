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
| 6B — Candidate revision | **IN PROGRESS — TRUSTED DATASET CONSTRUCTION** | Trusted multi-market DEV datasets + detector-only activity decision |
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

Historical qualification is governed by `P6B-OANDA-HISTORY-QUALIFICATION-V1` and observation contract `P6B_OANDA_OBSERVATION_POLICY_V2`.

## Historical collection and raw-gap qualification

All 16 preregistered instrument/year MID/M1 shards for 2019-2022 were collected through OANDA practice, independently re-fetched, validated, and reduced to credential-free reconciliation evidence. Raw price artifacts are ephemeral and deleted after validation.

Sealed raw inventory:

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

OANDA Provider Qualification run #27 (`31778696775`) completed successfully on attempt #2 at evidence commit `b04899e03931eda642af12e39926a84c310482f6`.

Universe-wide all-gap S5 result:

```text
all-gap evidence shards             16 / 16 PASS
raw missing intervals               122,626
S5 classified intervals             122,626
NO_PRICE_OBSERVATION intervals      122,626
UNRESOLVED_PROVIDER_GAP intervals         0
raw missing minutes               2,885,967
NO_PRICE_OBSERVATION minutes      2,885,967
UNRESOLVED_PROVIDER_GAP minutes           0
raw-gap-qualified instruments          4 / 4
```

Per instrument qualification:

```text
EUR_USD      37,770 / 37,770 gaps | 675,685 / 675,685 minutes | unresolved 0
XAU_USD      17,967 / 17,967 gaps | 709,776 / 709,776 minutes | unresolved 0
NAS100_USD   11,111 / 11,111 gaps | 711,344 / 711,344 minutes | unresolved 0
SPX500_USD   55,778 / 55,778 gaps | 789,162 / 789,162 minutes | unresolved 0
```

The XAU_USD/2019 first execution was interrupted technically; the failed job alone was rerun on the same frozen workflow/evidence commit and passed without evidence-policy or strategy changes.

Canonical universe result: `experiments/phase6b/P6B_ALL_GAP_S5_UNIVERSE_001.md`.

A fail-closed evidence-to-policy adapter is implemented in `src/romeo_crt_engine/market_data/s5_gap_policy_v2.py`. Partial, unresolved, coordinate-mismatched, or digest-unbound S5 evidence cannot enter aggregation as approved omission policy.

## Current trusted-data gate

`RAW_GAP_QUALIFIED` is a prerequisite, not detector-facing `TRUSTED` status.

Before any Phase-6B detector activity count may be opened, each accepted instrument must have:

```text
complete frozen MID/M1 source history
independent provider-value re-fetch PASS
all raw gaps bound to approved evidence
zero unresolved/provider-missing intervals
deterministic H1 derivation
deterministic New-York-midnight D1 derivation
frozen provider/instrument/session/price-quantum identities
frozen normalized H1/D1 digest
frozen P6B_CANONICAL_PRICE_DATASET_V2 identity
quality_status = TRUSTED
```

All four raw-gap-qualified instruments may proceed to this construction gate. No instrument is called `TRUSTED` until the canonical identity is actually built and verified.

After the exact trusted set is frozen, at least two trusted instruments are required to open the detector-only activity protocol. If fewer than two become trusted, Phase 6B terminates as `INSUFFICIENT_ELIGIBLE_UNIVERSE` without detector outcome access.

If at least two instruments are trusted, the only next outcome surface is `P6B-MULTI-MARKET-ACTIVITY-PROTOCOL-v1`:

```text
accepted instruments      >= 2
contributing instruments  >= 2
pooled TradePlans         >= 30
backtester                PROHIBITED
P&L                       PROHIBITED
```

## Current handoff

```text
Phase 6B                         IN PROGRESS — TRUSTED DATASET CONSTRUCTION
Alpha changes                    NONE AUTHORIZED
Frozen OANDA universe            4 SYMBOLS
Yearly raw validation            PASS 16/16
Independent refetch              PASS 4/4 PER INSTRUMENT
V2 reconciliation evidence       PASS 16/16
Exact missing-interval inventory PASS 122,626 INTERVALS
Universe all-gap classification  PASS 16/16; 122,626 / 122,626; 0 UNRESOLVED
Missing-minute reconciliation    PASS 2,885,967 / 2,885,967; 0 UNRESOLVED
Raw-gap-qualified instruments    PASS 4/4
Trusted H1 / NY-D1 datasets      PENDING / NEXT
Canonical TRUSTED identities     PENDING
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
- `experiments/phase6b/P6B_RECONCILIATION_STATUS_001.md`
- `experiments/phase6b/P6B_ALL_GAP_S5_PILOT_001.md`
- `experiments/phase6b/P6B_ALL_GAP_S5_UNIVERSE_001.md`
- `src/romeo_crt_engine/market_data/gap_reconciliation_v2.py`
- `src/romeo_crt_engine/market_data/s5_gap_policy_v2.py`
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
DETECTOR_ACTIVITY_COUNTS_AUTHORIZED    = false
BACKTEST_AUTHORIZED                    = false
MULTI_MARKET_PNL_OUTCOME_ACCESS        = false
PAPER_TRADING_AUTHORIZED               = false
SHADOW_TRADING_AUTHORIZED              = false
LIVE_TRADING_AUTHORIZED                = false
```
