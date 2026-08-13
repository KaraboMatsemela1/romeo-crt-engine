# Phase 6B — Candidate Revision Checklist

**Status:** **IN PROGRESS — HISTORICAL OANDA DATA QUALIFICATION**  
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
- [x] Add token-authorized-account preflight that prints only count and configured-account authorization boolean.

### Historical paging / provenance mechanics

- [x] Add deterministic M1 request-window generation with maximum 5000 candles/page.
- [x] Freeze 4500-minute default pages.
- [x] Redact account identity from request fingerprints.
- [x] Seal every page with request SHA-256 and raw response SHA-256.
- [x] Merge pages chronologically.
- [x] Deduplicate identical boundary candles.
- [x] Reject conflicting duplicate candles across page boundaries.
- [x] Treat provider-confirmed empty `M1` pages as raw provenance, not fabricated price data.
- [x] Add provider-value normalization independent of raw HTTP payload serialization.
- [x] Add leading/internal/trailing missing-interval enumeration.
- [x] Add exact independent re-fetch comparison primitives.

## E. Provider-neutral price data — completed offline

- [x] Preserve legacy Binance Phase-3 schema unchanged.
- [x] Add `P6B_CANONICAL_PRICE_DATASET_V2`.
- [x] Make price component first-class dataset identity.
- [x] Type activity semantics explicitly.
- [x] Require explicit positive pre-frozen price quantum before `TRUSTED` detector use.
- [x] Add deterministic v2 serialization/digests.
- [x] Convert OANDA M1 to v2 without fabricated volume/trade semantics.

## F. Session/gap and canonical aggregation

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
- [x] Record first-party evidence that NAS100/SPX500 hours changed inside DEV on 2021-06-28.
- [x] Refuse to project today's OANDA hours backward across the complete historical window.
- [ ] Freeze date-segmented OANDA session policies after raw-gap reconciliation.
- [ ] Freeze historical holiday/early-close evidence for all removed observations.
- [ ] Add accepted-instrument historical session fixtures.
- [ ] Cross-check canonical D1 against an explicitly aligned provider query where appropriate.

Canonical evidence: `experiments/phase6b/P6B_OANDA_HISTORICAL_SESSION_EVIDENCE_001.md`.

## G. Signal-price decision — frozen pre-outcome

- [x] Freeze signal OHLC to OANDA **MID / `price=M`**.
- [x] Freeze unsmoothed M1 as canonical signal-source retrieval.
- [x] Keep BID/ASK separate for later execution/friction evidence.
- [x] Make signal price component part of dataset identity/digest.

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

## I. Detector-only activity protocol — frozen pre-outcome

Protocol: `P6B-MULTI-MARKET-ACTIVITY-PROTOCOL-v1`.

- [x] Reuse the fixed 2019-01-01..2022-12-31 New-York DEV activity period.
- [x] Require exact instrument symbols to be frozen before any activity count is opened.
- [x] Require at least **2 accepted instruments**.
- [x] Require at least **2 contributing instruments**.
- [x] Retain minimum **30 pooled TradePlans**.
- [x] Allow only detector counts/reason distributions after trusted-data promotion.
- [x] Explicitly prohibit backtest/P&L/win-rate/expectancy/profit-factor/drawdown outcomes.
- [x] Machine-enforce the 2/2/30 decision logic.
- [x] Test 29 pooled TradePlans fails and 30 passes.
- [x] Freeze the protocol/evaluator/test implementation before provider counts.

## J. Runtime OANDA account/universe gate — COMPLETE

- [x] Preserve failed first account route as `P6B_OANDA_RUNTIME_QUALIFICATION_001`.
- [x] Update runtime account secret to an API-eligible practice account.
- [x] Confirm token authorizes the configured practice account.
- [x] Confirm account summary is available.
- [x] Discover 123 account instruments.
- [x] Match all 4 / 4 precommitted source families.
- [x] Freeze exact API symbols before detector activity access:
  - [x] `EUR_USD`
  - [x] `XAU_USD`
  - [x] `NAS100_USD`
  - [x] `SPX500_USD`
- [x] Freeze account/instrument metadata digests.
- [x] Freeze provider price quantum before activity access.
- [x] Confirm no detector activity count or P&L was opened during qualification.

## K. Historical-data qualification protocol — FROZEN / COLLECTION PENDING

Protocol: `P6B-OANDA-HISTORY-QUALIFICATION-V1`.

- [x] Freeze exact four-symbol universe.
- [x] Freeze practice / redacted account scope.
- [x] Freeze MID/M1, unsmoothed retrieval.
- [x] Freeze UTC raw interval `2019-01-01T00:00:00Z .. 2023-01-01T00:00:00Z` exclusive.
- [x] Freeze 4500-minute pages with 5000-candle hard maximum.
- [x] Freeze four independent one-hour provider-value re-fetch windows before full collection.
- [x] Freeze raw missing intervals to initial `UNRECONCILED` state.
- [x] Freeze no-synthetic-price rule.
- [x] Explicitly prohibit detector execution, TradePlan counts, reason distributions and all P&L metrics during data qualification.
- [x] Execute real 2019 historical MID/M1 smoke against all four frozen symbols.
- [x] Confirm smoke returns 60 / 60 complete M1 candles for every symbol.
- [x] Preserve request/raw-response/provider-value hashes without account credentials or raw price values in repo evidence.
- [ ] Collect complete sealed raw DEV M1 history for all four frozen instruments.
- [ ] Execute 4 / 4 independent re-fetch comparisons per instrument.
- [ ] Inventory every missing interval.
- [ ] Reconcile every removed expected observation to date-valid first-party session/holiday evidence.
- [ ] Leave unresolved/provider-missing intervals fail-closed.
- [ ] Build trusted H1 and New-York-midnight D1 datasets.
- [ ] Freeze one detector-facing `P6B_CANONICAL_PRICE_DATASET_V2` identity per trusted instrument.

Canonical artifacts:

- `experiments/phase6b/P6B_OANDA_HISTORY_QUALIFICATION_PROTOCOL_V1.md`
- `experiments/phase6b/P6B_OANDA_HISTORICAL_SESSION_EVIDENCE_001.md`
- `experiments/phase6b/P6B_OANDA_HISTORY_SMOKE_001.md`

## L. After trusted historical datasets exist

If fewer than two instruments reach `TRUSTED`, terminate before detector counts as `INSUFFICIENT_ELIGIBLE_UNIVERSE`.

If at least two are trusted:

- [ ] Freeze the exact trusted-instrument set before detector execution.
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
OANDA provider/account            QUALIFIED
Exact frozen universe             EUR_USD / XAU_USD / NAS100_USD / SPX500_USD
Historical protocol               FROZEN
2019 four-symbol M1 smoke         PASS 60/60 EACH
Historical session calendar       PARTIAL / DATE-SEGMENTED EVIDENCE REQUIRED
Complete 2019-2022 raw M1         PENDING
Trusted H1 / NY-D1 datasets       PENDING
Detector activity counts          NOT OPENED
Multi-market P&L outcomes         NOT AUTHORIZED
v0.1 OOS / CONFIRM                UNOPENED
Phase 7                           BLOCKED
Live trading                      NOT AUTHORIZED
```
