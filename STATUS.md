# Project Status

Updated: 2026-08-13

| Phase | Status | Primary exit condition |
|---|---|---|
| 0 — Engineering foundation | **COMPLETE** | Reproducible dev + CI + logging/storage/experiment contracts |
| 1 — Romeo corpus / reconciliation | **COMPLETE** | Evidence-indexed corpus + explicit evidence debts |
| 2 — Formal CRT spec | **COMPLETE — v0.1 FROZEN** | Deterministic v0.1 order path |
| 3 — Market data | **COMPLETE FOR BINANCE/BTCUSDT v0.1 ROUTE** | Trusted/reproducible D1/H1 dataset |
| 4 — CRT detector | **COMPLETE FOR v0.1** | Frozen deterministic detector |
| 5 — Backtester | **COMPLETE FOR v0.1** | Deterministic cost-aware simulator |
| 6 — Validation | **COMPLETE — INSUFFICIENT_EVIDENCE** | Terminal preregistered DEV decision |
| 6B — Candidate revision | **IN PROGRESS — LOCAL RAW OANDA COLLECTION READY** | Trusted multi-market DEV datasets + detector-only activity decision |
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

v0.1 OOS and CONFIRM remain unopened. Parameter optimization and paper/shadow/live promotion remain unauthorized.

## Active Phase 6B route

```text
candidate_version      CRT-C3-D1-H1-M1-BEAR-v0.2-MULTI-MARKET-RESEARCH
alpha_strategy_version CRT-C3-D1-H1-M1-BEAR-v0.1
detector_version       CRT-DETECTOR-v0.2-MULTI-MARKET
signal_component       MID
alpha changes          NONE AUTHORIZED
```

The exact frozen OANDA universe is `EUR_USD`, `XAU_USD`, `NAS100_USD`, and `SPX500_USD`.

Historical qualification is governed by `P6B-OANDA-HISTORY-QUALIFICATION-V1`. The fixed 2019 MID/M1 smoke passed for all four symbols with 60/60 complete candles each.

Complete collection is precommitted as four UTC calendar-year shards per frozen instrument (`16` total execution units). Exact raw-gap reconciliation is implemented and regression-tested: approved closure evidence must cover raw missing intervals exactly, may not leave unexplained minutes, and may not extend into provider-observed minutes.

## Local collection path

The repository contains a practice-only local collector and runbook:

- `scripts/collect_oanda_history_shard.py`
- `experiments/phase6b/P6B_OANDA_LOCAL_COLLECTION_RUNBOOK_V1.md`

The collector is restricted to the frozen four symbols and years 2019-2022, reads credentials only from the local runtime environment, preserves page-level request/raw-response provenance, enumerates raw gaps as `UNRECONCILED`, runs the mapped preregistered independent re-fetch, and keeps detector/TradePlan/P&L/paper/shadow/live authorization false.

Local raw outputs are Git-ignored at:

```text
artifacts/phase6b/oanda_raw/
```

The next required execution is the first full shard:

```text
EUR_USD / 2019
```

It is pending on the local/Hermes runtime where OANDA runtime credentials are available. After its manifest/redaction structure is validated, the same frozen collector is used for the remaining 15 shards.

Complete raw DEV collection, historical gap reconciliation, trusted H1/New-York-D1 dataset identities, and detector activity counts remain pending.

Canonical detail:

- `docs/checklists/phase-6b.md`
- `experiments/phase6b/P6B_OANDA_HISTORY_QUALIFICATION_PROTOCOL_V1.md`
- `experiments/phase6b/P6B_OANDA_HISTORY_SHARD_EXECUTION_V1.md`
- `experiments/phase6b/P6B_OANDA_LOCAL_COLLECTION_RUNBOOK_V1.md`
- `experiments/phase6b/P6B_OANDA_HISTORICAL_SESSION_EVIDENCE_001.md`
- `experiments/phase6b/P6B_OANDA_HISTORY_SMOKE_001.md`
- `experiments/phase6b/P6B_OANDA_HISTORY_COLLECTION_GATE_001.md`
- `research/romeo/phase6b/PRIMARY_SOURCE_PASS_003.md`
- `src/romeo_crt_engine/market_data/gap_reconciliation_v2.py`
- `scripts/collect_oanda_history_shard.py`

## Authorization

```text
V0_1_MUTATION_AUTHORIZED               = false
V0_1_OOS_OUTCOME_ACCESS_AUTHORIZED     = false
V0_1_CONFIRM_OUTCOME_ACCESS_AUTHORIZED = false
PARAMETER_OPTIMIZATION_AUTHORIZED      = false
FULL_RAW_HISTORY_COLLECTION_AUTHORIZED = true
MULTI_MARKET_ACTIVITY_COUNTS_OPENED    = false
MULTI_MARKET_PNL_OUTCOME_ACCESS        = false
PAPER_TRADING_AUTHORIZED               = false
SHADOW_TRADING_AUTHORIZED              = false
LIVE_TRADING_AUTHORIZED                = false
```
