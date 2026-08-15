# Phase 6D — Model #1 Invalidation / Stop Ownership 001

**Date:** 2026-08-15  
**Tracking:** Issue #98  
**Baseline:** Recovery 007 / PR #88; minimum-closure map PR #90; old-extreme selector PR #93; trigger/retrace contract PR #95; `thick` semantics PR #97  
**Mode:** bounded first-party evidence synthesis only  
**Issue #16 disposition:** `KEEP_BLOCKED`

## Decision

The current first-party corpus does not identify a deterministic universal Model #1 structural stop owner. Episode 1 directly includes stop language, but the admitted timed-text wording is deictic (`stop loss up here`) and the text artifact does not name the referenced structural object. Episode 9 directly supports a Turtle-Soup-low stop in a worked lower-timeframe True-MSS sequence, but that evidence cannot be transferred to Model #1 without an explicit source bridge.

Therefore:

```text
CLASSIFICATION                  = PARTIAL_DEICTIC_CONTEXT_ONLY
MODEL1_STOP_OWNER               = UNRESOLVED
MODEL1_SETUP_INVALIDATION       = UNRESOLVED
TRUE_MSS_TS_STOP_EXAMPLE        = DIRECT_EXAMPLE_ONLY
ONE_TICK_BUFFER                 = PROJECT_ONLY / NOT_ROMEO_CLAIM
NEW_CLOSING_FIELD_EVIDENCE      = 0
MODEL_1_GEOMETRY                = STRONG_PARTIAL / KEEP_BLOCKED
INDEPENDENT_CLOSURE_AUDIT       = NOT_READY
ISSUE_16                        = KEEP_BLOCKED
ISSUE_37                        = MUST_NOT_START
```

This report does not alter the frozen v0.1 Model-1-high + one-tick implementation. That historical candidate remains immutable. The purpose here is only to prevent project formalizations or True-MSS example semantics from being promoted as newly verified Romeo Model #1 doctrine.

## First-party evidence examined

### Episode 1 — Model #1 worked stop language

Source: `ROMEO-2025-S1`  
Locator: `https://www.youtube.com/watch?v=T7udbrWlARI&t=618s#auto-en-json3-10-18-10-56`  
Artifact SHA-256: `0f282f00bfdf78037c859a821cb5e489df877cd45cb30761146d11c90bb04aad`

Admitted timed-text excerpt:

> "stab again into the old high ... the thick up close candle which stabbed into the old high. You close below it ... that's the trigger you use to enter a short or a sell, stop loss up here ... target the lows one by one."

Safe evidence credit:

- the demonstrated Model #1 short includes a stop loss;
- the stop is structurally referenced by Romeo to something visible/deictic in the worked chart explanation;
- the text does not identify whether `up here` means the Model #1 candle high, the swept old high, the Turtle-Soup extreme, another structural high, or an execution price above one of those objects;
- no numerical buffer/tolerance is given in the admitted text.

Disposition:

`PARTIAL_DEICTIC_CONTEXT_ONLY`

A chart/audio frame that unambiguously binds `up here` to a named price object could strengthen this field. The current text artifact alone cannot.

### Episode 9 — Model #1 excerpt

Source: `ROMEO-2025-S9`  
Locator: `https://www.youtube.com/watch?v=2sxdsgcIeYA&t=122s#auto-en-json3-02-02-02-58`  
Artifact SHA-256: `5cfd666a2fb8492fcaa6d258b52126660a23a97dc9fd2230dbe1c009fd5b9ab0`

Admitted timed-text excerpt:

> "the one specific candle ... that liquidated the old high ... it's not a zone ... when they close below it ... retrades into model number one and then dumps."

Safe evidence credit:

- the Model #1 object is one specific candle;
- the close-trigger/retrade sequence is supported;
- this excerpt contains no direct stop/invalidation owner.

### Episode 9 — True-MSS worked stop example

Source: `ROMEO-2025-S9`  
Locator: `https://www.youtube.com/watch?v=2sxdsgcIeYA&t=923s#auto-en-json3-15-23-17-01`  
Artifact SHA-256: `e8a96a08580dfd76ced8f38a91d1d38a6d74476945810ed30bf462942247e85e`

Recovery 007 records the worked sequence as directly supporting a stop reference at the Turtle-Soup low in that lower-timeframe True-MSS example.

Safe evidence credit:

```text
TRUE_MSS_WORKED_EXAMPLE_STOP_REFERENCE = TURTLE_SOUP_LOW
```

What it does not prove:

```text
ALL_MODEL1_STOP_REFERENCES = TURTLE_SOUP_EXTREME
```

The latter would be an unsupported cross-entry-family promotion.

