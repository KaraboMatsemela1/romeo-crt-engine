# Phase 6B — Candidate Revision Checklist

**Status:** **IN PROGRESS — MULTI-MARKET PROVIDER/DATA GATE**  
**Active research target:** `CRT-C3-D1-H1-M1-BEAR-v0.2-MULTI-MARKET-RESEARCH`  
**Preserved failed research path:** `CRT-C3-D1-H1-M1-BULL-v0.2-RESEARCH` -> `EVIDENCE_INSUFFICIENT`  
**Phase 7:** **BLOCKED UNTIL A FUTURE CANDIDATE PASSES VALIDATION**

## A. Preserve predecessor evidence

- [x] Preserve `CRT-C3-D1-H1-M1-BEAR-v0.1` unchanged.
- [x] Preserve the Phase-6 `INSUFFICIENT_EVIDENCE` disposition.
- [x] Keep v0.1 OOS outcomes unopened.
- [x] Keep v0.1 CONFIRM outcomes unopened.
- [x] Keep parameter optimization disabled for v0.1.
- [x] Keep paper, shadow and live trading unauthorized.

## B. First successor precommitment — bullish D1 -> H1 Model #1

- [x] Review the post-Phase-2 evidence-debt ledger.
- [x] Review deferred direction, timeframe, entry-family, SMT, KOD and management variants.
- [x] Reject H4/W1 expansion while H4 anchors remain unresolved.
- [x] Reject True MSS expansion while the Romeo-specific structural algorithm remains unresolved.
- [x] Reject SMT/KOD/countertrend/journey-to-level bundling.
- [x] Prohibit tuning v0.1 numerical parameters merely to increase trade count.
- [x] Precommit `CRT-C3-D1-H1-M1-BULL-v0.2-RESEARCH` before any bullish outcome access.
- [x] Perform primary-source verification passes.
- [x] Preserve strong evidence that bullish CRT states exist and the broad `CRTH/L -> 50%` doctrine exists.
- [x] Refuse to promote secondary/symmetry assumptions into exact bullish alpha rules.
- [x] Produce written Gate 6B-1 decision: **`EVIDENCE_INSUFFICIENT`**.
- [x] Confirm no bullish historical strategy outcome was opened.
- [x] Close the bullish primary-source tracking issue with the insufficient-evidence result.

### Unresolved bullish predicates preserved for future re-entry

These remain intentionally unresolved rather than silently defaulted:

- [ ] exact old-`CRTL` / rolling-parent reference lifecycle;
- [ ] exact bullish Candle-2 sweep/reclaim rule;
- [ ] double-sided sweep treatment;
- [ ] exact Model #1 confirmation reference/timing from primary evidence;
- [ ] exact bullish structural stop owner;
- [ ] setup-specific midpoint consumption/expiry semantics;
- [ ] direction-neutral inheritance decision for all project parameters.

Canonical decision: `research/romeo/phase6b/BULLISH_MODEL1_GATE_DECISION.md`.

## C. Second successor selection — frozen bearish alpha, broader market universe

- [x] Select the lower-ambiguity successor after the bullish evidence gate failed.
- [x] Preserve the frozen bearish D1 -> H1 Model #1 strategy semantics.
- [x] Record that ADR-005 makes BTCUSDT an initial route whose result must not be generalized to forex/indices/metals.
- [x] Use Romeo-relevant market families as the ex-ante universe motivation, not historical profitability.
- [x] Precommit `CRT-C3-D1-H1-M1-BEAR-v0.2-MULTI-MARKET-RESEARCH`.
- [x] Prohibit instrument selection based on preliminary trade count/P&L.
- [x] Keep SMT inactive; related-market examples do not create an SMT order path.
- [x] Select OANDA v20 for provider qualification, subject to account/division instrument availability.

Canonical selection: `research/romeo/phase6b/MULTI_MARKET_CANDIDATE_SELECTION.md`.

## D. Gate 6B-MM-1 — OANDA provider/data qualification

### Provider contract and parser

- [x] Add provider-specific OANDA v20 adapter.
- [x] Support account-specific instrument discovery parsing.
- [x] Support M1 candle response parsing for midpoint/bid/ask components.
- [x] Require provider identity and M1 granularity.
- [x] Reject duplicate/out-of-order timestamps.
- [x] Skip incomplete tail candles by default.
- [x] Preserve market/session gaps instead of filling them.
- [x] Store OANDA `volume` as `price_count`, not exchange/trade volume.
- [x] Capture display precision, pip location, trade-unit precision and minimum trade size without inventing a historical tick size.
- [x] Add deterministic secret-free request fingerprinting.
- [x] Keep bearer token out of returned objects/provenance fingerprints.
- [x] Add practice/live endpoint constants while keeping live trading independently disabled.
- [x] Add OANDA environment variable names with empty values only.
- [x] Add ADR-006 documenting provider/calendar/metadata boundaries.
- [x] Add unit tests for the provider parser and safety behavior.

