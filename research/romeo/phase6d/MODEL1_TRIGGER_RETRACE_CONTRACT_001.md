# Phase 6D — Model #1 Trigger vs Retrace Contract 001

**Date:** 2026-08-15  
**Tracking:** Issue #94  
**Baseline:** Recovery 007 / PR #88; minimum-closure map PR #90; old-extreme selector PR #93  
**Mode:** bounded first-party evidence synthesis only  
**Issue #16 disposition:** `KEEP_BLOCKED`

## Decision

The admitted first-party evidence directly supports the **close beyond the selected Model #1 candle as the signal/entry trigger**. It does **not** establish that a later retrace into Model #1 is universally required before execution, and it does not define exact order-fill timing at the confirming close.

```text
CONTRACT_CLASSIFICATION          = CLOSE_IS_EXECUTION_TRIGGER
CONFIRMATION_SIGNAL              = DIRECT_SUPPORTED
RETRACE_REQUIREMENT              = NOT_PROVEN
ORDER_FILL_TIMING                = UNRESOLVED
RETRACE_ENTRY_PRICE/TOLERANCE    = UNRESOLVED
NEW_CLOSING_FIELD_EVIDENCE       = 0
MODEL_1_GEOMETRY                 = STRONG_PARTIAL / KEEP_BLOCKED
INDEPENDENT_CLOSURE_AUDIT        = NOT_READY
ISSUE_16                         = KEEP_BLOCKED
ISSUE_37                         = MUST_NOT_START
```

This classification is deliberately limited to the **semantic trigger**. It does not convert Romeo's wording into an implementation-specific market order, close-auction fill, next-tick order, limit order, or mandatory retracement entry.

## First-party evidence examined

### Episode 1 — 10:18–10:56

Source: `ROMEO-2025-S1`  
Locator: `https://www.youtube.com/watch?v=T7udbrWlARI&t=618s#auto-en-json3-10-18-10-56`  
Artifact SHA-256: `0f282f00bfdf78037c859a821cb5e489df877cd45cb30761146d11c90bb04aad`

Admitted timed-text excerpt:

> "stab again into the old high ... the thick up close candle which stabbed into the old high. You close below it ... that's the trigger you use to enter a short or a sell, stop loss up here ... target the lows one by one."

Safe evidence credit:

- a selected candle stabs into an old high;
- a later close below that selected candle is explicitly called **the trigger**;
- Romeo directly links that trigger to entering a short/sell;
- the excerpt does not specify exact broker order timing, price, slippage handling, retracement requirement, or setup expiry.

### Episode 1 — 15:05–15:41

Source: `ROMEO-2025-S1`  
Locator: `https://www.youtube.com/watch?v=T7udbrWlARI&t=905s#auto-en-json3-15-05-15-41`  
Artifact SHA-256: `99250b19cee13890422e00d2653814d156aabee2ee372e0362b71a6caf48fe8e`

Admitted timed-text excerpt:

> "high, stab into the old high ... a thick up close candle. As soon as you close below it, it's the trigger ... vice versa ... stab into the old low ... a thick down close candle and you use that as the trigger."

Safe evidence credit:

- reinforces the close relation as the trigger;
- directly states directional symmetry at the trigger level;
- does not define whether an order must be filled immediately after that close or after a later retracement;
- does not define the qualifying old-high/old-low selector or measurable `thick` rule.

### Episode 9 — 02:02–02:58

Source: `ROMEO-2025-S9`  
Locator: `https://www.youtube.com/watch?v=2sxdsgcIeYA&t=122s#auto-en-json3-02-02-02-58`  
Artifact SHA-256: `5cfd666a2fb8492fcaa6d258b52126660a23a97dc9fd2230dbe1c009fd5b9ab0`

Admitted timed-text excerpt:

> "the one specific candle ... that liquidated the old high ... it's not a zone ... when they close below it ... retrades into model number one and then dumps."

Safe evidence credit:

- reinforces that Model #1 is anchored to one specific candle rather than an arbitrary multi-candle zone;
- establishes a worked sequence in which a close below occurs before a later retrade into Model #1 and continuation;
- does **not** say that every valid Model #1 must retrade before entry;
- does **not** say that the retrade itself is the only valid entry trigger;
- does not define retrade tolerance, exact price, timeout, or cancellation semantics.

