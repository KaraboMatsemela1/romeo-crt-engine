# P0-FIX-002 — Bearish Old-CRTH Rule Clarification

**Source:** Romeo official Telegram  
**Fixture class:** FIRST-PARTY RULE CLARIFICATION  
**Doctrine relationship:** post-CRT-Secrets-2025 clarification; compatible with, but not silently merged into, the `CRT_SECRETS_2025` snapshot  
**Alpha-fixture status:** **PARTIAL P0-04 CLOSURE CREDIT ONLY**  
**Date recorded:** 2026-08-12

## First-party statement

In a post accompanying an NQ trade, Romeo states the ideal bearish reaction he wants to see as the following sequence:

1. candle opens;
2. price stabs into an **old CRTH**;
3. price dumps.

The same official channel also states in September 2025 that entire trading careers can be built around taking price from `CRTH/L` to the 50%, followed immediately by the phrase `Turtle souping CRTs`.

## What this resolves

### P0-04 — eligible reference subtype

The earlier Turtle Soup evidence used the broader phrase `old high / old low`. This first-party clarification narrows at least one valid bearish reference class to:

```text
REFERENCE_TYPE = OLD_CRTH
DIRECTION = BEARISH
```

Therefore the reference registry may safely include:

```python
ReferenceExtremeType.OLD_CRTH
```

as an explicitly source-backed candidate subtype.

This does **not** prove that every CRTH is eligible. `old` still requires lifecycle/freshness semantics.

## What this does NOT resolve

Do not infer from this text alone:

- exact definition of `old`;
- whether the CRTH must come from W1, D1, H4, or another timeframe;
- how the CRTH itself was selected;
- minimum or maximum stab distance;
- whether the stab candle must close back below the CRTH;
- whether the dump itself is the confirmation or merely the desired outcome;
- confirmation timeout;
- reference consumption/reuse;
- true breakout invalidation;
- exact entry model;
- stop placement;
- bullish mirror using `old CRTL`.

The bullish `old CRTL` mirror remains a symmetry hypothesis until Romeo states or demonstrates it explicitly enough to promote.

## Relationship to P0-01

`CRTH` depends on a previously defined CRT range. Therefore this clarification strengthens the dependency chain:

```text
PARENT CRT SELECTED
    ↓
CRTH / CRTL EXIST
    ↓
OLD CRTH MAY BECOME BEARISH TS REFERENCE
```

It does not solve the Parent CRT / Candle-1 selector itself.

## Relationship to P0-05

The wording begins with `When I'm bearish`, meaning the bearish context is already established before the stab into old CRTH.

Safe orchestration inference:

```text
CONTEXT_DIRECTION = BEARISH
    ↓
OLD_CRTH REACTION OBSERVED
```

Not:

```text
OLD_CRTH STAB
    ↓
therefore context must be bearish
```

This supports the existing rule that context direction precedes interpretation of manipulation evidence.

## Closure credit

```text
P0-04 eligible reference taxonomy:
    OLD_CRTH for bearish context = SOURCE-BACKED SUBTYPE

P0-04 full reference registry = OPEN
P0-04 confirmation predicate = OPEN
P0-04 lifecycle/consumption = OPEN
P0-04 overall status = PARTIALLY_RESOLVED
```

## Evidence quality

- first-party textual clarification from Romeo official Telegram;
- no dependence on third-party semantic summary for the key statement;
- associated NQ image/outcome is not required to establish the stated three-step ideal reaction rule;
- post-series timing means this should be stored as a clarification layer and reconciled deliberately before a 2025 doctrine freeze.
