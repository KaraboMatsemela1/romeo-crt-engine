# P0-04 — Deterministic Turtle Soup Primitive

**Candidate:** `CRT-C3-ALIGNED-v0.1-DRAFT`  
**Doctrine snapshot:** `CRT_SECRETS_2025`  
**Status:** **PARTIALLY RESOLVED / P0 REMAINS OPEN**  
**Date:** 2026-08-12

## Purpose

Define the smallest causal Turtle Soup event contract that can be used inside Romeo CRT without reducing the concept to a generic liquidity sweep or hindsight reversal label.

P0-04 remains critical because the first narrow v0.1 candidate currently requires local Turtle Soup manipulation before an approved entry model. If Turtle Soup is vague, the entire signal path becomes discretionary and the backtest cannot be trusted.

## Evidence base

### Primary / first-party provenance

Romeo's official Telegram repeatedly treats Turtle Soup as a core, persistent part of CRT and explicitly states that `T` in CRT symbolically includes **Time and Turtle Soup**. The official feed also:

- posts live Turtle Soup examples;
- refers to a `proper turtle soup entry`;
- defines KOD as the last Turtle Soup before the target is hit;
- later demonstrates cases where traders expected a local Turtle Soup but SMT supplied the relevant cross-market behavior instead.

These posts establish Turtle Soup as a first-class CRT primitive and show that it is not always equivalent to the final entry trigger.

### `ROMEO-2024-TS — What is turtle soup?`

The indexed transcript/summary gives the strongest current structural evidence:

- Turtle Soup is framed as a false breakout/breakdown around an **old high or old low**;
- bearish example: price trades **above** an old high and later reverses lower;
- bullish example: price trades **below** an old low and later reverses higher;
- Romeo describes the excursion as a `stab` through the old high/low;
- breakout buyers/sellers become trapped when continuation fails;
- higher-timeframe price action, market profile, timing and separate entry models remain surrounding context.

Because the detailed semantic extraction is not from a first-party transcript, those exact implementation semantics remain provisional.

### `ROMEO-2024-CRT — What is CRT?`

The foundation lecture adds an important range-level example: a selected candle can be Turtle Souped when price trades outside the range and then resolves back through/inside it rather than producing a true breakout. The project currently has stronger evidence that **close behavior matters** than evidence for one universal same-candle-close formula.

### Later 2025 reconciliation

Episodes 2, 3, 5, 7 and 9 consistently treat Turtle Soup as a manipulation / journey event that is interpreted inside:

```text
PARENT CRT
+ KEY LEVEL / LOCATION
+ TIME / CONTEXT
+ TARGET STATE
```

and then followed by a separate execution model such as Model #1 or true MSS.

This supports keeping:

```text
TurtleSoupEvent
```

separate from:

```text
EntrySignal
```

## Core deterministic contract that can be frozen at architecture level

### TSSEL-P001 — a reference extreme must pre-exist the excursion

**Status:** HIGH_CONFIDENCE / STRUCTURAL

A Turtle Soup is relational. It requires an already-existing price extreme.

Bearish:

```text
REFERENCE_HIGH exists before sweep_timestamp
```

Bullish:

```text
REFERENCE_LOW exists before sweep_timestamp
```

A random local reversal with no pre-existing reference extreme is not a Turtle Soup candidate.

Anti-look-ahead invariant:

```python
reference_extreme.created_at < sweep_timestamp
```

The engine may not discover the reference only after observing the winning reversal.

---

### TSSEL-P002 — the excursion must trade beyond the reference extreme

**Status:** HIGH_CONFIDENCE / STRUCTURAL

Bearish candidate:

```text
price > reference_high
```

Bullish candidate:

```text
price < reference_low
```

Equality alone is insufficient for a `sweep` event in the primitive contract.

Safe abstraction:

```python
if side == "BEARISH":
    excursion = observed_high > reference_price
elif side == "BULLISH":
    excursion = observed_low < reference_price
```

