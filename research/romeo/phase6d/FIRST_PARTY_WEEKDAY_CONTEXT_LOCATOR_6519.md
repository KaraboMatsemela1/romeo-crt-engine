# Phase 6D — First-Party Weekday Context Locator 6519

**Date:** 2026-08-15  
**Tracking:** Issue #84  
**Mode:** first-party locator/provenance recovery only  
**Disposition:** `LOCATOR_BOUND_DISCOVERY_ONLY / NO_CLOSING_FIELD_CREDIT`

## Direct observation

Romeo's official Telegram channel index (`@officialRomeotpt`) exposes the following first-party statement:

> Tuesdays and Wednesdays are my favourite days of the week.

The timestamp link associated with that statement resolves to the exact post identity:

- `https://t.me/officialRomeotpt/6519`

The statement is therefore attributable to Romeo's official first-party channel and the exact post ID is known.

## Retrieval boundary

The official channel/index page was directly observable during the bounded recovery pass, including the statement and its timestamp link. The direct single-post endpoint itself could not be fetched reproducibly by the available research fetcher (`cache miss`).

Consequently this record is deliberately **not** added to the replayable Phase-6D payload/acquisition-manifest/corpus-index chain. It preserves the exact first-party locator for a future direct-payload retry without pretending that a replayable payload was captured.

## Predicate relevance

Potential held predicate: `TIME_SELECTOR`.

What the statement directly establishes:

- Romeo expressed a preference for Tuesdays and Wednesdays in the surrounding trading-channel context.

What it does **not** establish:

- that Tuesday or Wednesday is a mandatory CRT eligibility condition;
- that other weekdays are invalid or excluded;
- a timezone or DST anchor;
- market, instrument, session or key-time scope;
- timeframe ownership;
- hard-filter versus contextual-weighting semantics;
- entry/confirmation semantics;
- invalidation;
- expiry;
- any deterministic state transition.

Preference language is not converted into a machine-executable weekday selector.

## TIME_SELECTOR missing fields after this discovery

```text
EXACT_PREDICATE               MISSING — preference is not an eligibility rule
INFORMATION_AVAILABILITY_TIME MISSING — no deterministic lifecycle semantics
DIRECTION_TIMEFRAME_OWNERSHIP MISSING — no owning market/timeframe defined
CONFIRMATION                  MISSING
INVALIDATION                  MISSING
EXPIRY                        MISSING
DATA_REQUIREMENTS             PARTIAL elsewhere; timezone/DST/scope unresolved
```

No existing `CLOSING` field is created or upgraded by this locator discovery.

## Governance disposition

```text
FIRST_PARTY_PROVENANCE        OBSERVED
EXACT_POST_ID                 6519
REPLAYABLE_PAYLOAD_CAPTURED   false
CORPUS_ADMISSION              false
PREDICATE_CLOSURE_CREDIT      false
CANDIDATE_READY               false
ISSUE_16_RECOMMENDATION       KEEP_BLOCKED
```

No candidate creation, detector/count work, backtest/P&L, OOS/CONFIRM access, paper execution, shadow trading or live trading is authorized by this artifact.