## Reconciliation

The Episode 1 wording is stronger than a generic descriptive example: Romeo explicitly calls the close **the trigger used to enter**. Therefore the bounded question can advance beyond `PARTIAL_CONTEXT_ONLY`.

The Episode 9 worked sequence does not contradict Episode 1. The safest reconciliation is:

```text
QUALIFY MODEL-1 CANDLE
        ↓
CONFIRMING CLOSE BEYOND SELECTED CANDLE
        ↓
MODEL-1 SIGNAL/TRIGGER BECOMES AVAILABLE
        ↓
POSSIBLE LATER RETRADE IN WORKED EXAMPLE
```

What the evidence does **not** prove is the execution policy after signal availability.

It would be an unsupported promotion to encode either of these as Romeo's universal rule:

```text
ON_CONFIRMING_CLOSE -> MARKET_ORDER_AT_CLOSE
```

or

```text
CONFIRMING_CLOSE -> WAIT_FOR_MANDATORY_RETRACE -> LIMIT_ENTRY
```

Neither exact order policy is defined by the admitted evidence.

## Required-field impact

### `CONFIRMATION`

This field materially strengthens.

Safe statement:

```text
For the admitted Model #1 examples, the close beyond the selected sweep candle is directly described as the trigger.
```

Disposition:

`DIRECT_SUPPORTED_AT_SIGNAL_LEVEL`

This is **not** marked `CLOSING` because the predicate cannot be instantiated reproducibly while the qualifying old extreme and candle-qualification semantics remain unresolved.

### `INFORMATION_AVAILABILITY_TIME`

The evidence supports a causal ordering constraint:

```text
signal must not be treated as available before the confirming close is known
```

However, the repository still lacks an explicit source-defined broker/order timestamp contract such as same-close execution, next tick, next bar open, or retracement touch.

Disposition:

`STRONG_PARTIAL`

### `EXACT_PREDICATE`

The trigger relation is narrower now, but the full predicate remains incomplete because Issue #91 found no deterministic old-high/old-low selector and the `thick` qualifier remains unresolved.

Disposition:

`STRONG_PARTIAL`

## Two-engineer test

Two engineers can now agree on the **trigger relation** if they are handed the same already-qualified Model #1 candle:

- bearish: close below the selected bearish Model #1 candle;
- bullish: inverse trigger around the selected bullish Model #1 candle.

They still cannot independently generate materially identical complete signals from raw market data because they can disagree on:

1. which old high/old low qualifies;
2. which sweep candle qualifies when multiple candidates exist;
3. whether `thick` is causal and how to measure it;
4. exact entry fill policy after trigger;
5. invalidation and buffer;
6. expiry/cancellation.

Therefore:

```text
TWO_ENGINEER_TEST = FAIL_FOR_COMPLETE_MODEL_1
```

## Remaining Model #1 closure debt

After this pass, the priority order is:

1. **Candle qualification / `thick` semantics** — mandatory measurable condition or descriptive wording?
2. **Invalidation / structural stop contract** — universal anchor versus example-specific placement.
3. **Expiry / cancellation** — when an otherwise triggered/qualified Model #1 ceases to be valid.
4. **Execution fill policy** — only if the final strategy specification requires a source-defined distinction between immediate post-close and retracement execution.
5. **Old-extreme selector** — remains semantic absence from Issue #91 and requires genuinely new first-party evidence; do not repeatedly search the same bounded passages.

The old-extreme selector remains the largest unresolved semantic, but its bounded route is exhausted. Research should therefore continue with the next distinct question rather than looping the same source set.

## Final disposition

```text
MODEL_1_CLOSE_TRIGGER       = DIRECT_SUPPORTED_AT_SIGNAL_LEVEL
MANDATORY_RETRACE_ENTRY     = NOT_PROVEN
EXACT_ORDER_FILL_TIMING     = UNRESOLVED
MODEL_1_GEOMETRY            = STRONG_PARTIAL
MODEL_1_CANDIDATE_READY     = FALSE
ISSUE_16                    = KEEP_BLOCKED
ISSUE_37                    = MUST_NOT_START
```

No candidate, detector/count, P&L/backtest, OOS/CONFIRM, paper, shadow, live, broker, threshold, or historical-result state is changed by this report.
