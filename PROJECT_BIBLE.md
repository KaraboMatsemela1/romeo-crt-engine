# Romeo CRT Engine — Project Bible

**Repository:** `KaraboMatsemela1/romeo-crt-engine`  
**Status:** Phases 0–5 complete / `CRT-BACKTEST-v0.1` frozen for Phase-6 validation  
**Live trading:** **NOT AUTHORIZED**

This document is the canonical source of truth for the project. If implementation, research notes, an AI agent, or a proposed strategy conflicts with this document, the conflict must be surfaced and resolved explicitly rather than silently encoded.

---

## 1. Mission

Build an evidence-driven algorithmic trading research and execution platform that studies Romeo / `@Romeotpt`'s publicly demonstrated CRT methodology, translates it into deterministic machine-readable rules, validates those rules rigorously, and only after passing explicit gates allows them to progress through paper, shadow, and tightly controlled live execution.

The intended lifecycle is:

```text
Observe
  -> understand market context
  -> detect a valid CRT setup
  -> score setup quality
  -> run independent risk checks
  -> execute only if authorized
  -> manage and reconcile the trade
  -> journal every decision
  -> learn offline
  -> produce a candidate strategy/model
  -> revalidate before promotion
```

The system must always be able to explain why a trade was accepted or rejected using strategy version, rule IDs, market context, risk decision, and source-traceable logic.

---

## 2. Non-negotiable principles

1. **Evidence before implementation.** Romeo strategy rules are not assumed. They must be extracted, reconciled, and linked to sources.
2. **Deterministic core before ML.** The first production candidate is a deterministic state machine. ML may later rank already-valid setups.
3. **No LLM-to-broker path.** AI may research, propose, classify, review, and explain; it must never bypass strategy/risk controls or directly invent arbitrary live orders.
4. **Risk is independent.** A valid setup can still be rejected by the risk engine. Strategy confidence cannot override hard limits.
5. **Fail closed.** Missing/stale/invalid critical inputs mean `NO TRADE`.
6. **Production versions are frozen.** Self-learning creates candidates; it never rewrites the live strategy after a loss or short sequence of outcomes.
7. **No look-ahead.** Historical simulation may only use information available at the decision timestamp.
8. **Realistic friction.** Backtests must include spread, commission, slippage and other material execution costs.
9. **Negative results are first-class results.** Failed hypotheses are preserved and reported.
10. **Profitability is not proof of correctness.** First reproduce the intended methodology; then test whether it has an edge.

---

## 3. Project systems

### A. Research and knowledge system
Consumes public sources such as videos, transcripts/notes, chart examples, and clarifications. Produces a source registry, glossary, candidate rules, examples/counterexamples, contradictions, confidence levels, and open questions.

### B. Quantitative CRT engine
Converts verified strategy concepts into deterministic algorithms and a state machine. It detects market structure, ranges, liquidity, sweeps, context, confirmations, invalidations, entries, stops and targets according to the frozen strategy version.

### C. Trading and operations system
Consumes approved signals, applies independent risk controls, simulates or executes orders, reconciles broker state, journals decisions, and exposes observability and kill controls.

### D. Learning system
Uses historical journal/features to train candidate ranking or regime models offline. Candidate models must pass the same promotion discipline as strategy changes.

---

## 4. Canonical architecture

```text
Romeo public sources
        |
        v
Source registry / research notes
        |
        v
Strategy knowledge base
        |
        v
Frozen CRT specification
        |
        v
Market data -> market state -> CRT detector -> candidate setup
                                         |
                                         v
                                   setup scorer
                                         |
                                         v
                                  independent risk
                                   /            \
                                  v              v
                            backtest/paper   execution adapter
                                                   |
                                                   v
                                                 broker
                                                   |
                                                   v
                                           reconciliation
                                                   |
                                                   v
                                             trade journal
                                                   |
                                                   v
                                         offline learning
                                                   |
                                                   v
                                         candidate version
                                                   |
                                                   v
                                      validation/promotion gates
```

No component above the risk/execution boundary may circumvent it.

---

## 5. Strategy research protocol

For each relevant Romeo source:

1. Register it in `research/romeo/SOURCE_REGISTRY.csv`.
2. Capture stable metadata: source ID, title, URL, publication date, duration and relevance.
3. Analyze it using `VIDEO_ANALYSIS_TEMPLATE.md`.
4. Separate **explicit statements** from **inference**.
5. Extract candidate rules using `RULE_TEMPLATE.md`.
6. Add terminology to `GLOSSARY.md`.
7. Add ambiguity to `OPEN_QUESTIONS.md`.
8. Record valid examples and counterexamples.
9. Record contradictions with earlier material.
10. Assign confidence honestly.
11. Only after reconciliation should a rule be promoted into the draft strategy spec.

