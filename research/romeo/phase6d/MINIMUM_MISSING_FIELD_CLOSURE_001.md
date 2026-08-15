# Phase 6D — Minimum Missing Field Closure 001

**Date:** 2026-08-15  
**Tracking:** Issue #89  
**Baseline:** Recovery 007 / PR #88 / merge `4ee5bc18b5574dcfb0989b424418f509fb3c00bc`  
**Mode:** evidence synthesis only  
**Issue #16 disposition:** `KEEP_BLOCKED`

## Decision

Recovery 007 materially improves first-party coverage but does not make either `MODEL_1_GEOMETRY` or `TRUE_MSS_ALGORITHM` deterministic enough for independent implementation. Both fail the two-engineer test because multiple implementation choices remain unspecified by the admitted first-party evidence.

```text
MODEL_1_GEOMETRY    = STRONG_PARTIAL / KEEP_BLOCKED
TRUE_MSS_ALGORITHM  = STRONG_PARTIAL / KEEP_BLOCKED
INDEPENDENT_CLOSURE_AUDIT = NOT_READY
ISSUE_37                  = MUST_NOT_START
```

No detector, count, P&L/backtest, OOS/CONFIRM, paper, shadow, live or broker action is authorized by this report.

## Evidence baseline

The analysis uses the current `PREDICATE_LEDGER_V2.json` plus Recovery 007's official YouTube-generated English `json3` timed-text excerpts.

Strongest Model #1 evidence:

- `ROMEO-2025-S1` 10:18–10:56: sweep into an old high, a specific up-close candle, close below it as a short trigger, with example stop/target framing.
- `ROMEO-2025-S1` 15:05–15:41: stated bearish/bullish symmetry around old highs/lows and the sweep candle.
- `ROMEO-2025-S1` 16:32–17:22: public timeframe mappings: monthly→daily Model #1, weekly→4H Model #1, daily→1H Model #1.
- `ROMEO-2025-S9` 02:02–02:58: the relevant object is one specific candle that liquidated the old high, not a zone; worked close/retrace example.

Strongest true-MSS evidence:

- `ROMEO-2025-S9` 08:49–09:23: bullish worked sequence — price stabs an old low and closes above the high that broke the low; after that close Romeo looks for retracement into the high/low area.
- `ROMEO-2025-S9` 15:23–17:01: lower-timeframe worked sequence — low/high/lower-low then break above the high that broke the low; example links to 5m SMT, retracement area and a Turtle-Soup-low stop reference.

## Field-level closure map

The ledger contract requires seven fields per predicate:

`EXACT_PREDICATE`, `INFORMATION_AVAILABILITY_TIME`, `DIRECTION_TIMEFRAME_OWNERSHIP`, `CONFIRMATION`, `INVALIDATION`, `EXPIRY`, `DATA_REQUIREMENTS`.

### MODEL_1_GEOMETRY

| Required field | State | Current support | Remaining closure debt |
|---|---|---|---|
| EXACT_PREDICATE | STRONG_PARTIAL | Sweep-candle + close trigger; symmetric recap; one-candle specificity | Deterministic qualifying-old-extreme selector; whether “thick” is a mandatory measurable condition or descriptive wording; exact relationship between close-trigger and later retrace execution |
| INFORMATION_AVAILABILITY_TIME | PARTIAL | Evidence implies the close is observed before the described trigger | Explicit information-time contract for all branches; whether entry is at close, next tradable event, or retrace |
| DIRECTION_TIMEFRAME_OWNERSHIP | STRONG_PARTIAL | Monthly→D1, Weekly→H4, Daily→H1 mappings; directional high/low symmetry | Complete ownership/scope for the executable candidate, including whether only the public mappings are permitted and what context owns direction |
| CONFIRMATION | PARTIAL | Close beyond the identified sweep candle is described as a trigger; S9 also shows retrade into Model #1 | Whether the close itself is the complete confirmation or whether retrace/another condition is required for entry |
| INVALIDATION | PARTIAL | Worked examples reference stop placement above/below local structure | Exact invalidation anchor, buffer/tolerance, and whether stop semantics are universal or example-specific |
| EXPIRY | MISSING | No admitted first-party artifact defines setup lifetime | Exact cancellation/expiry event or time boundary |
| DATA_REQUIREMENTS | PARTIAL | Candle geometry and timeframe mapping imply timestamped OHLC structure | Explicit minimum inputs for old-extreme construction, candle qualification, timeframe alignment and any required context |

### TRUE_MSS_ALGORITHM

| Required field | State | Current support | Remaining closure debt |
|---|---|---|---|
| EXACT_PREDICATE | STRONG_PARTIAL | Bullish sequence: old-low stab then close above “the high that broke the low”; lower-timeframe worked sequence repeats the relation | Deterministic swing/high-low construction; exact old-low selector; directly supported bearish form; whether displacement is required |
| INFORMATION_AVAILABILITY_TIME | PARTIAL | The worked rule is framed around a completed close before retracement | Explicit decision-time contract and whether the break/close is sufficient before any retrace entry logic |
| DIRECTION_TIMEFRAME_OWNERSHIP | PARTIAL | One worked sequence plus a lower-timeframe example associated with 5m SMT | Exact signal timeframe, context timeframe and ownership rule; example-specific 5m reference is not a universal ownership contract |
| CONFIRMATION | STRONG_PARTIAL | Close above the high that broke the low; later lower-timeframe break sequence | Exact confirmation for both directions and whether additional confirmation/displacement/retrace is mandatory |
| INVALIDATION | PARTIAL | Worked case references stop at Turtle Soup low | Universal invalidation rule versus example-specific risk framing; bearish invalidation absent |
| EXPIRY | MISSING | No admitted artifact defines true-MSS lifetime | Exact expiry/cancellation event or temporal boundary |
| DATA_REQUIREMENTS | PARTIAL | Requires ordered swing/extreme and candle-close information | Deterministic swing algorithm, synchronization/context inputs and minimum timeframe data contract |

