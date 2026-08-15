# Phase 6D — SMT Correspondence / Synchronization 001

**Date:** 2026-08-15  
**Tracking:** Issue #112  
**Baseline:** Recovery 007 / PR #88; held-predicate ranking PR #111  
**Mode:** bounded first-party evidence synthesis only  
**Issue #16 disposition:** `KEEP_BLOCKED`

## Decision

The current provenance-bound first-party corpus directly supports the basic SMT take/non-take primitive and a concrete EUR/DXY inverse example, but it does **not** define a deterministic corresponding-extreme construction or temporal synchronization rule.

Therefore:

```text
CLASSIFICATION                    = NO_DETERMINISTIC_CORRESPONDENCE_FOUND
BASIC_TAKE_NONTAKE_PRIMITIVE      = DIRECT_SUPPORTED
EUR_DXY_INVERSE_EXAMPLE           = DIRECT_SUPPORTED_AT_EXAMPLE_LEVEL
CORRESPONDING_EXTREME_RULE        = MISSING
SYNCHRONIZATION_WINDOW            = MISSING
EVENT_LATCHING_TIMESTAMP          = MISSING
NEW_CLOSING_FIELD_EVIDENCE        = 0
SMT_EXECUTABLE_SEMANTICS          = STRONG_PARTIAL / KEEP_BLOCKED
INDEPENDENT_CLOSURE_AUDIT         = NOT_READY
ISSUE_16                          = KEEP_BLOCKED
ISSUE_37                          = MUST_NOT_START
```

No same-candle, same-session, nearest-swing, pivot, lag-tolerance, resampling, or stale-data rule may be invented to fill these gaps.

## First-party evidence examined

### Episode 6 — basic divergence primitive

Source: `ROMEO-2025-S6`  
Locator: `https://www.youtube.com/watch?v=3IWgc52Dqsg&t=203s#auto-en-json3-03-23-03-44`  
Artifact SHA-256: `18a3f7c43e84e3707039ab8601ae7622e51e470e53d64c1b2d99d1da9c4e80d4`

Direct text:

> "one asset class taking a high or low while the other asset class does not take the high or the low."

What this proves:

- SMT compares at least two markets;
- the foundational relation is a take/non-take divergence around a high or low;
- a non-take on one side can participate in an SMT state.

What it does not prove:

- how to select the high/low on either chart;
- whether the two references must come from the same timestamp/candle/session;
- whether the references must be structurally homologous;
- maximum lag;
- whether one market may take the level several bars before the other comparison is evaluated;
- how stale/missing data is treated.

### Episode 6 — EUR/DXY example

Source: `ROMEO-2025-S6`  
Locator: `https://www.youtube.com/watch?v=3IWgc52Dqsg&t=1379s#auto-en-json3-22-59-23-19`  
Artifact SHA-256: `fa0d51d3713aff14c96b71c8e02366fd1ca09cec074fb83c0d3f3c5f1a88378b`

Direct text:

> "Euro took the low while the dollar did not take the high and that was the SMT."

What this proves:

- Romeo directly demonstrates an inverse-pair mapping where EUR low-taking is compared against DXY high-taking/non-taking;
- the example confirms that opposite-side extremes can correspond for an inverse relationship.

What it does not prove:

- which EUR low and DXY high were selected algorithmically;
- how their time windows correspond;
- whether the mapping is universally `EUR low ↔ DXY high` for every SMT context;
- exact event timestamp/latching;
- allowed timing drift;
- positive-correlation pair semantics.

### Episode 6 — confirmation hierarchy

Source: `ROMEO-2025-S6`  
Locator: `https://www.youtube.com/watch?v=3IWgc52Dqsg&t=1693s#auto-en-json3-28-13-31-56`  
Artifact SHA-256: `a1c10ff9a7f71f968ea9a10bd9439c9dba11aacbe6f8814e7e36c120b5cfa4b4`

Direct text:

> "look for a model number one confirmation on the lower time frame ... first confirmation of SMT; second confirmation ... a true market structure shift; If you see an SMT always wait for both confirmations."

What this proves:

- SMT is not itself an order trigger;
- Romeo directly associates lower-timeframe confirmation with SMT;
- Model #1 and True MSS are named confirmation mechanisms in the captured wording.

What it does not prove:

- when the SMT event becomes causally latched before confirmation begins;
- which of the paired instruments owns the confirmation;
- how long the SMT state remains valid;
- whether `both confirmations` means both alternatives, a sequence, or another source-context nuance beyond the minimal excerpt. The project must not over-interpret the ASR excerpt without fuller binding.

## Pair registry context

Official Telegram source `ROMEO-TG-SMT-PAIRS-6363` directly supplies the basic pair inventory:

```text
EU - DXY
NQ - ES
BTC - ETH
GOLD - SILVER
```

This closes a research-pair inventory, not the relationship mechanics.