### Rule status vocabulary

```text
VERIFIED
HIGH_CONFIDENCE
HYPOTHESIS
UNRESOLVED
REJECTED
```

A missing parameter must remain unresolved rather than being chosen because it improves a backtest.

---

## 6. Strategy rule taxonomy

The research must determine, with evidence:

- market context
- higher-timeframe bias
- exact CRT range definition
- relevant liquidity
- exact sweep/manipulation definition
- displacement requirement, if any
- confirmation requirement
- exact entry trigger
- invalidation
- stop placement
- target selection
- session/trading-window rules
- timeframe relationships
- permitted instruments
- trade-management rules
- explicit no-trade conditions
- distinct setup variants

Every frozen rule must define inputs, parameters, deterministic predicate/algorithm, output/state transition, edge cases, positive examples, negative examples, tests and provenance.

---

## 7. CRT state-machine target

The first strategy candidate should be expressible as a deterministic state machine such as:

```text
WAIT_FOR_CONTEXT
 -> RANGE_IDENTIFIED
 -> WAIT_FOR_LIQUIDITY_EVENT
 -> LIQUIDITY_EVENT_DETECTED
 -> WAIT_FOR_CONFIRMATION
 -> CONFIRMED
 -> RISK_CHECK
 -> ENTER
 -> MANAGE_POSITION
 -> EXIT
```

The first frozen transition subset is defined in `strategy/CRT_V0.1_SPEC.md`; broader CRT doctrine transitions remain versioned research/strategy work.

---

## 8. Market-data standards

### Raw layer
Immutable provider payloads/records wherever practical.

### Normalized layer
Canonical fields such as:

```text
timestamp
instrument
open
high
low
close
volume
bid/ask or spread where available
source/provider
ingestion timestamp
quality flags
```

### Derived layer
Versioned features such as session, ATR/volatility, swing points, range boundaries, liquidity levels, sweep state, market structure, HTF bias and CRT state.

Derived features must be reproducible from data version + feature code version.

### Data-quality gates
Reject or quarantine duplicate timestamps, impossible OHLC values, unacceptable gaps, timezone ambiguity, inconsistent symbol mapping, future timestamps and provider metadata loss.

---

## 9. Multi-timeframe and session correctness

All timeframes must derive from a single authoritative chronology. A lower timeframe may not observe an unfinished higher-timeframe candle as though it were closed.

Internal timestamps use UTC. Session definitions must retain the market timezone required by the verified strategy and correctly handle daylight-saving changes.

---

## 10. Backtesting requirements

Final validation uses an event-driven simulator. Vectorized research is permitted for exploration but cannot be the sole basis for production claims.

The simulator must prevent:

- future-bar access
- early use of future-confirmed swing points
- using the final HTF close before the candle closes
- retrospectively choosing the best range
- future stop/target path leakage

Execution assumptions must include at least spread, commission, slippage, tick/lot constraints and financing/latency when material.

Run at minimum ideal, normal/base, stressed and severe-friction scenarios.

The first frozen simulator is `CRT-BACKTEST-v0.1`. It consumes immutable detector `TradePlan`s and does not reimplement strategy validity. Its H1 event clock manages positions that were already open through a bar before activating plans confirmed at that bar close. Same-bar stop/target ambiguity resolves stop-first conservatively; adverse stop gaps use the worse bar open; favorable target-gap price improvement is disabled; finite-data open positions remain censored unless a strategy-defined exit exists.

The current short simulation assumption is `SYNTHETIC_LINEAR_SHORT_RESEARCH_V1`. Because the first observation route is Binance BTCUSDT Spot while the frozen strategy is bearish-only, this is a research abstraction and not an assertion that Binance Spot can execute the modeled naked short.

---

## 11. Validation standard

A strategy does not progress because total profit or win rate looks attractive.

Track at least:

- total return and CAGR where meaningful
- expectancy in R and currency
- profit factor
- Sharpe and Sortino where meaningful
- maximum drawdown
- recovery factor
- win rate
- average win/loss
- average R
- trade count
- worst losing streaks
- exposure and turnover
- breakdown by instrument/session/time/regime where relevant

### Required validation sequence

1. rule-level tests
2. known-example reproduction
3. in-sample exploration
4. candidate freeze
5. out-of-sample test
6. rolling walk-forward analysis
7. parameter sensitivity/stability
8. transaction-cost stress
9. Monte Carlo sequence/fill stress
10. regime analysis
11. cross-instrument robustness when claimed
12. independent leakage/overfit review
13. paper trading
14. shadow trading
15. controlled live canary only with explicit authorization

