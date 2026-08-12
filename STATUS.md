# Project Status

Updated: 2026-08-12

| Phase | Status | Primary exit condition |
|---|---|---|
| 0 — Engineering foundation | In progress | Reproducible dev + CI scaffold |
| 1 — Romeo corpus / reconciliation | **COMPLETE** | Evidence-indexed corpus + reconciled doctrine + explicit evidence debts |
| 2 — Formal CRT spec | **READY TO START / NOT FROZEN** | Deterministic CRT v0.1 with no unresolved active-path predicates |
| 3 — Market data | Not started | Trusted versioned dataset |
| 4 — CRT detector | Not started | Reproduce known examples |
| 5 — Backtester | Not started | Deterministic cost-aware simulator |
| 6 — Validation | Not started | Written robustness decision |
| 7 — Paper trading | Not started | Stable realtime semantics |
| 8 — Learning engine | Not started | OOS incremental value |
| 9 — Shadow trading | Not started | Production-like readiness |
| 10 — Controlled live | **NOT AUTHORIZED** | Explicit approval + canary gates |

## Phase 1 completion

Phase 1 research/reconciliation is complete as of 2026-08-12.

Completed:

- public Romeo foundation / CRT Secrets source registry established;
- first-pass evidence reviews completed through CRT Secrets Episode 10;
- Turtle Soup foundation, live tape-reading provenance and later source leads registered;
- glossary, open-question/evidence-debt system and per-video research notes established;
- `RULE_EVIDENCE_MATRIX.md` and `CONTRADICTION_MATRIX.md` created;
- P0 causal contracts created for parent CRT, key level, calendar, Turtle Soup and context direction;
- three closure/source-recovery passes completed;
- unsupported/unproven sources quarantined;
- source-attribution corrections recorded;
- causal fixture framework established;
- first integrated candidate `CRT-C3-ALIGNED-v0.1-DRAFT` written;
- minimal first-candidate doctrine boundary frozen for Phase 2;
- unresolved strategy semantics converted into explicit Phase-2 evidence debts.

Canonical Phase-1 closeout:

- `research/romeo/PHASE_1_COMPLETION_REPORT.md`
- `research/romeo/reconciliation/P0_MINIMAL_DOCTRINE_DECISION.md`

## Strategy status

```text
CRT-C3-ALIGNED-v0.1-DRAFT
```

remains:

- **NOT FROZEN**
- **NON-EXECUTABLE**
- **NOT AUTHORIZED FOR PROFITABILITY BACKTEST CLAIMS**
- **NOT PAPER-READY**
- **NOT LIVE-READY**

Phase 1 completion must not be interpreted as strategy validation.

## Phase 2 entry gate

Phase 2 must convert the evidence baseline into deterministic, testable rules. Before the candidate can move to `FROZEN_FOR_VALIDATION`, the active path must resolve:

1. parent CRT / Candle-1 eligibility and lifecycle;
2. key-level registry, ranking and reached/consumed state;
3. exact calendar policy for the chosen first parent/instrument route;
4. exact context-direction resolver;
5. Turtle Soup confirmation/reference lifecycle;
6. exactly one first entry model — Model #1 or true MSS;
7. target hierarchy and immutable `TargetPlan`;
8. structural stop reference plus execution buffer policy;
9. Candle-3 confirmation, expiry and `NO_SIGNAL` semantics;
10. positive/negative causal fixtures for all executable predicates.

Any required `UNKNOWN` state must fail closed.

## First v0.1 scope boundary

Current scope decision:

```text
Doctrine                    CRT_SECRETS_2025
Setup family                aligned Candle-3 reaction setup
Key-level role              REACTION_FROM_KEY_LEVEL only
Countertrend                disabled
Local Turtle Soup           required initially
SMT substitution            disabled initially
KOD requirement             excluded
Time exits                  excluded until deterministic
Entry model                 choose ONE in Phase 2
Unknown required state      NO_SIGNAL
```

## Immediate next actions — Phase 2

1. Select the first parent/instrument/timeframe route based on evidence completeness.
2. Resolve parent-selection and key-level predicates for that route.
3. Freeze its calendar and direction resolver.
4. Freeze Turtle Soup confirmation/lifecycle.
5. Choose **Model #1 or true MSS** based on determinism/fixture quality, not backtest profit.
6. Define target, structural stop and Candle-3 expiry.
7. Build positive/negative fixtures and unit-test contracts.
8. Run a formal freeze review before any strategy backtest is treated as meaningful.
