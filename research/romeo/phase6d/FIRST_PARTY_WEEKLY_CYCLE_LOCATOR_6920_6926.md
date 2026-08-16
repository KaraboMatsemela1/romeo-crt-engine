# Phase 6D — First-Party Weekly-Cycle Locator 6920–6926

**Date:** 2026-08-16  
**Tracking:** Issue #116  
**Mode:** new first-party locator/provenance recovery + field-level synthesis  
**Disposition:** `LOCATOR_BOUND_NEW_EVIDENCE / NO_CLOSING_FIELD_CREDIT`

## Why this pass legitimately re-entered Phase 6D

The current-corpus exhaustion checkpoint (`CURRENT_CORPUS_EXHAUSTION_001.md`) stopped repeated research over the already admitted evidence set and allowed re-entry only for genuinely new or newly recoverable first-party semantics tied to an exact missing field.

On 2026-08-16 the current official Romeo Telegram channel index (`@officialRomeotpt`) exposed a contiguous weekly-cycle sequence that is not present in the repository and directly addresses the previously unresolved weekday component of `TIME_SELECTOR`.

This is therefore new first-party evidence availability, not a re-reading of the exhausted corpus.

## Direct first-party observation

Official channel/index locator:

- `https://t.me/s/officialRomeotpt`

The index exposed these exact post identities and statements:

| Post | Direct locator | Observed first-party text | Immediate semantic role |
|---|---|---|---|
| 6920 | `https://t.me/officialRomeotpt/6920` | `Tuesday is turtle soup day.` | Tuesday is explicitly associated with Turtle Soup. |
| 6921 | `https://t.me/officialRomeotpt/6921` | `Wednesday is a classic buy/sell day.` | Wednesday is explicitly associated with a classic buy/sell-day role. |
| 6922 | `https://t.me/officialRomeotpt/6922` | `Thursday-Friday cap the weekly range.` | Thursday/Friday are explicitly associated with capping the weekly range. |
| 6923 | `https://t.me/officialRomeotpt/6923` | `And finally… Saturdays are for reviewing the week that was, Sundays are for planning the week to be. I just ran you through the weekly cycle of a trader’s life.. live :)` | The weekday statements are presented as one weekly-cycle sequence rather than unrelated comments. |
| 6924 | `https://t.me/officialRomeotpt/6924` | `This is the framework you work with every week.` | Romeo explicitly calls the sequence a recurring weekly framework. |
| 6925 | `https://t.me/officialRomeotpt/6925` | `Both public and private students.` | The framework is not framed as private-only doctrine. |
| 6926 | `https://t.me/officialRomeotpt/6926` | `This is the same for all of you.` | Romeo explicitly generalizes the framework to the addressed student population. |

The exact post IDs were bound from the timestamp links exposed by the official channel index.

## Bounded direct-post retrieval result

One direct retrieval attempt was made for every post in scope.

```text
6920  direct single-post fetch  CACHE_MISS
6921  direct single-post fetch  EMBED_SHELL_ONLY / no replayable text payload
6922  direct single-post fetch  CACHE_MISS
6923  direct single-post fetch  CACHE_MISS
6924  direct single-post fetch  CACHE_MISS
6925  direct single-post fetch  CACHE_MISS
6926  direct single-post fetch  CACHE_MISS
```

The official channel index itself exposed the text and timestamp-linked identities, but the available research runtime did not capture raw direct-post payload bytes suitable for the Phase-6D content-addressed payload/acquisition-manifest/corpus-index chain.

Accordingly:

```text
FIRST_PARTY_CHANNEL_IDENTITY    = true
POST_IDS_BOUND                  = true
INDEX_TEXT_DIRECTLY_OBSERVED    = true
REPLAYABLE_POST_PAYLOADS        = false
CORPUS_ADMISSION                = false
CLOSING_FIELD_CREDIT            = false
```

No source-registry, payload, acquisition-manifest, corpus-index, or predicate-ledger mutation is made by this locator-only report.

## Material semantic advancement over post 6519

The prior weekday locator (`FIRST_PARTY_WEEKDAY_CONTEXT_LOCATOR_6519.md`) contained preference language only:

```text
Tuesdays and Wednesdays are my favourite days of the week.
```

That could not safely become a time selector.

Posts 6920–6926 are materially stronger because Romeo now assigns explicit recurring roles to parts of the trading week and labels the sequence as the framework used every week.

The directly observed weekly taxonomy is:

```text
Tuesday            -> turtle soup day
Wednesday          -> classic buy/sell day
Thursday–Friday    -> cap the weekly range
Saturday           -> review the week that was
Sunday             -> plan the week to be
```

For strategy research, the first three mappings are potentially market-semantic. Saturday/Sunday are workflow/context semantics, not order predicates.

This advances the source-backed weekday doctrine from `PREFERENCE_CONTEXT` to `RECURRING_WEEKDAY_ROLE_TAXONOMY`.

It does **not** yet establish a complete executable time filter.

## `TIME_SELECTOR` field impact

### `EXACT_PREDICATE`

**State after discovery: `STRONG_PARTIAL / NO_CLOSING_CREDIT`**

Direct source evidence now gives explicit recurring weekday-role mappings rather than a mere preference.

Still unresolved:

- whether `Tuesday is turtle soup day` means Turtle Soup is required, merely favored, or only commonly expected;
- whether non-Turtle-Soup setups are invalid on Tuesday;
- what `classic buy/sell day` means as a deterministic event;
- what exact observable event proves that Thursday/Friday have `capped` the weekly range;
- whether the weekday taxonomy is a hard eligibility gate, context prior, expectation, ranking feature, or descriptive cycle.

### `INFORMATION_AVAILABILITY_TIME`

**State after discovery: `PARTIAL / NO_CLOSING_CREDIT`**

`This is the framework you work with every week` makes the weekday roles ex-ante recurring doctrine rather than a post-outcome label.

However the causal calendar boundary remains unresolved because no timezone, DST anchor, venue/session day boundary, holiday rule, or shortened-week handling is defined.

### `DIRECTION_TIMEFRAME_OWNERSHIP`

**State: `MISSING / PARTIAL_CONTEXT_ONLY`**

`Wednesday is a classic buy/sell day` explicitly permits both directional labels in the wording and therefore does not provide a direction-selection rule.

No source statement in this sequence defines:

- which timeframe owns the weekday state;
- which parent CRT is governed by it;
- which market/instrument/session the weekly cycle applies to;
- how direction is selected on Wednesday;
- whether Thursday/Friday range capping is directional or terminal-context logic.

### `CONFIRMATION`

**State: `MISSING`**

No machine-testable confirmation event is defined for the weekday roles.

### `INVALIDATION`

**State: `MISSING`**

No rule states what invalidates the day's expected role.

### `EXPIRY`

**State: `MISSING`**

The ordinary-language day labels imply a weekly sequence, but source evidence does not define the executable end boundary of an active Tuesday/Wednesday/Thursday-Friday state. A midnight, session close, parent-candle close, target hit, or next-key-time assumption would be project-authored.

### `DATA_REQUIREMENTS`

**State after discovery: `STRONG_PARTIAL / NO_CLOSING_CREDIT`**

The source now directly requires a representation capable of distinguishing at least:

```text
weekday
trading week
Tuesday / Wednesday / Thursday / Friday role
```

Still unresolved data semantics include:

- timezone and DST;
- trading-day/session boundary;
- venue calendar;
- holiday/short-week behavior;
- instrument/market scope;
- exact week-open/week-close ownership.

## Two-engineer test

Given an already-normalized label such as `Tuesday`, two engineers can now agree that Romeo's directly stated role is `turtle soup day`.

Starting from exchange timestamps and raw market data, the same engineers still cannot independently produce an identical executable `TIME_SELECTOR` because they must choose project-authored answers for:

- timezone/day boundary;
- market/session ownership;
- hard-filter versus contextual role;
- exact Tuesday Turtle-Soup qualification;
- Wednesday buy/sell determination;
- confirmation/invalidation/expiry.

Therefore:

```text
TWO_ENGINEER_TEST_FOR_WEEKDAY_LABELS = MATERIAL_ADVANCEMENT
TWO_ENGINEER_TEST_FOR_TIME_SELECTOR  = FAIL
```

## Safe doctrine statement

The strongest source-grounded statement currently allowed is:

> Romeo presents a recurring weekly framework in which Tuesday is associated with Turtle Soup, Wednesday with a classic buy/sell-day role, and Thursday–Friday with capping the weekly range.

Do not strengthen this into:

```text
Tuesday-only Turtle Soup eligibility
Wednesday mandatory entry day
Thursday/Friday no-entry rule
fixed weekly-range completion timestamp
New York calendar ownership
UTC calendar ownership
hard weekday filter
```

without additional direct first-party evidence.

## Exact next evidence needed

This new sequence creates positive closure leverage for `TIME_SELECTOR`, but raw-post provenance must first be completed before any field can receive `CLOSING` status.

After replayable payload admission, the highest-leverage missing semantic questions are:

1. **Calendar ownership:** what timezone/session defines Tuesday, Wednesday and Thursday–Friday for this framework?
2. **Filter semantics:** are these weekday roles mandatory eligibility states, expected tendencies, or contextual priors?
3. **Tuesday qualification:** what exact Turtle-Soup state makes Tuesday a valid trade day?
4. **Wednesday direction:** what determines the `buy` versus `sell` branch?
5. **Lifecycle:** when does each weekday state become active, invalidate, and expire?

A new task should target one of these only if a new first-party source directly addresses it.

## Governance disposition

```text
NEW_FIRST_PARTY_EVIDENCE              = true
WEEKDAY_ROLE_TAXONOMY                 = DIRECT_INDEX_OBSERVATION
REPLAYABLE_PAYLOAD_CAPTURED           = false
CORPUS_ADMISSION                      = false
CLOSING_FIELD_EVIDENCE                = 0
CLOSED_PREDICATES                     = 0
TIME_SELECTOR                         = STRONGER_PARTIAL / KEEP_BLOCKED
CANDIDATE_READY                       = false
ISSUE_16                              = KEEP_BLOCKED
ISSUE_37                              = MUST_NOT_START
```

No candidate creation, detector/count activity, backtest/P&L, OOS/CONFIRM access, paper execution, shadow trading, live trading, parameter fitting, or outcome-based weekday selection is authorized by this report.