This does **not** yet define a minimum penetration distance.

---

### TSSEL-P003 — an excursion alone is not a confirmed Turtle Soup

**Status:** HIGH_CONFIDENCE

The 2024 material describes false breakout/breakdown and reversal, not merely taking a high/low.

Therefore:

```text
REFERENCE_EXTREME
      ↓
EXCURSION
      ↓
TURTLE_SOUP_CANDIDATE
```

is allowed, but:

```text
EXCURSION
      ↓
CONFIRMED_TURTLE_SOUP
```

is prohibited without failure/reversal evidence.

The project must distinguish:

```text
SWEEP_ONLY
TURTLE_SOUP_CANDIDATE
TURTLE_SOUP_CONFIRMED
```

---

### TSSEL-P004 — continuation failure / reversal evidence is required

**Status:** HIGH_CONFIDENCE CONCEPT / EXECUTABLE PREDICATE UNRESOLVED

The defining semantic difference between a true breakout and Turtle Soup is failure of continuation beyond the reference followed by movement away from the excursion.

Bearish skeleton:

```text
old high
  ↓
trade above old high
  ↓
continuation higher fails
  ↓
price resolves lower
```

Bullish skeleton:

```text
old low
  ↓
trade below old low
  ↓
continuation lower fails
  ↓
price resolves higher
```

What counts as `failure` is still blocking.

Do **not** invent:

```python
confirmation = close < reference_high
```

as a universal Romeo rule until direct evidence determines whether confirmation is:

- same-candle close back through the level;
- close back inside a parent range;
- later candle close;
- Model #1 close condition;
- true-MSS confirmation;
- or setup-family dependent.

---

### TSSEL-P005 — Turtle Soup is an event, not the order trigger

**Status:** HIGH_CONFIDENCE / ORCHESTRATION

The foundational lecture explicitly says multiple entry models exist around Turtle Soup, and later CRT episodes repeatedly use separate Model #1 / true-MSS execution logic.

Required architecture:

```text
TURTLE_SOUP_CANDIDATE / CONFIRMED EVENT
            ↓
CONTEXT / ENTRY-MODEL QUALIFICATION
            ↓
TRADE PLAN
```

Prohibited:

```python
if turtle_soup:
    send_order()
```

---

### TSSEL-P006 — parent context and key level must already exist for v0.1

**Status:** PROJECT SCOPE + HIGH-CONFIDENCE CROSS-SOURCE

The first narrow candidate does not scan all market highs/lows globally.

Required v0.1 order:

```text
PARENT CRT SELECTED
      ↓
REACTION KEY LEVEL SELECTED
      ↓
DIRECTION / TARGET STATE VALID
      ↓
CANDLE-3 ELIGIBLE
      ↓
SEARCH FOR LOCAL TURTLE SOUP
```

This is a deliberate restriction to avoid converting the entire chart into thousands of arbitrary sweep candidates.

---

### TSSEL-P007 — the swept structural extreme must be preserved for risk/invalidation

**Status:** HIGH_CONFIDENCE DATA CONTRACT

Episode 9 uses the Turtle Soup structural extreme as the demonstrated stop reference.

The event therefore must retain:

```text
structural_extreme_price
structural_extreme_timestamp
```

rather than only a boolean `turtle_soup=True`.

Exact execution buffer beyond that extreme remains P1-04.

## Proposed event model

```python
TurtleSoupEvent(
    event_id,
    parent_crt_id,
    key_level_id,
    instrument,
    execution_timeframe,
    direction,                   # BULLISH | BEARISH
    reference_extreme_id,
    reference_type,              # UNRESOLVED taxonomy
    reference_price,
    reference_created_at,
    sweep_timestamp,
    sweep_price,
    excursion_distance,
    state,                       # CANDIDATE | CONFIRMED | INVALID | EXPIRED
    failure_confirmation_type,   # UNRESOLVED
    confirmation_timestamp,
    structural_extreme_price,
    structural_extreme_timestamp,
    observed_at,
    evidence_ids,
)
```

