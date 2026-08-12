# Project Status

Updated: 2026-08-12

| Phase | Status | Primary exit condition |
|---|---|---|
| 0 — Engineering foundation | In progress | Reproducible dev + CI scaffold |
| 1 — Romeo corpus | **IN PROGRESS** | Evidence-indexed relevant corpus |
| 2 — Formal CRT spec | Not frozen | Deterministic CRT v0.1 candidate |
| 3 — Market data | Not started | Trusted versioned dataset |
| 4 — CRT detector | Not started | Reproduce known examples |
| 5 — Backtester | Not started | Deterministic cost-aware simulator |
| 6 — Validation | Not started | Written robustness decision |
| 7 — Paper trading | Not started | Stable realtime semantics |
| 8 — Learning engine | Not started | OOS incremental value |
| 9 — Shadow trading | Not started | Production-like readiness |
| 10 — Controlled live | Not authorized | Explicit approval + canary gates |

## Phase 1 progress

- Initial public corpus inventory created: 14 foundation / CRT Secrets / CRTology sources.
- Evidence protocol committed in `research/romeo/PHASE_1_RESEARCH_LOG.md`.
- Foundation lecture `ROMEO-2024-CRT` completed through provisional transcript-backed evidence pass.
- `CRT secrets ep.1` completed through provisional transcript-backed evidence pass.
- No candidate rule has been promoted to `VERIFIED` yet.

## Current blocker / uncertainty

The project does not yet have a fully verified, source-traceable Romeo CRT specification. Current indexed transcripts and AI summaries are discovery/evidence aids, but strategy-critical rules still require direct-source confirmation and chart-fixture extraction. Do not guess strategy-critical rules to accelerate implementation.

## Immediate next actions

1. Direct evidence pass: `What is turtle soup?`
2. Direct/evidence pass: CRT Secrets episodes 2–9.
3. Extract chart examples and counterexamples as future test fixtures.
4. Reconcile definitions of Turtle Soup, Model #1, 50% target, key level, SMT, true MSS, timeframe mapping and failure semantics.
5. Only then begin freezing `CRT-v0.1`.