## Minimum semantic closure sets

These are the smallest semantic questions that must be resolved before the respective predicate can plausibly pass a two-engineer audit. Audio/frame verification can confirm wording, but it cannot manufacture missing semantics.

### Model #1 — ranked closure debt

1. **Qualifying old-extreme selector** — What exact prior high/low is eligible to be “the old high/low” for Model #1? This is the highest-leverage missing semantic because the rest of the geometry cannot be instantiated reproducibly without it.
2. **Trigger versus retrace execution contract** — Is the close beyond the sweep candle itself the executable entry trigger, or does Model #1 require/permit a retrace into that candle/area before entry? If both are valid, the contexts must be explicitly versioned.
3. **Candle qualification** — Is “thick up-close/down-close candle” a mandatory filter? If yes, what deterministic measurement defines `thick`; if no, first-party evidence must make clear it is descriptive rather than causal.
4. **Invalidation/stop semantics** — Exact structural anchor and tolerance/buffer; distinguish universal rule from worked-example placement.
5. **Expiry** — Exact event/time at which an otherwise valid Model #1 setup is cancelled.
6. **Complete ownership/data contract** — Pin the allowed public HTF→signal mappings and the minimum context/data fields needed for deterministic use.

### True MSS — ranked closure debt

1. **Deterministic swing construction** — Algorithmically define “the high that broke the low” / corresponding bearish structure without discretionary chart interpretation.
2. **Bearish symmetric rule** — Obtain direct first-party support for the bearish construction rather than assuming symmetry.
3. **Signal/context timeframe ownership** — Define which timeframe constructs the swing and which timeframe owns the MSS signal; the 5m worked example is not enough to universalize.
4. **Break/close/displacement contract** — Confirm whether a candle-body close is sufficient and whether displacement or another quality condition is mandatory.
5. **Retracement/entry contract** — Define the exact post-MSS retracement region and whether touching/entering that region is required for execution.
6. **Invalidation and expiry** — Universal invalidation anchor plus setup cancellation boundary.
7. **Minimum data contract** — Exact data required to construct swings and evaluate the rule reproducibly.

## Wording-verification debt versus semantic-absence debt

### Targeted audio/frame verification can resolve wording confidence

Prioritize these existing locators:

1. Model #1 — S1 10:18–10:56: verify `thick up close candle`, `close below it`, and stop wording against audio/chart frame.
2. Model #1 — S1 15:05–15:41: verify the bullish/bearish symmetric recap and exact close relation.
3. Model #1 — S9 02:02–02:58: verify `one specific candle`, `not a zone`, and whether the worked retrace is described as required or illustrative.
4. True MSS — S9 08:49–09:23: verify `closing above the high that broke the low`, exact chart swing labels, and retracement-area boundaries.
5. True MSS — S9 15:23–17:01: verify the lower-timeframe sequence, the 5m/SMT relationship and stop wording.

Audio/frame confirmation of these phrases would increase provenance confidence but **would not by itself close** old-extreme selection, swing construction, invalidation or expiry unless the visual/audio contains explicit additional semantics not present in the timed text.

### Genuinely missing first-party semantics

The current corpus does not directly define:

- deterministic old-high/old-low eligibility for Model #1;
- a measurable `thick` threshold, or an explicit statement that no threshold is required;
- Model #1 expiry;
- deterministic swing construction for true MSS;
- directly evidenced bearish true-MSS construction;
- true-MSS universal timeframe ownership;
- true-MSS expiry;
- universal invalidation semantics for either predicate.

These require either additional technical frames/audio surrounding the held sources that explicitly contain the missing rule, or a new first-party Romeo source. Generic ICT doctrine receives zero closure credit.

## Closure-distance ranking

`MODEL_1_GEOMETRY` remains the nearest predicate to closure because the corpus already provides directional geometry, one-candle specificity and three public timeframe mappings. `TRUE_MSS_ALGORITHM` has a strong bullish worked rule but is farther from deterministic closure because its core swing-construction algorithm and bearish form remain undefined.

Priority:

```text
1. MODEL_1_GEOMETRY
2. TRUE_MSS_ALGORITHM
```

## Exact next bounded recovery mission

Do not perform another broad channel sweep. Search only for explicit first-party answers to these questions, in this order:

1. Model #1: **How does Romeo choose the qualifying “old high/old low”?**
2. Model #1: **Is “thick” causal and measurable, or descriptive only?**
3. Model #1: **Does entry occur on the closing trigger or only/also on a retrace; what invalidates and expires the setup?**
4. True MSS: **How are the swing points / “high that broke the low” constructed deterministically?**
5. True MSS: **What is the directly stated bearish form, owning timeframe, invalidation and expiry?**

The first pass should inspect audio/frames around the five existing Recovery 007 locators above. If those contain no explicit additional semantics, stop that route and classify the remaining field as semantic absence rather than repeatedly re-searching the same material.

## Final disposition

```text
MODEL_1_GEOMETRY:
  recommendation = KEEP_BLOCKED
  independent_closure_audit = NOT_READY

TRUE_MSS_ALGORITHM:
  recommendation = KEEP_BLOCKED
  independent_closure_audit = NOT_READY

ISSUE_16 = BLOCKED_NO_VERIFIED_PREDICATE_CLOSURE
ISSUE_37 = MUST_NOT_START
```

This report changes research prioritization only. It does not change any project gate.