Red flags include a narrow magic optimum, OOS collapse, edge disappearing under small cost changes, profits dominated by very few trades, unrealistic fills, or repeated reinterpretation after observing test results.

Phase 6 must also treat insufficient trade frequency as a valid result. A frozen candidate is not weakened merely to create a larger trade count.

---

## 12. Monte Carlo requirements

Estimate distributions for maximum drawdown, losing streaks, sequence risk, missed-trade sensitivity, slippage/spread degradation and probability of violating the capital/risk mandate.

The project is more interested in survival and robustness than in the prettiest historical equity curve.

---

## 13. Risk engine

Risk authorization is separate from strategy logic.

Controls must include or explicitly scope:

- risk per trade
- daily and weekly loss budget
- maximum drawdown
- maximum concurrent positions
- gross/net exposure
- correlated exposure
- per-instrument exposure
- spread/slippage threshold
- stale-data protection
- consecutive-loss/circuit-breaker behavior
- broker/internal reconciliation state
- emergency kill switch

Any unavailable critical risk input means rejection of new trades.

Example values such as `0.5%` risk per trade may be used as research defaults, but are not treated as optimal conclusions unless validated.

---

## 14. Execution safety

Execution infrastructure must support deterministic order intents, unique idempotency keys, acknowledgement tracking, rejection handling, partial fills where relevant, duplicate-order protection, position reconciliation, startup reconciliation, stale-price checks, price sanity limits, clock monitoring, persistent order events, and controlled shutdown.

The broker is the external source of truth for actual positions. If broker state disagrees with internal state, new trading should stop until reconciled.

---

## 15. Journal and auditability

Record accepted and rejected candidates. Each decision should retain:

```text
event timestamp
strategy version
code/git version
data version
instrument/direction
market context
features
rule results
setup score
risk decision
order intent
broker events
exit/result
reason codes
```

The journal is both the production audit trail and the future learning dataset.

---

## 16. Self-learning policy

Do **not** implement:

```text
loss -> AI rewrites strategy -> next live trade uses new rule
```

Implement:

```text
production journal
 -> offline learning
 -> candidate strategy/model
 -> backtest
 -> OOS/walk-forward
 -> shadow/paper validation
 -> promotion review
 -> frozen production version
```

Suggested statuses:

```text
RESEARCH
 -> CANDIDATE
 -> FROZEN_FOR_VALIDATION
 -> PAPER
 -> SHADOW
 -> LIVE_CANARY
 -> LIVE_APPROVED
 -> RETIRED
```

---

## 17. ML policy

The first useful ML task is expected to be **setup-quality ranking** after deterministic CRT validity has already been established.

Possible features include session, volatility, range size, sweep depth, HTF context, distance to liquidity, day/time, previous-session state and entry configuration.

Requirements:

- time-aware splits
- leakage prevention
- simple baseline first
- calibration measurement
- feature/data/model versioning
- explainability
- drift monitoring
- deterministic strategy baseline retained
- no direct production promotion

---

## 18. AI-agent responsibilities

### ResearchAgent
Collects sources, extracts evidence, identifies contradictions and proposes structured rules.

### StrategyAgent
Turns verified concepts into deterministic specifications and tests. Cannot directly promote production.

### QuantAgent
Runs experiments, reports both positive and negative results, and challenges apparent edge.

### ReviewAgent
Searches for leakage, look-ahead, overfitting, survivorship/selection bias and implementation/spec mismatches.

### RiskAgent
Evaluates portfolio/risk policy and cannot relax hard limits autonomously.

### ExecutionAgent
Executes already-approved intents and records/reconciles broker state.

No single agent should invent, validate, approve and deploy its own trading rule.

---

## 19. Engineering standards

Start with Python 3.12+ for research and orchestration. Candidate tools include NumPy, pandas/Polars, PyArrow, Pydantic, pytest, Hypothesis, scikit-learn, LightGBM/XGBoost when justified, PostgreSQL, Parquet and an experiment registry such as MLflow.

Add Rust only after profiling proves a performance-critical need.

Quality expectations:

- typed public interfaces
- lint/format/type checks
- unit/integration/regression/strategy tests
- deterministic seeds
- reproducible dependency management
- no secrets in git
- CI before merge
- ADRs for architectural decisions

---

## 20. SDLC

```text
issue or research question
 -> branch
 -> implementation/research artifact
 -> tests/evidence
 -> docs
 -> pull request
 -> independent review
 -> merge
 -> strategy/model release tagging when applicable
```