No unresolved field may be silently populated with broker/default heuristics.

## Proposed state machine

```text
WAIT_FOR_VALID_CONTEXT
        ↓
REFERENCE_EXTREME_SELECTED
        ↓
WAIT_FOR_EXCURSION
        ↓
PRICE TRADES BEYOND REFERENCE?
   ├── NO → WAIT / EXPIRE
   └── YES
        ↓
TURTLE_SOUP_CANDIDATE
        ↓
WAIT_FOR_SOURCE-DEFINED FAILURE CONFIRMATION
   ├── TRUE BREAKOUT / INVALID → INVALID
   ├── TIMEOUT → EXPIRED
   └── CONFIRMED
        ↓
TURTLE_SOUP_CONFIRMED
        ↓
WAIT_FOR APPROVED ENTRY MODEL
```

The `failure confirmation`, `true breakout`, and `timeout` transitions remain blocked.

## What remains unresolved / blocking

### TSSEL-B001 — qualifying reference-extreme taxonomy

We still do not have a deterministic Romeo registry for which prior highs/lows qualify.

Do not assume all of the following are equivalent:

```text
immediately previous candle high/low
swing high/low
old daily high/low
old weekly high/low
parent CRT high/low
session high/low
equal highs/lows
key-level high/low
intermediate high/low
```

The primitive requires a pre-existing extreme, but the selector for **which** extreme is P0-blocking.

This blocker overlaps P0-02 and P0-01 and should be resolved with source fixtures rather than an independent generic swing algorithm.

---

### TSSEL-B002 — reference freshness / age

Unresolved:

- minimum age before a high/low can be considered `old`;
- maximum age after which it expires;
- whether a level remains valid after multiple approaches;
- whether intermediate highs/lows have different rules from parent CRT extremes.

No arbitrary bar-count age is authorized.

---

### TSSEL-B003 — consumed-reference logic

Unresolved whether a reference becomes consumed after:

```text
first touch
first penetration
first Turtle Soup
clean close through
successful target delivery
multiple sweeps
```

This is important because replaying the same historical high/low indefinitely would inflate setup count.

Until deterministic:

```text
reference_consumption_state = UNKNOWN
```

Any test depending on reused levels must remain blocked.

---

### TSSEL-B004 — minimum / maximum excursion distance

Source language supports trading **beyond** the reference but does not currently define a numerical penetration threshold.

Do not optimize:

```text
1 tick
0.1 ATR
1 pip
5 pips
x% of parent range
```

from historical profitability.

For raw event capture, strict inequality may be recorded, but no trade qualification may depend on an invented minimum excursion.

---

### TSSEL-B005 — exact confirmation / close-back rule

This is the largest remaining Turtle Soup blocker.

Evidence supports:

```text
false breakout/breakdown
+
failed continuation
+
reversal away
```

but not yet one universal formula for `CONFIRMED`.

Questions:

1. Must the sweep candle close back inside the reference level?
2. Must it close inside the entire parent CRT range?
3. Can confirmation occur on a later candle?
4. Is close-back merely the Turtle Soup event while Model #1/true MSS is the entry confirmation?
5. Does the answer change across parent/execution timeframes?
6. Can a violent intrabar rejection qualify before candle close in some models?

Until resolved:

```text
TURTLE_SOUP_CONFIRMED = UNKNOWN
```

for the executable v0.1 path.

---

### TSSEL-B006 — confirmation timeout / event expiry

The project does not know how long continuation may fail after the excursion and still belong to the same Turtle Soup event.

Do not choose:

```text
same candle
next candle
N bars
end of session
end of parent Candle 3
```

without evidence.

A timestamped candidate can exist in research data, but it cannot be upgraded after an arbitrary hindsight window.

