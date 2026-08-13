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
| 6 — Validation | **COMPLETE — INSUFFICIENT_EVIDENCE** | Preregistered DEV gate reached a terminal written decision |
| 6B — Candidate revision | **IN PROGRESS — EVIDENCE GATE OPEN** | One independently motivated successor reaches deterministic spec eligibility |
| 7 — Paper trading | **BLOCKED FOR v0.1** | No paper promotion from insufficient validation evidence |
| 8 — Learning engine | Not started | Requires a sufficiently evidenced deterministic baseline |
| 9 — Shadow trading | Not started | Requires paper/production-like readiness |
| 10 — Controlled live | **NOT AUTHORIZED** | Explicit approval + canary gates |

## Current validation disposition

```text
Strategy    CRT-C3-D1-H1-M1-BEAR-v0.1
Detector    CRT-DETECTOR-v0.1
Simulator   CRT-BACKTEST-v0.1.1
Phase 6     COMPLETE
Disposition INSUFFICIENT_EVIDENCE
Paper       NOT AUTHORIZED
Shadow      NOT AUTHORIZED
Live        NOT AUTHORIZED
```

`CRT-BACKTEST-v0.1.1` is a Phase-6 data-gap compatibility patch to the v0.1 simulator. It permits ordered/non-overlapping H1 input across explicitly governed market-data gaps and does not change entry, stop, target, sizing, friction, or same-bar execution semantics.

The next legitimate project track is **new evidence-backed candidate research/revision**, not Phase 7.

## Phase 6B — candidate revision

Phase 6B is now **IN PROGRESS** on a separately versioned research track.

The precommitted successor research target is:

```text
CRT-C3-D1-H1-M1-BULL-v0.2-RESEARCH
```

Selection rationale is recorded in:

- `research/romeo/phase6b/PHASE_6B_CANDIDATE_SELECTION.md`
- `research/romeo/phase6b/BULLISH_MODEL1_EVIDENCE_GATE.md`
- `research/romeo/phase6b/PRIMARY_SOURCE_PASS_001.md`
- `docs/checklists/phase-6b.md`

This is deliberately **not yet an executable or frozen v0.2 strategy**. It isolates the pre-existing bullish-representativeness debt while retaining the already deterministic D1 -> H1 route. H4/W1 expansion remains deferred because H4 clock anchors are unresolved, and True MSS remains deferred because its Romeo-specific structural algorithm is not deterministic enough yet.

The first source-verification pass confirmed first-party provenance for Episode 1 and found strong independent secondary corroboration of a bullish Model #1 inverse, but the accessible first-party YouTube representation did not expose transcript text. The exact bullish parent manipulation/reclaim predicate, setup-specific midpoint target semantics and exact structural stop owner therefore remain open.

Current gate:

```text
Phase 6B candidate selection          COMPLETE
Gate 6B-1 primary-source evidence    OPEN
v0.2 deterministic specification     BLOCKED
v0.2 alpha implementation            BLOCKED
v0.2 historical outcome access       NOT AUTHORIZED
v0.1 OOS / CONFIRM access            NOT AUTHORIZED
Phase 7 paper trading                BLOCKED
```

No rule may be added merely to increase the four-trade v0.1 DEV sample. The new candidate must earn its predicates from evidence before any fresh historical outcome is opened.

## Phase 6 — final result

The protocol was frozen before new historical outcomes were opened:

```text
P6-VALIDATION-PROTOCOL-v1
DEV       2019-01-01 .. 2022-12-31
OOS       2023-01-01 .. 2025-08-31
QUARANTINE 2025-09-01 .. 2025-09-30
CONFIRM   2025-10-01 .. 2026-07-31
```

Sequential access was enforced. DEV was opened only after its trusted dataset identity had first been sealed and then reproduced byte-for-byte on an independent provider retrieval. OOS and CONFIRM were never opened.

### Frozen DEV dataset

```text
dataset_version          3e8a39fec1062ef902e8a1ad
manifest_sha256          761b561885f94cdb440be02d3a84169549d7bafd8e820bb9654c77ed8aed9e97
normalized_sha256        46682c2d793dbdd0a0939862f444d19b4817559c8989a7fde031598d52cb29f5
M1 rows                  2,074,680
H1 rows                     34,578
complete NY D1               1,418
raw UTC daily archives       1,461
excluded UTC archives           20
REST exact verification         48
checksum verification         1,413
```

Data-quality governance:

- `P6-DATA-QUALITY-AMENDMENT-001`: independently evidenced Binance trading suspension on 2019-03-12 02:00–08:00 UTC.
- `P6-DATA-QUALITY-AMENDMENT-002`: 20 checksum-authenticated incomplete/malformed UTC archives conservatively excluded whole from normalization.
- no missing market observations were synthesized or filled.

