# Phase 6B — Candidate Revision Checklist

**Status:** **IN PROGRESS — OANDA UNIVERSE FROZEN / HISTORICAL DATA QUALIFICATION NEXT**  
**Active research target:** `CRT-C3-D1-H1-M1-BEAR-v0.2-MULTI-MARKET-RESEARCH`  
**Underlying frozen alpha:** `CRT-C3-D1-H1-M1-BEAR-v0.1`  
**Detector:** `CRT-DETECTOR-v0.2-MULTI-MARKET`  
**Phase 7:** **BLOCKED UNTIL A FUTURE CANDIDATE PASSES FULL VALIDATION**

## A. Historical integrity

- [x] Preserve v0.1 strategy, detector, simulator and Phase-6 evidence unchanged.
- [x] Preserve v0.1 `INSUFFICIENT_EVIDENCE` result.
- [x] Keep v0.1 OOS unopened.
- [x] Keep v0.1 CONFIRM unopened.
- [x] Keep v0.1 parameter optimization prohibited.
- [x] Keep paper, shadow and live trading unauthorized.

## B. Bullish successor evidence gate

- [x] Precommit `CRT-C3-D1-H1-M1-BULL-v0.2-RESEARCH` before outcomes.
- [x] Perform primary-source verification passes.
- [x] Preserve evidence for bullish CRT states and broader `CRTH/L -> 50%` doctrine.
- [x] Refuse to infer exact bullish order rules from bearish code symmetry.
- [x] Close Gate 6B-1 as `EVIDENCE_INSUFFICIENT`.
- [x] Confirm no bullish historical strategy outcome was opened.

Canonical decision: `research/romeo/phase6b/BULLISH_MODEL1_GATE_DECISION.md`.

## C. Active multi-market successor

- [x] Select `CRT-C3-D1-H1-M1-BEAR-v0.2-MULTI-MARKET-RESEARCH`.
- [x] Preserve the frozen bearish v0.1 alpha rules without relaxation.
- [x] Precommit source families: NAS100/NQ proxy, SPX500/ES proxy, EUR/USD, Gold/USD.
- [x] Keep SMT inactive.
- [x] Select OANDA v20 subject to actual account availability.
- [x] Prohibit post-count or post-P&L instrument cherry-picking.

Canonical selection: `research/romeo/phase6b/MULTI_MARKET_CANDIDATE_SELECTION.md`.

## D. Provider/data engineering

- [x] Add OANDA v20 provider adapter.
- [x] Add credential-safe authorized-account preflight.
- [x] Support account-specific instrument discovery.
- [x] Support M1 MID/BID/ASK candle parsing.
- [x] Skip incomplete candle tails by default.
- [x] Reject duplicate/out-of-order provider observations.
- [x] Never synthesize missing observations.
- [x] Type OANDA candle activity as `PRICE_COUNT`, not exchange volume/trade count.
- [x] Keep account identity and bearer token out of persisted qualification artifacts.
- [x] Default runtime qualification to practice.
- [x] Add paged historical request provenance and response SHA-256 sealing.
- [x] Deduplicate identical page-boundary candles.
- [x] Reject conflicting duplicate candles across page boundaries.
- [x] Build deterministic retrieval-level provenance digest.

Canonical provider decisions:

- `docs/adr/ADR-006-oanda-v20-multi-market-qualification.md`
- `docs/adr/ADR-009-oanda-execution-evidence-boundary.md`

## E. Provider-neutral signal data

- [x] Preserve legacy Binance Phase-3 schema unchanged.
- [x] Add `P6B_CANONICAL_PRICE_DATASET_V2`.
- [x] Make price component first-class dataset identity.
- [x] Freeze signal OHLC to OANDA MID / `price=M`.
- [x] Freeze unsmoothed M1 as canonical signal source.
- [x] Keep BID/ASK separate for later execution evidence.
- [x] Require explicit positive price quantum before `TRUSTED` detector use.
- [x] Add deterministic v2 serialization/digests.

Canonical decisions:

- `docs/adr/ADR-007-provider-neutral-canonical-price-data.md`
- `experiments/phase6b/P6B_OANDA_PRICE_COMPONENT_DECISION.md`

