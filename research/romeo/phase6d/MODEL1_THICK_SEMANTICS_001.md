# Phase 6D — Model #1 `thick` Semantics 001

**Date:** 2026-08-15  
**Tracking:** Issue #96  
**Baseline:** Recovery 007 / PR #88; minimum-closure map PR #90; old-extreme selector PR #93; trigger/retrace contract PR #95  
**Mode:** bounded first-party evidence synthesis only  
**Issue #16 disposition:** `KEEP_BLOCKED`

## Decision

Romeo's admitted first-party timed text repeatedly uses the adjective `thick` for the Model #1 sweep candle in both bearish and bullish descriptions. The current first-party corpus does **not** define a numerical formula, threshold, comparison set, or explicit mandatory-vs-descriptive rule for `thick`.

Therefore the safe bounded classification is:

```text
THICK_TERM_USAGE                = DIRECT_REPEATED
THICK_CAUSALITY                 = UNRESOLVED
THICK_NUMERIC_DEFINITION        = ABSENT
CLASSIFICATION                  = NO_DETERMINISTIC_THICK_RULE_FOUND
PROJECT_BODY_FRACTION_0_50      = PROJECT_ONLY / NOT_ROMEO_CLAIM
NEW_CLOSING_FIELD_EVIDENCE      = 0
MODEL_1_GEOMETRY                = STRONG_PARTIAL / KEEP_BLOCKED
INDEPENDENT_CLOSURE_AUDIT       = NOT_READY
ISSUE_16                        = KEEP_BLOCKED
ISSUE_37                        = MUST_NOT_START
```

The historical v0.1 `body / full_range >= 0.50` parameter remains an immutable project formalization for that frozen candidate. This report does not rewrite, invalidate, optimize, or retroactively reinterpret the v0.1 result. It only prevents that project parameter from being promoted into a new Romeo-derived predicate without first-party evidence.

## First-party evidence examined

### Episode 1 — 10:18–10:56

Source: `ROMEO-2025-S1`  
Locator: `https://www.youtube.com/watch?v=T7udbrWlARI&t=618s#auto-en-json3-10-18-10-56`  
Artifact SHA-256: `0f282f00bfdf78037c859a821cb5e489df877cd45cb30761146d11c90bb04aad`

Admitted timed-text excerpt:

> "stab again into the old high ... the thick up close candle which stabbed into the old high. You close below it ... that's the trigger you use to enter a short or a sell, stop loss up here ... target the lows one by one."

What this proves:

- Romeo uses `thick` to describe the selected bearish up-close sweep candle in the Model #1 explanation;
- the selected candle participates in the close-trigger relation established by Issue #94;
- `thick` is source language, not a term invented by the project.

What this does not prove:

- a body/range threshold;
- ATR-relative size;
- body percentile;
- minimum absolute range;
- comparison against preceding candles;
- whether `thick` is a hard rejection condition rather than descriptive emphasis.

### Episode 1 — 15:05–15:41

Source: `ROMEO-2025-S1`  
Locator: `https://www.youtube.com/watch?v=T7udbrWlARI&t=905s#auto-en-json3-15-05-15-41`  
Artifact SHA-256: `99250b19cee13890422e00d2653814d156aabee2ee372e0362b71a6caf48fe8e`

Admitted timed-text excerpt:

> "high, stab into the old high ... a thick up close candle. As soon as you close below it, it's the trigger ... vice versa ... stab into the old low ... a thick down close candle and you use that as the trigger."

What this proves:

- Romeo repeats the `thick` adjective in the bearish explanation;
- the bullish inverse description also uses `thick` for the down-close candle;
- the term is directionally symmetric in the admitted explanation.

What this does not prove:

- that every non-`thick` candle is invalid;
- a machine-testable definition of `thick`;
- whether the same quantitative property, if one exists, must be direction-neutral;
- any source-backed numerical value.

## Project-parameter separation

The existing repository deliberately introduced a numerical threshold for the frozen v0.1 candidate:

```text
P2-PARAM-M1-THICK-050
body / full_range >= 0.50
```

Canonical governance records explicitly state that this number was introduced as a transparent project parameter because Romeo's source wording remained qualitative.

Relevant project records:

- `docs/adr/ADR-004-freeze-narrow-d1-h1-model1-subset.md`
- `strategy/CRT_V0.1_SPEC.md`
- `research/romeo/phase6b/BULLISH_MODEL1_EVIDENCE_GATE.md`