Any change to strategy validity, entry, exit, stop, target, session/time logic, position sizing, feature transformation or ML threshold requires version-impact assessment and appropriate revalidation.

---

## 21. Phase roadmap

### Phase 0 — Engineering foundation
Build repository structure, Python project, CI, tests, configuration/secrets pattern, logging, storage contracts, docs, ADRs, agent contract and experiment conventions.

**Exit:** a clean clone can reproduce the development/test environment without hidden manual steps.

### Phase 1 — Romeo corpus acquisition
Catalogue relevant public videos, capture metadata, obtain permitted transcripts/notes, tag relevance, extract terminology/rules/examples/session/timeframe/entry/SL/TP/management statements, identify contradictions and build rule provenance.

**Exit:** every candidate concept is traceable to evidence and the relevant corpus is indexed.

### Phase 2 — Formal CRT specification
Formalize range, liquidity, sweep, context, confirmation, entry, stop, target, invalidation, sessions, timeframe relationships, no-trade conditions and setup variants. Build positive/negative fixtures and freeze `CRT-v0.1`.

**Exit:** no strategy-critical term remains intentionally vague in the frozen candidate; unresolved items are excluded or explicitly parameterized.

### Phase 3 — Market-data engine
Implement provider abstraction, historical ingestion, immutable raw data, normalization, timezone/DST handling, validation, gaps/duplicates, resampling, synchronized timeframes, sessions and dataset versioning.

**Exit:** a historical window can be reproduced deterministically from a trusted dataset.

### Phase 4 — CRT detection primitives
Implement candles, ranges, liquidity/manipulation state, context, confirmations, invalidations, entry/SL/TP candidates, explanations and source-derived fixtures around the frozen first route.

**Exit:** frozen examples and counterexamples reproduce without LLM judgement in the execution path and trusted canonical data can be consumed causally.

### Phase 5 — Backtester
Implement event clock, account/portfolio state, orders/fills, costs, stop/target sequencing, sizing, metrics, journals and deterministic run provenance around frozen detector outputs.

**Status:** **COMPLETE — `CRT-BACKTEST-v0.1` FROZEN FOR PHASE 6.**

**Exit achieved:** identical code/data/config/quantity contracts produce identical cost-aware results; lifecycle regressions cover target, stop, same-bar ambiguity, gaps, costs, activation conflicts and finite-data censoring; preregistered provider-backed integration succeeded.

The first preregistered September 2025 BTCUSDT sample produced 27 rolling detector candidates and **zero valid TradePlans**. All four cost scenarios therefore had zero closed trades and unchanged realized equity. This result is preserved as `INSUFFICIENT PERFORMANCE EVIDENCE`, not treated as profit or loss, and the period/strategy were not changed after observation.

### Phase 6 — Strategy validation
Preserve the frozen strategy/detector/simulator baseline, preregister development/OOS/final-confirmatory windows, build separately versioned trusted datasets, measure setup/trade frequency, and run OOS, walk-forward, parameter sensitivity, friction stress, Monte Carlo, regime/instrument/session breakdowns and independent leakage/overfit review when sample size supports them.

**Exit:** written decision to `REJECT`, `REVISE_AS_NEW_VERSION`, declare `INSUFFICIENT_EVIDENCE`, or `PROMOTE_TO_PAPER_CANDIDATE`.

### Phase 7 — Paper trading
Add live data, scheduler, independent risk service/module, paper broker, state persistence, alerts, reconciliation and comparison against simulated expectations.

**Exit:** realtime system semantics are stable and predefined observation/trade-count gates are met.

### Phase 8 — Learning engine
Build feature contract, interpretable setup-quality baseline, time-aware training, calibration, explainability, drift metrics, model registry and promotion policy.

**Exit:** ML demonstrates incremental OOS value without bypassing validity/risk controls.

### Phase 9 — Shadow trading
Consume production-like data and broker conditions but send no real orders. Measure executable prices, latency, slippage availability, reconciliation and failure handling.

**Exit:** operational discrepancies are understood and readiness controls pass.

### Phase 10 — Controlled live deployment
Requires explicit owner authorization, tiny canary capital, tested kill switch/reconciliation, alerts/on-call process, daily risk reporting, drift monitoring, rollback and predefined scale/stop criteria.

**Exit:** only after live-canary criteria pass may capital be deliberately increased.

---

## 22. First major milestone — M1 Romeo CRT Strategy Reproduction

M1 requires:

- relevant Romeo corpus catalogued
- glossary established
- every frozen rule linked to evidence
- explicit vs inferred rules separated
- examples and counterexamples catalogued
- strategy-critical ambiguity resolved or excluded
- `CRT-v0.1` frozen
- machine-readable fixtures created
- detector reproduces known examples
- tests cover each rule

**M1 has intentionally zero profitability requirement.** Correct representation comes before edge testing.

---

## 23. Experiment governance

Every experiment records:

- experiment ID and hypothesis
- strategy/model version
- git commit
- dataset/version and exact time window
- instruments/timeframes
- cost assumptions
- parameters/configuration
- random seed where applicable
- metrics and artifacts
- conclusion and weaknesses
- exploratory vs confirmatory classification

Do not overwrite or hide failed experiments.

---

## 24. Prohibited practices

- optimizing against the final test set
- deleting losing periods without predeclared justification
- silently changing rule meaning after seeing results
- look-ahead or future-confirmed features
- cherry-picking instruments/parameters without robust validation
- presenting simulated returns as guaranteed/expected live returns
- allowing an LLM to place discretionary live broker orders
- committing broker/API credentials
- martingale/averaging-down behavior unless separately researched, bounded and approved
- disabling risk controls because a setup appears unusually strong
- automatic capital scale-up based on short-term P&L

---

## 25. Current status

```text
Phase 0  Engineering foundation     COMPLETE
Phase 1  Romeo corpus acquisition   COMPLETE
Phase 2  Formal strategy spec       COMPLETE — FROZEN_FOR_VALIDATION
Phase 3  Market data                COMPLETE
Phase 4  CRT detector               COMPLETE — CRT-DETECTOR-v0.1 FROZEN
Phase 5  Backtester                 COMPLETE — CRT-BACKTEST-v0.1 FROZEN
Phase 6  Validation                 READY TO START
Phase 7  Paper trading              NOT STARTED
Phase 8  Learning engine            NOT STARTED
Phase 9  Shadow trading             NOT STARTED
Phase 10 Controlled live            NOT AUTHORIZED
```

The current frozen validation handoff is:

```text
strategy   CRT-C3-D1-H1-M1-BEAR-v0.1
detector   CRT-DETECTOR-v0.1
simulator  CRT-BACKTEST-v0.1
```

Machine-readable freezes:

```text
strategy/CRT_V0.1_FREEZE_MANIFEST.json
strategy/CRT_V0.1_DETECTOR_FREEZE_MANIFEST.json
strategy/CRT_V0.1_BACKTEST_FREEZE_MANIFEST.json
```

Phase 3 established provider-backed immutable/verified market data and froze dataset `ee1300f0da50e4debcbbc3b7` as a compact detector-integration fixture.

Phase 4 enforces trusted-manifest/content equality, exhaustive rolling C1/C2/C3 enumeration, future-C3 D1 leakage protection, frozen-fixture parity and deterministic candidate/rejection explanations.

Phase 5 validates simulator semantics and reproducibility. The preregistered September 2025 provider-backed replay produced 27 rolling C1/C2/C3 candidates but zero valid TradePlans. Therefore no strategy performance conclusion is possible from that month. Negative/zero-activity evidence is preserved without loosening the frozen strategy.

The largest current need is now a preregistered Phase-6 validation protocol plus larger separately versioned trusted historical windows. Profitability has not been established.

---

## 26. Immediate next actions

1. Write and freeze the Phase-6 validation protocol before observing the next historical results.
2. Mechanically select development, OOS and untouched final-confirmatory windows before retrieval/analysis.
3. Define minimum trade-count / insufficient-evidence criteria before seeing outcomes.
4. Build trusted separately versioned datasets for those windows.
5. Measure candidate and valid-TradePlan frequency with the frozen strategy/detector unchanged.
6. Run the predeclared IDEAL/BASE/STRESSED/SEVERE cost matrix.
7. Run parameter sensitivity only as a robustness diagnostic; any rule change becomes a new strategy version and cannot overwrite v0.1.
8. Add walk-forward, Monte Carlo and regime/session analysis only when sample size supports meaningful inference.
9. Produce a written Phase-6 decision: `REJECT`, `REVISE_AS_NEW_VERSION`, `INSUFFICIENT_EVIDENCE`, or `PROMOTE_TO_PAPER_CANDIDATE`.
10. Do not promote to paper/shadow/live without their explicit gates; `LIVE_TRADING_AUTHORIZED = false` remains unchanged.

---

## 27. Governance of this bible

Material changes to research methodology, validation gates, independent risk authority, self-learning behavior, or live-trading authorization require explicit review and should be captured with an ADR where architectural/governance intent changes.