## F. Session/gap and aggregation mechanics

- [x] Add `MARKET_CLOSED`, `SESSION_BREAK`, `HOLIDAY_OR_EARLY_CLOSE`, `PROVIDER_MISSING`, `UNKNOWN_GAP` categories.
- [x] Permit only evidenced closure/session/holiday categories to remove expected observations.
- [x] Fail closed on `PROVIDER_MISSING` and `UNKNOWN_GAP`.
- [x] Build session-aware H1 from actual M1 observations.
- [x] Build project-owned New-York-midnight D1.
- [x] Test missing expected minute -> failure.
- [x] Test evidenced session break -> allowed without synthetic price.
- [x] Test provider-missing gap -> cannot be approved.
- [x] Test DST spring-forward D1 wall-clock semantics.
- [ ] Commit accepted-instrument regular availability/session implementation.
- [ ] Reconcile every 2019-2022 holiday/early-close deviation with independent evidence.
- [ ] Add accepted-instrument historical session fixtures.
- [ ] Cross-check canonical D1 against explicitly aligned provider data where appropriate.

Note: the repository connector blocked executable session-timetable writes during the 2026-08-13 qualification turn. This remains an explicit unresolved gate; no timetable was silently inferred in code.

## G. Detector compatibility — frozen

- [x] Add `CRT-DETECTOR-v0.2-MULTI-MARKET`.
- [x] Keep candidate version separate from underlying v0.1 alpha version.
- [x] Call the frozen v0.1 evaluator instead of reimplementing alpha validity.
- [x] Require emitted `TradePlan`s to retain v0.1 strategy version.
- [x] Require MID signal data and trusted v2 digest parity.
- [x] Achieve exact v0.1 fixture parity for state, reason, rule trace, evidence IDs, causal digest and TradePlan.
- [x] Freeze detector compatibility manifest before provider-backed outcomes.
- [x] Preserve legacy v0.1 Backtest Smoke.

Canonical artifacts:

- `docs/adr/ADR-008-multi-market-detector-compatibility.md`
- `strategy/CRT_V0.2_MULTI_MARKET_DETECTOR_COMPATIBILITY_MANIFEST.json`

## H. Detector-only activity protocol — frozen pre-outcome

Protocol: `P6B-MULTI-MARKET-ACTIVITY-PROTOCOL-v1`.

- [x] Reuse fixed `2019-01-01 .. 2022-12-31` New-York DEV activity period.
- [x] Require exact symbols to be frozen before activity access.
- [x] Require at least 2 accepted instruments.
- [x] Require at least 2 contributing instruments.
- [x] Require at least 30 pooled TradePlans.
- [x] Permit only detector counts/reason distributions.
- [x] Prohibit backtest/P&L/win-rate/expectancy/profit-factor/drawdown outcomes.
- [x] Machine-enforce 2/2/30 decision logic.
- [x] Test 29 pooled plans fails and 30 passes.
- [x] Freeze evaluator/test implementation before provider counts.

Possible decisions:

```text
INSUFFICIENT_ELIGIBLE_UNIVERSE
INSUFFICIENT_MULTI_MARKET_SAMPLE
SUFFICIENT_ACTIVITY_FOR_PERFORMANCE_PROTOCOL
```

Canonical artifacts:

- `experiments/phase6b/P6B_MULTI_MARKET_ACTIVITY_PROTOCOL_V1.md`
- `strategy/P6B_MULTI_MARKET_ACTIVITY_GATE_FREEZE_MANIFEST.json`

## I. Runtime qualification

### Qualification 001

- [x] Confirm secrets were present without exposing values.
- [x] Confirm token authorized 5 practice accounts.
- [x] Confirm original configured account belonged to that authorized set.
- [x] Record HTTP 403 on required account/instrument surfaces.
- [x] Seal `ACCOUNT_NOT_V20_ELIGIBLE_FOR_REQUIRED_ENDPOINTS`.

Canonical record: `experiments/phase6b/P6B_OANDA_RUNTIME_QUALIFICATION_001.md`.

### Qualification 002

