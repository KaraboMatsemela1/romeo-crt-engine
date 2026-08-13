# Project Status

Updated: 2026-08-13

| Phase | Status | Primary exit condition |
|---|---|---|
| 0 — Engineering foundation | **COMPLETE** | Reproducible dev + CI + logging/storage/experiment contracts |
| 1 — Romeo corpus / reconciliation | **COMPLETE** | Evidence-indexed corpus + reconciled doctrine + explicit evidence debts |
| 2 — Formal CRT spec | **COMPLETE — FROZEN_FOR_VALIDATION** | Deterministic CRT v0.1 with no unresolved active-path predicates |
| 3 — Market data | **COMPLETE** | Provider-backed trusted/reproducible D1/H1 dataset |
| 4 — CRT detector | **COMPLETE** | Frozen fixtures + trusted-data detector integration reproduced causally |
| 5 — Backtester | **READY TO START** | Deterministic cost-aware event-driven simulator |
| 6 — Validation | Not started | Written robustness decision |
| 7 — Paper trading | Not started | Stable realtime semantics |
| 8 — Learning engine | Not started | OOS incremental value |
| 9 — Shadow trading | Not started | Production-like readiness |
| 10 — Controlled live | **NOT AUTHORIZED** | Explicit approval + canary gates |

## Current frozen handoff

```text
Strategy  CRT-C3-D1-H1-M1-BEAR-v0.1
Detector  CRT-DETECTOR-v0.1
Dataset   ee1300f0da50e4debcbbc3b7
```

None of these identifiers is a profitability claim.

Machine-readable detector handoff:

```text
strategy/CRT_V0.1_DETECTOR_FREEZE_MANIFEST.json
```

## Phase 4 completion

Phase 4 is complete for the first frozen CRT route.

Detector route:

```text
trusted canonical dataset
 -> manifest/content verification
 -> canonical D1/H1 adapter
 -> exhaustive rolling C1/C2/C3 instances
 -> frozen evaluate_bearish_c3()
 -> deterministic state/reason/rule evidence
 -> immutable TradePlan when eligible
```

Frozen detector:

```text
CRT-DETECTOR-v0.1
```

### Phase-4 guarantees

- the detector reuses the frozen Phase-2 executable strategy instead of duplicating its predicates;
- only trusted canonical data whose H1/D1 content reproduces the declared manifest digest is accepted;
- provider/venue/symbol and row counts are checked before evaluation;
- every rolling C1/C2/C3 triple is evaluated; parents are not selected retrospectively based on success;
- C3 final D1 high/low/close are excluded from the strategy decision path;
- only completed H1 observations fully inside C3 are passed to the strategy evaluator;
- future-C3 D1 price mutation is regression-tested and cannot change the decision/TradePlan;
- all seven frozen Phase-2 machine fixtures reproduce through the detector entry point;
- every evaluated candidate/rejection carries strategy, detector and dataset identity plus reason, rule trace, evidence IDs and causal-input SHA-256;
- detector runs receive a deterministic `run_sha256`;
- the detector contains no fill/P&L, position-sizing, independent-risk or broker-order authority;
- no Phase-2 strategy parameter was changed.

### Frozen fixture parity

```text
Cases       7
TRADE_PLAN  1
NO_SIGNAL   6
```

Positive fixture geometry remains:

```text
entry   106.0
stop    113.25
target  100.0
```

### Provider-backed detector integration

The exact frozen Phase-3 dataset was reconstructed from current provider bytes and passed through the detector trust boundary.

```text
Detector Smoke run  31667680273
Job                 94345649883
Result              SUCCESS
Receipt SHA          4554c8e30828a4283c9f28ed78b40829ddd1142f5ad382ddcb551034e92b974a
Detector run SHA     26820611750f54736a0caf8755a293f744915e2fd3e241e8247aaef3a723f866
```

Observed detector result:

```text
status            INSUFFICIENT_D1_HISTORY
candidate_count   0
no_signal_count   0
trade_plan_count  0
```

This is expected because `ee1300...` contains only one complete New-York D1. A valid C1/C2/C3 instance requires at least three D1 candles.

`INSUFFICIENT_D1_HISTORY` is an integration-window result, not `NO_SIGNAL`, not a losing trade and not evidence about profitability.

Canonical Phase-4 artifacts:

- `src/romeo_crt_engine/crt/detector.py`
- `tests/strategy/test_crt_detector_phase4.py`
- `scripts/run_crt_detector.py`
- `scripts/reconstruct_frozen_dataset.py`
- `docs/DETECTOR.md`
- `docs/PHASE_4_COMPLETION_REPORT.md`
- `docs/reviews/PHASE_4_GATE_REVIEW.md`
- `docs/checklists/phase-4.md`
- `strategy/CRT_V0.1_DETECTOR_FREEZE_MANIFEST.json`

## Phase 3 trusted-data baseline

Frozen integration dataset:

```text
dataset_version         ee1300f0da50e4debcbbc3b7
manifest_sha256          eaf828ee3acc8adf9e3b931cc6a55d385b0be61b58ae72f01205b3f6034a2141
normalized_sha256        86f6f69176e68655032f3d12910572214de2fa04266c5615146ae03e9f414fc2
market_data_code_sha256  8fbcbb435ce47a405f3500a66935f633136669750cfbe2e014ce1649d4b6140d
dependency_lock_sha256   13653ec2f358aa078fb3a4189299cc8e1f4b71e930cdc3141a8e044de14effa5
```

Route:

```text
Binance Public Data
 -> Binance Spot BTCUSDT
 -> DAILY 1m provider archives
 -> checksum + REST verification
 -> normalized UTC M1
 -> exact elapsed-hour H1
 -> New-York local-midnight D1
 -> immutable manifest/receipt
```

The frozen dataset remains a compact detector-integration fixture. It is not the full historical validation sample.

## Frozen strategy boundary

```text
Strategy                     CRT-C3-D1-H1-M1-BEAR-v0.1
Doctrine                     CRT_SECRETS_2025
Lifecycle                    FROZEN_FOR_VALIDATION
Direction                    BEARISH ONLY
Parent timeframe             D1
Execution timeframe          H1
Source timezone              America/New_York
Setup family                 Candle-3 reaction from C1 CRTH
Entry model                  Model #1 core
Primary target               C1 midpoint / 50%
Unknown required state       NO_SIGNAL
Countertrend                 disabled
SMT substitution             disabled
KOD                          excluded
True MSS                     excluded
Time exits                   excluded
```

Frozen project parameters remain:

```text
P2-PARAM-M1-THICK-050 = body/full_range >= 0.50
P2-PARAM-STOP-1TICK   = structural high + one instrument tick
```

No Phase-4 implementation changed them.

## What completion does NOT mean

The project is still:

- **NOT proven profitable**;
- **NOT paper-ready**;
- **NOT shadow-ready**;
- **NOT live-ready**.

`LIVE_TRADING_AUTHORIZED = false` remains unchanged.

## Phase 5 entry gate

Phase 5 may start only under these constraints:

1. consume frozen detector outputs rather than reimplementing strategy validity inside the simulator;
2. preserve strategy `CRT-C3-D1-H1-M1-BEAR-v0.1` and detector `CRT-DETECTOR-v0.1` while testing the first candidate;
3. build an event-driven clock that never exposes future H1/D1 state before its close;
4. keep `TradePlan` geometry immutable after detector confirmation;
5. separate strategy/detector state from account, risk and simulated execution state;
6. model spread, commission, slippage and tick/quantity constraints explicitly;
7. define deterministic same-bar stop/target sequencing rather than assuming favorable fills;
8. report open positions at finite dataset end as censored/marked according to an explicit research policy rather than inventing a strategy time exit;
9. version every historical dataset used for simulation;
10. create a larger trusted historical dataset before interpreting performance statistics;
11. preserve negative results and execution failures;
12. do not alter the frozen detector merely because early P&L is poor.

## Immediate next actions — Phase 5

1. Define event clock and simulation state contracts.
2. Define order-intent and simulated-fill models around immutable `TradePlan` outputs.
3. Define conservative transaction-cost assumptions for BTCUSDT Spot, acknowledging the current archive lacks historical bid/ask spread.
4. Implement stop/target ordering and gap/slippage policies.
5. Implement account/equity/position bookkeeping with deterministic decimal/tick handling.
6. Add candidate, order, fill, position and result journals with strategy/detector/data provenance.
7. Add no-lookahead regression tests at entry, stop, target and dataset boundaries.
8. Build a larger separately versioned trusted historical BTCUSDT sample for simulation.
9. Run simulator-integrity fixtures before computing strategy-performance metrics.
10. Independently review Phase-5 fill realism and leakage before moving to Phase 6 validation.
