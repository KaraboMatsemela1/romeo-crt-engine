# Phase 6B — Candidate Revision Checklist

**Status:** **IN PROGRESS — RUNTIME OANDA DATA QUALIFICATION REQUIRED**  
**Active research target:** `CRT-C3-D1-H1-M1-BEAR-v0.2-MULTI-MARKET-RESEARCH`  
**Underlying frozen alpha:** `CRT-C3-D1-H1-M1-BEAR-v0.1`  
**Preserved failed research path:** `CRT-C3-D1-H1-M1-BULL-v0.2-RESEARCH` -> `EVIDENCE_INSUFFICIENT`  
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
- [x] Establish that bullish CRT states are source-backed.
- [x] Preserve the broader `CRTH/L -> 50%` evidence.
- [x] Refuse to infer the exact bullish order path from bearish code symmetry.
- [x] Close Gate 6B-1 as **`EVIDENCE_INSUFFICIENT`**.
- [x] Confirm no bullish historical strategy outcome was opened.

Canonical decision: `research/romeo/phase6b/BULLISH_MODEL1_GATE_DECISION.md`.

## C. Active successor — multi-market observation expansion

- [x] Select `CRT-C3-D1-H1-M1-BEAR-v0.2-MULTI-MARKET-RESEARCH`.
- [x] Preserve the frozen bearish v0.1 alpha rules without relaxation.
- [x] Use Romeo/source relevance—not P&L—as the market-universe motivation.
- [x] Precommit source families: NAS100/NQ proxy, SPX500/ES proxy, EUR/USD, Gold/USD.
- [x] Keep SMT inactive.
- [x] Select OANDA v20 for provider qualification subject to actual account/division availability.
- [x] Prohibit post-count or post-P&L instrument cherry-picking.

Canonical selection: `research/romeo/phase6b/MULTI_MARKET_CANDIDATE_SELECTION.md`.

## D. OANDA provider/data engineering — completed offline

### Provider and credentials boundary

- [x] Add OANDA v20 provider adapter.
- [x] Support account-specific instrument discovery.
- [x] Support M1 `M`, `B`, and `A` candle parsing.
- [x] Skip incomplete candle tails by default.
- [x] Reject duplicate/out-of-order provider observations.
- [x] Never synthesize missing observations.
- [x] Keep OANDA `volume` as typed `PRICE_COUNT`, not exchange volume/trade count.
- [x] Keep account ID and bearer token out of persisted qualification artifacts.
- [x] Default runtime qualification to OANDA practice.
- [x] Require explicit opt-in for any live read.
- [x] Add runtime env variable names only; no values committed.
- [x] Add manual practice-only GitHub Actions qualification workflow.

Canonical provider decision: `docs/adr/ADR-006-oanda-v20-multi-market-qualification.md`.

### Redacted execution metadata discovery

- [x] Upgrade discovery schema to `P6B_OANDA_INSTRUMENT_DISCOVERY_V2`.
- [x] Capture instrument type, display precision, pip location and trade-unit precision.
- [x] Capture minimum trade size.
- [x] Capture maximum order units and maximum position size when returned.
- [x] Capture instrument margin rate when returned.
- [x] Capture commission structure when returned.
- [x] Capture financing rates/days when returned.
- [x] Capture guaranteed-stop mode when returned.
- [x] Capture provider unit precision step separately from price quantum.
- [x] Add redacted account summary parser for home currency, account margin rate, hedging and GSLO mode.
- [x] Deliberately omit account ID, balance and NAV from the qualification artifact.
- [x] Continue to prohibit deriving `price_tick_size` from `displayPrecision`.

### Historical retrieval provenance

- [x] Add deterministic M1 request-window generation with maximum 5000 candles/page.
- [x] Default to 4500-minute pages.
- [x] Redact account identity from request fingerprints.
- [x] Seal every page with request SHA-256 and raw response SHA-256.
- [x] Merge pages chronologically.
- [x] Deduplicate identical boundary candles.
- [x] Reject conflicting duplicate candles across page boundaries.
- [x] Build deterministic retrieval-level provenance digest.

## E. Provider-neutral price data — completed offline

