# P0-02 — KeyLevelSelector and Ranking

**Candidate:** `CRT-C3-ALIGNED-v0.1-DRAFT`  
**Doctrine snapshot:** `CRT_SECRETS_2025`  
**Status:** **PARTIALLY RESOLVED / P0 REMAINS OPEN**  
**Date:** 2026-08-12

## Purpose

Define the causal contract for selecting and tracking Romeo CRT key levels before any lower-timeframe Turtle Soup, Model #1, true MSS, or Candle-3 reaction is allowed to become an executable candidate.

This blocker remains P0 because Episodes 5, 7, 9 and 10 consistently place location/context before entry-pattern interpretation. A wrong key level can make an otherwise visually convincing lower-timeframe pattern irrelevant or actively misleading.

## Evidence base

### First-party Romeo evidence

Romeo's official Telegram:

- directly links `CRT secrets episode 5: Key level` (`p8UYOgVn1-g`);
- states that when the lower timeframes are difficult to read, moving to the higher timeframe makes the answer clearer;
- explicitly states that one may trade either the **journey of price to the key level** or the **reaction of price from the key level**;
- references Episode 5 immediately after that statement.

This is the strongest first-party evidence for the two-role key-level taxonomy and the HTF-before-LTF interpretation order.

### Indexed Episode-5 evidence

The indexed Episode-5 summary reports:

- key levels may be based on **price or time**;
- marking the correct key level, the type of level, the reaction at the level, the timing of the hit, and lower-timeframe behavior are all separate questions;
- a key level is a location where a reaction/bounce is expected;
- convincing lower-timeframe reversal structures may appear **before** the actual key level is reached;
- fake MSS-like structures can therefore trap pattern-first traders;
- the true reaction is associated with the actual key-level interaction and the correct time.

Because these details are derived from indexed/AI-generated summary material rather than an authoritative first-party transcript, they remain `PROVISIONAL` until direct visual/audio verification.

## What P0-02 can now resolve

### KLSEL-P001 — Key level is a context object, never a direct entry

**Status:** HIGH_CONFIDENCE / ORCHESTRATION

A key level qualifies location/time context. It cannot independently emit an order.

Required architecture:

```text
HTF CONTEXT
    ↓
KEY LEVEL
    ↓
LOCATION / TIME STATE
    ↓
LTF EVENT
    ↓
ENTRY MODEL
    ↓
RISK
```

Prohibited:

```python
if key_level_touched:
    enter_trade()
```

---

### KLSEL-P002 — Key-level role must be predeclared

**Status:** HIGH_CONFIDENCE / FIRST-PARTY SUPPORTED

The two roles are:

```text
DESTINATION
    price is traveling toward the level

REACTION_ORIGIN
    price has reached the relevant level and a reaction trade may be evaluated
```

These are separate setup families and must not be merged into a single bidirectional `key_level_trade` signal.

A level may eventually transition from destination to reaction-origin, but the exact transition event remains unresolved.

---

### KLSEL-P003 — Higher-timeframe context owns key-level interpretation

**Status:** HIGH_CONFIDENCE / FIRST-PARTY + CROSS-SOURCE

For the first candidate, lower-timeframe structures do not create the key-level narrative.

Safe direction of information flow:

```text
W1 / D1 / H4 CONTEXT
        ↓
KEY LEVEL STATE
        ↓
LTF PATTERN INTERPRETATION
```

Unsafe direction:

```text
winning LTF pattern
        ↓
search backwards for a key level that explains it
```

Every LTF candidate must carry the pre-existing `key_level_id` and evidence timestamp.

---

### KLSEL-P004 — Key-level type domain includes price and time

**Status:** PROVISIONAL-HIGH

The Episode-5 indexed material explicitly distinguishes price- and time-based key levels.

For the domain model:

```python
KeyLevelType = PRICE | TIME | COMPOSITE | UNKNOWN
```

`COMPOSITE` is an engineering representation for a level requiring both price and time qualification; it is not yet claimed as Romeo's own named category.

No concrete price-level subtype or time-window subtype may be populated until separately evidenced.

---

### KLSEL-P005 — Reaction trades require the level to be causally reached

**Status:** HIGH_CONFIDENCE / SAFETY RECONCILIATION

Episode 5 warns that convincing reversal/MSS-like structures may form before the real level.

Therefore, for `REACTION_ORIGIN` setups:

```text
LEVEL_PENDING
    ↓
LEVEL_REACHED
    ↓
TIME / CONTEXT QUALIFIED
    ↓
LTF CONFIRMATION
```

A pre-level pattern is not allowed to upgrade the level state retrospectively.

