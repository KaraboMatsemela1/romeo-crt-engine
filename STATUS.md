# Project Status

Updated: 2026-08-13

| Phase | Status | Primary exit condition |
|---|---|---|
| 0 — Engineering foundation | **COMPLETE** | Reproducible dev + CI + logging/storage/experiment contracts |
| 1 — Romeo corpus / reconciliation | **COMPLETE** | Evidence-indexed corpus + reconciled doctrine + explicit evidence debts |
| 2 — Formal CRT spec | **COMPLETE — v0.1 FROZEN** | Deterministic CRT v0.1 with no unresolved active-path predicates |
| 3 — Market data | **COMPLETE FOR BINANCE/BTCUSDT ROUTE** | Provider-backed trusted/reproducible D1/H1 dataset |
| 4 — CRT detector | **COMPLETE FOR v0.1** | Frozen fixtures + trusted-data detector integration reproduced causally |
| 5 — Backtester | **COMPLETE** | Deterministic cost-aware event-driven simulator |
| 6 — Validation | **COMPLETE — INSUFFICIENT_EVIDENCE** | Preregistered BTCUSDT DEV gate reached terminal written decision |
| 6B — Candidate revision | **IN PROGRESS — MULTI-MARKET PROVIDER/DATA QUALIFICATION** | One independently justified successor becomes eligible for preregistered validation |
| 7 — Paper trading | **BLOCKED** | Requires explicit promotion from a future validation protocol |
| 8 — Learning engine | Not started | Requires a sufficiently evidenced deterministic baseline and labels |
| 9 — Shadow trading | Not started | Requires paper/production-like readiness |
| 10 — Controlled live | **NOT AUTHORIZED** | Explicit approval + canary gates |

## Frozen historical v0.1 disposition

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

`CRT-BACKTEST-v0.1.1` is the Phase-6 data-gap compatibility patch to the v0.1 simulator. It permits ordered/non-overlapping H1 input across explicitly governed market-data gaps and does not change entry, stop, target, sizing, friction, or same-bar execution semantics.

## Phase 6 — sealed result

The preregistered validation chronology was:

```text
DEV         2019-01-01 .. 2022-12-31
OOS         2023-01-01 .. 2025-08-31
QUARANTINE  2025-09-01 .. 2025-09-30
CONFIRM     2025-10-01 .. 2026-07-31
```

Sequential access was enforced. DEV was opened only after its trusted dataset identity was sealed and independently reproduced. OOS and CONFIRM remain unopened.

### Frozen DEV dataset

```text
dataset_version          3e8a39fec1062ef902e8a1ad
manifest_sha256          761b561885f94cdb440be02d3a84169549d7bafd8e820bb9654c77ed8aed9e97
normalized_sha256        46682c2d793dbdd0a0939862f444d19b4817559c8989a7fde031598d52cb29f5
M1 rows                  2,074,680
H1 rows                     34,578
complete NY D1               1,418
rolling detector candidates  1,416
valid TradePlans                  4
BASE closed trades                4
required DEV minimum             30
```

Therefore:

```text
activity gate                      INSUFFICIENT_DEV_SAMPLE
Phase-6 disposition                INSUFFICIENT_EVIDENCE
parameter optimization             PROHIBITED
OOS outcome access                 NOT AUTHORIZED
CONFIRM outcome access             NOT AUTHORIZED
paper promotion                    NOT AUTHORIZED
```

The four cost-scenario results remain preserved for audit but are statistically insufficient for edge claims. No sensitivity optimization, walk-forward inference, Monte Carlo inference, OOS run, or CONFIRM run was performed after the activity gate failed.

Canonical Phase-6 artifacts include:

- `experiments/phase6/P6_VALIDATION_PROTOCOL_V1.md`
- `experiments/phase6/P6_DEV_DATA_FREEZE_001.json`
- `experiments/phase6/P6_DEV_RESULT_001.json`
- `experiments/phase6/P6_DEV_RESULT_001.md`
- `docs/reviews/PHASE_6_GATE_REVIEW.md`
- `docs/PHASE_6_COMPLETION_REPORT.md`

## Phase 6B — candidate revision

Phase 6B is **IN PROGRESS**. It does not mutate v0.1 and does not authorize access to the unopened v0.1 OOS/CONFIRM outcomes.

### Successor attempt 1 — bullish D1 -> H1 Model #1

Research candidate:

```text
CRT-C3-D1-H1-M1-BULL-v0.2-RESEARCH
```

Final evidence-gate disposition:

```text
Gate 6B-1 = EVIDENCE_INSUFFICIENT
```

The source review established that bullish CRT states are genuinely part of Romeo's doctrine and strongly corroborated a bullish Model #1 inverse. However, the accessible primary-source record did not close all required order-path semantics without relying on symmetry assumptions, including the exact rolling-parent CRTL lifecycle, bullish Candle-2 sweep/reclaim and double-sweep handling, exact confirmation reference/timing, structural stop owner, and setup-specific midpoint lifecycle.