---

### TSSEL-B007 — true-breakout invalidation

A false breakout implies a contrasting true-breakout path, but the exact invalidation is unresolved.

Potential—but unverified—candidates include:

```text
close beyond reference
sustained closes beyond reference
break + hold + continuation
parent-range breakout
```

No true-breakout detector is authorized yet.

---

### TSSEL-B008 — equal highs / equal lows

Later Romeo material discusses equal-low baiting in examples, but the foundational source does not give enough evidence to decide whether equal highs/lows are:

- valid reference extremes;
- separate liquidity objects;
- confluence only;
- or setup-specific.

Keep explicit `reference_type=UNKNOWN` rather than collapsing them into old highs/lows.

---

### TSSEL-B009 — exact timing window

Romeo repeatedly treats Time as critical, but the first Turtle Soup lecture does not provide an executable time window for all Turtle Soups.

Therefore a global:

```python
valid_turtle_soup_hours = [...]
```

is prohibited.

Timing must be sourced per parent/setup family.

---

### TSSEL-B010 — interaction with SMT substitution

Official later material shows cases where a trader expected the local low to Turtle Soup but SMT played the manipulation role instead.

For first v0.1:

```text
require_local_turtle_soup = True
allow_smt_substitution = False
```

This remains a project scoping choice, not a universal Romeo doctrine claim.

## Distinguish event layers

The project should preserve these separately:

```text
ReferenceExtreme
    ↓
LiquidityExcursion
    ↓
TurtleSoupCandidate
    ↓
TurtleSoupConfirmation
    ↓
EntryModelConfirmation
    ↓
TradePlan
```

This prevents a common implementation mistake where all of these concepts collapse into one boolean.

### Suggested objects

```python
ReferenceExtreme(
    id,
    price,
    side,
    source_timeframe,
    created_at,
    reference_type,
    state,
)

LiquidityExcursion(
    id,
    reference_extreme_id,
    observed_at,
    extreme_price,
    distance,
)

TurtleSoupCandidate(
    id,
    excursion_id,
    context_id,
    created_at,
)

TurtleSoupConfirmation(
    id,
    candidate_id,
    confirmation_type,
    confirmed_at,
)
```

## Anti-look-ahead requirements

### 1. Reference must exist first

Prohibited:

```python
reference = nearest_prior_high_that_makes_the_reversal_look_valid_afterward
```

### 2. Candidate cannot become confirmed because target later hit

Prohibited:

```python
confirmed = future_move_reached_target
```

### 3. KOD cannot define basic Turtle Soup confirmation

`last_turtle_soup_before_target` is a retrospective KOD label, not a causal Turtle Soup predicate.

### 4. Structural extreme must be known at entry time

Do not replace the actual sweep high/low with the later most favorable extreme of the completed move.

### 5. Confirmation window must be predeclared

No selecting the number of bars that gives the best historical win rate before strategy freeze.

## Positive fixture requirements

Before P0-04 can close, collect at least 5 bullish + 5 bearish direct-source examples with:

- selected parent/context visible;
- selected reference high/low visible **before** excursion;
- excursion timestamp and price;
- exact candle/frame Romeo treats as confirmation;
- distinction from entry model;
- structural extreme preserved;
- valid/invalid time context if discussed.

Prefer fixtures across:

```text
W1 parent
D1 parent
H4 parent (after P0-03 closes)
```

and at least two instrument classes if the doctrine is claimed to be cross-market.

## Negative fixture requirements

At least 10 negative examples covering:

1. high/low touched but not penetrated;
2. clean breakout that continues;
3. sweep with no qualifying reversal confirmation;
4. reversal with no pre-existing eligible reference;
5. pre-key-level fake Turtle Soup;
6. already-consumed reference;
7. wrong-time Turtle Soup if direct evidence supports time invalidation;
8. countertrend event rejected by v0.1 direction filter;
9. SMT manipulation case with no local Turtle Soup;
10. ambiguous nested references.