### Provider-neutral canonical price data

- [x] Add ADR-007 and preserve the frozen Binance `PHASE3_DATASET_MANIFEST_V1` unchanged.
- [x] Add additive `P6B_CANONICAL_PRICE_DATASET_V2` models.
- [x] Make price component first-class dataset identity.
- [x] Represent OANDA activity explicitly as `PRICE_COUNT` rather than fake base/quote volume or trade count.
- [x] Represent unavailable activity as unavailable rather than numeric zero.
- [x] Require explicit positive `price_quantum` plus source classification before a v2 dataset may become detector-facing `TRUSTED` data.
- [x] Add deterministic provider-neutral price-bar serialization/digests.
- [x] Add OANDA M1 -> canonical-price-v2 conversion without fabricated activity semantics.

### Session/gap and aggregation contracts

- [x] Add versioned gap taxonomy: `MARKET_CLOSED`, `SESSION_BREAK`, `HOLIDAY_OR_EARLY_CLOSE`, `PROVIDER_MISSING`, `UNKNOWN_GAP`.
- [x] Permit only evidence-backed market/session/holiday categories to remove expected observations.
- [x] Prohibit `PROVIDER_MISSING` and `UNKNOWN_GAP` from being approved as expected trading downtime.
- [x] Build session-aware H1 aggregation from actual M1 observations with no synthetic prices.
- [x] Build New-York-midnight D1 aggregation for explicitly eligible local dates.
- [x] Preserve partial-hour expected closures only when every missing minute is covered by the frozen gap policy.
- [x] Add test: missing expected minute fails closed.
- [x] Add test: evidenced session break can explain a missing observation without filling it.
- [x] Add test: provider-missing interval cannot be reclassified as an expected session break.
- [x] Add test: New-York D1 spring-forward envelope is 23 absolute hours while remaining midnight-to-midnight wall-clock D1.
- [ ] Freeze account/division + instrument-specific OANDA session policy from authoritative provider evidence.
- [ ] Add exact provider/session calendar fixtures for every accepted instrument.
- [ ] Add holiday/early-close fixture registry for validation windows.
- [ ] Cross-check project D1 aggregation against an explicitly aligned provider query where appropriate.

### Price/execution metadata decisions

- [x] Freeze signal-detection price component to **MID / OANDA `M`** before outcomes (`P6B-OANDA-PRICE-COMPONENT-001`).
- [x] Freeze unsmoothed M1 as the canonical OANDA signal-source retrieval mode.
- [x] Keep bid/ask separate from signal geometry and require them for the later execution/friction contract.
- [ ] Freeze bid/ask historical execution-friction methodology.
- [ ] Resolve executable price quantum without assuming `displayPrecision == historical tick size`.
- [ ] Resolve quantity/position-size translation for each accepted instrument type.
- [ ] Record short-capability/account-instrument execution boundary separately from alpha validity.

### Credential-safe runtime qualification

- [x] Add a credential-free instrument-discovery manifest builder.
- [x] Ensure discovery manifest contains no account ID or token.
- [x] Add ex-ante source-family intersection before any strategy outcome access.
- [x] Add `scripts/qualify_oanda_v20.py` with practice default and explicit live-read opt-in.
- [x] Add manual practice-only `OANDA Provider Qualification` GitHub Actions workflow.
- [x] Require runtime/repository secrets rather than committed credentials.
- [x] Assert qualification manifest keeps strategy/paper/live authorization false.
- [ ] Query the actual OANDA practice account instrument universe.
- [ ] Map source market families to exact available API symbols.
- [ ] Record account/division-specific metadata without committing account ID/token.
- [ ] Freeze the first accepted instrument list before strategy outcome access.
- [ ] Retrieve bounded M1 samples for each candidate instrument.
- [ ] Implement pagination/retrieval manifest for multi-page history.
- [ ] Re-fetch sealed historical slices and compare provider values.
- [ ] Freeze raw-response/request/normalization provenance contract.

### CI / regression verification

- [x] Diagnose and resolve initial Ruff findings without strategy/data-semantic changes.
- [x] Diagnose and resolve MyPy HTTP-response typing issue without behavior change.
- [x] Diagnose and resolve v2 aggregation activity typing issue without behavior change.
- [x] Confirm Ruff passes on the current code checkpoint.
- [x] Confirm MyPy passes on the current code checkpoint.
- [x] Confirm full pytest suite passes on the current code checkpoint.
- [x] Confirm preserved Backtest Smoke passes on the current code checkpoint.
- [x] Confirm the preserved September-2025 BTCUSDT detector enumeration remains outcome-independent.

## E. Gate 6B-MM-2 — pre-outcome universe freeze

**Blocked until Gate 6B-MM-1 runtime provider/data qualification is complete.**

Initial source-relevant family whitelist, subject to actual account availability:

```text
US NAS 100 / NQ proxy
US SPX 500 / ES proxy
EUR/USD
Gold/USD
```

