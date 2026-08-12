# P0-FIX-003 — Context Direction Can Flip on New Convincing CRT Evidence

**Fixture class:** `CANDIDATE_TEXTUAL`
**Blocker:** P0-05 Context Direction
**Doctrine baseline:** `CRT_SECRETS_2025`
**Source:** Romeo official Telegram
**Source URL:** https://t.me/s/officialRomeotpt?before=6461
**Evidence type:** first-party textual clarification

## First-party statement

Romeo states, in substance, that when a trader expects a bearish CRT but is shown a convincing bullish CRT instead, the trader should evaluate changing bias and act.

A later official Telegram post applies the same lesson to Bitcoin and says traders were liquidated by fading a bullish CRT.

## Safe inference

`context_direction` is not a permanently fixed label for the whole week/day/session.

The engine must support a causal, timestamped state transition:

```text
CURRENT_CONTEXT_DIRECTION
        ↓
NEW OPPOSITE CRT EVIDENCE
        ↓
QUALIFIES UNDER SOURCE-BACKED FLIP PREDICATE?
   ├── UNKNOWN / NO → retain prior state or fail closed
   └── YES
        ↓
SUPERSEDE PRIOR DIRECTION
        ↓
NEW CONTEXT_DIRECTION
```

## What this fixture resolves

- direction state must be versioned and timestamped;
- a prior bearish expectation can be superseded by later bullish CRT evidence;
- the opposite is expected to be testable as a separate mirror once directly evidenced;
- the engine must not treat HTF bias as immutable after initial selection.

## What this fixture does NOT resolve

- exact definition of `convincing CRT`;
- which timeframe owns the flip;
- whether the flip requires a close, Turtle Soup, Model #1, true MSS, target-state change, or combination;
- conflict handling across W1/D1/H4;
- exact bullish/bearish numeric predicate;
- whether a flip is immediate or only after a candle closes.

## Engineering consequence

Use a history-aware object rather than a single mutable enum with no provenance:

```python
ContextDirectionState(
    direction,            # BULLISH | BEARISH | NEUTRAL | UNKNOWN
    valid_from,
    supersedes_state_id,
    evidence_ids,
    observed_at,
    resolver_version,
)
```

Every trade candidate must reference the direction state that existed at its decision timestamp.

## Closure credit

This fixture earns **architecture-level P0-05 credit** for state transition semantics.
It does **not** close the alpha predicate that determines when a direction flip is valid.

## Status

`P0-05 remains PARTIALLY_RESOLVED`.