The registry does not define:

- corresponding swing/extreme selection;
- pair polarity for every relationship;
- synchronization;
- primary/traded leg;
- lifecycle.

## Cross-check against the historical SMT gate

`research/romeo/phase6c/SMT_EVIDENCE_GATE.md` previously isolated the exact same unresolved strategy-critical fields.

For corresponding extremes it records as unknown whether extrema must belong to:

- the same named candle/session/window;
- exact-matching timestamps;
- nearest swings;
- parent CRT extremes;
- session highs/lows;
- another source-defined object.

For synchronization it records no first-party executable value for:

- exact timestamp equality;
- same lower-timeframe candle;
- same session;
- allowed lag;
- stale-data cutoff.

Recovery 007 materially improved source quality by capturing direct Episode 6 timed text, but the admitted direct wording still does not answer those questions.

## Why the EUR/DXY example is not enough

A worked example can identify the two plotted/extreme concepts Romeo used in that instance. It does not automatically define the general selector from raw market data.

Two engineers may reasonably implement different correspondence policies:

```text
same timestamp candle highs/lows
nearest prior structural swing
same-session extreme
same parent-CRT extreme
latest unbroken extreme
fixed lookback high/low
```

All would be plausible attempts to operationalize the example, but none is directly selected by the source evidence.

Therefore:

```text
WORKED_EXAMPLE_BINDING != GENERAL_CORRESPONDENCE_ALGORITHM
```

## Information-availability impact

The SMT relationship is inherently cross-market and causal. At a claimed decision time `t`, both markets' observations must be available by `t`.

That is an engineering anti-look-ahead requirement, but it is **not** a Romeo-defined synchronization window.

The project can safely enforce:

```text
NO_FUTURE_CROSS_MARKET_DATA
```

without claiming:

```text
ROMEO_SYNCHRONIZATION_WINDOW = X
```

The source still does not state when an SMT state becomes latched, how long it can wait for a non-take, or when one side becomes too stale to compare.

## Required-field impact

### `EXACT_PREDICATE`

State remains:

`STRONG_PARTIAL`

Direct take/non-take semantics exist, but the compared objects are not deterministically constructible.

### `INFORMATION_AVAILABILITY_TIME`

State remains:

`MISSING / PARTIAL_CAUSAL_CONSTRAINT`

The engine must avoid future data, but the source-defined event timing/latching window is absent.

### `DATA_REQUIREMENTS`

State remains:

`STRONG_PARTIAL`

The pair registry and need for synchronized multi-market data are clear, but exact structural reference and synchronization inputs are undefined.

## Two-engineer test

Give two engineers raw EUR/USD and DXY data plus the direct source wording. They can agree that EUR taking a low while DXY does not take the corresponding high can constitute SMT in the demonstrated inverse example.

They cannot deterministically agree on:

- which EUR low to evaluate;
- which DXY high corresponds to it;
- the allowed time relationship;
- when the comparison expires;
- what to do if the two markets form candidate extremes at different times.

Therefore:

```text
TWO_ENGINEER_TEST = FAIL_FOR_EXECUTABLE_SMT
```

## Remaining SMT closure debt

After this pass, major unresolved fields remain:

1. corresponding-extreme construction — semantic absence;
2. synchronization/event latching — semantic absence;
3. positive-pair and universal inverse-pair polarity;
4. traded-instrument / confirmation ownership;
5. exact Turtle-Soup substitution predicate;
6. invalidation;
7. expiry.

The basic divergence primitive, pair inventory, EUR/DXY worked example, substitution possibility and confirmation hierarchy are valuable direct evidence, but do not close the executable predicate.

## Next recommendation

Do not repeat the same Episode 6 take/non-take text looking for a correspondence formula it does not contain.

The next step should be an **SMT closure-exhaustion synthesis** that decides whether another distinct current-corpus SMT question has enough leverage to justify a bounded pass, or whether SMT should also transition to `WAIT_FOR_NEW_SMT_EVIDENCE`.

A likely candidate for evaluation in that synthesis is pair polarity/traded-leg ownership because the current corpus contains one direct inverse EUR/DXY example, but no universal positive-pair directional rule is ledger-bound.

Do not create that micro-pass until the synthesis shows it can materially change closure distance.

## Final disposition

```text
SMT_CORRESPONDENCE_RULE           = MISSING
SMT_SYNCHRONIZATION_RULE          = MISSING
SMT_EXECUTABLE_SEMANTICS          = STRONG_PARTIAL
SMT_CANDIDATE_READY               = FALSE
CLOSED_PREDICATES                 = 0
ISSUE_16                          = KEEP_BLOCKED
ISSUE_37                          = MUST_NOT_START
```

No candidate, detector/count, protected outcome, OOS/CONFIRM, broker, paper, shadow, live, parameter, or historical-result state is changed by this report.
