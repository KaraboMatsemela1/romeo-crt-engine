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

### CI / static verification

- [x] Backtest smoke remained green after the initial provider change.
- [x] Diagnose initial CI failure as Ruff-only style findings.
- [x] Apply focused Ruff fixes without strategy/data-semantic changes.
- [ ] Confirm Ruff passes on the latest head.
- [ ] Confirm MyPy passes on the latest head.
- [ ] Confirm full pytest suite passes on the latest head.
- [ ] Confirm Backtest Smoke passes on the latest head.

### Runtime provider qualification — blocked until credentials are supplied at execution time

- [ ] Query the actual OANDA practice account instrument universe.
- [ ] Map source market families to exact available API symbols.
- [ ] Record account/division-specific metadata without committing account ID/token.
- [ ] Freeze the first accepted instrument list before strategy outcome access.
- [ ] Retrieve bounded M1 samples for each candidate instrument.
- [ ] Implement pagination/retrieval manifest for multi-page history.
- [ ] Re-fetch sealed historical slices and compare provider values.
- [ ] Freeze raw-response/request/normalization provenance contract.

### Calendar and gap semantics

- [x] Explicitly reject OANDA's default 17:00 New-York daily alignment as the strategy D1 definition.
- [x] Require project-owned New-York-midnight D1 construction.
- [ ] Define OANDA market-closed/session-break/holiday/provider-missing/unknown-gap taxonomy in code.
- [ ] Add provider/session calendar fixtures for accepted instruments.
- [ ] Add DST fixtures around New-York wall-clock D1 boundaries.
- [ ] Demonstrate H1 and D1 aggregation from OANDA observations without synthetic prices.
- [ ] Cross-check project D1 aggregation against an explicitly aligned provider query where appropriate.

### Price/execution metadata decisions

- [ ] Freeze signal-detection price component (`M`, `B`, or `A`) before outcomes.
- [ ] Freeze bid/ask use for execution-friction validation.
- [ ] Resolve executable tick/price quantum without assuming `displayPrecision == historical tick size`.
- [ ] Resolve quantity/position-size translation for each instrument type.
- [ ] Record short-capability/account-instrument execution boundary separately from alpha validity.

## E. Gate 6B-MM-2 — pre-outcome universe freeze

**Blocked until Gate 6B-MM-1 provider/data qualification is complete.**

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

- [ ] Demonstrate frozen v0.1 strategy logic can consume the provider-neutral canonical D1/H1 bars without alpha changes.
- [ ] Preserve all v0.1 regression tests unchanged.
- [ ] Confirm immutable `TradePlan` output remains the detector/backtester boundary.
- [ ] Confirm no provider-specific logic enters the strategy validity predicates.
- [ ] Confirm execution/cost changes are versioned separately from alpha validity.
- [ ] Freeze the multi-market detector/simulator compatibility chain before outcomes.

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
OANDA provider ADR                PROPOSED
Latest CI                         RECHECKING AFTER RUFF FIX
Actual OANDA instrument discovery NOT RUN — runtime credentials absent
Multi-market strategy outcomes    NOT AUTHORIZED
v0.1 OOS / CONFIRM                UNOPENED
Phase 7                           BLOCKED
Live trading                      NOT AUTHORIZED
```
