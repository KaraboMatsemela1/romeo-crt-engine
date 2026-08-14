# Phase 6B — Candidate Revision Selection

**Date:** 2026-08-13  
**Status:** **IN PROGRESS — RESEARCH PRECOMMITMENT**  
**Predecessor:** `CRT-C3-D1-H1-M1-BEAR-v0.1`  
**Selected research target:** `CRT-C3-D1-H1-M1-BULL-v0.2-RESEARCH`  
**Executable:** **NO**  
**Frozen for validation:** **NO**  
**Historical outcome access authorized:** **NO NEW ACCESS**  
**Paper / shadow / live:** **NOT AUTHORIZED**

## Purpose

Phase 6B exists because the frozen v0.1 candidate completed its preregistered DEV gate with `INSUFFICIENT_EVIDENCE`. The correct response is not to relax v0.1 after observing its result. It is to return to evidence that was already deferred before validation, choose one independently motivated expansion hypothesis, verify it from source material, and assign it a new strategy version.

This document records that choice before any v0.2 historical performance is inspected.

## Immutable predecessor

The following chain remains historical evidence and must not be rewritten:

```text
strategy   CRT-C3-D1-H1-M1-BEAR-v0.1
detector   CRT-DETECTOR-v0.1
simulator  CRT-BACKTEST-v0.1.1
DEV result INSUFFICIENT_EVIDENCE
```

The v0.1 OOS and CONFIRM windows remain unopened. Phase 6B does not authorize inspecting them, tuning against them, or relabeling them as development data.

## Candidate-selection rule

A Phase 6B successor may be selected only because it is:

1. supported by pre-existing source/evidence debt;
2. narrow enough to isolate one strategy change;
3. implementable causally once its remaining evidence gate closes;
4. compatible with the project's existing trusted data and execution semantics where possible; and
5. selected without comparing historical P&L among alternatives.

Trade count alone is not a reason to add a rule.

## Alternatives considered

### A — Bullish D1 -> H1 Model #1 mirror

**Disposition:** **SELECTED FOR PRIMARY-SOURCE VERIFICATION**

Why it is the best next research target:

- bullish representativeness was already recorded as a deferred/validation debt before the Phase-6 result;
- the Episode-1 research extraction records a bullish Model #1 inverse example around an old low / down-close model candle, although that extraction is still provisional and requires primary-source confirmation;
- first-party material independently establishes `CRTH/L -> 50%` as a core CRT extreme-to-objective relationship and acknowledges convincing bullish CRT states;
- it keeps the already deterministic D1 parent and H1 execution route, avoiding the unresolved H4 candle-anchor problem;
- it changes direction/setup symmetry rather than introducing a new timeframe, new entry family, cross-market dependency, or new target-management system.

This is a **research target**, not evidence that the bullish mirror is already deterministic.

### B — H4 parent -> M15 Model #1

**Disposition:** DEFER

Reason: Romeo's timeframe-pairing evidence is useful, but the exact H4 clock-anchor sequence is still unresolved. A four-hour boundary choice changes the parent range, sweep, midpoint, Candle-2 close, Candle-3 window and Model #1 observations. Provider defaults may not be substituted.

### C — W1 parent -> H4 Model #1

**Disposition:** DEFER

Reason: the Weekly reference open is substantially better evidenced than H4, but the execution leg is H4-dependent. Until H4 boundaries and venue/session treatment are closed, this route is not validation-ready.

### D — True MSS entry family

**Disposition:** DEFER

Reason: the corpus supports True MSS as a Romeo entry family, but exact swing construction, qualifying reference high/low, break condition, entry region and relation to SMT/Turtle Soup/FVG remain underdefined. Generic BOS/MSS is prohibited as a substitute.

### E — SMT substitution / direct SMT expansion

**Disposition:** DEFER

Reason: pair registry, polarity, corresponding-extreme semantics, synchronization and substitution rules are unresolved. SMT remains context/confirmation and must not directly emit orders.

### F — KOD, countertrend, journey-to-key-level, Candle-2 trading, adaptive 50%, time exits

**Disposition:** DEFER

Reason: each introduces a separate unresolved predicate or a hindsight/curve-fitting surface. Bundling any of them into the first successor would make causal attribution impossible.

### G — Change v0.1 numerical parameters to generate more trades

**Disposition:** **PROHIBITED AS PHASE-6B SELECTION LOGIC**

Examples include lowering the Model #1 `thick` threshold, changing midpoint-consumption handling, widening reference tolerances, changing stop buffer, or weakening confirmation solely because the DEV sample was sparse.

