# P0 Unresolved First-Party Leads

**Status:** SEARCH LEADS ONLY / NON-EXECUTABLE  
**Date:** 2026-08-12

## Purpose

Preserve first-party Romeo statements that appear highly relevant to unresolved P0 rules but whose notation, timezone, attached image, or exact strategy meaning is not currently recoverable enough to implement safely.

These leads must not be decoded by intuition or by copying secondary-community interpretations.

## LEAD-001 — asset-class numeric notation

Romeo official Telegram posts:

```text
Forex: 159159
Index futures: 26102610
Crypto: 12481248
```

followed by `Little telegramie for you, keen learner.`

### Why it may matter

The notation appears in the period immediately surrounding Candle Anatomy / Key Level material and may encode time/candle sequencing, asset-class scheduling, or another CRT relationship.

### What is known

- first-party Romeo text;
- explicit distinction among Forex, index futures, and crypto;
- attached image exists on Telegram but is not currently retrievable through the research interface.

### What is unknown

- separators/grouping;
- whether values are clock hours, timeframe ratios, candle numbers, session codes, or something else;
- timezone;
- relationship to H4 anchors;
- whether the notation applies to CRT-v0.1 at all.

### Critical rule

Do **not** transform this into guessed schedules such as:

```text
Forex H4 = 1/5/9/...
Index H4 = 2/6/10/...
Crypto = 1/2/4/8/...
```

without an explicit Romeo explanation or directly inspectable source image that proves the decoding.

**P0 impact:** possible P0-03/P0-02 lead only; zero closure credit.

---

## LEAD-002 — synchronization-time list

Romeo official Telegram posts:

```text
00:00
03:00
08:15
09:30
13:30
```

and says that if a move is missed, traders can use these times to `get in sync`, without rushing/FOMO.

### Unknowns

- timezone;
- market/instrument scope;
- whether these are macro windows, sessions, entry windows, key times, review times, or another timing taxonomy;
- whether daylight-saving adjustment is implied;
- relationship to parent candle construction.

### Critical rule

These values are **not H4 anchors unless Romeo explicitly says so**.

**P0 impact:** possible P0-02 time-context/P0-03 calendar lead only.

---

## LEAD-003 — inaccessible Telegram chart media

Several first-party Telegram posts contain chart images that are linked by the public Telegram HTML, but the image CDN currently returns a cache/network failure in the research environment.

Examples include media adjacent to:
- key-level expectation/outcome posts;
- asset-class numeric notation;
- synchronization-time posts;
- NQ old-CRTH clarification.

### Research policy

A hidden/unretrievable image cannot be treated as though its visual contents are known.

Do not infer:
- instrument labels;
- timeframe labels;
- chart timezone;
- exact marked levels;
- candle boundaries;
- entry/stop/target annotations.

Once images become directly inspectable, promote them into immutable source/fixture records with timestamps and hashes where possible.

---

## LEAD-004 — exact H4 anchors still absent from explicit Romeo text

Targeted searches of Romeo's official Telegram have not yet surfaced an explicit text statement listing canonical H4 open times.

Secondary CRT communities frequently publish H4 schedules, but those are not accepted as Romeo-primary evidence.

**Disposition:** P0-03 remains open.

## Research consequence

These leads are intentionally stored instead of discarded because they may later unlock P0 closure when:
- attached first-party chart media becomes accessible;
- Romeo explains the notation elsewhere;
- a direct transcript/video frame provides the missing semantics.

Until then:

```text
UNRESOLVED_FIRST_PARTY_LEAD
    ≠
EXECUTABLE_RULE
```