### DEV activity gate

Workflow run `31682441984`, job `94390737742`, produced:

```text
rolling detector candidates   1,416
valid TradePlans                  4
BASE closed trades                4
required DEV minimum             30
activity gate     INSUFFICIENT_DEV_SAMPLE
```

Therefore the preregistered protocol requires:

```text
Phase-6 disposition               INSUFFICIENT_EVIDENCE
parameter optimization            PROHIBITED
OOS outcome access                NOT AUTHORIZED
CONFIRM outcome access            NOT AUTHORIZED
paper promotion                   NOT AUTHORIZED
```

### Descriptive four-trade cost results

These values are preserved for audit but are statistically insufficient for edge claims.

| Scenario | Trades | Win rate | Expectancy R | Net P&L | Profit factor | Final equity |
|---|---:|---:|---:|---:|---:|---:|
| IDEAL | 4 | 50% | -0.0130 | -31.03 | 0.969 | 99,968.97 |
| BASE | 4 | 50% | -0.1264 | -256.36 | 0.743 | 99,743.64 |
| STRESSED | 4 | 50% | -0.1963 | -395.18 | 0.604 | 99,604.82 |
| SEVERE | 4 | 50% | -0.2659 | -533.42 | 0.465 | 99,466.58 |

No sensitivity optimization, walk-forward inference, Monte Carlo inference, OOS run, or CONFIRM run was performed because the activity gate failed.

Canonical Phase-6 artifacts:

- `experiments/phase6/P6_VALIDATION_PROTOCOL_V1.md`
- `experiments/phase6/P6_DATA_QUALITY_AMENDMENT_001.md`
- `experiments/phase6/P6_DATA_QUALITY_AMENDMENT_002.md`
- `experiments/phase6/P6_DEV_DATA_FREEZE_001.json`
- `experiments/phase6/P6_DEV_DATA_FREEZE_001.md`
- `experiments/phase6/P6_DEV_OUTCOME_ACCESS_GATE_001.md`
- `experiments/phase6/P6_DEV_RESULT_001.json`
- `experiments/phase6/P6_DEV_RESULT_001.md`
- `docs/reviews/PHASE_6_GATE_REVIEW.md`
- `docs/PHASE_6_COMPLETION_REPORT.md`
- `docs/checklists/phase-6.md`

## Interpretation boundary

The Phase-6 result does **not** prove that all CRT trading is unprofitable and does not evaluate Romeo's entire discretionary methodology.

It establishes the narrower result that the exact deterministic reproduction candidate:

```text
CRT-C3-D1-H1-M1-BEAR-v0.1
```

is too selective on BTCUSDT over the preregistered four-year DEV window to support statistical validation or promotion.

v0.1 must not be relaxed in place after seeing this result. Any attempt to increase activity requires a new version backed by additional source evidence or a separately proven implementation defect.

## Frozen historical handoff retained

Strategy freeze artifacts remain:

- `strategy/CRT_V0.1_FREEZE_MANIFEST.json`
- `strategy/CRT_V0.1_DETECTOR_FREEZE_MANIFEST.json`
- `strategy/CRT_V0.1_BACKTEST_FREEZE_MANIFEST.json`

Earlier engineering evidence remains valid:

- Phase 3 established provider-backed immutable/verified market data.
- Phase 4 established deterministic frozen-strategy detection and fixture parity.
- Phase 5 established causal event-driven simulation and preserved the zero-activity September 2025 quarantine result.
- Phase 6 established a larger trusted DEV sample and correctly stopped because the frozen candidate produced only four trades.

## Current authorization

```text
P6_OOS_OUTCOME_ACCESS_AUTHORIZED     = false
P6_CONFIRM_OUTCOME_ACCESS_AUTHORIZED = false
PARAMETER_OPTIMIZATION_AUTHORIZED    = false
PAPER_TRADING_AUTHORIZED             = false
SHADOW_TRADING_AUTHORIZED            = false
LIVE_TRADING_AUTHORIZED              = false
```

## Immediate next actions — candidate revision track

1. Preserve v0.1 and all Phase-6 evidence unchanged.
2. Complete Gate 6B-1 primary-source verification for the selected bullish D1 -> H1 Model #1 research target.
3. Do not write executable bullish alpha until the required parent, entry, stop, target and expiry predicates are source-closed.
4. If Gate 6B-1 passes, create a new strategy version rather than mutating v0.1.
5. Build new positive/negative fixtures and deterministic rule contracts before looking at fresh validation outcomes.
6. Repeat detector/backtester compatibility and preregistered validation gates for the new candidate.
7. Keep OOS/CONFIRM from v0.1 untouched unless a future explicit governance protocol authorizes otherwise.
8. Do not start Phase 7 paper trading unless a future candidate independently passes validation gates.
9. Keep live trading disabled.
