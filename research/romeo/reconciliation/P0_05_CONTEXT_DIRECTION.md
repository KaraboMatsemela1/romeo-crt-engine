# P0-05 — Higher-Timeframe Context Direction

**Candidate:** `CRT-C3-ALIGNED-v0.1-DRAFT`  
**Doctrine snapshot:** `CRT_SECRETS_2025`  
**Status:** **PARTIALLY RESOLVED / P0 REMAINS OPEN**  
**Date:** 2026-08-12

## Purpose

Define a causal, auditable contract for higher-timeframe market direction so the first CRT candidate can reject counter-direction setups without using future trend knowledge or arbitrarily choosing whichever timeframe agrees with the trade.

The intended output domain is:

```text
BULLISH
BEARISH
NEUTRAL
UNKNOWN
```

P0-05 remains a freeze blocker because Episode 8 makes direction alignment a setup-quality filter and Episode 9 requires SMT to be interpreted only after higher-timeframe direction is already known.

## Evidence base

### 2024 CRT foundation

The first-pass foundation transcript/summary records that Romeo uses **closes versus wicks** when determining bias and emphasizes waiting for candle closures rather than using wick movement alone as confirmation.

Safe interpretation:

- close information can carry directional evidence;
- wick-only excursions cannot automatically establish a durable directional state;
- the exact close relationship required for the canonical HTF direction algorithm is still not fully defined.

This source does **not** safely justify a generic rule such as `green candle = bullish` or `close > prior close = bullish`.

### Episode 8 — When does CRT fail?

The indexed Episode-8 material states that one major apparent CRT failure class is taking a CRT against prevailing/higher-timeframe direction.

Current supported policy:

```text
HTF BULLISH  -> prefer/allow bullish CRT
HTF BEARISH  -> prefer/allow bearish CRT
COUNTERTREND -> reject from v0.1 / separate experiment
```

Episode 8 does not provide, in the currently available evidence, the complete deterministic algorithm for how HTF bullish/bearish state itself is calculated.

### Episode 9 — Connecting the dots

Episode 9 provides the strongest orchestration constraint:

```text
Bullish SMT -> only meaningful under already-established bullish HTF context
Bearish SMT -> only meaningful under already-established bearish HTF context
```

Therefore SMT cannot be used to create the higher-timeframe direction that is later used to validate the same SMT event. That would be circular.

### Episode 4 / Candle anatomy

Episode 4 reinforces that the trade candle and its context are chosen before lower-timeframe pattern detection. The indexed summary describes directional CRT/Turtle-Soup examples, but does not provide a sufficiently reliable universal bias algorithm.

## What P0-05 can now resolve

### DIR-P001 — direction is a pre-entry context state

**Status:** HIGH_CONFIDENCE / ORCHESTRATION

`context_direction` must exist before:

- Candle-3 trade approval;
- SMT directional interpretation;
- lower-timeframe Model #1 / true-MSS execution;
- countertrend rejection.

Required information flow:

```text
CAUSAL HTF MARKET STATE
        ↓
CONTEXT_DIRECTION
        ↓
KEY LEVEL / TARGET / C3 STATE
        ↓
SMT + LTF CONFIRMATION
        ↓
ENTRY
```

Prohibited circularity:

```text
SMT says bullish
    ↓
therefore HTF direction = bullish
    ↓
therefore bullish SMT is valid
```

---

### DIR-P002 — direction and candidate direction are separate fields

**Status:** ENGINEERING RESOLVED

Represent separately:

```python
context_direction   # market / HTF state
candidate_direction # direction the proposed CRT trade wants to take
```

Alignment:

```python
if context_direction == BULLISH and candidate_direction == BULLISH:
    ALIGNED
elif context_direction == BEARISH and candidate_direction == BEARISH:
    ALIGNED
elif context_direction in {NEUTRAL, UNKNOWN}:
    UNKNOWN
else:
    COUNTERTREND
```

For v0.1:

```text
ALIGNED      -> may continue
COUNTERTREND -> reject
UNKNOWN      -> no trade
```

This alignment function is safe once both input directions are independently and causally defined.

---

### DIR-P003 — first v0.1 excludes countertrend CRT

**Status:** HIGH_CONFIDENCE / SCOPE DECISION

```python
allow_countertrend = False
```

This is a project scope decision supported by Episode 8's consistency guidance. It does not claim countertrend CRT can never work.

Any future countertrend study must use a separate strategy/experiment version.

---

### DIR-P004 — SMT is downstream of direction

**Status:** HIGH_CONFIDENCE

Episode 9 supports:

```text
context_direction first
SMT interpretation second
```

Therefore:

```python
SMTEvent.context_direction_source != SMTEvent itself
```

The direction state must have its own timestamp and evidence lineage prior to SMT qualification.

