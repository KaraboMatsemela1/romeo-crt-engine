# P0-01 — Parent CRT / Candle-1 Selector

**Candidate:** `CRT-C3-ALIGNED-v0.1-DRAFT`  
**Doctrine snapshot:** `CRT_SECRETS_2025`  
**Status:** **PARTIALLY RESOLVED / P0 REMAINS OPEN**  
**Date:** 2026-08-12

## Purpose

Define, without hindsight, which candle becomes the parent CRT / Candle 1 range that all downstream reasoning references.

This blocker is critical because the selected parent determines:

- range high / low
- midpoint / 50%
- Candle 2 and Candle 3 identity
- Turtle Soup references
- key-level interaction state
- direction and target state
- Model #1 / true-MSS execution context

A wrong parent selection can make an otherwise correct lower-timeframe detector produce a completely different strategy.

## Evidence basis used in this pass

This reconciliation pass uses already committed Episode evidence because fresh web-source retrieval was unavailable during this session. No new transcript wording is promoted from unverified memory.

Relevant committed evidence:

- `ROMEO-2024-CRT`
  - every candle is modeled as a range;
  - the trader must explicitly choose which timeframe/range is being traded before evaluating the setup;
  - nested/inside-range handling remains unresolved.
- `ROMEO-2025-S2`
  - analysis begins from a specific candle;
  - Candle 1 range is explicitly selected;
  - price then Turtle Soups that range and attacks the opposite side.
- `ROMEO-2025-S3`
  - Candle 1 is the accumulation anchor of the stateful CRT journey;
  - exact live Candle-1 selection predicate remains unresolved.
- `ROMEO-2025-S4`
  - the first analysis decision is which candle is being traded;
  - select the parent candle before technical-pattern detection;
  - initial parent-timeframe scope is H4 / D1 / W1.
- `ROMEO-2025-S7`
  - Candle 3 assumes an already-defined parent CRT and completed Candle 2;
  - retrospective phase labeling is unsafe.

## Core reconciliation decision

We can now separate **parent selection contract** from **parent eligibility alpha**.

### Parent selection contract — high confidence / architecture-safe

The engine may enforce the following before the exact Romeo selector is known:

```text
1. Parent timeframe is explicitly chosen from the allowed strategy scope.
2. A parent-candle candidate must be a time-bounded candle object.
3. The candidate must be selected before downstream LTF patterns are allowed to create a TradePlan.
4. Once the selected Candle 1 is closed, its high/low range is immutable for that parent CRT instance.
5. Later Turtle Soup, Model #1, true MSS, target delivery, or profitable outcome may not be used to decide retrospectively which candle "should have been" Candle 1.
6. If multiple parent candidates remain ambiguous under the frozen selector, the state is UNKNOWN and the strategy fails closed.
```

These are causal/governance rules. They do **not** solve the missing Romeo eligibility predicate.

## What Candle 1 currently means

The safest current object-level definition is:

```text
Candle 1 = the selected parent/trade candle whose completed range
           becomes the reference range for the following CRT journey.
```

From Episode 2 / Episode 3 evidence:

```text
CANDLE 1
  -> accumulation / parent range
  -> range high and low become reference boundaries
  -> subsequent journey may manipulate / Turtle Soup that range
  -> later state progresses toward target delivery
```

This definition is sufficient for the data model, but **not sufficient for signal generation** because we still do not know which completed candle qualifies when multiple choices exist.

## Candidate causal state model

```text
WAIT_FOR_PARENT_TIMEFRAME
        ↓
PARENT_TIMEFRAME_SELECTED
        ↓
WAIT_FOR_CLOSED_CANDLE_CANDIDATE
        ↓
CLOSED_CANDLE_OBSERVED
        ↓
APPLY_PARENT_ELIGIBILITY_RULE   # BLOCKED
    ├── REJECTED
    ├── AMBIGUOUS -> UNKNOWN / NO TRADE
    └── ELIGIBLE
        ↓
PARENT_CRT_SELECTED
        ↓
FREEZE CANDLE-1 RANGE
        ↓
ALLOW DOWNSTREAM CRT STATE
```

Important:

```text
PARENT_CRT_SELECTED
```

must occur before a lower-timeframe winner is known.

## Proposed data model

```python
ParentCandleCandidate(
    candidate_id,
    instrument,
    timeframe,
    open_time,
    close_time,
    open_price,
    high,
    low,
    close,
    midpoint_50,
    eligibility_state,      # UNKNOWN | REJECTED | ELIGIBLE | SELECTED
    selection_reason_ids,
    observed_closed_at,
    selected_at,
    selector_version,
)
```

When selected:

```python
CRTContext(
    parent_crt_id,
    parent_candle_id,
    context_timeframe,
    range_high,
    range_low,
    midpoint_50,
    selected_at,
    selector_version,
    evidence_ids,
)
```

The parent range must be immutable after selection for that strategy instance.

## Resolved constraints

### PCRT-P001 — parent/trade candle is selected before entry-pattern detection

**Status:** HIGH_CONFIDENCE / ARCHITECTURE

Evidence: 2024 foundation + Episode 4.

Engineering rule:

```text
no parent_crt_id -> no Model #1 / true-MSS order candidate
```

Lower-timeframe detectors may still emit research events, but they cannot create an executable TradePlan without parent context.

---

### PCRT-P002 — initial parent timeframe scope is H4 / D1 / W1

**Status:** HIGH_CONFIDENCE / SCOPE

For `CRT-C3-ALIGNED-v0.1-DRAFT`:

```text
parent_timeframe ∈ {H4, D1, W1}
```

This is a whitelist, not proof that every setup traverses all three.

H4 remains unavailable for validation until P0-03 H4 anchors are resolved.

---

### PCRT-P003 — Candle 1 defines the parent range

**Status:** PROVISIONAL-HIGH

Episode 2 explicitly links selected Candle 1 range to later Turtle Soup / opposite-side journey logic.

Working calculation after Candle 1 is selected and closed:

```python
range_high = candle1.high
range_low = candle1.low
midpoint_50 = (range_high + range_low) / 2
```

No later candle may rewrite those values for the same parent CRT instance.

---

### PCRT-P004 — parent selection must be causal

**Status:** ENGINEERING_CONSTRAINT

Prohibited:

```python
# hindsight selection
parent = candle_with_best_future_turtle_soup_or_target_result
```

Also prohibited:

```python
# search backward after finding a winning LTF entry
parent = best_explanatory_prior_candle(winning_entry)
```

Selection must be reproducible using only the information set available at `selected_at`.

---

### PCRT-P005 — ambiguous parent state fails closed

**Status:** ENGINEERING_CONSTRAINT

Until the Romeo eligibility/ranking rule is complete:

```text
multiple plausible parents + no deterministic tie-breaker
    -> PARENT_SELECTION_UNKNOWN
    -> NO TRADE
```

Never pick the larger range, smaller range, nearest candle, higher timeframe, or more profitable candidate unless the frozen strategy explicitly defines that rule.

---

### PCRT-P006 — Candle-1 range must exist before Candle-2/Candle-3 causal use

**Status:** HIGH_CONFIDENCE / CAUSAL INTERPRETATION

If Candle 2 manipulates Candle 1's range, Candle 1's final high/low must already be known before that manipulation can be evaluated against the complete parent range.

For the first strategy candidate, use the conservative causal contract:

```text
Candle 1 must be CLOSED before its completed high/low are used as the parent range.
```

This avoids using a future Candle-1 high/low intrabar.

Whether Romeo ever defines an active/incomplete candle as parent context for another setup family is outside v0.1 and requires separate evidence.

## What remains unresolved / blocking

### PCRT-B001 — exact eligibility rule

We still do not know the deterministic predicate that distinguishes:

```text
this completed H4/D1/W1 candle = Candle 1
```

from:

```text
this completed H4/D1/W1 candle = ordinary candle / ignore
```

Potential attributes must **not** be invented:

- range size
- candle color
- body/wick ratio
- displacement
- opening position
- key-level proximity
- liquidity condition
- day-of-week
- previous-candle relationship
- `thick` adjective

unless source evidence explicitly assigns them to Candle-1 selection.

---

### PCRT-B002 — consecutive-candle semantics

Open question:

```text
Is Candle 2 always the immediately next chronological candle after selected Candle 1?
```

and therefore:

```text
Is Candle 3 always the immediately next candle after Candle 2?
```

The public three-candle framing strongly suggests chronological progression, but the committed evidence is not precise enough to freeze this globally.

For v0.1 this must be directly verified rather than assumed.

---

### PCRT-B003 — inside bars / nested ranges

The 2024 foundation explicitly leaves inside-bar treatment as a special case.

Need deterministic answers for:

- inside candle after candidate parent
- parent candle inside a larger W1/D1/H4 candle
- overlapping ranges
- multiple active nested CRTs
- which parent owns a lower-timeframe event

Until resolved:

```text
ambiguous nested ownership -> UNKNOWN -> NO TRADE
```

---

### PCRT-B004 — parent supersession / expiry

Need a rule for when a selected parent CRT stops being active or is replaced:

- Target 1 reached?
- Target 2 reached?
- opposite breakout?
- time expiry / next candle sequence?
- new higher-timeframe parent?
- invalidation / incomplete state?

Without this, the engine can incorrectly attach later events to stale parent contexts.

---

### PCRT-B005 — multi-timeframe ownership

If W1, D1 and H4 each contain plausible CRTs at the same time:

- can all remain active?
- does one own the trade?
- does W1 provide context while D1 is trade candle?
- can H4 be parent while D1 is only narrative?

`W1 -> D1 -> H4` notation does not itself answer ownership.

The selector must carry explicit roles such as:

```text
context_parent
trade_parent
execution_parent
```

only if source evidence supports those distinctions.

## Anti-look-ahead tests required

### Test 1 — future target leakage

Given three possible prior candles, later price reaches one candle's opposite extreme.

Expected:

```text
selector result at historical decision time must not change
because of future target outcome
```

### Test 2 — future Turtle Soup leakage

A later Turtle Soup looks perfect relative to Candle A but not Candle B.

Expected:

```text
parent selection cannot be made after observing the Turtle Soup
unless the source rule explicitly defines selection at that later timestamp
and all candidate information is still causal.
```

### Test 3 — final Candle-1 OHLC leakage

While a candidate Candle 1 is still active, its eventual high occurs later.

Expected:

```text
completed range_high cannot be used before candle close
```

for the first v0.1 parent-range contract.

### Test 4 — nested ambiguity

Two source-valid parent candidates overlap.

Expected:

```text
no deterministic ranking -> UNKNOWN -> NO TRADE
```

not an arbitrary tie-break.

## Fixture requirements to close P0-01

Minimum direct-source fixture set:

### Positive examples

At least 5 examples documenting:

- instrument
- parent timeframe
- exact Candle-1 timestamp
- why Romeo selects that candle
- Candle-1 OHLC/range
- following Candle-2/Candle-3 timestamps
- lower-timeframe relationship

### Negative / counterexamples

At least 5 examples showing visually plausible candles that are **not** selected, including if possible:

- inside bar
- overlapping range
- wrong context candle
- wrong timeframe
- nearby candle before/after the true parent

### Required direct-source targets

Priority:

1. 2024 CRT foundation chart examples where Romeo explicitly chooses the range.
2. Episode 2 around 02:25–04:37 where the specific candle / Candle-1 range is selected.
3. Episode 4 around 03:54–08:52 where trade-candle choice is discussed.
4. Episode 7 examples that show Candle 1 / Candle 2 / Candle 3 timestamps together.
5. Live tape-reading session because it can reveal the selection decision before outcome.

## Interim implementation policy

The project may implement the **interface and fail-closed contract** now, but not a production selector.

Allowed:

```python
class ParentCRTSelector(Protocol):
    def select(self, market_state, timestamp) -> ParentSelectionResult:
        ...
```

Allowed states:

```text
NO_CANDIDATE
AMBIGUOUS
SELECTED
DATA_UNAVAILABLE
```

But the default research implementation must remain:

```text
UNRESOLVED_SELECTOR -> no executable strategy signal
```

Do not insert a heuristic selector merely to unlock backtesting.

## P0-01 acceptance status

| Requirement | Status |
|---|---|
| parent selected before entry patterns | **HIGH CONFIDENCE** |
| initial parent timeframe whitelist | **HIGH CONFIDENCE — H4/D1/W1** |
| selected Candle-1 high/low define range | **PROVISIONAL-HIGH** |
| selected range immutable | **ENGINEERING RESOLVED** |
| completed range used only after close | **CONSERVATIVE v0.1 CAUSAL RULE** |
| exact Candle-1 eligibility predicate | **OPEN / BLOCKING** |
| Candle1->2->3 exact chronological semantics | **OPEN / BLOCKING** |
| inside/nested/overlap policy | **OPEN / BLOCKING** |
| parent expiry/supersession | **OPEN / BLOCKING** |
| W1/D1/H4 ownership rules | **OPEN / BLOCKING** |
| positive/negative chart fixtures | **NOT YET CAPTURED** |

### P0-01 disposition

```text
P0-01 = PARTIALLY_RESOLVED
strategy freeze = BLOCKED
```

The project now knows what a selected parent CRT **must look like as a causal object**, but not yet the deterministic Romeo rule that chooses it from the stream of completed candles.

## Next action

When direct-source retrieval is available, perform a visual/timestamp fixture pass rather than another broad summary pass.

The single most important question is:

> At the moment Romeo points to a candle and says, effectively, "this is the candle/range I am trading," what facts already visible on the chart distinguish that candle from its neighboring candles?

Until that is answered reproducibly, Parent CRT selection stays fail-closed.