- [x] Preserve legacy Binance Phase-3 schema unchanged.
- [x] Add `P6B_CANONICAL_PRICE_DATASET_V2`.
- [x] Make price component first-class dataset identity.
- [x] Type activity semantics explicitly.
- [x] Require explicit positive pre-frozen price quantum before `TRUSTED` detector use.
- [x] Add deterministic v2 serialization/digests.
- [x] Convert OANDA M1 to v2 without fabricated volume/trade semantics.

Canonical decision: `docs/adr/ADR-007-provider-neutral-canonical-price-data.md`.

## F. Session/gap and canonical aggregation — mechanics completed, actual schedules pending

- [x] Add gap categories: `MARKET_CLOSED`, `SESSION_BREAK`, `HOLIDAY_OR_EARLY_CLOSE`, `PROVIDER_MISSING`, `UNKNOWN_GAP`.
- [x] Allow only evidenced closure/session/holiday categories to remove expected observations.
- [x] Prohibit `PROVIDER_MISSING` and `UNKNOWN_GAP` from being treated as expected downtime.
- [x] Build session-aware H1 from actual M1 observations.
- [x] Build project-owned New-York-midnight D1.
- [x] Keep provider-native default Daily alignment from redefining strategy D1.
- [x] Test missing expected minute -> fail closed.
- [x] Test evidenced session break -> allowed without synthetic price.
- [x] Test provider-missing gap -> cannot be approved.
- [x] Test spring-forward D1 -> 23 absolute hours while remaining NY midnight-to-midnight.
- [ ] Freeze actual OANDA account/division + instrument session policies for accepted symbols.
- [ ] Freeze holiday/early-close evidence for validation windows.
- [ ] Add accepted-instrument session fixtures.
- [ ] Cross-check canonical D1 against an explicitly aligned provider query where appropriate.

## G. Signal-price decision — frozen pre-outcome

- [x] Freeze signal OHLC to OANDA **MID / `price=M`**.
- [x] Freeze unsmoothed M1 as canonical signal-source retrieval.
- [x] Keep BID/ASK separate for later execution/friction evidence.
- [x] Make signal price component part of dataset identity/digest.

Canonical decision: `experiments/phase6b/P6B_OANDA_PRICE_COMPONENT_DECISION.md`.

## H. Detector compatibility — completed and frozen

- [x] Add `CRT-DETECTOR-v0.2-MULTI-MARKET`.
- [x] Record candidate version separately from underlying alpha version.
- [x] Call the frozen v0.1 evaluator rather than reimplement alpha validity.
- [x] Require all emitted `TradePlan`s to retain v0.1 strategy version.
- [x] Require MID signal data.
- [x] Require trusted v2 content digest parity.
- [x] Confirm provider activity metadata is not an alpha input.
- [x] Achieve exact v0.1 fixture parity for state, reason, rule trace, evidence IDs, causal digest and TradePlan.
- [x] Freeze compatibility manifest before provider-backed outcomes.
- [x] Preserve legacy v0.1 regressions and Backtest Smoke.

Canonical artifacts:

- `docs/adr/ADR-008-multi-market-detector-compatibility.md`
- `strategy/CRT_V0.2_MULTI_MARKET_DETECTOR_COMPATIBILITY_MANIFEST.json`

## I. Detector-only activity protocol — completed and frozen pre-outcome

Protocol: `P6B-MULTI-MARKET-ACTIVITY-PROTOCOL-v1`.

- [x] Reuse the fixed 2019-01-01..2022-12-31 New-York DEV activity period.
- [x] Require exact instrument symbols to be frozen before any activity count is opened.
- [x] Require at least **2 accepted instruments**.
- [x] Require at least **2 contributing instruments**.
- [x] Retain minimum **30 pooled TradePlans**.
- [x] Allow only detector counts/reason distributions.
- [x] Explicitly prohibit backtest/P&L/win-rate/expectancy/profit-factor/drawdown outcomes.
- [x] Machine-enforce the 2/2/30 decision logic.
- [x] Test 29 pooled TradePlans fails and 30 passes.
- [x] Freeze the protocol/evaluator/test implementation before provider counts.
- [x] Verify activity-gate implementation with CI and preserved Backtest Smoke.

Possible decisions:

```text
INSUFFICIENT_ELIGIBLE_UNIVERSE
INSUFFICIENT_MULTI_MARKET_SAMPLE
SUFFICIENT_ACTIVITY_FOR_PERFORMANCE_PROTOCOL
```

A sufficient activity result still does **not** authorize P&L.

Canonical artifacts:

- `experiments/phase6b/P6B_MULTI_MARKET_ACTIVITY_PROTOCOL_V1.md`
- `strategy/P6B_MULTI_MARKET_ACTIVITY_GATE_FREEZE_MANIFEST.json`

## J. Execution evidence boundary — partially frozen, simulator intentionally blocked

- [x] Record OANDA buy/long as positive units and sell/short as negative units.
- [x] Separate unit precision step from price quantum.
- [x] Record minimum/maximum unit constraints as account/instrument metadata.
- [x] Record natural short-open sell/BID-side and short-close buy/ASK-side execution evidence.
- [x] Capture commission, financing and home-currency dependencies during qualification.
- [x] Decide not to reuse the synthetic-linear BTCUSDT simulator blindly for OANDA.
- [ ] Freeze actual accepted-instrument price quantum.
- [ ] Freeze actual account/instrument commission/base execution contract.
- [ ] Freeze historical BID/ASK synchronization and fill rules.
- [ ] Freeze home-currency conversion methodology.
- [ ] Freeze quantity/risk sizing translation by accepted instrument.
- [ ] Create multi-market simulator only if the detector-only activity gate passes.

Canonical decision: `docs/adr/ADR-009-oanda-execution-evidence-boundary.md`.

## K. Runtime Gate 6B-MM-1 — current hard blocker

Requires runtime-only OANDA **practice** credentials:

```text
OANDA_ACCOUNT_ID
OANDA_API_TOKEN
```

The repo/tooling is ready to execute the qualification without persisting either credential.

Outstanding runtime work:

- [ ] Run actual OANDA practice account summary + instrument discovery.
- [ ] Confirm exact availability of the precommitted source-family instruments.
- [ ] Freeze exact API symbols before detector activity access.
- [ ] Freeze account/instrument metadata digests.
- [ ] Resolve accepted-instrument price quantum from an authoritative contract.
- [ ] Freeze actual session/holiday policy per accepted symbol.
- [ ] Retrieve bounded/sealed MID M1 samples.
- [ ] Independently re-fetch selected sealed samples and compare provider values.
- [ ] Freeze the exact DEV dataset identities.

## L. After runtime data qualification

If fewer than two source-family instruments are eligible, terminate the activity protocol as `INSUFFICIENT_ELIGIBLE_UNIVERSE` without opening detector counts.

If at least two are eligible:

- [ ] Commit the exact-symbol universe freeze amendment.
- [ ] Run detector-only activity protocol; do not invoke the backtester.
- [ ] Seal the activity result.
- [ ] If activity < 30 pooled TradePlans or <2 contributing instruments: stop as `INSUFFICIENT_MULTI_MARKET_SAMPLE`.
- [ ] If activity passes: freeze OANDA execution/cost/conversion semantics.
- [ ] Build/freeze a separately versioned multi-market simulator.
- [ ] Preregister full performance DEV/OOS/CONFIRM protocol.
- [ ] Only that later protocol may authorize P&L outcome access.

## Current handoff

```text
Phase 6B                           IN PROGRESS
Bullish successor                 EVIDENCE_INSUFFICIENT / PRESERVED
Active successor                  BEARISH v0.1 ALPHA / MULTI-MARKET v0.2 RESEARCH
Alpha changes                     NONE AUTHORIZED
OANDA provider/parser             IMPLEMENTED + TESTED
Redacted account metadata         IMPLEMENTED + TESTED
Execution-aware instrument schema IMPLEMENTED + TESTED
Paged history provenance          IMPLEMENTED + TESTED
Provider-neutral price data v2    IMPLEMENTED + TESTED
Session-aware aggregation engine  IMPLEMENTED + TESTED
Actual session schedules          NOT FROZEN
Signal price component            MID / FROZEN PRE-OUTCOME
Multi-market detector             PARITY VERIFIED + FROZEN
Activity protocol                 2 / 2 / 30 + P&L FIREWALL / FROZEN
Runtime qualification workflow    READY
Actual OANDA account discovery    NOT RUN — EXTERNAL RUNTIME DEPENDENCY
Exact instrument universe         NOT FROZEN
Detector activity counts          NOT OPENED
Multi-market P&L outcomes         NOT AUTHORIZED
v0.1 OOS / CONFIRM                UNOPENED
Phase 7                           BLOCKED
Live trading                      NOT AUTHORIZED
```
