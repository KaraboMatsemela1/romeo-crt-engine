# Phase 6D — First-Party MOB-Level Locator 6744

**Date:** 2026-08-17  
**Tracking:** Issue #118  
**Mode:** new first-party locator/provenance recovery + field-level synthesis  
**Disposition:** `LOCATOR_BOUND_NEW_EVIDENCE / NO_CLOSING_FIELD_CREDIT`

## Why this pass legitimately re-entered Phase 6D

Issue #42 and the current-corpus exhaustion checkpoint permit a new bounded Phase-6C/6D task only when genuinely new first-party material directly addresses an exact missing predicate field or when a previously unavailable original payload becomes recoverable.

On 2026-08-17 the official Romeo Telegram channel index exposed post `6744`, which is not represented in the repository. Repository searches for `6744`, `make or break`, and the MOB wording returned no existing capture.

The statement directly addresses part of the still-open `KEY_LEVEL_SELECTOR` lifecycle debt, especially `INVALIDATION` / cancellation behavior and reconciliation item `KLSEL-B005 — consumed / invalidated / superseded semantics`.

This is new evidence availability, not a re-mine of the exhausted admitted corpus.

## Direct first-party observation

Official channel/index locator:

- `https://t.me/s/officialRomeotpt?before=6745`

Timestamp-bound direct post locator exposed by the official index:

- `https://t.me/officialRomeotpt/6744`

The official index directly exposes the following text:

```text
CRT terminology: MOB.
The “make or break” level.
If this level is broken through, the target will be hit. If this level is respected, it will block the target from reaching.
In case of the latter; scratch the trade idea and look for another one.
```

The timestamp link on the same first-party index binds that statement to post `6744`.

## Bounded direct-post retrieval result

Exactly one direct single-post retrieval was attempted in this pass.

```text
6744  direct single-post fetch  CACHE_MISS / no replayable original post payload
```

A separate environment download attempt reached the official Telegram channel-index route and received HTTP 200 with HTML content, but the runtime did not expose those response bytes as a retrievable file artifact. That is source contact, not a content-addressable payload capture.

Accordingly:

```text
FIRST_PARTY_CHANNEL_IDENTITY    = true
POST_ID_BOUND                   = true
INDEX_TEXT_DIRECTLY_OBSERVED    = true
DIRECT_POST_REPLAYABLE_PAYLOAD  = false
CORPUS_ADMISSION                = false
CLOSING_FIELD_CREDIT            = false
```

No source-registry, payload-store, acquisition-manifest, corpus-index, or predicate-ledger mutation is made by this locator-only report. This preserves the Phase-6D rule that ledger closure credit requires replayable provenance through the content-addressed chain.

## Exact target predicate / fields

```text
predicate = KEY_LEVEL_SELECTOR
primary field = INVALIDATION
secondary field = EXPIRY / cancellation lifecycle
related blocker = KLSEL-B005 consumed / invalidated / superseded semantics
```

The evidence is deliberately scoped to the named `MOB` level. It is not generalized to every Romeo key level.

## What the statement directly establishes

### 1. `MOB` is Romeo terminology for a level

The source explicitly names:

```text
MOB = “make or break” level
```

This is a direct first-party terminology statement.

It does **not** define how a MOB is discovered or selected from market data.

### 2. The level has two stated outcome branches

Romeo directly contrasts:

```text
MOB broken through -> target will be hit
MOB respected      -> level blocks target from reaching
```

This proves that, in the named MOB context, break-versus-respect of the level changes the validity of the target path.

The wording does not define a deterministic raw-price predicate for `broken through` or `respected`.

### 3. Respect of the MOB has an explicit cancellation instruction

Romeo directly instructs that when the latter branch occurs — the level is respected and blocks the target — the trader should:

```text
scratch the trade idea
look for another one
```

This is direct evidence for a MOB-specific cancellation/no-longer-pursue-the-idea semantic. It is stronger than generic example stop language because the cancellation instruction is stated as the consequence of the level-respected branch.

It still does not specify order-management mechanics for an already-open position, nor whether `scratch` means cancel a pending idea, flatten an open position, or simply abandon further pursuit after a pre-entry invalidation event.

## `KEY_LEVEL_SELECTOR` field impact

### `EXACT_PREDICATE`

**State after discovery: `PARTIAL / NO_CLOSING_CREDIT`**

The source adds one named level concept and a binary broken-versus-respected relationship.

Still missing for deterministic use:

- algorithm for selecting a MOB;
- whether MOB is a subtype of the Episode-5 key-level family, an objective barrier, or a separate concept;
- exact price representation of the level;
- exact meaning of `broken through`;
- exact meaning of `respected`;
- tolerance, wick/body/close semantics;
- source timeframe and owning context.

### `INFORMATION_AVAILABILITY_TIME`

**State: `MISSING / NO_CLOSING_CREDIT`**

The statement describes conditional branches but does not define when the break/respect event becomes causally knowable from live bars.