---

### DIR-P005 — close evidence is stronger than wick-only evidence

**Status:** PROVISIONAL-HIGH

The 2024 foundation repeatedly distinguishes candle closures from wick excursions when discussing bias/confirmation.

Safe architectural consequence:

```text
WICK_EVENT
    -> evidence / liquidity event
    -> cannot alone finalize HTF direction

QUALIFYING_CLOSE_EVENT
    -> may update direction state
```

But the exact close predicate remains unresolved.

Do **not** implement any of these without direct verification:

```python
bullish = close > prior_close
bullish = close > prior_high
bullish = close > candle_open
bearish = close < prior_close
bearish = close < prior_low
bearish = close < candle_open
```

Some may be components of Romeo's method, but the corpus pass does not yet establish one of them as the canonical HTF direction resolver.

---

### DIR-P006 — final active-candle close cannot be used before it exists

**Status:** ENGINEERING CONSTRAINT

If direction requires a candle close, the state can only change after that candle actually closes.

Prohibited:

```python
# decision at 14:00, D1 closes later
if daily.final_close > daily.open:
    context_direction = BULLISH
```

unless the Daily candle had already closed by the decision timestamp.

For an active HTF candle:

```text
final_close = UNKNOWN
```

Only completed prior candles and causal intrabar snapshots may be consumed.

---

### DIR-P007 — timeframe conflicts cannot be resolved by voting or hindsight

**Status:** ENGINEERING CONSTRAINT

Potential state:

```text
W1 = BULLISH
D1 = BEARISH
H4 = BULLISH
```

The project currently has no source-backed rule authorizing:

```python
majority_vote(W1, D1, H4)
highest_timeframe_always_wins()
nearest_timeframe_always_wins()
weighted_vote_by_timeframe_seconds()
```

If the frozen direction policy cannot resolve a conflict causally:

```text
context_direction = UNKNOWN
        ↓
NO TRADE
```

---

### DIR-P008 — direction owner must be explicit and versioned

**Status:** ENGINEERING CONTRACT / ALPHA RULE BLOCKED

The resolver must eventually expose:

```python
DirectionDecision(
    direction,
    owner_timeframe,
    supporting_timeframes,
    conflicting_timeframes,
    selected_at,
    evidence_ids,
    resolver_version,
)
```

`owner_timeframe` may not be inferred from which timeframe later predicted the trade correctly.

## What remains unresolved / blocking

### DIR-B001 — exact direction predicate

We still do not know the complete deterministic rule that converts HTF price action into:

```text
BULLISH | BEARISH | NEUTRAL
```

Need direct evidence for:

- which close relationship matters;
- whether previous candle high/low is the reference;
- whether candle open participates;
- whether multiple closes are required;
- whether key-level/liquidity state participates in direction;
- whether direction can be declared intrabar or only on completed HTF bars.

---

### DIR-B002 — which timeframe owns context direction

Unresolved cases include:

```text
W1 parent setup -> is W1 itself the direction owner, or a higher context?
D1 parent setup -> W1 direction, D1 direction, or combined state?
H4 parent setup -> D1 direction, W1+D1 hierarchy, or another mapping?
```

The project notation `W1 -> D1 -> H4` is analysis ordering, not evidence that W1 always wins.

---

### DIR-B003 — conflict resolution across W1/D1/H4

Need direct examples where Romeo explicitly handles opposing HTF states.

Until then:

```text
unresolved conflict -> UNKNOWN -> NO TRADE
```

---

### DIR-B004 — relationship between CRT direction and market direction

A selected CRT may have its own directional objective while the surrounding market has a broader directional state.

Need to distinguish:

```text
market_context_direction
parent_crt_direction
candidate_trade_direction
```

The exact derivation of each remains partially unresolved.

---

### DIR-B005 — role of parent candle color/anatomy

It is unsafe to assume:

```text
bullish parent candle -> bullish context
bearish parent candle -> bearish context
```

because the corpus contains examples where manipulation/reversal logic can produce movement opposite to the starting candle color/anatomy.

Candle color may be evidence, but it is not authorized as the direction algorithm.

---

### DIR-B006 — neutral/range state

CRT is explicitly range-based, and some contexts may not have a valid directional bias yet.

Need source-backed semantics for when state is:

```text
NEUTRAL
```

rather than forcing bullish/bearish classification.

Until resolved, ambiguous/ranging contexts may be represented as `UNKNOWN` for v0.1.

## Proposed non-executable direction interface

```python
class ContextDirectionResolver:
    def resolve(
        self,
        market_state,
        parent_crt,
        observed_at,
    ) -> DirectionDecision:
        ...
```