Until exact reach semantics are defined:

```text
level_reached = UNKNOWN
        ↓
NO REACTION TRADE
```

---

### KLSEL-P006 — Pre-level LTF patterns are explicit negative fixtures

**Status:** HIGH_CONFIDENCE / TESTING DIRECTIVE

The test corpus must contain examples where:

```text
LTF Turtle Soup / MSS / Model-like reversal appears
BUT
actual selected key level has not been reached
```

Expected result:

```text
REJECT_PREMATURE_LTF_PATTERN
```

This is a first-class negative case, not noise to ignore.

---

### KLSEL-P007 — Key-level selection must be frozen before outcome

**Status:** ENGINEERING CONSTRAINT

Prohibited:

```python
key_level = level_that_later_reversed_best
```

or:

```python
ranked_level = nearest_level_after_trade_winner_is_known
```

The selector must output its candidate/ranking from information available at `selected_at`.

If multiple candidate levels remain tied under the frozen selector:

```text
KEY_LEVEL_AMBIGUOUS
        ↓
NO TRADE
```

---

## What remains unresolved / blocking

### KLSEL-B001 — exact price key-level taxonomy

We do not yet have a reliable deterministic list of what Romeo accepts as a price key level.

Do not assume any of the following are universally valid:

```text
old high / old low
previous day high / low
previous week high / low
CRT high / low
FVG boundary
order block
breaker
OTE level
session high / low
round number
```

Some appear elsewhere as liquidity/objective/context examples, but Episode 5 does not yet give a deterministic universal registry.

---

### KLSEL-B002 — exact time key-level taxonomy

Episode 5 supports time as part of key-level logic, but the exact time objects are unresolved.

Do not silently equate key time with:

```text
London open
New York open
midnight NY
hourly macros
session opens
specific clock lists
```

unless the selected doctrine source explicitly defines them for this setup family.

---

### KLSEL-B003 — W1 / D1 / H4 ranking and conflict resolution

There is no reliable rule yet for:

```text
W1 level vs D1 level
D1 level vs H4 level
overlapping levels
nearby stacked levels
opposing directional levels
```

The project notation `W1 → D1 → H4` is a top-down analysis hierarchy, **not** sufficient evidence for a numeric or absolute ranking algorithm.

Prohibited shortcut:

```python
rank = timeframe_seconds  # higher timeframe always wins
```

until directly evidenced.

---

### KLSEL-B004 — exact `level reached` predicate

Unresolved whether reach requires:

```text
first tick/touch
wick through
body trade-through
close at/beyond
specific tolerance band
Turtle Soup of the level
```

No epsilon/tolerance may be optimized from historical outcomes.

---

### KLSEL-B005 — consumed / invalidated / superseded semantics

We do not yet know:

- when a touched level remains active;
- when a reaction consumes it;
- whether a clean breakout invalidates it;
- whether a level may be reused;
- when a newer HTF level supersedes an older one;
- how a destination level becomes a reaction-origin level.

Until defined, these states must fail closed for any strategy path that depends on them.

---

### KLSEL-B006 — exact direction relationship

A key level alone does not establish trade direction.

The first candidate still requires P0-05 to define:

```text
context_direction = BULLISH | BEARISH | NEUTRAL | UNKNOWN
```

Key-level role and direction must remain separate fields.

---

### KLSEL-B007 — exact time qualification at the level

Episode 5 links the genuine reaction/true MSS with the correct time, but no deterministic time gate has yet been frozen.

Therefore:

```text
correct_time = UNKNOWN
```

until P0-03/time-source reconciliation supplies a setup-specific predicate.

## Proposed selector contract

```python
class KeyLevelSelector:
    def select(
        self,
        market_state,
        parent_crt,
        observed_at,
    ) -> KeyLevelSelectionResult:
        ...
```

Result:

```python
KeyLevelSelectionResult(
    status,              # NO_CANDIDATE | AMBIGUOUS | SELECTED | DATA_UNAVAILABLE
    selected_level_id,
    candidates,
    selected_at,
    selector_version,
    evidence_ids,
)
```

Candidate object:

```python
KeyLevelCandidate(
    id,
    source_timeframe,
    level_type,          # PRICE | TIME | COMPOSITE | UNKNOWN
    price_reference,
    time_reference,
    role,                # DESTINATION | REACTION_ORIGIN | UNKNOWN
    state,               # PENDING | REACHED | CONSUMED | INVALID | UNKNOWN
    valid_from,
    observed_at,
    evidence_ids,
)
```

No field may be filled by future outcome inspection.

## Recommended state machine