## Candidate detector contract

```python
class TurtleSoupDetector:
    def observe(
        self,
        market_state,
        parent_crt,
        key_level,
        context_direction,
        observed_at,
    ) -> TurtleSoupResult:
        ...
```

Result states:

```text
NO_REFERENCE
WAITING_FOR_EXCURSION
CANDIDATE
WAITING_FOR_CONFIRMATION
CONFIRMED
INVALID
EXPIRED
AMBIGUOUS
DATA_UNAVAILABLE
```

For the executable path:

```text
AMBIGUOUS | DATA_UNAVAILABLE | unresolved confirmation
    ↓
NO TRADE
```

## Minimal v0.1 recommendation

Do **not** broaden v0.1 into a general Turtle Soup scanner.

Once P0-04 closes, the first strategy should accept only Turtle Soup events that occur:

```text
inside an already-selected parent CRT
+
at/after an already-selected reaction key level
+
in aligned HTF direction
+
during Candle-3 eligibility
```

This makes Turtle Soup a **local manipulation primitive** inside the existing CRT state machine.

It also reduces false positives without claiming every excluded Turtle Soup is invalid in Romeo's broader doctrine.

## Current disposition

| Requirement | Status |
|---|---|
| pre-existing reference extreme required | **HIGH CONFIDENCE / RESOLVED STRUCTURE** |
| bearish excursion above reference high | **HIGH CONFIDENCE / RESOLVED STRUCTURE** |
| bullish excursion below reference low | **HIGH CONFIDENCE / RESOLVED STRUCTURE** |
| excursion alone is insufficient | **HIGH CONFIDENCE** |
| failure/reversal required conceptually | **HIGH CONFIDENCE** |
| Turtle Soup separate from entry model | **HIGH CONFIDENCE / RESOLVED ORCHESTRATION** |
| preserve structural extreme | **HIGH CONFIDENCE DATA CONTRACT** |
| exact reference-extreme taxonomy | **OPEN / BLOCKING** |
| old-high/old-low age/freshness | **OPEN / BLOCKING** |
| consumed-reference logic | **OPEN / BLOCKING** |
| excursion threshold | **OPEN / BLOCKING FOR TRADE QUALIFICATION** |
| exact close/failure confirmation | **OPEN / CRITICAL BLOCKER** |
| confirmation timeout | **OPEN / BLOCKING** |
| true-breakout invalidation | **OPEN / BLOCKING** |
| equal-high/low treatment | **OPEN / BLOCKING** |
| exact time filter | **OPEN / BLOCKING if required by setup family** |

### P0-04 disposition

```text
P0-04 = PARTIALLY_RESOLVED
strategy freeze = BLOCKED
```

## Direct-source verification priority

1. `What is turtle soup?` original video frames around 11:06–16:00 for exact bearish/bullish confirmation behavior.
2. `What is CRT?` examples around the breakout-vs-Turtle-Soup explanation to determine close-back semantics relative to the selected candle range.
3. CRT live tape-reading (`1EK-LMwgJ3c`) for real-time reference selection and confirmation.
4. Episode 2 KOD chart to separate base Turtle Soup confirmation from KOD/Model #1 entry.
5. Episode 7 Candle-3 examples for key-level Turtle Soup that occurs before exact 50%.
6. Episode 9 trade framing for Turtle-Soup extreme / stop relationship.

## Promotion rule

P0-04 closes only when:

```text
reference-extreme eligibility is deterministic
AND
excursion condition is deterministic
AND
confirmation/failure condition is deterministic
AND
reference consumption/expiry is deterministic
AND
positive/negative direct-source fixtures reproduce the rule causally
```

Until then the architecture may implement the event classes/interfaces, but:

```text
TURTLE_SOUP_CONFIRMATION_UNKNOWN
        ↓
NO EXECUTABLE SIGNAL
```
