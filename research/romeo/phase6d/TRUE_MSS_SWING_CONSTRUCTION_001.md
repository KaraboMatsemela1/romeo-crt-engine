# Phase 6D — True MSS Swing Construction 001

**Date:** 2026-08-15  
**Tracking:** Issue #104  
**Baseline:** Recovery 007 / PR #88; minimum-closure analysis PR #90; Model #1 exhaustion PR #103  
**Mode:** bounded first-party evidence synthesis only  
**Issue #16 disposition:** `KEEP_BLOCKED`

## Decision

Romeo's provenance-bound first-party evidence directly defines a **bullish relational sequence** for True MSS:

```text
old-low stab
    ↓
low → high → lower low
    ↓
break / close above the high that broke the low
    ↓
True MSS condition in the worked examples
```

This materially narrows the rule, but it does **not** define a deterministic algorithm for constructing the `low`, intervening `high`, and `lower low` from raw candles. No pivot width, fractal rule, protected-high definition, zigzag threshold, displacement threshold, or equivalent swing-selection algorithm is first-party defined in the current provenance-bound corpus.

Therefore:

```text
CLASSIFICATION                  = PARTIAL_SEQUENCE_ONLY
BULLISH_RELATIONAL_SEQUENCE     = DIRECT_SUPPORTED
REFERENCE_HIGH_RELATION         = DIRECT_SUPPORTED_AT_EXAMPLE_LEVEL
RAW_CANDLE_SWING_CONSTRUCTION   = MISSING
BEARISH_CONSTRUCTION            = MISSING
NEW_CLOSING_FIELD_EVIDENCE      = 0
TRUE_MSS_ALGORITHM              = STRONG_PARTIAL / KEEP_BLOCKED
INDEPENDENT_CLOSURE_AUDIT       = NOT_READY
ISSUE_16                        = KEEP_BLOCKED
ISSUE_37                        = MUST_NOT_START
```

The project must not convert this partial sequence into a generic ICT/BOS/CHOCH swing algorithm.

## First-party evidence examined

### Episode 9 — 08:49–09:23

Source: `ROMEO-2025-S9`  
Locator: `https://www.youtube.com/watch?v=2sxdsgcIeYA&t=529s#auto-en-json3-08-49-09-23`  
Artifact SHA-256: `a4e74d1145f0c8988cdad03f51108fd0029bf37d69830041bcad6377d86162c1`

Admitted text:

> "price stabbing into an old low and then closing above the high that broke the low. And this is a true market structure shift. So after this close above, look for them to retrace into this area between the high and the low."

What this proves:

- an old-low stab precedes the demonstrated bullish True MSS;
- the validating event is a **close above** a particular reference high;
- Romeo names that reference as `the high that broke the low`;
- after that close, the worked rule looks for retracement into the area between the referenced high and low.

What it does not prove:

- how the old low is selected;
- how many raw candles define the low/high sequence;
- how to identify the relevant high when multiple local highs exist;
- whether a wick excursion can define the swing before the required close;
- whether displacement/body size is mandatory;
- bearish construction;
- universal timeframe ownership;
- expiry.

### Episode 9 — 15:23–17:01

Source: `ROMEO-2025-S9`  
Locator: `https://www.youtube.com/watch?v=2sxdsgcIeYA&t=923s#auto-en-json3-15-23-17-01`  
Artifact SHA-256: `e8a96a08580dfd76ced8f38a91d1d38a6d74476945810ed30bf462942247e85e`

Admitted text:

> "in the five-minute time frame ... SMT ... on the lower time frame ... low high lower low break above the high that broke the low ... unlocks the OTE; area between the high and the low ... good area to buy with the stop loss being the low of the turtle soup."

What this adds:

- the worked bullish sequence is explicitly ordered `low → high → lower low` before the break;
- the break is above the reference described as `the high that broke the low`;
- the example associates this structure with lower-timeframe execution and a 5-minute SMT context;
- the post-shift area is tied to the high/low range in the example;
- the worked stop reference is the Turtle-Soup low.

What it does not add:

- a raw-candle pivot algorithm;
- a rule for choosing one `high` among overlapping/same-level candidates;
- the minimum excursion needed for a high/low to become structural;
- a universal requirement that 5-minute is the True MSS timeframe;
- a bearish mirror.

### Episode 5 — worked True MSS sequence

Source: `ROMEO-2025-S5`  
Recovery 007 artifact SHA-256: `ad593f7409a0bbf70a30d68a693e1d9c7e0a445d0ef9eec8c0c371e31a54d3f2`

