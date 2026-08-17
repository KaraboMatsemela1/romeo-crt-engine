# Phase 6D — First-Party Old-CRTH Reaction Locator 6615

**Date:** 2026-08-17  
**Tracking:** Issue #120  
**Mode:** new first-party locator/provenance recovery + field-level synthesis  
**Disposition:** `LOCATOR_BOUND_NEW_EVIDENCE / NO_CLOSING_FIELD_CREDIT`

## Why this pass legitimately re-entered Phase 6D

Issue #42 and Issue #16 permit a bounded Phase-6C/6D re-entry when genuinely new first-party material directly addresses an exact missing predicate field.

On 2026-08-17 the official Romeo Telegram channel index exposed post `6615`, which is not represented in the repository source registry or existing research artifacts. Before acquisition, Issue #120 preregistered the target as:

```text
primary predicate = TURTLE_SOUP_CONFIRMATION
primary field     = EXACT_PREDICATE
secondary field   = CONFIRMATION
```

The statement is relevant because the held Turtle Soup debt includes qualifying old-extreme interaction and confirmation semantics. The source does not itself label the sequence `Turtle Soup`, so this report treats it only as adjacent first-party evidence about a bearish reaction involving an `old CRTH`; it does not promote a universal Turtle Soup rule by association.

## Direct first-party observation

Official channel/index locator:

- `https://t.me/s/officialRomeotpt/6615`

Timestamp-bound direct post locator exposed by the official index:

- `https://t.me/officialRomeotpt/6615`

The official index directly exposes the following text:

```text
When I’m bearish, this is the ideal reaction I want to see:

1- Candle opens.
2- Stabs into an old CRTH.
3- Dumps.
```

The timestamp link on the same first-party index binds that statement to post `6615`.

## Bounded direct-post retrieval result

Exactly one direct single-post retrieval was attempted in this pass.

```text
6615  direct single-post fetch  CACHE_MISS / no replayable original post payload
```

The official channel-index route itself was directly readable and exposed the text plus the timestamp binding, but the single-post route did not yield a replayable original payload in the current retrieval environment.

Accordingly:

```text
FIRST_PARTY_CHANNEL_IDENTITY    = true
POST_ID_BOUND                   = true
INDEX_TEXT_DIRECTLY_OBSERVED    = true
DIRECT_POST_REPLAYABLE_PAYLOAD  = false
CORPUS_ADMISSION                = false
CLOSING_FIELD_CREDIT            = false
```

No source-registry, payload-store, acquisition-manifest, corpus-index, or predicate-ledger mutation is made by this locator-only report. This preserves the Phase-6D rule that closing credit requires the replayable content-addressed provenance chain.

## Exact target predicate / fields

```text
predicate        = TURTLE_SOUP_CONFIRMATION
primary field    = EXACT_PREDICATE
secondary field  = CONFIRMATION
adjacent field   = DIRECTION_TIMEFRAME_OWNERSHIP
```

The evidence is scoped to Romeo's stated **bearish ideal reaction involving an old CRTH**. It is not generalized to every old high, every CRT high, every Turtle Soup setup, Model #1, or every bearish CRT.

## What the statement directly establishes

### 1. Direction is explicit

Romeo explicitly scopes the sequence with:

```text
When I’m bearish
```

This is direct bearish ownership for the described ideal reaction.

It does **not** define how the bearish bias is obtained, what timeframe owns that bias, or whether the sequence is valid when higher/lower timeframes disagree.

### 2. The sequence is ordered around candle opening and an old CRTH interaction

The source directly orders three stages:

```text
candle opens
    -> stabs into an old CRTH
    -> dumps
```

This is stronger than an unsequenced mention of an old extreme because the interaction is explicitly positioned after the candle opens and before the desired bearish move.

The source does **not** define:

- how the `old CRTH` is selected from multiple historical candidates;
- whether `stabs into` requires a wick only, body overlap, trade-through, touch, or close relation;
- minimum or maximum excursion beyond/into the old CRTH;
- whether a close back below the old CRTH is mandatory;
- what price movement qualifies as `dumps`;
- the candle timeframe or parent/child ownership;
- the information-availability timestamp at which the reaction becomes confirmed.

### 3. `old CRTH` is a required object in this stated ideal reaction

The second step does not say merely `a high`; it names an `old CRTH`.

For this stated bearish ideal reaction, the source therefore supports an old-CRT-high interaction as part of the desired path. It does not establish that any old CRTH qualifies or define an age, recency, untouched/touched, nearest, highest, session, or liquidity-ranking selector.

### 4. The terminal verb is qualitative, not a deterministic confirmation event

The third step is:

```text
dumps
```

That directly communicates the desired post-interaction direction, but it is not a machine-testable magnitude, close, displacement, target, or time-window rule.

Therefore the source cannot by itself tell two independent engineers exactly which raw bar first confirms the reaction.

## `TURTLE_SOUP_CONFIRMATION` field impact

### `EXACT_PREDICATE`

**State after discovery: `STRONGER_PARTIAL / NO_CLOSING_CREDIT`**

The source materially narrows one bearish old-extreme interaction path to an ordered structure:

```text
bearish context
    -> candle opens
    -> interaction with an old CRTH
    -> bearish movement
```

This is useful semantic evidence, but the predicate remains incomplete because the selector for the old CRTH and the raw geometry of `stabs into` / `dumps` are undefined.

The source also does not label this reaction as `Turtle Soup`, so it cannot be used to assert equivalence between the described reaction and the complete Turtle Soup predicate.

