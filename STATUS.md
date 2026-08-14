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
| 6 — Validation | **COMPLETE — INSUFFICIENT_EVIDENCE** | Terminal preregistered v0.1 DEV decision |
| 6B — Candidate revision | **COMPLETE — INSUFFICIENT_MULTI_MARKET_SAMPLE** | Terminal preregistered multi-market activity decision |
| 6C — Doctrine research | **BLOCKED — NO VERIFIED FIRST-PARTY PREDICATE CLOSURE** | Resume only when direct first-party evidence closes a deterministic held predicate |
| 6D — Research infrastructure | **COMPLETE — RESEARCH INFRASTRUCTURE V1** | Provenance-bound acquisition + predicate/fixture/corpus gates merged green |
| 7 — Paper trading | **BLOCKED** | Requires a future candidate that passes full validation |
| 8 — Learning engine | Not started | Requires sufficient deterministic labels |
| 9 — Shadow trading | Not started | Requires paper readiness |
| 10 — Controlled live | **NOT AUTHORIZED** | Explicit future approval + canary gates |

## Frozen historical validation results

```text
Phase 6 v0.1
strategy      CRT-C3-D1-H1-M1-BEAR-v0.1
candidates    1,416
TradePlans    4 / required 30
decision      INSUFFICIENT_EVIDENCE

Phase 6B
candidate     CRT-C3-D1-H1-M1-BEAR-v0.2-MULTI-MARKET-RESEARCH
alpha         CRT-C3-D1-H1-M1-BEAR-v0.1
detector      CRT-DETECTOR-v0.2-MULTI-MARKET
signal        MID
decision      INSUFFICIENT_MULTI_MARKET_SAMPLE

Phase 6C
candidate_ready_rows        0
verified predicate closures 0
decision                    BLOCKED_NO_VERIFIED_PREDICATE_CLOSURE
```

The v0.1 OOS and CONFIRM windows remain unopened. Historical Phase-6/6B/6C evidence may not be rewritten or repaired in place.

## Phase 6D — First-Party Research Infrastructure V1

Phase 6D addresses the source-acquisition and deterministic-evidence bottleneck discovered in Phase 6C. It is research infrastructure, not a new alpha-candidate phase.

Completed V1 contracts:

```text
registry-bound source capture            COMPLETE
SHA-256 artifact provenance              COMPLETE
canonical acquisition manifests          COMPLETE
strict source-registry schema/row width  COMPLETE
predicate evidence ledger                COMPLETE
causal closure field enforcement         COMPLETE
doctrine delta validation                COMPLETE
positive + negative fixture gate         COMPLETE
deterministic corpus index               COMPLETE
research readiness audit                 COMPLETE
CI                                       RUFF + MYPY + 133 PYTEST PASS
candidate/detector/outcome authorization FALSE
```

Current machine-readable predicate debts:

```text
SS_MEANING_AND_CAUSAL_RULE
SMT_EXECUTABLE_SEMANTICS
MODEL_1_GEOMETRY
TRUE_MSS_ALGORITHM
TURTLE_SOUP_CONFIRMATION
KEY_LEVEL_SELECTOR
TIME_SELECTOR
DYNAMIC_BIAS_TRANSITION
```

All remain unresolved at V1 completion. Partial doctrine from Phase 6C is preserved as research evidence but is not promoted into executable predicate fields without direct artifact-level support.

Canonical Phase 6D records:

- `research/romeo/phase6d/PHASE_6D_RESEARCH_INFRA_CHARTER.md`
- `research/romeo/phase6d/PREDICATE_LEDGER_V1.json`
- `docs/checklists/phase-6d.md`
- `src/romeo_crt_engine/research/source_acquisition_v1.py`
- `src/romeo_crt_engine/research/registry_v1.py`
- `src/romeo_crt_engine/research/predicate_ledger_v1.py`
- `src/romeo_crt_engine/research/doctrine_diff_v1.py`
- `src/romeo_crt_engine/research/fixture_gate_v1.py`
- `src/romeo_crt_engine/research/corpus_index_v1.py`
- `scripts/build_first_party_capture_manifest.py`
- `scripts/audit_phase6d_research_readiness.py`

## Phase 6C re-entry condition

Phase 6C remains blocked until at least one of these becomes directly available:

1. a verified new first-party CRTology episode with technical content;
2. direct captions/transcript/technical frames for Episode 1, Episode 6, Episode 9, or the original Turtle Soup source;
3. a first-party Romeo text/chart post that explicitly closes one held predicate including causal timing/ownership/confirmation semantics.

When such evidence appears, Phase 6D tooling must ingest and hash the source, update the predicate ledger, and require positive/negative causal fixtures before any separate candidate precommitment is considered.

## Authorization

```text
V0_1_MUTATION_AUTHORIZED                    = false
V0_1_OOS_OUTCOME_ACCESS_AUTHORIZED          = false
V0_1_CONFIRM_OUTCOME_ACCESS_AUTHORIZED      = false
PARAMETER_OPTIMIZATION_AUTHORIZED           = false
LOWER_PHASE6B_ACTIVITY_THRESHOLD            = false
PHASE6C_NEW_ALPHA_CANDIDATE_SELECTED         = false
PHASE6C_ALPHA_IMPLEMENTATION_AUTHORIZED      = false
PHASE6C_DETECTOR_ACTIVITY_AUTHORIZED         = false
PHASE6D_RESEARCH_INFRA_ONLY                  = true
PERFORMANCE_PROTOCOL_AUTHORIZED              = false
BACKTEST_AUTHORIZED                          = false
MULTI_MARKET_PNL_OUTCOME_ACCESS              = false
PAPER_TRADING_AUTHORIZED                     = false
SHADOW_TRADING_AUTHORIZED                    = false
LIVE_TRADING_AUTHORIZED                      = false
```
