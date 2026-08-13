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
| 6B — Candidate revision | **IN PROGRESS — HERMES LOCAL RAW COLLECTION QUEUED** | Trusted multi-market DEV datasets + detector-only activity decision |
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

The collector is restricted to the frozen four symbols and years 2019-2022, reads credentials only from the local runtime environment, preserves page-level request/raw-response provenance, enumerates raw gaps as `UNRECONCILED`, runs the mapped preregistered independent re-fetch, self-checks manifest redaction/authorization state, and keeps detector/TradePlan/P&L/paper/shadow/live authorization false.

Local raw outputs are Git-ignored at:

```text
artifacts/phase6b/oanda_raw/
```

## Persistent Hermes control plane

GitHub is now the persistent control channel for the local Hermes executor:

```text
control file      ops/hermes/CONTROL.json
control branch    agent/phase-6b-candidate-revision
poll interval     300 seconds
auto execute      READY tasks
result channel    GitHub Issue #14 / [HERMES_RESULT]
local state       ~/.hermes/state/romeo-crt-engine-control.json
```

Queued tasks:

```text
P6B-001  READY  EUR_USD / 2019 first full shard
P6B-002  READY  remaining 15 frozen shards; depends on P6B-001 PASS
```

Once Hermes is bootstrapped with the persistent watcher, the user does not need to manually tell Hermes to check GitHub for each task. Hermes must stop the chain on failure and may never relax strategy/data gates or expose local secrets/raw OANDA M1 files.

After all 16 shards are collected, historical gap reconciliation, trusted H1/New-York-D1 dataset identities, and detector activity counts remain separate gated work.

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
- `ops/hermes/CONTROL.json`
- `ops/hermes/tasks/P6B-001.yaml`
- `ops/hermes/tasks/P6B-002.yaml`

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
