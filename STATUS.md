# Project Status

Updated: 2026-08-13

| Phase | Status | Primary exit condition |
|---|---|---|
| 0 — Engineering foundation | **COMPLETE** | Reproducible dev + CI + logging/storage/experiment contracts |
| 1 — Romeo corpus / reconciliation | **COMPLETE** | Evidence-indexed corpus + reconciled doctrine + explicit evidence debts |
| 2 — Formal CRT spec | **COMPLETE — FROZEN_FOR_VALIDATION** | Deterministic CRT v0.1 with no unresolved active-path predicates |
| 3 — Market data | **COMPLETE** | Provider-backed trusted/reproducible D1/H1 dataset |
| 4 — CRT detector | **COMPLETE** | Frozen fixtures + trusted-data detector integration reproduced causally |
| 5 — Backtester | **COMPLETE** | Deterministic cost-aware event-driven simulator |
| 6 — Validation | **READY TO START** | Written robustness decision from preregistered OOS/walk-forward/stress evidence |
| 7 — Paper trading | Not started | Stable realtime semantics |
| 8 — Learning engine | Not started | OOS incremental value |
| 9 — Shadow trading | Not started | Production-like readiness |
| 10 — Controlled live | **NOT AUTHORIZED** | Explicit approval + canary gates |

## Current frozen validation handoff

```text
Strategy   CRT-C3-D1-H1-M1-BEAR-v0.1
Detector   CRT-DETECTOR-v0.1
Simulator  CRT-BACKTEST-v0.1
```

Machine-readable freezes:

- `strategy/CRT_V0.1_FREEZE_MANIFEST.json`
- `strategy/CRT_V0.1_DETECTOR_FREEZE_MANIFEST.json`
- `strategy/CRT_V0.1_BACKTEST_FREEZE_MANIFEST.json`

None of these identifiers or phase completions is a profitability claim.

## Phase 5 completion

Phase 5 is complete as a deterministic event-driven simulator.

The frozen execution contract includes:

- H1 event order: manage positions already open through the bar, then activate plans confirmed at that bar close;
- immutable detector `TradePlan` geometry;
- entry reference must equal the canonical confirmation close;
- Decimal position sizing rounded down to instrument quantity step;
- explicit fee, half-spread and slippage assumptions;
- conservative same-bar stop/target resolution: `STOP_FIRST_CONSERVATIVE`;
- adverse stop gaps use the worse bar open;
- favorable target-gap price improvement disabled;
- open positions at finite dataset end remain censored rather than receiving an invented time exit;
- simultaneous same-timestamp plans fail closed when the group exceeds available capacity;
- simulator implementation SHA, detector-run SHA, quantity step, config SHA and result state are bound into deterministic run identity.

Execution assumption:

```text
SYNTHETIC_LINEAR_SHORT_RESEARCH_V1
```

The first trusted observation feed is Binance BTCUSDT Spot while the strategy is bearish-only. The simulator's short position is therefore a research abstraction, **not** a claim that the modeled naked short is directly executable on Binance Spot.

Canonical Phase-5 artifacts:

- `src/romeo_crt_engine/backtest/models.py`
- `src/romeo_crt_engine/backtest/engine.py`
- `src/romeo_crt_engine/backtest/__init__.py`
- `tests/unit/test_backtest_phase5.py`
- `scripts/run_backtest.py`
- `docs/BACKTESTER.md`
- `docs/PHASE_5_COMPLETION_REPORT.md`
- `docs/reviews/PHASE_5_GATE_REVIEW.md`
- `strategy/CRT_V0.1_BACKTEST_FREEZE_MANIFEST.json`
- `experiments/phase5/P5_SIMULATION_WINDOW_001.md`
- `experiments/phase5/P5_SIMULATION_WINDOW_001_RESULTS.json`

### Simulator integrity evidence

Final deterministic engineering gate for the frozen simulator source:

```text
simulator source head  dbd29ae17ed067511d4c256398bc088903577691
CI run                 31670117944
CI job                 94352804983
locked install          PASS
Ruff                    PASS
strict MyPy             PASS
pytest                  PASS
```

Provider-backed preregistered replay:

```text
Backtest Smoke run  31670117938
Job                 94352804834
Result              SUCCESS
```

### P5-SIM-001 — preserved zero-activity result

Before observing results, the complete September 2025 BTCUSDT UTC calendar month was preregistered mechanically around the Phase-3 September source dates.

Observed trusted shape:

```text
M1 observations       43,200
H1 observations          720
complete NY D1             29
rolling C1/C2/C3           27
valid TradePlans            0
```

All four preregistered cost scenarios therefore produced:

```text
completed trades       0
realized equity   100000
net P&L                 0
expectancy R     undefined
```

This is **not** evidence of profit or loss. It is an integration result showing that this one-month sample generated no valid frozen-strategy TradePlans. The month was not replaced and the strategy/detector were not loosened after the result.

## What completion does NOT mean

The project is still:

- **NOT proven profitable**;
- **NOT statistically validated**;
- **NOT paper-ready**;
- **NOT shadow-ready**;
- **NOT live-ready**.

`LIVE_TRADING_AUTHORIZED = false` remains unchanged.

## Phase 6 entry gate

Phase 6 may start only under these constraints:

1. preserve `CRT-C3-D1-H1-M1-BEAR-v0.1`, `CRT-DETECTOR-v0.1` and `CRT-BACKTEST-v0.1` as the frozen baseline;
2. preregister development, OOS and confirmatory windows before observing their results;
3. create separately versioned trusted datasets for each declared validation window;
4. keep the final confirmatory test untouched during development and sensitivity work;
5. first establish whether the frozen strategy produces a statistically meaningful trade sample at all;
6. report insufficient trade frequency as a result rather than weakening strategy rules;
7. run predeclared IDEAL/BASE/STRESSED/SEVERE cost scenarios and parameter sensitivity without rewriting the frozen candidate in place;
8. use walk-forward, Monte Carlo and regime/session breakdowns only when sample size makes them meaningful;
9. preserve every experiment and negative result;
10. treat Spot-observation/synthetic-short simulation as research-only until an executable short-capable venue/instrument contract is separately approved;
11. no paper promotion without a written Phase-6 robustness decision;
12. live trading remains prohibited.

## Immediate next actions — Phase 6

1. Write and freeze the validation protocol before retrieving/observing the next historical results.
2. Define mechanically selected development, OOS and untouched confirmatory calendar windows.
3. Define minimum sample-size / insufficient-evidence handling before results.
4. Build trusted versioned datasets for the preregistered windows.
5. Measure frozen-strategy candidate and TradePlan frequency without changing rules.
6. Run cost and parameter-sensitivity matrices only under the preregistered protocol.
7. Add rolling/walk-forward and Monte-Carlo analysis if trade count supports inference.
8. Produce a written `REJECT`, `REVISE_AS_NEW_VERSION`, `INSUFFICIENT_EVIDENCE`, or `PROMOTE_TO_PAPER_CANDIDATE` decision.
9. Keep paper/shadow/live disabled unless their own gates are explicitly passed.
