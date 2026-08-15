# Phase 6D — Model #1 Expiry / Cancellation 001

**Date:** 2026-08-15  
**Tracking:** Issue #100  
**Baseline:** Recovery 007 / PR #88; minimum-closure map PR #90; Model #1 bounded passes through PR #99  
**Mode:** bounded first-party evidence synthesis only  
**Issue #16 disposition:** `KEEP_BLOCKED`

## Decision

The current provenance-bound first-party corpus contains **no deterministic Model #1 expiry/cancellation rule**. `PREDICATE_LEDGER_V2.json` requires `EXPIRY` for `MODEL_1_GEOMETRY`, but the Model #1 row has no first-party evidence item mapped to that field.

The historical v0.1 strategy expires new-entry eligibility at Candle-3 close. That is an immutable frozen project formalization for `CRT-C3-D1-H1-M1-BEAR-v0.1`; it is not a newly verified Romeo rule and receives zero first-party closure credit here.

```text
CLASSIFICATION                  = NO_DETERMINISTIC_MODEL1_EXPIRY_FOUND
MODEL1_EXPIRY                   = MISSING
MODEL1_CANCELLATION             = MISSING
GENERAL_TIME_CONTEXT            = PARTIAL / NOT_MODEL1_EXPIRY
V0.1_C3_CLOSE_EXPIRY            = HISTORICAL_PROJECT_FORMALIZATION_ONLY
NEW_CLOSING_FIELD_EVIDENCE      = 0
MODEL_1_GEOMETRY                = STRONG_PARTIAL / KEEP_BLOCKED
INDEPENDENT_CLOSURE_AUDIT       = NOT_READY
ISSUE_16                        = KEEP_BLOCKED
ISSUE_37                        = MUST_NOT_START
```

## Evidence boundary

### Provenance-bound Model #1 evidence

The current first-party Model #1 row in `PREDICATE_LEDGER_V2.json` contains evidence for:

- `EXACT_PREDICATE` — Model #1 prioritization, sweep-candle/close trigger, directional symmetry, one-specific-candle wording;
- `DIRECTION_TIMEFRAME_OWNERSHIP` — public monthly→daily, weekly→4H and daily→1H Model #1 mappings.

It contains **no evidence item for `EXPIRY`**.

Recovery 007's admitted Model #1 excerpts establish geometry/trigger relationships, but none says when an otherwise valid Model #1 becomes stale, cancelled, or no longer eligible.

### General time/Candle-3 material

The wider corpus contains partial doctrine that timing matters, Candle-3 eligibility depends on prior state, and strategy framing may include time as a dimension. Those facts are not equivalent to a Model #1 expiry rule.

A general proposition such as:

```text
TIME_MATTERS = true
```

cannot safely become:

```text
MODEL1 expires at Candle-3 close
```

without an explicit first-party bridge.

Likewise, a position-level time-exit discussion does not define pre-entry setup expiry.

## Historical v0.1 project rule

The frozen v0.1 specification states:

```text
new-entry eligibility exists only inside Candle 3
if no confirmed Model #1 occurs before C3 closes -> NO_SIGNAL
```

This rule was part of the deterministic project freeze. It remains valid for interpreting the historical v0.1 candidate and its immutable Phase 6/6B results.

It must not be relabeled as a universal Romeo Model #1 lifecycle rule.

Therefore:

```text
V0.1_C3_EXPIRY_SOURCE_TYPE = PROJECT_FORMALIZATION
FIRST_PARTY_CLOSURE_CREDIT = ZERO
```

No historical spec, detector, count or result is changed by this classification.

## Setup expiry vs other lifecycle concepts

The project must keep these separate:

### Pre-entry setup expiry

Question:

> After a Model #1 geometry/trigger path becomes possible, what event or time boundary makes a new entry no longer valid?

Current source state:

`MISSING`

### Pre-entry structural invalidation

Question:

> What price/structure event destroys the setup before entry?

Current source state from Issue #98:

`UNRESOLVED / PARTIAL_DEICTIC_CONTEXT_ONLY`