Before detector execution:

- [ ] freeze exact API instrument symbols;
- [ ] freeze inclusion/exclusion reasons before outcomes;
- [ ] freeze required historical coverage;
- [ ] freeze provider/data version for every instrument;
- [ ] prohibit dropping an instrument because its strategy result is poor;
- [ ] prohibit adding an instrument after seeing favorable preliminary results.

## F. Gate 6B-MM-3 — new multi-market validation preregistration

**No strategy outcome access until this gate is complete.**

- [ ] Define new development window(s) based on verified provider coverage.
- [ ] Define new OOS window(s).
- [ ] Define a new final-confirmatory window.
- [ ] Keep v0.1 reserved OOS/CONFIRM untouched unless separately authorized by explicit governance.
- [ ] Freeze per-instrument minimum activity gates.
- [ ] Freeze pooled minimum activity gates.
- [ ] Prevent one instrument from silently dominating the pooled conclusion.
- [ ] Freeze asset-class-appropriate friction assumptions before results.
- [ ] Freeze sensitivity/robustness plan before results.
- [ ] Freeze multiple-comparison controls before results.
- [ ] Freeze Monte Carlo eligibility threshold before results.
- [ ] Freeze promotion/rejection/insufficient-evidence decision rules.
- [ ] Independently review leakage, selection bias and overfit controls.
- [ ] Seal all dataset identities before detector/backtest access.

## G. Detector/backtester compatibility

- [x] Demonstrate frozen v0.1 strategy logic can consume provider-neutral canonical D1/H1 bars without alpha changes.
- [x] Preserve all legacy v0.1 regression tests unchanged and green while adding Phase-6B data code.
- [x] Create separately versioned `CRT-DETECTOR-v0.2-MULTI-MARKET` compatibility identity.
- [x] Record both candidate version `v0.2-MULTI-MARKET` and underlying alpha version `v0.1` on detector runs/candidates.
- [x] Require every emitted `TradePlan` to retain `strategy_version = CRT-C3-D1-H1-M1-BEAR-v0.1`.
- [x] Confirm exact parity across all frozen v0.1 fixtures for state, reason, rule trace, evidence IDs, causal-input digest and TradePlan.
- [x] Fail closed when v2 normalized content does not match the trusted dataset identity.
- [x] Fail closed on non-MID signal data for the active candidate.
- [x] Confirm no provider activity metadata enters strategy validity predicates.
- [x] Freeze detector compatibility baseline in `strategy/CRT_V0.2_MULTI_MARKET_DETECTOR_COMPATIBILITY_MANIFEST.json` before provider-backed outcomes.
- [x] Confirm CI and the preserved BTCUSDT Backtest Smoke remain green after detector compatibility work.
- [ ] Freeze provider-backed execution/cost semantics before adapting the simulator to OANDA data.
- [ ] Resolve quantity-step / instrument sizing semantics before provider-backed simulation.
- [ ] Create separately versioned multi-market simulator compatibility identity only after execution/friction contracts are frozen.

Canonical detector compatibility decision: `docs/adr/ADR-008-multi-market-detector-compatibility.md`.

## H. Promotion boundary

- [ ] Do not start Phase 7 unless a future candidate receives `PROMOTE_TO_PAPER_CANDIDATE` from its own preregistered validation protocol.
- [ ] Do not treat sufficient trade count as proof of edge.
- [ ] Do not treat positive DEV or pooled P&L as permission to skip OOS/confirmatory gates.
- [ ] Keep hard risk controls independent from strategy scoring.
- [ ] Keep live trading disabled until the full roadmap authorizes it.

## Current handoff

```text
Phase 6B                           IN PROGRESS
Bullish successor                 EVIDENCE_INSUFFICIENT / PRESERVED
Active successor                  BEARISH D1 -> H1 MODEL #1 / MULTI-MARKET
Alpha changes                     NONE AUTHORIZED
OANDA provider adapter            IMPLEMENTED
Provider-neutral price data v2    IMPLEMENTED + TESTED
Session-aware H1/D1 aggregation   IMPLEMENTED + TESTED
Signal price component            MID / FROZEN PRE-OUTCOME
Multi-market detector             IMPLEMENTED + PARITY VERIFIED
Detector compatibility baseline   FROZEN PRE-OUTCOME
Runtime qualification command     READY
Manual OANDA practice workflow    READY
CI / MyPy / pytest                GREEN
Preserved Backtest Smoke          GREEN
Actual OANDA instrument discovery NOT RUN — runtime credentials required
Exact instrument universe         NOT FROZEN
Execution/friction contract       NOT FROZEN
Multi-market simulator            BLOCKED ON EXECUTION CONTRACT
Multi-market strategy outcomes    NOT AUTHORIZED
v0.1 OOS / CONFIRM                UNOPENED
Phase 7                           BLOCKED
Live trading                      NOT AUTHORIZED
```