- [x] Update runtime account secret externally without committing account identity.
- [x] Rerun the existing audited qualification job using the updated secret.
- [x] Confirm account summary is available.
- [x] Confirm account home currency is USD.
- [x] Confirm provider returned 123 instruments.
- [x] Confirm **4/4 precommitted source families matched**.
- [x] Verify the redacted qualification artifact is credential-free and outcome-locked.
- [x] Seal provider/account response hashes.

Canonical records:

- `experiments/phase6b/P6B_OANDA_RUNTIME_QUALIFICATION_002.json`
- `experiments/phase6b/P6B_OANDA_RUNTIME_QUALIFICATION_002.md`

## J. Exact universe freeze

- [x] Freeze `EUR_USD` for the EUR/USD family.
- [x] Freeze `XAU_USD` for the Gold/USD family.
- [x] Freeze `NAS100_USD` for the NQ proxy family.
- [x] Freeze `SPX500_USD` for the ES proxy family.
- [x] Freeze all four matched aliases; do not select a subset based on later counts/outcomes.
- [x] Satisfy the activity protocol's minimum eligible-universe threshold (`4 >= 2`).
- [x] Keep detector activity counts closed pending trusted historical datasets.

Canonical freeze: `experiments/phase6b/P6B_OANDA_UNIVERSE_FREEZE_001.md`.

## K. Price quantum — frozen pre-activity

- [x] Define provider price quantum from OANDA's price-precision policy, not as an asserted exchange tick/pip.
- [x] Freeze `EUR_USD = 0.00001`.
- [x] Freeze `XAU_USD = 0.001`.
- [x] Freeze `NAS100_USD = 0.1`.
- [x] Freeze `SPX500_USD = 0.1`.
- [x] Set source type to `PROVIDER_PRICE_PRECISION_POLICY`.
- [x] Add deterministic helper and unit tests.

Canonical decision: `docs/adr/ADR-010-oanda-provider-price-quantum.md`.

## L. Current historical-data gate

- [ ] Freeze executable regular availability/session rules for the four accepted symbols.
- [ ] Retrieve bounded/sealed MID M1 data for all four symbols for `2019-01-01 .. 2022-12-31`.
- [ ] Independently re-fetch selected sealed samples and compare values.
- [ ] Enumerate every unexpected historical missing interval.
- [ ] Evidence and version legitimate holiday/early-close closures; leave unexplained gaps fail-closed.
- [ ] Build deterministic H1 and New-York-midnight D1 for each symbol.
- [ ] Freeze one trusted `P6B_CANONICAL_PRICE_DATASET_V2` identity per symbol.
- [ ] Confirm no synthetic prices were introduced.
- [ ] Only after all four dataset identities are frozen, open detector activity counts.

## M. After trusted DEV datasets

- [ ] Run detector-only activity protocol; do not invoke backtester.
- [ ] Seal per-instrument and pooled TradePlan counts/reason distributions.
- [ ] Apply frozen 2/2/30 gate.
- [ ] If insufficient: preserve `INSUFFICIENT_MULTI_MARKET_SAMPLE` and stop without P&L.
- [ ] If sufficient: freeze OANDA execution/cost/conversion semantics.
- [ ] Build/freeze separately versioned multi-market simulator.
- [ ] Preregister full performance DEV/OOS/CONFIRM protocol.
- [ ] Only that later protocol may authorize P&L outcome access.

## Current handoff

```text
Phase 6B                           IN PROGRESS
Active successor                  BEARISH v0.1 ALPHA / MULTI-MARKET v0.2 RESEARCH
OANDA practice account            QUALIFIED
Available account instruments     123
Precommitted family matches       4 / 4
Frozen exact symbols              EUR_USD / XAU_USD / NAS100_USD / SPX500_USD
Provider price quantum            FROZEN PRE-ACTIVITY
Historical session exceptions     NOT YET RECONCILED
Trusted 2019-2022 datasets        NOT YET FROZEN
Detector activity counts          NOT OPENED
Multi-market P&L outcomes         NOT AUTHORIZED
v0.1 OOS / CONFIRM                UNOPENED
Phase 7                           BLOCKED
Live trading                      NOT AUTHORIZED
```