### Position time exit

Question:

> After an order is filled, can/should the position be closed because a time boundary is reached?

This is a separate management predicate. General time-exit references in broader trade framing do not answer Model #1 pre-entry expiry.

### Target consumption

Historical v0.1 rejects a setup when its frozen target is consumed before entry. This is a candidate-specific project lifecycle guard and cannot be promoted as universal Model #1 cancellation without direct first-party evidence.

## Rejected promotions

Do not claim any of these as Romeo Model #1 semantics from the current corpus:

```text
expiry = Candle-3 close
expiry = end of session
expiry = next key time
expiry = next HTF candle open
expiry = N lower-timeframe candles after trigger
expiry = target touch
expiry = first opposing signal
expiry = end of day
```

Any future project candidate may preregister a deterministic lifecycle parameter if governance explicitly labels it as a project formalization, but that does not close the first-party predicate.

## Required-field impact

### `EXPIRY`

State remains:

`MISSING`

No provenance-bound first-party artifact currently supplies a deterministic Model #1 expiry/cancellation predicate.

### `INFORMATION_AVAILABILITY_TIME`

Issue #94 established that the confirming close is the semantic trigger availability point. That does not tell us how long the triggered setup remains eligible.

State remains:

`STRONG_PARTIAL`

### `EXACT_PREDICATE`

No closure upgrade. The full Model #1 predicate still depends on unresolved old-extreme selection, `thick` semantics, invalidation/stop ownership, and lifecycle.

State:

`STRONG_PARTIAL`

## Two-engineer test

Two engineers given the same first-party corpus can both recognize the close trigger, yet one might allow entry indefinitely after that trigger while another might expire at Candle-3/session/HTF boundaries. The source does not deterministically select among those lifecycle policies.

Therefore:

```text
TWO_ENGINEER_TEST = FAIL_FOR_MODEL1_EXPIRY
```

## Model #1 closure state after bounded passes

The completed bounded passes now establish:

```text
old-high/old-low selector     = NO_SELECTOR_RULE_FOUND
close vs retrace              = CLOSE_IS_EXECUTION_TRIGGER; mandatory retrace NOT_PROVEN
`thick` semantics             = NO_DETERMINISTIC_THICK_RULE_FOUND
stop/invalidation             = PARTIAL_DEICTIC_CONTEXT_ONLY
expiry/cancellation           = NO_DETERMINISTIC_MODEL1_EXPIRY_FOUND
```

Strong source-backed pieces remain:

- one-specific-candle Model #1 object;
- directional sweep-candle examples;
- close beyond the selected candle as the semantic trigger;
- bullish/bearish trigger symmetry in Episode 1;
- three public HTF→Model #1 timeframe mappings.

But the remaining debts are semantic absences or frame-bound ambiguities, not broad-search problems.

## Next recommendation

Do **not** continue another broad Model #1 corpus sweep.

The next safe action should be a **Model #1 closure-exhaustion synthesis** that reconciles Issues #89/#91/#94/#96/#98/#100 and decides whether any additional current-corpus-only research action has positive closure leverage.

Expected decision rule:

- if an unresolved field has a specific uninspected first-party frame/audio locator capable of resolving it, create one bounded recovery;
- otherwise classify the field as requiring genuinely new first-party evidence and stop looping the current corpus.

Only after that synthesis should the queue decide whether to pivot to the next-nearest predicate such as `TRUE_MSS_ALGORITHM`.

## Final disposition

```text
MODEL1_EXPIRY                 = MISSING
V0.1_C3_CLOSE_RULE            = PROJECT_ONLY / HISTORICAL
MODEL_1_GEOMETRY              = STRONG_PARTIAL
MODEL_1_CANDIDATE_READY       = FALSE
ISSUE_16                      = KEEP_BLOCKED
ISSUE_37                      = MUST_NOT_START
```

No candidate, detector/count, P&L/backtest, OOS/CONFIRM, paper, shadow, live, broker, time-window optimization, threshold, or historical-result state is changed by this report.