### `INFORMATION_AVAILABILITY_TIME`

**State: `MISSING / NO_CLOSING_CREDIT`**

The source gives an order of events but not the exact live-data timestamp at which `stabs into` or `dumps` becomes knowable/confirmed.

No close-time, intrabar, or next-bar decision rule may be inferred.

### `DIRECTION_TIMEFRAME_OWNERSHIP`

**State after discovery: `PARTIAL_CONTEXT_ONLY / NO_CLOSING_CREDIT`**

Bearish direction is explicit. Timeframe ownership is absent.

The post therefore strengthens direction context without closing the composite ownership field.

### `CONFIRMATION`

**State after discovery: `STRONGER_PARTIAL / NO_CLOSING_CREDIT`**

The source directly says the desired continuation after the old-CRTH interaction is a bearish move (`dumps`). That supplies a qualitative confirmation consequence and ordering.

It remains non-deterministic because no threshold, close rule, displacement rule, target, elapsed time, or first-confirmed bar is defined.

### `INVALIDATION`

**State: `MISSING`**

No condition is stated for when the bearish reaction idea is invalidated.

### `EXPIRY`

**State: `MISSING`**

No age, session, candle-count, time, reuse, or supersession rule is stated.

### `DATA_REQUIREMENTS`

**State after discovery: `PARTIAL_CONTEXT_ONLY / NO_CLOSING_CREDIT`**

At minimum, the described sequence requires candle chronology, candle-open state, a pre-existing `old CRTH` object, and subsequent price movement.

The source does not define how to derive the old CRTH or the exact observations needed to classify `stabs into` and `dumps`.

## Relationship to the existing Turtle Soup blocker

Issue #16 currently records that Turtle Soup still lacks:

```text
qualifying-extreme selection
confirmation
ownership
invalidation
expiry
```

Post `6615` narrows the semantic shape of one bearish old-CRTH reaction but does not resolve the qualifying-extreme selector or machine-testable confirmation event.

Therefore:

```text
TURTLE_SOUP_CONFIRMATION = STRONGER_PARTIAL / STILL_BLOCKING
```

## Two-engineer test

Given a pre-labeled sequence such as:

```text
BIAS = BEARISH
CANDLE_STATE = OPENED
OLD_CRTH_INTERACTION = STAB
POST_INTERACTION_MOVE = DUMP
```

two engineers can agree that it matches the order Romeo describes in post `6615`.

Starting only from raw timestamped OHLC/quote data, the same engineers still have to invent material parts of the classifier:

- which historical CRTH is the qualifying `old CRTH`;
- the exact geometry of `stabs into`;
- whether the event is intrabar or close-confirmed;
- the exact magnitude/time definition of `dumps`;
- timeframe ownership;
- invalidation and expiry;
- whether and when the sequence is specifically Turtle Soup rather than another bearish CRT reaction.

Therefore:

```text
TWO_ENGINEER_TEST_FOR_ORDERED_REACTION_DESCRIPTION = MATERIAL_ADVANCEMENT
TWO_ENGINEER_TEST_FOR_TURTLE_SOUP_CONFIRMATION     = FAIL
```

## Explicit non-promotions

This report does not authorize any of the following:

```text
POST_6615_EQUALS_TURTLE_SOUP          = false
ANY_OLD_CRTH_QUALIFIES                = false
STAB_EQUALS_WICK                      = false
DUMP_THRESHOLD_DEFINED                = false
CLOSE_CONFIRMATION_DEFINED            = false
TIMEFRAME_OWNERSHIP_CLOSED            = false
TURTLE_SOUP_PREDICATE_CLOSED          = false
NEW_ALPHA_CANDIDATE                   = false
RUN_DETECTOR_OR_COUNTS                = false
RUN_BACKTEST_OR_PNL                   = false
OPEN_OOS_CONFIRM                      = false
PAPER_TRADING                         = false
SHADOW_TRADING                        = false
LIVE_TRADING                          = false
```

The frozen Phase-6/6B results remain immutable. OOS and CONFIRM remain unopened. Paper/live safety gates are unchanged.

## Follow-up rule

Do not create another task merely to decompose the same `stabs into` / `dumps` ambiguity.

A future bounded re-entry is justified only if new first-party Romeo material directly supplies one of the remaining exact fields, for example:

1. how the qualifying old CRTH/high is selected;
2. the exact wick/body/close/tolerance geometry for the old-CRTH interaction;
3. a machine-testable bearish confirmation event or threshold;
4. timeframe/context ownership;
5. invalidation/expiry/reuse semantics; or
6. a replayable original payload for post `6615` that can enter the Phase-6D provenance chain.

## Final disposition

```text
NEW_FIRST_PARTY_EVIDENCE              = true
TARGET_PREDICATE                      = TURTLE_SOUP_CONFIRMATION
TARGET_FIELD_PRIMARY                  = EXACT_PREDICATE
TARGET_FIELD_SECONDARY                = CONFIRMATION
BEARISH_OLD_CRTH_SEQUENCE             = DIRECT_BUT_PARTIAL
REPLAYABLE_ORIGINAL_PAYLOAD           = false
CLOSING_FIELD_CREDIT                  = false
TURTLE_SOUP_CONFIRMATION              = STRONGER_PARTIAL / KEEP_BLOCKED
ISSUE_16                              = KEEP_BLOCKED
ISSUE_37                              = MUST_NOT_START
OOS_CONFIRM                           = UNOPENED
PAPER_SHADOW_LIVE                     = NOT_AUTHORIZED
```
