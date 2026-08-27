# Phase 6D — first-party time-only entry statement 6938

**Date:** 2026-08-27  
**Tracking:** Issue #146  
**Target predicate:** `TIME_SELECTOR`  
**Target field:** `EXACT_PREDICATE` / execution-role semantics  
**Mode:** bounded first-party evidence classification only  
**Gate impact:** none

## Source

Official Romeo Telegram channel:

- channel: `@officialRomeotpt`
- post locator: `https://t.me/officialRomeotpt/6938`
- current official channel index: `https://t.me/s/officialRomeotpt`

The public official channel index currently exposes the statement:

> “Sometimes I place a trade after analysing the charts a lot, after price action shows me a reason to enter. Sometimes I enter based on time.”

The direct single-post route currently renders as Telegram's post widget locator in this runtime; it does not expose a content-addressed payload suitable for admission into the existing Phase-6D payload/manifest chain. This report therefore treats the statement as direct first-party index text with a stable official post locator, not as a replayably captured original payload artifact.

## Exact field question

Prior status leaves `TIME` incomplete on, among other things, `hard-filter semantics`. The bounded question for this pass is narrower:

> Is time only contextual/preference information, or can time itself own an entry decision in at least some Romeo executions?

## Direct support

The statement directly supports only this proposition:

```text
TIME_CAN_OWN_ENTRY_DECISION_IN_SOME_CASES = true
```

It also distinguishes two entry bases in Romeo's own wording:

```text
PRICE_ACTION_REASONED_ENTRY = occurs sometimes
TIME_BASED_ENTRY            = occurs sometimes
```

This is stronger than the earlier preference-only evidence such as favourite weekdays, because it explicitly links time to the act of entering a trade.

## What this does not support

No deterministic implementation semantics are provided for:

- which exact time or times qualify;
- timezone, DST, venue or session-day ownership;
- weekday/session boundaries;
- whether time-only entry is a universal rule, optional branch, exception, or discretionary practice;
- direction selection;
- required market state or preconditions;
- confirmation;
- invalidation;
- expiry;
- owning timeframe;
- data requirements beyond the existence of time;
- interaction with Turtle Soup, CRT, key levels, SMT, Model #1 or True MSS.

The word `sometimes` specifically prevents promoting the statement into a universal hard filter or unconditional entry rule.

## Predicate-ledger classification

```text
TIME_SELECTOR.EXACT_PREDICATE = STRONGER_PARTIAL
CLOSING_FIELD_CREDIT          = 0
CLOSED_PREDICATES             = 0
CANDIDATE_READY_ROWS          = 0
```

Rationale: the evidence resolves the narrow role question that time can be sufficient for an entry decision in some cases, but it does not define the conditions under which that branch is valid. Two independent engineers still could not implement the same deterministic `TIME_SELECTOR` from this statement.

## Safety / authorization

```text
CREATE_NEW_ALPHA_CANDIDATE        = false
RUN_DETECTOR_OR_COUNTS            = false
RUN_BACKTEST_OR_PNL               = false
OPEN_OOS_CONFIRM                  = false
LOWER_ACTIVITY_THRESHOLD          = false
PAPER_TRADING                     = false
SHADOW_TRADING                    = false
LIVE_TRADING                      = false
```

Phase 6 and 6B historical results remain immutable. This evidence does not reopen any protected outcome surface.

## Disposition

```text
NEW_FIRST_PARTY_EVIDENCE = ADMITTED_AS_LOCATOR_BOUND_DIRECT_TEXT
TIME_ROLE_SEMANTICS      = STRONGER_PARTIAL
TIME_SELECTOR            = KEEP_BLOCKED
ISSUE_16                 = KEEP_BLOCKED / CLOSED_NOT_PLANNED
ISSUE_42                 = NO_DOWNSTREAM_GATE_CHANGE
```

Further bounded re-entry is justified only by new first-party material that supplies an exact deterministic missing field, such as the actual qualifying time/session contract, ownership, confirmation, invalidation or expiry. Do not re-mine the exhausted corpus for this statement.