The frozen specification states that the source does not provide a numerical formula for every qualitative term and labels the `0.50` threshold a deterministic project interpretation, not a Romeo quotation or universal truth.

Therefore:

```text
SOURCE TERM        = `thick`
SOURCE FORMULA     = UNKNOWN
V0.1 PROJECT RULE  = body/full_range >= 0.50
SOURCE CREDIT FOR 0.50 = ZERO
```

## Why `MANDATORY_BUT_UNQUANTIFIED` is not promoted

The repeated wording makes `thick` strategy-relevant enough that it cannot simply be discarded without evidence. However, the bounded direct excerpts do not contain an explicit source statement equivalent to:

```text
A Model #1 candle MUST be thick
```

or:

```text
If the candle is not thick, Model #1 is invalid
```

The project must therefore distinguish:

```text
TERM_APPEARS_IN_RULE_EXPLANATION = true
```

from:

```text
HARD_FILTER_CAUSALITY = proven
```

The second proposition is not established by the current evidence.

For that reason, `MANDATORY_BUT_UNQUANTIFIED` would still overstate the source. The fail-closed classification is `NO_DETERMINISTIC_THICK_RULE_FOUND` with causality unresolved.

## Forbidden substitutions

Until Romeo directly defines the property, do not claim any of the following as Romeo semantics:

```text
body / full_range >= X
body >= k * ATR
range >= k * ATR
body percentile >= P
body larger than previous N candles
range larger than previous N candles
fixed pip/point minimum
volume threshold
volatility percentile
```

A future candidate may use a preregistered project parameter only if governance explicitly labels it as a project formalization and does not choose it after observing protected outcomes. That would create a new candidate version and would not close the first-party predicate debt.

## Required-field impact

### `EXACT_PREDICATE`

The close-trigger relation strengthened in Issue #94, but the Model #1 candle-qualification rule remains incomplete.

Safe state:

`STRONG_PARTIAL`

Reason:

- source uses `thick` repeatedly;
- no deterministic meaning is available;
- old-high/old-low selector remains unresolved from Issue #91.

### `DATA_REQUIREMENTS`

The evidence is insufficient to say whether deterministic Model #1 requires only OHLC candle direction/range or an additional comparative volatility dataset.

Safe state:

`PARTIAL`

Do not add ATR, rolling percentile, volume, or comparison-window data merely to operationalize the adjective.

## Two-engineer test

If two independent engineers are told only:

> select the `thick` up-close/down-close candle

then they can make materially different choices among candles with different body/range characteristics.

Even if both agree on the close-trigger relation from Issue #94, they cannot reproduce identical candidate selection without an invented definition.

Therefore:

```text
TWO_ENGINEER_TEST = FAIL_FOR_COMPLETE_MODEL_1
```

## Remaining Model #1 closure debt

After this pass:

1. **Old-extreme selector** — bounded route exhausted in Issue #91; requires genuinely new first-party semantics.
2. **`thick` qualification** — source term confirmed but deterministic semantics absent; requires a new explicit first-party definition or an independently versioned project formalization that receives zero closure credit.
3. **Invalidation / structural stop contract** — next distinct source-recovery target.
4. **Expiry / cancellation** — exact Model #1 lifecycle remains missing.
5. **Exact order-fill timing** — semantic close trigger is direct, but broker fill policy remains unresolved if source-level distinction is required.

The next dependency-safe research action should focus on the structural invalidation/stop evidence already present in Episodes 1 and 9, not loop again on `thick` without new source material.

## Final disposition

```text
THICK_SOURCE_TERM             = DIRECT
THICK_HARD_FILTER             = UNRESOLVED
THICK_NUMERIC_THRESHOLD       = UNKNOWN
V0.1_0_50_PARAMETER           = HISTORICAL_PROJECT_PARAMETER_ONLY
MODEL_1_GEOMETRY              = STRONG_PARTIAL
MODEL_1_CANDIDATE_READY       = FALSE
ISSUE_16                      = KEEP_BLOCKED
ISSUE_37                      = MUST_NOT_START
```

No candidate, detector/count, P&L/backtest, OOS/CONFIRM, paper, shadow, live, broker, threshold, or historical-result state is changed by this report.
