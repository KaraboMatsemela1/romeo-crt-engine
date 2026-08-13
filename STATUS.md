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
| 6B — Candidate revision | **IN PROGRESS — OANDA UNIVERSE FROZEN / HISTORICAL DATA QUALIFICATION NEXT** | Trusted multi-market DEV datasets + detector-only activity decision |
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

v0.1 OOS (`2023-01-01 .. 2025-08-31`) and CONFIRM (`2025-10-01 .. 2026-07-31`) remain unopened. Parameter optimization and paper/shadow/live promotion remain unauthorized.

## Phase 6B research history

### Bullish successor

```text
candidate CRT-C3-D1-H1-M1-BULL-v0.2-RESEARCH
decision  EVIDENCE_INSUFFICIENT
outcomes  NOT OPENED
```

The bullish path was preserved without symmetry inference or historical outcome access.

### Active successor

```text
candidate_version      CRT-C3-D1-H1-M1-BEAR-v0.2-MULTI-MARKET-RESEARCH
alpha_strategy_version CRT-C3-D1-H1-M1-BEAR-v0.1
detector_version       CRT-DETECTOR-v0.2-MULTI-MARKET
signal_component       MID
alpha changes          NONE AUTHORIZED
```

The active question is whether the unchanged frozen bearish alpha produces enough deterministic opportunities across an ex-ante Romeo-relevant market universe to justify a later performance protocol.

## Runtime OANDA qualification

### Qualification 001 — preserved failed account route

```text
P6B_OANDA_RUNTIME_QUALIFICATION_001 = ACCOUNT_NOT_V20_ELIGIBLE_FOR_REQUIRED_ENDPOINTS
```

The first configured account was recognized by a valid practice token but returned HTTP 403 on required v20 account/instrument surfaces. No instrument universe or detector outcomes were opened.

Canonical record:

- `experiments/phase6b/P6B_OANDA_RUNTIME_QUALIFICATION_001.md`

### Qualification 002 — successful practice account

GitHub Actions run `31696424928`, attempt `2`, job `94438165028` completed successfully after the runtime account secret was changed.

```text
authorized practice accounts by token  5
configured account authorized           yes
account summary available               yes
account home currency                   USD
available instruments                   123
precommitted source-family matches      4 / 4
qualification artifact safe             true
```

Provider response identities:

```text
available instrument names SHA-256  2e77a962f559c51d37120ebe842ba62cd0c42e07f50fe845ced04df7ad0755d2
raw instrument response SHA-256     e9ea9a83b2b0f66605f79a94e9c5ca6f21549dd1f1cbbe739077165fe604ea64
raw account summary SHA-256         63cd8a2960941c199239250a12bd5954e7533113a9dfb8c9379236b4c42c9a22
```

Canonical records:

- `experiments/phase6b/P6B_OANDA_RUNTIME_QUALIFICATION_002.json`
- `experiments/phase6b/P6B_OANDA_RUNTIME_QUALIFICATION_002.md`

## Frozen Phase-6B OANDA universe

All four precommitted aliases matched, so all four are frozen. No post-discovery filtering is allowed for this candidate.

| Source family | OANDA symbol | Type |
|---|---|---|
| EUR/USD | `EUR_USD` | CURRENCY |
| Gold/USD | `XAU_USD` | METAL |
| US NAS 100 / NQ proxy | `NAS100_USD` | CFD |
| US SPX 500 / ES proxy | `SPX500_USD` | CFD |

Canonical freeze:

- `experiments/phase6b/P6B_OANDA_UNIVERSE_FREEZE_001.md`

This clears the `>=2 accepted instruments` universe gate but does **not** open detector activity counts.

## Provider/data engineering already complete

Implemented and regression-covered before outcome access:

- OANDA v20 provider adapter and redacted account/instrument discovery;
- provider-neutral `P6B_CANONICAL_PRICE_DATASET_V2`;
- M1 MID/BID/ASK parsing with MID frozen as the signal component;
- no fabricated volume/trade-count semantics (`PRICE_COUNT` only);
- paged M1 retrieval provenance with request/response SHA-256;
- duplicate/out-of-order/conflicting-page rejection;
- fail-closed gap taxonomy;
- project-owned H1 and New-York-midnight D1 reconstruction;
- exact v0.1 detector fixture parity under `CRT-DETECTOR-v0.2-MULTI-MARKET`;
- frozen detector-only 2/2/30 activity protocol;
- preserved BTCUSDT backtest regression boundary.

## Price quantum — frozen pre-activity

OANDA provider price quantum is defined from the provider price-precision contract and is explicitly **not** claimed to be an exchange tick or pip.

| Symbol | displayPrecision | Frozen provider price quantum |
|---|---:|---:|
| `EUR_USD` | 5 | `0.00001` |
| `XAU_USD` | 3 | `0.001` |
| `NAS100_USD` | 1 | `0.1` |
| `SPX500_USD` | 1 | `0.1` |

Canonical decision:

- `docs/adr/ADR-010-oanda-provider-price-quantum.md`

Code/test support:

- `src/romeo_crt_engine/market_data/oanda_price_quantum.py`
- `tests/unit/test_oanda_price_quantum_phase6b.py`

## Detector-only activity protocol

Frozen before any multi-market detector count:

```text
protocol                         P6B-MULTI-MARKET-ACTIVITY-PROTOCOL-v1
DEV activity period              2019-01-01 .. 2022-12-31 New York
minimum accepted instruments     2
minimum contributing instruments 2
minimum pooled TradePlans        30
backtester                       PROHIBITED
P&L outcome access               PROHIBITED
```

The exact four-symbol universe now satisfies only the first threshold. No counts have been opened.

## Current data-quality gate

Next work is historical-data qualification for the four frozen symbols:

1. freeze/document regular provider availability windows and historical holiday/early-close evidence;
2. retrieve bounded/sealed MID M1 data for `2019-01-01 .. 2022-12-31`;
3. independently re-fetch selected sealed samples and compare values;
4. classify every unexpected missing interval fail-closed;
5. build deterministic H1 and New-York-midnight D1 without synthetic prices;
6. freeze one trusted v2 dataset identity per instrument;
7. only then open detector counts and apply the frozen 2/2/30 activity gate.

The repository connector did not permit executable session-timetable writes during this turn, so session/holiday implementation remains explicitly unresolved rather than silently inferred.

## Authorization

```text
V0_1_MUTATION_AUTHORIZED               = false
V0_1_OOS_OUTCOME_ACCESS_AUTHORIZED     = false
V0_1_CONFIRM_OUTCOME_ACCESS_AUTHORIZED = false
PARAMETER_OPTIMIZATION_AUTHORIZED      = false
MULTI_MARKET_ACTIVITY_COUNTS_OPENED    = false
MULTI_MARKET_PNL_OUTCOME_ACCESS        = false
PAPER_TRADING_AUTHORIZED               = false
SHADOW_TRADING_AUTHORIZED              = false
LIVE_TRADING_AUTHORIZED                = false
```
