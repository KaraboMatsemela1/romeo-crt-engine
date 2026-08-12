# P0 Minimal Doctrine Decision — Handoff to Phase 2

**Candidate:** `CRT-C3-ALIGNED-v0.1-DRAFT`  
**Doctrine:** `CRT_SECRETS_2025`  
**Decision date:** 2026-08-12  
**Status:** PHASE-1 SCOPE DECISION / NON-EXECUTABLE

## Purpose

Phase 1 found that several parts of the full Romeo public doctrine remain too ambiguous to encode safely. This decision reduces the first strategy candidate to the smallest coherent subset without choosing interpretations based on backtest performance.

A scope exclusion means **not active in v0.1**; it does not mean the excluded concept is false or unimportant.

## v0.1 doctrine boundary

### Included in the first candidate

- `CRT_SECRETS_2025` doctrine snapshot only;
- parent CRT / trade-candle object selected causally;
- higher-timeframe context established before entry scanning;
- preselected key-level context;
- `REACTION_FROM_KEY_LEVEL` family only;
- Candle-2 complete before Candle-3 eligibility;
- Candle-3 open is eligibility, not entry;
- directionally aligned setups only;
- local Turtle Soup manipulation path initially required;
- one deterministic entry model chosen in Phase 2: **Model #1 OR true MSS**, not both initially;
- structural invalidation reference;
- immutable pre-trade price target plan;
- independent risk engine;
- `UNKNOWN` on any required field => `NO_SIGNAL`.

### Excluded from first v0.1

| Concept | v0.1 disposition | Reason |
|---|---|---|
| Journey-to-key-level trading | EXCLUDED | entry/exit semantics not deterministic enough |
| Countertrend CRT | EXCLUDED | direction resolver itself must first be frozen |
| SMT as direct entry | PROHIBITED | source evidence treats SMT as context/confirmation |
| SMT substitution for local Turtle Soup | EXCLUDED | exact substitution rule unresolved |
| KOD requirement | EXCLUDED | ex-ante classifier unresolved / hindsight hazard |
| Time exits | EXCLUDED | exact time-exit policy unresolved |
| Candle-2 trading | EXCLUDED | higher ambiguity / not needed for first candidate |
| Generic BOS/MSS | PROHIBITED | must not replace Romeo true MSS |
| Generic FVG entry | PROHIBITED | FVG role is not a standalone approved entry family |
| Adaptive `near 50%` rules | EXCLUDED | numeric threshold would invite curve fitting |
| Strong-trend retracement override | EXCLUDED | regime predicate unresolved |
| 2026 CRTology refinements | VERSION-SEPARATED | cannot silently rewrite 2025 doctrine |

## Parent/timeframe decision

Phase 1 does **not** authorize blindly using every `{W1,D1,H4}` parent in the first backtest.

Phase 2 must select the first parent/timeframe route only after its candle calendar and execution mapping are deterministic.

Preferred risk-reduction order:

1. use the parent/timeframe route with the strongest source-backed calendar and fixtures;
2. freeze that route;
3. validate it independently;
4. add other parent routes as separately versioned expansions.

If H4 semantics remain ambiguous, H4 must be excluded rather than constructed from provider defaults.

## Direction decision

```text
allow_countertrend = False
```

Required direction values:

```text
BULLISH
BEARISH
NEUTRAL
UNKNOWN
```

`UNKNOWN`, unresolved cross-timeframe conflict, or an unqualified bias flip blocks the trade.

No moving-average, majority-vote, future-trend, candle-color, or best-backtest resolver may be introduced as a substitute for missing Romeo evidence.

## Key-level decision

Only `REACTION_FROM_KEY_LEVEL` is eligible for the first candidate.

Required ordering:

```text
PRESELECT LEVEL
    ↓
WAIT FOR QUALIFYING LEVEL INTERACTION
    ↓
ONLY THEN CONSIDER LTF MANIPULATION / ENTRY
```

A lower-timeframe reversal before the selected level is reached does not become a valid v0.1 entry merely because it later works.

## Turtle Soup decision

For first v0.1:

```text
require_local_turtle_soup = True
allow_smt_substitution = False
```

However, `TurtleSoupConfirmed` remains blocked until Phase 2 freezes:

- eligible reference type/lifecycle;
- exact failure/reversal confirmation;
- event expiry;
- true-breakout invalidation;
- consumed-reference rules.

A strict excursion alone is only `TurtleSoupCandidate`.

## Entry-model decision

Phase 2 must choose exactly one first executable entry family:

```text
MODEL_1
OR
TRUE_MSS
```

Selection criteria are **evidence completeness, determinism and fixture quality**, not which one gives a better exploratory backtest.

The second entry family may be added only after the first is frozen as a separately measurable variant.

## Exit decision

First candidate should use fully specified price exits only.

A target must be selected before order approval and stored in the immutable `TradePlan`.

Time exits remain disabled until source semantics are deterministic.

## Fail-closed contract

The Phase-2 compiler must enforce:

```python
if any_required_strategy_state is UNKNOWN:
    return NO_SIGNAL

if evidence_contract_not_satisfied:
    return NO_SIGNAL

if risk_engine_rejects:
    return NO_ORDER
```

No research convenience default may turn an unresolved value into a trading decision.

## Phase-2 freeze gate

The first candidate can move to `FROZEN_FOR_VALIDATION` only when every active-path item below is deterministic:

1. parent selection/lifecycle;
2. active calendar/timeframe route;
3. context direction;
4. key-level selection/ranking/reach state;
5. Turtle Soup confirmation/lifecycle;
6. one entry model;
7. target hierarchy;
8. structural stop + execution buffer;
9. Candle-3 confirmation/expiry;
10. positive and negative fixtures for each rule;
11. no unresolved contradiction changes the signal;
12. all decisions use only information available at timestamp `t`.

Until then:

```text
CRT-C3-ALIGNED-v0.1-DRAFT
    = RESEARCH SPECIFICATION
    ≠ EXECUTABLE STRATEGY
```