Admitted text includes:

> "true MSS example is low high lower low ... blast through the high that broke the low."

This cross-source first-party evidence reinforces the **same relational sequence**, which is important: the Episode 9 wording is not a one-off transcription accident.

It still does not define the lower-level swing-construction algorithm.

## Safe relational abstraction

The current first-party corpus supports this much for the demonstrated bullish form:

```text
L0 = a qualifying low
H1 = a high formed after L0
L2 = a lower low formed after H1

H1 is the relational reference because the subsequent move from H1
participates in producing/breaking below L0 to create L2.

Bullish shift condition in the worked examples:
    a later close occurs above H1.
```

This abstraction is descriptive of the direct sequence; it is **not yet executable** because `L0`, `H1`, and `L2` cannot be uniquely constructed from raw candles using source-defined rules.

## Why generic swing algorithms are forbidden

The following would each produce different True MSS signals while remaining plausible engineering choices:

```text
N-bar fractal pivot
left/right pivot width
zigzag percentage
ATR reversal threshold
protected high/low algorithm
highest high between two lows
last up-close candle before lower low
BOS/CHOCH library default
minimum displacement body
```

Romeo's current provenance-bound evidence does not select one of these algorithms.

Using any of them and calling it `TRUE_MSS_ALGORITHM` would replace a source gap with project discretion.

## Frame-bindable versus semantic debt

A technical frame around the Episode 9 examples could unambiguously identify **which plotted high** Romeo points to in those examples. That would improve fixture binding and eliminate ambiguity about the worked chart.

However, a chart frame showing one example does not necessarily define the general algorithm by which a future raw candle sequence selects structural pivots.

Therefore the missing debt is primarily **semantic**, not merely a locator problem:

```text
EXAMPLE_REFERENCE_BINDING = potentially frame-improvable
GENERAL_SWING_CONSTRUCTION = semantic absence
```

This is why the classification is `PARTIAL_SEQUENCE_ONLY` rather than `FRAME_BINDABLE_PARTIAL` as the final predicate state.

## Required-field impact

### `EXACT_PREDICATE`

State remains:

`STRONG_PARTIAL`

The relational sequence is now highly constrained and directly cross-source supported, but raw-candle construction is unresolved.

### `CONFIRMATION`

The bullish worked form supports a close above the reference high as the confirmation event.

State:

`STRONG_PARTIAL`

It is not a complete closing field because bearish form, swing construction, ownership, lifecycle and other branches remain unresolved.

### `DATA_REQUIREMENTS`

Current safe minimum implication:

- ordered timestamped OHLC data;
- sufficient historical context to identify candidate swing sequences;
- contextual old-low / Turtle-Soup and possibly SMT evidence where the setup family requires it.

But the exact lookback/window/structure inputs cannot be frozen until the swing algorithm is defined.

State:

`PARTIAL`

## Two-engineer test

Two engineers given the same already-labeled `low → high → lower low` sequence can agree that a close above the intervening reference high satisfies the demonstrated bullish shift relation.

Two engineers starting from raw candles can still select different lows/highs because the source does not define how pivots are constructed.

Therefore:

```text
TWO_ENGINEER_TEST = FAIL_FOR_COMPLETE_TRUE_MSS
```

## Next exact True MSS question

The swing-construction route is exhausted in the current text corpus unless a new first-party source explicitly defines pivot formation.

The next highest-leverage distinct question from the minimum-closure map is:

> **Does Romeo directly define the bearish True MSS construction, rather than requiring the project to assume symmetry?**

That pass should inspect first-party True MSS material only and classify whether a bearish sequence is directly stated/demonstrated. It must not infer `high → low → higher high → close below low` merely by symmetry.

After bearish-form recovery, the remaining major debts are expected to include:

- timeframe/context ownership;
- displacement/quality requirement;
- retracement/entry contract;
- invalidation generalization;
- expiry.

## Final disposition

```text
TRUE_MSS_BULLISH_SEQUENCE       = DIRECT_SUPPORTED
TRUE_MSS_RAW_SWING_ALGORITHM    = MISSING
TRUE_MSS_BEARISH_RULE           = MISSING
TRUE_MSS_ALGORITHM              = STRONG_PARTIAL
TRUE_MSS_CANDIDATE_READY        = FALSE
ISSUE_16                        = KEEP_BLOCKED
ISSUE_37                        = MUST_NOT_START
```

No candidate, detector/count, protected outcome, validation-window, broker, paper, shadow, live, parameter, or historical-result state is changed by this report.