No decision-time contract may be inferred.

### `DIRECTION_TIMEFRAME_OWNERSHIP`

**State: `MISSING`**

No timeframe, market, direction, parent CRT, or setup-family ownership is specified.

### `CONFIRMATION`

**State: `PARTIAL_CONTEXT_ONLY`**

`broken through` versus `respected` clearly matters, but neither state has a machine-testable confirmation event.

### `INVALIDATION`

**State after discovery: `STRONG_PARTIAL / NO_CLOSING_CREDIT`**

This is the main semantic advance.

For a trade idea whose target path depends on the named MOB level, the source directly supports:

```text
MOB respected and blocks target
        -> scratch the trade idea
```

That is an explicit cancellation consequence.

It is **not** sufficient to close `INVALIDATION` because two engineers must still invent the exact raw-market predicate that proves the MOB was `respected`, and the source does not establish that this rule applies to every key-level candidate.

### `EXPIRY`

**State after discovery: `PARTIAL / NO_CLOSING_CREDIT`**

The source supplies an event-driven idea-cancellation instruction for the MOB-respected branch. This is lifecycle evidence, but not a complete expiry contract.

Still unresolved:

- whether an untouched MOB expires by time;
- whether a broken MOB is consumed or reusable;
- whether a respected MOB remains active for a different target/idea;
- whether `scratch` applies before entry, after entry, or both;
- when a newer level supersedes the MOB.

### `DATA_REQUIREMENTS`

**State: `PARTIAL_CONTEXT_ONLY`**

At minimum the concept requires a target, a MOB level, and observable price interaction with that level. The source does not define the data construction needed to derive those objects deterministically.

## Impact on `KLSEL-B005`

The reconciliation blocker currently asks when a touched level remains active, when reaction consumes it, whether breakout invalidates it, whether reuse is permitted, and when a newer level supersedes an older one.

Post 6744 materially narrows one sub-question only:

```text
for a named MOB level,
if the level is respected such that it blocks the target,
the current trade idea is to be scratched.
```

That is useful invalidation/cancellation doctrine, but it does not resolve the broader consumed/reused/superseded state machine.

Therefore:

```text
KLSEL-B005 = STRONGER_PARTIAL / STILL_BLOCKING
```

## Two-engineer test

Given a pre-labeled event such as:

```text
MOB_STATE = RESPECTED_AND_BLOCKING_TARGET
```

two engineers can now agree that the source-grounded consequence is to scratch that trade idea.

Starting from raw timestamped OHLC/quote data, the same engineers still cannot independently produce the same event because the source does not define:

- MOB selection;
- level construction;
- break-versus-respect geometry;
- timeframe ownership;
- information-availability timing;
- reuse/consumption/supersession;
- target ownership.

Therefore:

```text
TWO_ENGINEER_TEST_FOR_MOB_CANCELLATION_CONSEQUENCE = MATERIAL_ADVANCEMENT
TWO_ENGINEER_TEST_FOR_KEY_LEVEL_SELECTOR           = FAIL
```

## Explicit non-promotions

This report does not authorize any of the following:

```text
MOB_AS_UNIVERSAL_KEY_LEVEL            = false
KEY_LEVEL_TAXONOMY_CLOSED             = false
KEY_LEVEL_RANKING_CLOSED              = false
LEVEL_REACHED_PREDICATE_CLOSED        = false
KEY_LEVEL_INVALIDATION_CLOSED         = false
KEY_LEVEL_EXPIRY_CLOSED               = false
KEY_LEVEL_SELECTOR_CLOSED             = false
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

Do not create another task merely to decompose the same MOB ambiguity.

A future bounded re-entry is justified only if first-party Romeo material directly supplies one of the remaining exact fields, for example:

1. how the MOB level is selected/constructed;
2. the exact wick/body/close/tolerance rule for `broken through` or `respected`;
3. timeframe/context ownership;
4. direct consumed/reuse/supersession semantics; or
5. a replayable original payload for post 6744 that can enter the Phase-6D provenance chain.

## Final disposition

```text
NEW_FIRST_PARTY_EVIDENCE              = true
TARGET_PREDICATE                      = KEY_LEVEL_SELECTOR
TARGET_FIELD_PRIMARY                  = INVALIDATION
TARGET_FIELD_SECONDARY                = EXPIRY
MOB_CANCELLATION_SEMANTICS            = DIRECT_BUT_PARTIAL
REPLAYABLE_ORIGINAL_PAYLOAD           = false
CLOSING_FIELD_CREDIT                  = false
KEY_LEVEL_SELECTOR                    = STRONGER_PARTIAL / KEEP_BLOCKED
ISSUE_16                              = KEEP_BLOCKED
ISSUE_37                              = MUST_NOT_START
OOS_CONFIRM                           = UNOPENED
PAPER_SHADOW_LIVE                     = NOT_AUTHORIZED
```
