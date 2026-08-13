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
| 6B — Candidate revision | **IN PROGRESS — OANDA RUNTIME/DATA QUALIFICATION BLOCKER** | Exact source-relevant market universe + trusted provider-neutral data frozen before new validation |
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

## Gate 6B-MM-1 — OANDA provider/data qualification

OANDA v20 is the current candidate provider for non-Binance market-data qualification.

### Provider adapter and qualification tooling — implemented

The Phase-6B branch now contains:

- `src/romeo_crt_engine/market_data/providers/oanda_v20.py` — account instrument discovery + M1 M/B/A candle parsing;
- `src/romeo_crt_engine/market_data/oanda_qualification.py` — ex-ante source-family intersection + redacted discovery manifest;
- `scripts/qualify_oanda_v20.py` — runtime-only credential-safe qualification command;
- `.github/workflows/oanda-provider-qualification.yml` — manual, practice-only qualification workflow using repository secrets;
- `.env.example` — OANDA variable names with no values;
- `docs/adr/ADR-006-oanda-v20-multi-market-qualification.md` — provider/calendar/security boundary;
- provider and qualification unit tests.

The adapter deliberately:

- rejects duplicate/out-of-order provider observations;
- skips incomplete tail candles by default;
- never synthesizes missing market observations;
- preserves OANDA candle activity as `price_count` rather than pretending it is exchange volume/trade count;
- captures display precision/pip/trade-size metadata without claiming display precision is historical executable tick size;
- keeps bearer tokens out of data objects and provenance fingerprints.

### Provider-neutral price data v2 — implemented

ADR-007 introduces additive provider-neutral contracts without changing the frozen Binance v0.1 schema:

```text
P6B_CANONICAL_PRICE_DATASET_V2
```

Implemented contracts now provide:

- first-class price-component identity;
- typed optional activity semantics (`PRICE_COUNT`, base/quote volume, trade count) rather than overloaded fields;
- deterministic canonical price serialization/digests;
- explicit positive price quantum + source classification before data can be detector-facing `TRUSTED`;
- OANDA M1 -> canonical-price-v2 conversion without invented activity values.

Canonical artifact:

- `docs/adr/ADR-007-provider-neutral-canonical-price-data.md`

### Session-aware H1 / D1 reconstruction — implemented and tested

Phase 6B now has an additive session/gap model with categories:

```text
MARKET_CLOSED
SESSION_BREAK
HOLIDAY_OR_EARLY_CLOSE
PROVIDER_MISSING
UNKNOWN_GAP
```

Only the first three may remove expected observations, and only when backed by the frozen session policy/evidence. `PROVIDER_MISSING` and `UNKNOWN_GAP` cannot be used to excuse missing data.

The new aggregation layer:

- builds H1 from actual expected M1 observations;
- permits known partial-hour closure only when every absent minute is policy-covered;
- produces no synthetic bars/prices;
- builds strategy-calendar D1 for explicitly eligible New-York local dates;
- preserves the New-York midnight wall clock through DST.

Tests prove:

- an unexplained missing expected minute fails closed;
- an evidenced session break can explain an absence without filling it;
- a provider-missing gap cannot be promoted to expected downtime;
- the 2026 spring-forward New-York D1 spans 23 absolute hours while remaining midnight-to-midnight wall-clock D1.

The exact account/division + instrument session calendars are **not yet frozen**; that requires actual runtime instrument discovery and authoritative provider schedule evidence for the accepted symbols.

### Signal price component — frozen pre-outcome

Decision:

```text
OANDA signal component = MID / price=M
smoothing               = false
canonical source        = M1
```

Bid/ask remain separate future execution/friction inputs; they do not alter the MID alpha geometry.

Canonical decision:

- `experiments/phase6b/P6B_OANDA_PRICE_COMPONENT_DECISION.md`

### Regression gates

At the current code checkpoint:

```text
Ruff                   PASS
MyPy                   PASS
pytest                 PASS
Backtest Smoke         PASS
v0.1 regression chain  PRESERVED
```

The preserved September-2025 BTCUSDT smoke workflow still reconstructs its original trusted dataset, runs the detector/backtest chain, and verifies detector enumeration remains outcome-independent.

### Runtime qualification — current hard blocker

The exact instrument list is account/regulatory-division dependent and must be discovered from the actual OANDA practice account at runtime. No account ID or API token is committed to the repository.

The initial source-relevant family whitelist, subject to actual account availability, remains:

```text
US NAS 100 / NQ proxy
US SPX 500 / ES proxy
EUR/USD
Gold/USD
```

The manual `OANDA Provider Qualification` workflow is ready to query the account once the runtime/repository secrets exist:

```text
OANDA_ACCOUNT_ID
OANDA_API_TOKEN
```

The GitHub app used during this research session cannot inspect repository secret names/values, so credential presence is not assumed.

### Remaining Gate 6B-MM-1 work

1. run actual OANDA practice account instrument discovery;
2. freeze exact API symbols from the precommitted source-family whitelist before outcomes;
3. freeze account/division + instrument session/holiday calendars;
4. retrieve bounded MID M1 samples and implement multi-page retrieval manifests;
5. independently re-fetch sealed samples and freeze API provenance;
6. resolve executable price quantum without assuming `displayPrecision == tick size`;
7. freeze bid/ask execution/friction methodology and quantity translation;
8. complete provider-neutral detector compatibility/versioning;
9. conduct independent provider/data gate review.

Only after Gate 6B-MM-1 and the exact instrument-universe freeze pass may a new multi-market validation protocol be preregistered.

## Current authorization

```text
V0_1_MUTATION_AUTHORIZED               = false
V0_1_OOS_OUTCOME_ACCESS_AUTHORIZED     = false
V0_1_CONFIRM_OUTCOME_ACCESS_AUTHORIZED = false
PARAMETER_OPTIMIZATION_AUTHORIZED      = false
MULTI_MARKET_OUTCOME_ACCESS_AUTHORIZED = false
PAPER_TRADING_AUTHORIZED               = false
SHADOW_TRADING_AUTHORIZED              = false
LIVE_TRADING_AUTHORIZED                = false
```

## Immediate next actions

1. configure runtime-only OANDA practice credentials outside the repository and run the manual qualification workflow;
2. freeze the exact eligible source-relevant OANDA symbols before strategy outcomes;
3. freeze instrument-specific session/holiday and price-quantum contracts;
4. seal/re-fetch trusted MID M1 data and canonical v2 H1/D1 outputs;
5. build/freeze the provider-neutral detector compatibility chain;
6. preregister the new multi-market validation protocol only after the data gate passes;
7. keep v0.1 OOS/CONFIRM unopened and Phase 7 blocked.