## Project-formalization boundary

The frozen v0.1 specification introduced:

```text
structural stop reference = Model-1-core high
execution buffer          = 1 instrument tick
```

Canonical records explicitly separate source-derived structure from project execution parameters:

- `docs/adr/ADR-004-freeze-narrow-d1-h1-model1-subset.md`
- `strategy/CRT_V0.1_SPEC.md`

The one-tick value is explicitly a project execution parameter and receives zero first-party closure credit.

The historical v0.1 choice of Model-1-core high as the stop reference was part of that candidate's frozen deterministic formalization. It must not be retroactively relabeled as a directly verified Romeo universal Model #1 stop rule.

Therefore:

```text
V0.1_STOP_REFERENCE         = HISTORICAL_FROZEN_PROJECT_FORMALIZATION
V0.1_EXECUTION_BUFFER       = HISTORICAL_PROJECT_PARAMETER
NEW_FIRST_PARTY_CREDIT      = ZERO
```

## Setup invalidation versus broker stop

These are distinct questions and must not be collapsed.

### Setup invalidation

Question:

> Before or after confirmation, what event means the Model #1 thesis is no longer valid as a strategy setup?

Current source state:

`UNRESOLVED`

The historical v0.1 implementation invalidates a pending model-candle instance when a later H1 candle makes a new higher high before bearish confirmation. That remains a frozen project rule for v0.1, not newly verified Romeo semantics.

### Structural stop reference

Question:

> If a Model #1 trade is taken, which structural price object owns the stop?

Current source state:

`PARTIAL_DEICTIC_CONTEXT_ONLY`

### Execution stop price / buffer

Question:

> How far beyond the structural object should an order be placed?

Current source state:

`MISSING`

No first-party evidence in the bounded material defines one tick, spread, ATR, fixed pips/points, or another execution tolerance.

## Rejected promotions

Do not infer any of these as Romeo's universal Model #1 rule:

```text
stop = model_candle_high + 1 tick
stop = old_high + 1 tick
stop = turtle_soup_high + 1 tick
stop = model_candle_high + spread
stop = structural_high + ATR buffer
stop = confirming_candle_high
```

Likewise, do not infer a bullish mirror from the bearish `stop loss up here` wording without direct evidence.

## Required-field impact

### `INVALIDATION`

Current safe state:

`PARTIAL`

Why it does not close:

- a stop is directly mentioned in a Model #1 worked example;
- its exact owner is not textually bound;
- setup-cancellation semantics remain distinct and unresolved;
- execution buffer is absent.

### `EXACT_PREDICATE`

No change to closure status.

`MODEL_1_GEOMETRY = STRONG_PARTIAL`

The unresolved stop owner compounds the already unresolved old-extreme selector and `thick` semantics.

## Two-engineer test

Give two engineers the current source evidence and ask them to implement the stop. One may choose the Model #1 candle high; another may choose the swept old high or a Turtle-Soup structural extreme. Each choice is plausible from broader context, but the admitted source does not deterministically choose among them.

Therefore:

```text
TWO_ENGINEER_TEST = FAIL_FOR_MODEL1_INVALIDATION
```

## Remaining Model #1 closure debt

After this pass:

1. **Old-extreme selector** — unresolved; bounded route exhausted in Issue #91.
2. **`thick` semantics** — source term direct; deterministic meaning absent from Issue #96.
3. **Structural stop owner / setup invalidation** — deictic partial evidence only; requires chart/frame binding or new explicit first-party statement.
4. **Expiry / cancellation** — next distinct bounded target; no direct Model #1 lifecycle rule is yet admitted.
5. **Exact execution fill policy** — close is direct signal trigger, but broker fill policy remains unspecified if source-level distinction is required.

The next dependency-safe research pass should target **Model #1 expiry/cancellation semantics**, not loop the same stop excerpt unless a technical chart frame becomes directly bindable.

## Final disposition

```text
MODEL1_STOP_MENTION           = DIRECT
MODEL1_STOP_OWNER             = UNRESOLVED
MODEL1_SETUP_INVALIDATION     = UNRESOLVED
TRUE_MSS_TS_STOP              = DIRECT_EXAMPLE_ONLY
V0.1_ONE_TICK_BUFFER          = PROJECT_ONLY
MODEL_1_GEOMETRY              = STRONG_PARTIAL
MODEL_1_CANDIDATE_READY       = FALSE
ISSUE_16                      = KEEP_BLOCKED
ISSUE_37                      = MUST_NOT_START
```

No candidate, detector/count, P&L/backtest, OOS/CONFIRM, paper, shadow, live, broker, stop-optimization, threshold, or historical-result state is changed by this report.