No bullish strategy outcome was opened. This is an evidence insufficiency result, not a profitability rejection.

Canonical artifacts:

- `research/romeo/phase6b/PHASE_6B_CANDIDATE_SELECTION.md`
- `research/romeo/phase6b/BULLISH_MODEL1_EVIDENCE_GATE.md`
- `research/romeo/phase6b/PRIMARY_SOURCE_PASS_001.md`
- `research/romeo/phase6b/PRIMARY_SOURCE_PASS_002.md`
- `research/romeo/phase6b/BULLISH_MODEL1_GATE_DECISION.md`

### Successor attempt 2 — frozen bearish alpha across a broader market universe

Active research candidate:

```text
CRT-C3-D1-H1-M1-BEAR-v0.2-MULTI-MARKET-RESEARCH
```

This route changes the **observation/validation market universe**, not the frozen alpha predicates.

Rationale:

- ADR-005 deliberately selected Binance BTCUSDT as the first engineering/validation route and explicitly prohibits generalizing its result to forex, index, metal, or other instruments;
- Romeo's evidence corpus is multi-market;
- expanding the market universe can be preregistered without weakening the strategy merely because BTCUSDT generated four DEV trades.

No alpha-rule change is authorized for this successor.

Canonical selection:

- `research/romeo/phase6b/MULTI_MARKET_CANDIDATE_SELECTION.md`

## Gate 6B-MM-1 — OANDA v20 provider/data qualification

OANDA v20 is the current candidate provider for non-Binance market-data qualification.

Implemented on the Phase-6B branch:

- provider-specific adapter `src/romeo_crt_engine/market_data/providers/oanda_v20.py`;
- account-specific instrument discovery parsing;
- provider-specific M1 candle parsing for midpoint/bid/ask price components;
- complete-candle filtering;
- duplicate/out-of-order protection;
- no synthetic filling of market/session gaps;
- OANDA candle activity retained as `price_count`, not misrepresented as exchange/trade volume;
- precision/pip/trade-size metadata captured without inventing a historical tick size;
- secret-free deterministic request fingerprints;
- OANDA practice/live endpoint separation;
- environment variable names only in `.env.example`;
- provider unit tests;
- ADR-006 documenting the qualification contract.

### Critical calendar boundary

OANDA provider-native default daily alignment must **not** redefine the frozen CRT strategy calendar.

The required route is:

```text
OANDA M1/H1 observations
        ↓
UTC provider chronology
        ↓
explicit market/session-gap classification
        ↓
project-owned New-York-midnight D1 aggregation
        ↓
frozen bearish CRT strategy
```

### Runtime qualification still required

The exact instrument list is account/regulatory-division dependent and must be discovered from the actual OANDA practice account at runtime. No account ID or API token is committed to the repository.

The initial source-relevant family whitelist, subject to actual account availability, is:

```text
US NAS 100 / NQ proxy
US SPX 500 / ES proxy
EUR/USD
Gold/USD
```

This list must be converted into an exact frozen API-symbol manifest **before** any strategy outcome access. Instruments may not be kept/dropped based on preliminary trade count or P&L.

Outstanding Gate 6B-MM-1 work:

1. confirm the latest branch passes Ruff, MyPy, pytest and Backtest Smoke;
2. run account-specific instrument discovery with runtime-only practice credentials;
3. freeze the signal price component and execution bid/ask policy;
4. implement/freeze session-gap taxonomy and calendars for accepted instruments;
5. prove New-York-midnight D1 aggregation across DST and closures;
6. resolve executable tick/price quantum without assuming display precision is a historical tick size;
7. implement sealed API-response/re-fetch provenance;
8. freeze the exact first instrument universe before outcomes;
9. conduct an independent provider/data gate review.

Only then may a new multi-market validation protocol be preregistered.

## Current authorization

```text
V0_1_MUTATION_AUTHORIZED              = false
V0_1_OOS_OUTCOME_ACCESS_AUTHORIZED    = false
V0_1_CONFIRM_OUTCOME_ACCESS_AUTHORIZED= false
PARAMETER_OPTIMIZATION_AUTHORIZED     = false
MULTI_MARKET_OUTCOME_ACCESS_AUTHORIZED= false
PAPER_TRADING_AUTHORIZED              = false
SHADOW_TRADING_AUTHORIZED             = false
LIVE_TRADING_AUTHORIZED               = false
```

## Immediate next actions

1. Complete CI/static verification for the OANDA qualification adapter.
2. Add the provider/session gap policy and canonical aggregation tests that do not require credentials.
3. Prepare a runtime-only OANDA qualification command that never prints or persists account credentials.
4. When practice credentials are available at runtime, discover the exact account instrument universe and freeze the eligible source-relevant symbols before any strategy outcomes.
5. Preregister a new multi-market validation protocol only after the provider/data gate passes.
6. Keep v0.1 OOS/CONFIRM unopened and Phase 7 blocked.