```text
WAIT_FOR_PARENT_CRT
        ↓
PARENT_CRT_SELECTED
        ↓
GENERATE_KEY_LEVEL_CANDIDATES
        ↓
APPLY SOURCE-BACKED RANKING
   ├── NONE → NO_KEY_LEVEL
   ├── TIE / AMBIGUOUS → NO TRADE
   └── SELECTED
        ↓
FREEZE KEY_LEVEL ROLE
   ├── DESTINATION
   └── REACTION_ORIGIN
        ↓
TRACK CAUSAL LOCATION STATE
        ↓
IF DESTINATION:
    evaluate journey-to-level strategy family

IF REACTION_ORIGIN:
    reject pre-level LTF reversal candidates
    wait for source-defined level reach
    wait for source-defined time qualification
    wait for approved LTF confirmation
        ↓
ENTRY CANDIDATE
```

The **candidate generation**, **ranking**, **reach**, and **time qualification** boxes remain blocked.

## Minimal v0.1 scope recommendation

To reduce ambiguity, the first executable candidate should use only **one key-level setup family** once direct evidence is sufficient.

Recommended selection after source verification:

```text
REACTION_FROM_KEY_LEVEL
```

Reason: Episode 5 provides a particularly explicit negative rule for this family — pre-level fake reversals must be rejected — which gives us stronger testability than an undefined journey-to-level entry path.

This is a project scoping recommendation, not yet an alpha claim.

Until the actual level taxonomy/ranking is resolved, even `REACTION_FROM_KEY_LEVEL` remains blocked.

## Required direct-source fixture set

Before P0-02 can close:

### Positive fixtures

At least 5 examples with:

- parent timeframe visible;
- level marked before reaction;
- reason/type for level selection known;
- timestamp when level became selected known;
- level reached event visible;
- accepted LTF confirmation visible.

### Negative fixtures

At least 5 examples covering:

- convincing LTF reversal before the true level;
- wrong candidate key level;
- multiple nearby levels;
- level touched at wrong time;
- level already consumed/invalid;
- lower-timeframe pattern without HTF key-level narrative.

## Acceptance criteria

P0-02 closes only when:

1. valid price-level types are explicitly enumerated;
2. valid time-level types are explicitly enumerated or time levels are explicitly excluded from v0.1;
3. candidate generation is deterministic;
4. W1/D1/H4 ranking/conflict logic is deterministic;
5. `reached`, `consumed`, and `invalid` are deterministic;
6. reaction time qualification is deterministic or explicitly excluded;
7. positive and negative fixtures exist;
8. historical selection uses only information available at `selected_at`;
9. ambiguous ties fail closed.

## Current disposition

| Requirement | Status |
|---|---|
| key level before entry | **HIGH CONFIDENCE / RESOLVED ORCHESTRATION** |
| destination vs reaction-origin roles | **HIGH CONFIDENCE / FIRST-PARTY SUPPORTED** |
| HTF owns LTF interpretation | **HIGH CONFIDENCE / RESOLVED ORCHESTRATION** |
| price/time level domain | **PROVISIONAL-HIGH** |
| reject pre-level reversal patterns | **HIGH CONFIDENCE** |
| causal preselection / no hindsight | **ENGINEERING RESOLVED** |
| exact price-level taxonomy | **OPEN / BLOCKING** |
| exact time-level taxonomy | **OPEN / BLOCKING** |
| W1/D1/H4 ranking | **OPEN / BLOCKING** |
| exact reach predicate | **OPEN / BLOCKING** |
| consumed/invalid state | **OPEN / BLOCKING** |
| exact time qualification | **OPEN / BLOCKING** |

### P0-02 disposition

```text
P0-02 = PARTIALLY_RESOLVED
strategy freeze = BLOCKED
```

## Next verification targets

1. Episode 5 original chart frames where the actual key level is marked before the fake LTF bottom/top.
2. Episode 7 examples where Candle 3 is accepted/rejected based on the key level.
3. Episode 9 framing examples that show the pre-trade liquidity/key-level target.
4. Episode 10 material around `correct key level` and draw liquidity.
5. Live tape-reading (`1EK-LMwgJ3c`) for examples selected in real time before outcome.

## Promotion rule

No concrete `KeyLevelSelector` alpha algorithm is authorized yet.

Safe implementation may include:

- data structures;
- selector/result interfaces;
- immutable timestamps/evidence;
- destination/reaction-origin role;
- fail-closed ambiguity;
- negative pre-level-pattern fixtures.

But until candidate generation and ranking are directly evidenced:

```text
KEY_LEVEL_UNKNOWN / AMBIGUOUS
        ↓
NO EXECUTABLE SIGNAL
```
