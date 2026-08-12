# Project Status

Updated: 2026-08-12

| Phase | Status | Primary exit condition |
|---|---|---|
| 0 — Engineering foundation | **COMPLETE** | Reproducible dev + CI + logging/storage/experiment contracts |
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

## Pre-Phase-3 gate review

A full repository review was performed after Phase 2 and before Phase 3.

The review checked:

- Project Bible / roadmap / status consistency;
- frozen strategy specification and freeze manifest;
- deterministic implementation and fixtures;
- strategy-vs-code calendar semantics;
- open evidence debt and excluded doctrine;
- CI, lint and strict typing;
- Phase-0 foundation completeness;
- logging/storage/experiment provenance contracts;
- paper/live safety state.

Findings corrected before Phase 3:

1. **C3 calendar bug:** the implementation previously accepted any D1 `CandleWindow` with midnight endpoints, including a malformed multi-day window. It now requires exactly the next New-York local date, matching the already-frozen strategy specification.
2. **Phase-0 logging contract:** added provider-neutral structured event logging.
3. **Phase-0 storage contract:** added immutable artifact and dataset integrity/version references plus a provider-neutral store protocol.
4. **Experiment convention:** added versioned experiment provenance rules.
5. **Stale docs/checklists:** README and Phase 0/1/2 checklists were brought in line with canonical status.

The C3 fix is a semantic-preserving implementation correction to match the frozen spec; it does not alter the v0.1 trading rule.

## Phase 0 completion

Phase 0 is now complete.

Foundation includes:

- Python 3.12+ package metadata and reproducible dependency declaration;
- CI with Ruff, strict MyPy and pytest;
- safe `.env.example` and secret/data ignore conventions;
- provider-neutral structured logging contract;
- provider-neutral storage/integrity contracts;
- documentation, ADRs and AI-agent operating contract;
- experiment provenance/versioning convention;
- project check script and tests.

Market-data provider selection, database schema and concrete storage adapters remain Phase-3 decisions behind these interfaces.

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
- DST, parent-enumeration, C3-window and future-confirmation causality tests;
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

## Phase 3 entry gate

Phase 3 may start only with the following constraints:

1. do not change frozen v0.1 strategy semantics while building data infrastructure;
2. raw provider observations must be retained immutably or content-addressed wherever practical;
3. every normalized dataset must have a versioned manifest and integrity digest;
4. provider symbol, venue, timezone, price precision and tick-size metadata must be explicit;
5. internal observation timestamps use UTC while analytical D1/H1 boundaries preserve `America/New_York` wall clock;
6. DST transition behavior must be tested;
7. duplicate, out-of-order, impossible-OHLC and missing/stale observations must be detected and classified;
8. no provider-native D1 bar may be assumed canonical without equivalence verification;
9. data corrections must create a new dataset version rather than silently rewriting a frozen validation dataset;
10. the frozen strategy consumes only trusted normalized data after these gates pass.

## Immediate next actions — Phase 3

1. Select and document the first provider/instrument/venue route.
2. Define raw observation and instrument metadata schemas.
3. Implement immutable/content-addressed raw storage behind the Phase-0 storage contract.
4. Implement normalized UTC observations and New-York D1/H1 candle construction.
5. Add DST, gap, duplicate, ordering and OHLC validation.
6. Build dataset manifest hashing/versioning.
7. Prove provider-native/canonical boundary equivalence or always construct canonical bars ourselves.
8. Freeze the first trusted dataset version before Phase-4 detector evaluation.
