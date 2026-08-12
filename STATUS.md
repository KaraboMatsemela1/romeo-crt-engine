# Project Status

Updated: 2026-08-12

| Phase | Status | Primary exit condition |
|---|---|---|
| 0 — Engineering foundation | In progress | Reproducible dev + CI scaffold |
| 1 — Romeo corpus / reconciliation | **COMPLETE** | Evidence-indexed corpus + reconciled doctrine + explicit evidence debts |
| 2 — Formal CRT spec | **COMPLETE — FROZEN_FOR_VALIDATION** | Deterministic CRT v0.1 with no unresolved active-path predicates |
| 3 — Market data | **READY TO START** | Trusted versioned D1/H1 dataset for the frozen route |
| 4 — CRT detector | Not started | Reproduce frozen fixtures and known examples |
| 5 — Backtester | Not started | Deterministic cost-aware simulator |
| 6 — Validation | Not started | Written robustness decision |
| 7 — Paper trading | Not started | Stable realtime semantics |
| 8 — Learning engine | Not started | OOS incremental value |
| 9 — Shadow trading | Not started | Production-like readiness |
| 10 — Controlled live | **NOT AUTHORIZED** | Explicit approval + canary gates |

## Phase 2 completion

Phase 2 formal strategy specification is complete as of 2026-08-12.

Frozen candidate:

```text
CRT-C3-D1-H1-M1-BEAR-v0.1
```

Lifecycle:

```text
FROZEN_FOR_VALIDATION
```

Phase 2 delivered:

- a deterministic bearish-only D1 → H1 strategy route;
- canonical New-York Daily candle semantics;
- exhaustive rolling D1 parent-candidate generation to eliminate hindsight Candle-1 selection;
- a fixed reaction key level at C1 `CRTH`;
- a conservative bearish Candle-2 sweep + close-reclaim subtype;
- Candle-3 eligibility and expiry semantics;
- Model #1 selected as the sole v0.1 entry family;
- explicit versioned formalization of the qualitative `thick` candle term;
- deterministic Model-1 confirmation/invalidation;
- immutable primary target at C1 midpoint / 50%;
- structural stop reference at Model-1 high plus versioned execution buffer;
- fail-closed reason codes;
- immutable `TradePlan` output before independent risk approval;
- machine-readable positive/negative fixtures;
- DST, parent-enumeration and future-confirmation causality tests;
- an adversarial freeze review;
- a machine-readable freeze manifest;
- all unresolved broader-doctrine questions reclassified as deferred/versioned rather than hidden active defaults.

Canonical Phase-2 artifacts:

- `strategy/CRT_V0.1_SPEC.md`
- `strategy/CRT_V0.1_FREEZE_MANIFEST.json`
- `src/romeo_crt_engine/crt/v0_1.py`
- `tests/strategy/fixtures/crt_v0_1_cases.json`
- `strategy/reviews/CRT_V0.1_FREEZE_REVIEW.md`
- `docs/adr/ADR-004-freeze-narrow-d1-h1-model1-subset.md`
- `research/romeo/OPEN_QUESTIONS.md`

## Frozen v0.1 boundary

```text
Doctrine                    CRT_SECRETS_2025
Direction                   BEARISH ONLY
Parent timeframe            D1
Execution timeframe         H1
Source timezone             America/New_York
Setup family                Candle-3 reaction from C1 CRTH
Countertrend                disabled
SMT substitution            disabled
KOD                         excluded
True MSS                    excluded
Time exits                  excluded
Entry model                 Model #1 core
Primary target              C1 midpoint / 50%
Unknown required state      NO_SIGNAL
```

Two explicit project parameters are frozen before profitability testing:

```text
P2-PARAM-M1-THICK-050 = body/full_range >= 0.50
P2-PARAM-STOP-1TICK   = structural high + one instrument tick
```

They are **project formalizations**, not represented as Romeo numerical claims. Later validation must sensitivity-test them without rewriting this candidate in place.

## What Phase 2 completion does NOT mean

The frozen candidate is:

- **NOT proven profitable**;
- **NOT yet evaluated on a trusted historical dataset**;
- **NOT paper-ready**;
- **NOT shadow-ready**;
- **NOT live-ready**.

No backtest result was used to choose the frozen v0.1 rules or parameters.

`LIVE_TRADING_AUTHORIZED = false` remains unchanged.

## Immediate next actions — Phase 3 / Phase 4 preparation

1. Build the trusted raw/normalized market-data pipeline for the frozen D1/H1 route.
2. Freeze instrument/symbol/venue metadata before historical evaluation.
3. Build New-York D1 and H1 candle construction with DST/data-quality checks.
4. Version the resulting dataset.
5. Implement/reuse the frozen detector against real historical observations.
6. Reproduce machine fixtures and source-derived examples without LLM judgement.
7. Only after data + detector integrity gates pass begin meaningful historical simulation/validation work.