A parameter change may become a later separately justified candidate only if independently motivated and preregistered; it cannot be reverse-engineered from the v0.1 outcome.

## Selected research candidate

```text
Candidate ID        CRT-C3-D1-H1-M1-BULL-v0.2-RESEARCH
Doctrine snapshot   CRT_SECRETS_2025
Parent timeframe    D1
Execution timeframe H1
Calendar             existing NY-midnight D1 / completed H1 route
Setup family         reaction from parent CRT extreme
Direction            BULLISH ONLY — pending evidence gate
Entry family         Model #1 core — bullish semantics pending evidence gate
Target family        parent 50% candidate — pending bullish source verification
Risk boundary        independent / unchanged architecturally
Unknown state        NO_SIGNAL
```

The candidate is intentionally **bullish-only**, rather than immediately creating a bidirectional strategy. This isolates the new hypothesis. A future combined strategy would require its own portfolio/interaction semantics and validation decision.

## What is inherited versus reopened

### Inherited engineering invariants

Unless new evidence proves an incompatibility, Phase 6B preserves:

- causal information availability;
- New-York wall-clock D1 construction;
- completed-H1 execution observations;
- immutable parent measurements after close;
- `UNKNOWN -> NO_SIGNAL`;
- target predeclaration;
- independent risk approval;
- deterministic detector/backtester separation;
- provenance, journaling and strategy-version discipline;
- conservative execution/friction accounting;
- no synthetic market observations.

### Reopened alpha predicates

The bullish candidate must **not** inherit bearish rules by code symmetry without evidence. The evidence gate must explicitly close:

1. bullish parent manipulation around C1 `CRTL`;
2. whether `old CRTL` is a qualifying bullish reaction reference for this setup family;
3. bullish Model #1 candle geometry and confirmation;
4. bullish structural stop reference;
5. bullish target / 50% semantics;
6. target-consumption / expiry semantics where direction matters;
7. any numerical parameter that cannot be justified as direction-neutral.

## Anti-overfit precommitment

Before the bullish evidence gate closes:

```text
V0_1_MUTATION_AUTHORIZED             = false
V0_2_HISTORICAL_OUTCOME_ACCESS       = false
V0_2_PARAMETER_OPTIMIZATION          = false
V0_1_OOS_OUTCOME_ACCESS_AUTHORIZED   = false
V0_1_CONFIRM_OUTCOME_ACCESS_AUTHORIZED = false
PAPER_TRADING_AUTHORIZED             = false
LIVE_TRADING_AUTHORIZED              = false
```

The team must not:

- search historical BTCUSDT results to decide what the bullish rules should be;
- select bullish thresholds by maximizing trade count or P&L;
- inspect v0.1 reserved OOS/CONFIRM windows to guide v0.2 design;
- assume every bearish predicate has a valid bullish inverse;
- bundle extra variants merely to exceed a minimum sample gate.

## Phase 6B gates

### Gate 6B-1 — primary-source evidence closure

Close the predicates in `BULLISH_MODEL1_EVIDENCE_GATE.md` using direct source material and contradiction reconciliation.

**Exit:** `EVIDENCE_SUFFICIENT_TO_SPECIFY` or `EVIDENCE_INSUFFICIENT`.

### Gate 6B-2 — deterministic v0.2 draft

Only after Gate 6B-1 passes:

- create a formal v0.2 strategy specification;
- create positive and negative fixtures before historical outcome testing;
- implement separate v0.2 rule contracts without changing v0.1;
- demonstrate causal fixture parity.

### Gate 6B-3 — detector/backtester compatibility

Prove that the new candidate's TradePlans are consumed by deterministic simulation without changing execution semantics merely to improve results.

### Gate 6B-4 — new validation protocol

Preregister a **new** development/OOS/confirmatory protocol and access policy appropriate to v0.2 before inspecting validation outcomes.

A future protocol must explicitly decide whether any historical window previously reserved for v0.1 is eligible for reuse. No reuse is authorized by this document.

## Phase 6B current decision

```text
v0.1                          PRESERVED
Phase 7 from v0.1             BLOCKED
selected successor hypothesis BULLISH D1 -> H1 MODEL #1
v0.2 status                   RESEARCH ONLY
primary-source evidence gate  OPEN
coding of bullish alpha       NOT AUTHORIZED YET
historical v0.2 backtest      NOT AUTHORIZED YET
```

The next action is evidence closure, not backtesting.