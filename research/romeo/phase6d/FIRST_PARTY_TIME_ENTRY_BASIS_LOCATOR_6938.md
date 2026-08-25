# Phase 6D — First-Party Time Entry-Basis Locator 6938

**Date:** 2026-08-25  
**Tracking:** Issue #141  
**Mode:** new first-party locator/provenance recovery + bounded field synthesis  
**Disposition:** `DIRECT_INDEX_OBSERVATION / MATERIAL_ROLE_ADVANCEMENT / NO_CLOSING_FIELD_CREDIT`

## Re-entry justification

The current-corpus exhaustion checkpoint allows Phase-6C/6D re-entry only when genuinely new first-party evidence or newly recoverable source material directly addresses an exact missing predicate field.

The current official Romeo Telegram channel index (`@officialRomeotpt`) exposes a new statement at post `6938` that is not represented in the repository and directly addresses the still-missing `TIME_SELECTOR` role semantics recorded in Issues #16/#42.

Target before acquisition:

```text
predicate = TIME_SELECTOR
field     = EXACT_PREDICATE / hard-filter-vs-context semantics
question  = Can time itself be an entry basis, rather than only a preference/context prior?
```

This is not a re-mining pass over the exhausted corpus.

## Direct first-party observation

Official channel/index locator:

- `https://t.me/s/officialRomeotpt`

The channel index directly exposes this text:

> Sometimes I place a trade after analysing the charts a lot, after price action shows me a reason to enter. Sometimes I enter based on time.

The timestamp link resolves to the exact official post locator:

- `https://t.me/officialRomeotpt/6938`

Repository search found no prior issue or evidence artifact handling this exact statement/post before Issue #141 was preregistered.

## Bounded direct-post retrieval result

One direct retrieval of the exact post locator was attempted after preregistration.

The available direct-post response exposed the official Telegram embed shell and exact `data-telegram-post="officialRomeotpt/6938"` binding, but did not expose replayable original message payload bytes/text suitable for the existing content-addressed Phase-6D payload/manifest/corpus chain.

Accordingly:

```text
FIRST_PARTY_CHANNEL_IDENTITY    = true
POST_ID_BOUND                   = true
INDEX_TEXT_DIRECTLY_OBSERVED    = true
DIRECT_POST_IDENTITY_BOUND      = true
REPLAYABLE_POST_PAYLOAD         = false
CORPUS_ADMISSION                = false
CLOSING_FIELD_CREDIT            = false
```

No source-registry, payload, acquisition-manifest, corpus-index, or predicate-ledger mutation is justified by this locator-only acquisition state.

## Exact semantic advancement

The new statement is materially stronger than the earlier preference-only and recurring-weekday-role evidence.

Romeo explicitly contrasts two entry bases:

1. price action provides a reason to enter after chart analysis;
2. on some occasions, entry is based on time.

The strongest directly supported interpretation is therefore:

```text
TIME_CAN_BE_AN_ENTRY_BASIS = DIRECT_FIRST_PARTY_STATEMENT
TIME_IS_ONLY_CONTEXT       = contradicted by this statement
TIME_IS_ALWAYS_REQUIRED    = not established
TIME_IS_A_UNIVERSAL_FILTER = not established
```

This closes one qualitative ambiguity: the project must not classify Romeo's time doctrine as merely descriptive calendar context or personal weekday preference. Time can participate at the entry-decision layer.

It does **not** define an executable time selector.

## `TIME_SELECTOR` field impact

### `EXACT_PREDICATE` / role semantics

**State after discovery: `STRONGER_PARTIAL / DIRECT_ENTRY_ROLE / NO_CLOSING_CREDIT`**

Directly supported:

- Romeo sometimes enters based on time.
- Price-action-based entry and time-based entry are presented as distinct possible bases.

Still unresolved:

- the exact time/key-time values;
- whether time alone is sufficient or still requires hidden contextual prerequisites;
- whether the rule is instrument-, session-, weekday-, or setup-specific;
- whether time is an eligibility gate, trigger, ranking feature, or alternative execution path in each model;
- whether a non-time-based entry remains valid when a time condition is absent.

### `INFORMATION_AVAILABILITY_TIME`

**State: `MISSING FOR EXECUTION`**

The statement proves that time may matter at entry, but it provides no clock value, calendar rule, timezone, DST anchor, session boundary, or activation timestamp.

### `DIRECTION_TIMEFRAME_OWNERSHIP`

**State: `MISSING`**

No timeframe, instrument, direction, parent candle, or market/session owns the time-based entry state in this statement.

### `CONFIRMATION`

**State: `MISSING`**

The contrast with price action does not establish whether time-based entry requires separate confirmation or what such confirmation would be.

### `INVALIDATION`

**State: `MISSING`**

No invalidation event is defined.

### `EXPIRY`

**State: `MISSING`**

No expiry or missed-entry lifecycle is defined.

### `DATA_REQUIREMENTS`

**State: `STRONGER_PARTIAL / NO_CLOSING_CREDIT`**

A faithful future implementation must be capable of representing a time-derived entry condition as a first-class input rather than treating time as commentary only.

The exact required temporal data remain undefined because source evidence does not identify timezone, session calendar, key times, tolerance windows, holiday handling, or market scope.

## Two-engineer test

Two engineers can independently agree on the qualitative source-backed statement:

```text
Romeo sometimes uses time itself as a basis for entry.
```

They still cannot independently implement identical raw-data logic because they would need to invent the time values, ownership, eligibility semantics, confirmation, invalidation, and expiry.

Therefore:

```text
TWO_ENGINEER_TEST_FOR_ROLE_SEMANTICS = PASS_QUALITATIVE
TWO_ENGINEER_TEST_FOR_TIME_SELECTOR  = FAIL
```

## Safe doctrine statement

The strongest source-grounded statement currently allowed is:

> Romeo explicitly says that some entries are based on price-action reasons and that sometimes he enters based on time; therefore time can operate at the entry-decision layer, but this statement does not define the executable timing rule.

Do not strengthen this into any of the following without new direct first-party evidence:

```text
specific London/New York key time
UTC or New York calendar ownership
fixed minute-of-hour trigger
Tuesday/Wednesday mandatory entry window
entry without any other prerequisite
universal hard time filter
fixed tolerance window
fixed invalidation or expiry
```

## Governance disposition

```text
NEW_FIRST_PARTY_EVIDENCE              = true
TARGET_FIELD                           = TIME_SELECTOR role semantics
DIRECT_ROLE_ADVANCEMENT               = time may be entry basis
REPLAYABLE_PAYLOAD_CAPTURED           = false
CORPUS_ADMISSION                      = false
CLOSING_FIELD_EVIDENCE                = 0
CLOSED_PREDICATES                     = 0
TIME_SELECTOR                         = STRONGER_PARTIAL / KEEP_BLOCKED
CANDIDATE_READY                       = false
ISSUE_16                              = KEEP_BLOCKED
ISSUE_37                              = MUST_NOT_START
OOS_CONFIRM                           = UNOPENED
PAPER_SHADOW_LIVE                     = NOT_AUTHORIZED
```

No candidate creation, detector/count activity, backtest/P&L, OOS/CONFIRM access, paper execution, shadow trading, live trading, parameter fitting, or outcome-based time selection is authorized by this report.

## Exact next evidence needed

Re-enter only if a new or newly recoverable first-party source directly defines at least one of these missing fields:

1. exact key time / clock value or deterministic time construction;
2. timezone/session/calendar ownership;
3. whether time is a hard eligibility filter, a trigger, or an alternative entry path;
4. model/timeframe/instrument ownership;
5. confirmation requirements for a time-based entry;
6. invalidation and expiry of the time state.
