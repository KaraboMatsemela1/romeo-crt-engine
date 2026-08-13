# Project Status

Updated: 2026-08-13

| Phase | Status | Primary exit condition |
|---|---|---|
| 0 — Engineering foundation | **COMPLETE** | Reproducible dev + CI + logging/storage/experiment contracts |
| 1 — Romeo corpus / reconciliation | **COMPLETE** | Evidence-indexed corpus + explicit evidence debts |
| 2 — Formal CRT spec | **COMPLETE — v0.1 FROZEN** | Deterministic v0.1 order path |
| 3 — Market data | **COMPLETE FOR BINANCE/BTCUSDT v0.1 ROUTE** | Trusted/reproducible D1/H1 dataset |
| 4 — CRT detector | **COMPLETE FOR v0.1** | Frozen deterministic detector |
| 5 — Backtester | **COMPLETE FOR v0.1** | Deterministic cost-aware simulator |
| 6 — Validation | **COMPLETE — INSUFFICIENT_EVIDENCE** | Terminal preregistered DEV decision |
| 6B — Candidate revision | **IN PROGRESS — EXTERNAL OANDA RUNTIME QUALIFICATION REQUIRED** | Exact source-relevant universe + trusted OANDA datasets frozen before activity access |
| 7 — Paper trading | **BLOCKED** | Requires future validated paper promotion |
| 8 — Learning engine | Not started | Requires sufficient deterministic labels |
| 9 — Shadow trading | Not started | Requires paper readiness |
| 10 — Controlled live | **NOT AUTHORIZED** | Explicit future approval + canary gates |

## Frozen v0.1 result

```text
strategy   CRT-C3-D1-H1-M1-BEAR-v0.1
detector   CRT-DETECTOR-v0.1
simulator  CRT-BACKTEST-v0.1.1
DEV        2019-01-01 .. 2022-12-31
candidates 1,416
TradePlans 4
required   30
decision   INSUFFICIENT_EVIDENCE
```

The result is preserved. v0.1 OOS (`2023-01-01 .. 2025-08-31`) and CONFIRM (`2025-10-01 .. 2026-07-31`) remain unopened. Parameter optimization, paper, shadow and live trading remain unauthorized.

## Phase 6B attempt 1 — bullish research path

```text
candidate CRT-C3-D1-H1-M1-BULL-v0.2-RESEARCH
decision  EVIDENCE_INSUFFICIENT
outcomes  NOT OPENED
```

Primary-source work established that bullish CRT states exist, but the exact bullish rolling-parent CRTL lifecycle, C2 sweep/reclaim/double-sweep semantics, Model #1 confirmation, structural stop owner and setup-specific midpoint lifecycle could not be closed without symmetry assumptions.

Canonical decision:

- `research/romeo/phase6b/BULLISH_MODEL1_GATE_DECISION.md`

## Phase 6B active successor — multi-market observation expansion

```text
candidate_version      CRT-C3-D1-H1-M1-BEAR-v0.2-MULTI-MARKET-RESEARCH
alpha_strategy_version CRT-C3-D1-H1-M1-BEAR-v0.1
detector_version       CRT-DETECTOR-v0.2-MULTI-MARKET
signal_component       MID
alpha changes          NONE AUTHORIZED
```

The research question is now whether the unchanged frozen bearish alpha produces a sufficient sample across an ex-ante Romeo-relevant market universe.

Precommitted market families, subject to actual OANDA account availability:

```text
US NAS 100 / NQ proxy
US SPX 500 / ES proxy
EUR/USD
Gold/USD
```

Exact API symbols must be frozen before detector activity counts are opened and may not be selected from count/P&L results.

## Completed Phase 6B engineering/governance

### OANDA provider qualification

Implemented:

- account-specific instrument discovery;
- redacted account-summary discovery;
- M1 MID/BID/ASK candle parsing;
- complete-candle checks;
- duplicate/out-of-order rejection;
- no synthetic gap filling;
- practice-default credential-safe qualification command/workflow;
- `P6B_OANDA_INSTRUMENT_DISCOVERY_V2` manifest.

The redacted runtime manifest is designed to capture execution-relevant account/instrument metadata including home currency, margin/hedging/GSLO mode, unit precision, minimum/maximum sizes, commission and financing where returned. It deliberately omits account ID, token, balance and NAV.

Canonical provider boundary:

- `docs/adr/ADR-006-oanda-v20-multi-market-qualification.md`
- `docs/adr/ADR-009-oanda-execution-evidence-boundary.md`

### Provider-neutral data v2

Implemented:

```text
P6B_CANONICAL_PRICE_DATASET_V2
```

OANDA candle activity is typed as `PRICE_COUNT`; it is not fabricated as Binance base/quote volume or trade count. Price component and an explicit pre-frozen positive price quantum are part of detector-facing trusted identity.

Canonical decision:

- `docs/adr/ADR-007-provider-neutral-canonical-price-data.md`

### Historical retrieval provenance

Implemented before the real DEV download:

- deterministic <=5000-candle request windows;
- 4500-minute default page size;
- secret/account-redacted request fingerprints;
- per-page raw-response SHA-256;
- chronological page merge;
- identical boundary deduplication;
- conflicting boundary rejection;
- retrieval-level provenance digest.

### Session-aware canonical aggregation

Implemented mechanics:

```text
MARKET_CLOSED
SESSION_BREAK
HOLIDAY_OR_EARLY_CLOSE
PROVIDER_MISSING
UNKNOWN_GAP
```

Only evidenced closure/session/holiday categories may remove expected observations. Unknown/provider-missing gaps fail closed. H1 and New-York-midnight D1 are constructed from actual M1 observations without synthetic prices; DST wall-clock behavior is tested.

Actual accepted-instrument session/holiday policies remain unfrozen until runtime discovery.

### Signal component

Frozen before outcomes:

```text
OANDA signal OHLC = MID / price=M
smoothing         = false
canonical source  = M1
```

Bid/ask remain separate execution/friction evidence.

Canonical decision:

- `experiments/phase6b/P6B_OANDA_PRICE_COMPONENT_DECISION.md`

### Detector compatibility

`CRT-DETECTOR-v0.2-MULTI-MARKET` calls the frozen v0.1 evaluator and preserves v0.1 on every emitted `TradePlan`.

Exact fixture parity is verified for:

- decision state;
- reason code;
- rule trace;
- evidence IDs;
- causal-input digest;
- TradePlan.

Compatibility baseline is frozen pre-outcome:

- `docs/adr/ADR-008-multi-market-detector-compatibility.md`
- `strategy/CRT_V0.2_MULTI_MARKET_DETECTOR_COMPATIBILITY_MANIFEST.json`

### Detector-only activity gate

Frozen protocol:

```text
protocol                       P6B-MULTI-MARKET-ACTIVITY-PROTOCOL-v1
DEV activity period            2019-01-01 .. 2022-12-31 New York
minimum accepted instruments   2
minimum contributing instruments 2
minimum pooled TradePlans      30
backtester                     PROHIBITED
P&L outcome access             PROHIBITED
```

Machine-enforced decisions:

```text
INSUFFICIENT_ELIGIBLE_UNIVERSE
INSUFFICIENT_MULTI_MARKET_SAMPLE
SUFFICIENT_ACTIVITY_FOR_PERFORMANCE_PROTOCOL
```

Even a sufficient activity result authorizes only the next execution-model/performance-protocol work; it does not authorize P&L.

Canonical artifacts:

- `experiments/phase6b/P6B_MULTI_MARKET_ACTIVITY_PROTOCOL_V1.md`
- `strategy/P6B_MULTI_MARKET_ACTIVITY_GATE_FREEZE_MANIFEST.json`

## Verification status

The provider/data, detector compatibility and activity-gate work has been iterated through repository CI. A preserved BTCUSDT Backtest Smoke remains part of the regression boundary so Phase 6B additions cannot silently rewrite the historical v0.1 chain.

The latest substantive code checkpoint corrected only a test fixture in paged-history conflict validation after CI correctly rejected an impossible OHLC test candle.

## Current hard blocker — runtime OANDA qualification

The repo is now ready for the first credentialed **practice-only** qualification pass, but this environment cannot inspect or supply the repository secrets and cannot dispatch the newly added manual workflow.

Required runtime/repository secrets:

```text
OANDA_ACCOUNT_ID
OANDA_API_TOKEN
```

The workflow/command will use them without writing either value into the qualification artifact.

### Required runtime sequence

1. Run OANDA practice account summary + instrument discovery.
2. Intersect the actual account universe with the precommitted four market families.
3. If fewer than two are eligible, stop before detector counts as `INSUFFICIENT_ELIGIBLE_UNIVERSE`.
4. Freeze exact API symbols, metadata digests and inclusion/exclusion reasons.
5. Freeze accepted-instrument session/holiday and price-quantum contracts.
6. Retrieve/seal/re-fetch MID M1 DEV data for 2019–2022.
7. Build/freeze trusted v2 H1/D1 datasets.
8. Run the detector-only 2/2/30 activity protocol with the backtester disabled.
9. If activity is insufficient, preserve the result and stop without P&L.
10. Only if activity passes, complete/freeze OANDA execution/cost/conversion simulation and preregister a full performance protocol.

## Authorization

```text
V0_1_MUTATION_AUTHORIZED               = false
V0_1_OOS_OUTCOME_ACCESS_AUTHORIZED     = false
V0_1_CONFIRM_OUTCOME_ACCESS_AUTHORIZED = false
PARAMETER_OPTIMIZATION_AUTHORIZED      = false
MULTI_MARKET_ACTIVITY_COUNTS_OPENED    = false
MULTI_MARKET_PNL_OUTCOME_ACCESS        = false
PAPER_TRADING_AUTHORIZED               = false
SHADOW_TRADING_AUTHORIZED              = false
LIVE_TRADING_AUTHORIZED                = false
```