```python
DirectionDecision(
    direction,             # BULLISH | BEARISH | NEUTRAL | UNKNOWN
    owner_timeframe,
    supporting_timeframes,
    conflicting_timeframes,
    evidence_events,
    selected_at,
    resolver_version,
)
```

Every evidence event needs:

```python
DirectionEvidence(
    timeframe,
    event_type,            # CLOSE_RELATION | WICK_EVENT | KEY_LEVEL_STATE | OTHER
    reference_id,
    observed_at,
    value,
    confidence,
)
```

The architecture can be implemented before the alpha resolver is finalized, but the production/default resolver must return `UNKNOWN` where the source-backed rule is absent.

## Candidate state machine

```text
WAIT_FOR_PARENT_CONTEXT
        ↓
COLLECT CAUSAL HTF DIRECTION EVIDENCE
        ↓
APPLY SOURCE-BACKED DIRECTION RESOLVER
   ├── BULLISH
   ├── BEARISH
   ├── NEUTRAL
   └── UNKNOWN
        ↓
COMPARE WITH CANDIDATE DIRECTION
   ├── ALIGNED      -> continue
   ├── COUNTERTREND -> reject v0.1
   └── UNKNOWN      -> no trade
        ↓
KEY LEVEL / TARGET / FAILURE FILTERS
        ↓
SMT / LTF EXECUTION
```

## Test requirements

Before P0-05 can close, fixtures must include at least:

### Positive

- clearly bullish HTF context + bullish CRT candidate;
- clearly bearish HTF context + bearish CRT candidate;
- direction state known before the LTF signal;
- SMT occurring after direction is already established.

### Negative / conflict

- bearish CRT candidate inside bullish HTF context;
- bullish CRT candidate inside bearish HTF context;
- W1/D1 conflict;
- D1/H4 conflict;
- wick-only apparent break with no qualifying close;
- active unclosed HTF candle where final close would later reverse the apparent direction;
- ranged/ambiguous context that must return `UNKNOWN`.

## Acceptance criteria

P0-05 closes only when:

1. exact bullish predicate is deterministic;
2. exact bearish predicate is deterministic;
3. neutral/unknown handling is deterministic;
4. direction owner timeframe is explicit for each v0.1 parent setup;
5. W1/D1/H4 conflict handling is deterministic;
6. required close-vs-wick semantics are explicit;
7. no final active-candle close is used early;
8. at least 5 positive + 5 negative/conflict fixtures exist;
9. direction is established before SMT/LTF entry evidence;
10. countertrend disposition is frozen before backtest.

## Current disposition

| Requirement | Status |
|---|---|
| direction before entry | **HIGH CONFIDENCE / RESOLVED ORCHESTRATION** |
| aligned-only v0.1 | **HIGH CONFIDENCE / SCOPE RESOLVED** |
| SMT downstream of HTF direction | **HIGH CONFIDENCE** |
| close evidence > wick-only evidence | **PROVISIONAL-HIGH** |
| causal timestamping | **ENGINEERING RESOLVED** |
| conflict fail-closed | **ENGINEERING RESOLVED** |
| exact bullish algorithm | **OPEN / BLOCKING** |
| exact bearish algorithm | **OPEN / BLOCKING** |
| direction owner timeframe | **OPEN / BLOCKING** |
| W1/D1/H4 conflict rule | **OPEN / BLOCKING** |
| neutral/range predicate | **OPEN / BLOCKING** |

### P0-05 disposition

```text
P0-05 = PARTIALLY_RESOLVED
strategy freeze = BLOCKED
```

## First-candidate recommendation

Do not attempt a W1/D1/H4 majority-vote bias model.

For the first executable candidate, use exactly one directly verified direction policy with an explicit owner timeframe per parent setup family. Until that policy is evidenced:

```text
context_direction = UNKNOWN
        ↓
NO EXECUTABLE SIGNAL
```

This is preferable to introducing a conventional trend filter that may improve a backtest but cease to reproduce Romeo's doctrine.

## Next direct-source verification targets

1. 2024 foundation video around the close-vs-wick bias discussion (~35:22–36:01).
2. Episode 8 visual examples of aligned vs counter-direction CRTs.
3. Episode 9 HTF candle/narrative example preceding bullish/bearish SMT.
4. Live tape-reading session for bias called before outcome.
5. Romeo chart posts where a bullish/bearish HTF view is stated before the move and the exact candle evidence is visible.

## Promotion rule

No concrete `ContextDirectionResolver` alpha algorithm is authorized yet.

Safe implementation now includes:

- direction enums;
- decision/evidence objects;
- alignment function;
- timestamp/evidence lineage;
- conflict -> `UNKNOWN`;
- `allow_countertrend=False`;
- prevention of circular SMT-derived bias.

The alpha resolver remains blocked until the exact direction rule is directly evidenced.
