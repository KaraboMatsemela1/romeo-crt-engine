# P0 First-Party Clarifications — Romeo Official Telegram

**Candidate:** `CRT-C3-ALIGNED-v0.1-DRAFT`  
**Base doctrine:** `CRT_SECRETS_2025`  
**Status:** RECONCILIATION ADDENDUM / DOES NOT CLOSE P0 BY ITSELF  
**Date:** 2026-08-12

## Purpose

Capture concise first-party Romeo statements that materially narrow the remaining P0 search space but do not yet constitute complete deterministic algorithms.

Post-series statements are stored as **clarifications** rather than silently rewriting the `CRT_SECRETS_2025` snapshot. They may be promoted into the v0.1 strategy only through explicit reconciliation.

---

## CLAR-TS-001 — Old CRTH is an explicit bearish reaction reference

### First-party statement

In an NQ post, Romeo states that when he is bearish, his ideal reaction is:

```text
1. Candle opens
2. Stabs into an old CRTH
3. Dumps
```

### Safe reconciliation

This promotes one explicit bearish Turtle-Soup/reference subtype candidate:

```text
ReferenceExtremeType.OLD_CRTH
```

It narrows the broad 2024 `old high` language toward an old **CRT High** in at least this bearish setup class.

### Not resolved

- what makes a CRTH `old`;
- owning timeframe;
- reference expiry/consumption;
- stab tolerance;
- close-back requirement;
- confirmation timing;
- bullish `old CRTL` mirror.

**P0 impact:** P0-04 reference taxonomy narrowed; overall P0-04 remains open.

---

## CLAR-TS-002 — CRTH/L → 50% is explicitly associated with Turtle-Souping CRTs

### First-party statement

In September 2025, Romeo states that trading careers can be built around taking price from `CRTH/L` to the 50%, immediately followed by `Turtle souping CRTs`.

### Safe reconciliation

This strengthens the relationship:

```text
CRT EXTREME (CRTH / CRTL)
        ↓
TURTLE-SOUP / REACTION CONTEXT
        ↓
50% OBJECTIVE
```

This is consistent with the Episode-8 Target-1 treatment.

### Not resolved

- whether every valid Turtle Soup must use a CRTH/CRTL rather than another old high/low;
- exact target-touch semantics;
- exact entry/confirmation;
- whether 50% is universally T1 for every setup family.

**P0 impact:** strengthens P0-04 and later P1 target research; no P0 closure by itself.

---

## CLAR-DIR-001 — Context direction is stateful, not immutable

### First-party statement

Romeo says that when a trader expects a bearish CRT but the market presents a convincing bullish CRT instead, the trader should evaluate changing bias and act swiftly. He later references the same principle in a Bitcoin example.

### Safe reconciliation

The engine must not model context direction as an immutable label fixed for an entire week/day merely because the initial HTF expectation was bullish or bearish.

Required conceptual state machine:

```text
INITIAL_CONTEXT_DIRECTION
        ↓
NEW OPPOSITE CRT EVIDENCE
        ↓
IS OPPOSITE CRT SOURCE-DEFINED AS CONVINCING?
   ├── UNKNOWN → retain/UNKNOWN according frozen policy
   └── YES → DIRECTION_TRANSITION_CANDIDATE
        ↓
new context direction becomes available causally
```

The exact `convincing CRT` predicate remains unresolved and must not be replaced with hindsight trend detection.

### Engineering implication

Direction objects should retain:

```python
DirectionState(
    value,
    established_at,
    evidence_ids,
    supersedes_direction_id,
    transition_reason,
)
```

rather than a timeless `bias = bullish/bearish` scalar.

**P0 impact:** P0-05 architecture materially refined; exact resolver still open.

---

## CLAR-CLOSE-001 — Close versus a reference level can be decision-relevant

### First-party statement

In a Bitcoin follow-up, Romeo specifically highlights that price did not close above a named level (120,000) before congratulating followers on the result.

### Safe reconciliation

This provides first-party support that **close location relative to a reference can be meaningful** in at least some CRT trade frames. It is compatible with the 2024/2025 indexed evidence emphasizing closes over wick-only excursions.

### Not resolved

Do not generalize this into:

```python
if close_below_level:
    bearish = True
```

for all contexts.

Unknown:
- what the 120,000 level represented;
- which timeframe close was relevant;
- whether it was direction, invalidation, confirmation, or target-state evidence;
- whether the same predicate applies to CRTH/CRTL.

**P0 impact:** supporting evidence for P0-05/P0-04 close significance; no exact predicate promoted.

---

## CLAR-TIME-001 — Explicit synchronization times exist, but their strategy role/timezone is unresolved

### First-party statement

Romeo posts the times:

```text
00:00
03:00
08:15
09:30
13:30
```

and says that if a move is missed, traders can use these times to `get in sync` and should not FOMO.

### Safe reconciliation

The first-party corpus therefore contains explicit intraday synchronization times.

However, the post does not by itself establish:

- timezone;
- instrument class;
- whether these are entry windows, key times, session anchors, macro times, or review checkpoints;
- whether the list is universal;
- relationship to H4 candle construction.

### Critical non-inference

These times **must not** be used to close P0-03 H4 anchors.

They are stored as:

```text
TimeReferenceCandidate(
    values=[00:00,03:00,08:15,09:30,13:30],
    timezone=UNKNOWN,
    semantics=SYNC_TIME_UNKNOWN,
)
```

**P0 impact:** narrows the time-source search for P0-02/P0-03 but remains non-executable.

---

## Reconciliation consequences

### P0-04

New safe addition:

```text
bearish OLD_CRTH = explicitly source-backed reference subtype candidate
```

Full reference registry, confirmation, timeout and lifecycle remain open.

### P0-05

New safe addition:

```text
context_direction is versioned/stateful and may transition when new qualifying opposite CRT evidence appears
```

The transition trigger remains open.

### P0-03

No H4 anchor closure. Explicit sync times must not be mistaken for bar anchors.

### P0-02

The existence of explicit time references is reinforced, but their key-level semantics remain undefined.

## Promotion policy

These clarifications reduce the search space; they do not authorize backtesting of unresolved rules.

Every executable promotion still requires:
- exact predicate;
- causal availability timestamp;
- positive fixtures;
- negative fixtures;
- contradiction reconciliation;
- frozen strategy version.
