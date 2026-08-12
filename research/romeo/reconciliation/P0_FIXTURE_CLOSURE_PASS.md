# P0 Closure / Fixture Pass

**Candidate:** `CRT-C3-ALIGNED-v0.1-DRAFT`  
**Doctrine snapshot:** `CRT_SECRETS_2025`  
**Status:** STARTED / NO P0 CLOSED YET  
**Date:** 2026-08-12

## Purpose

Close the five partially resolved P0 blockers with **direct, chart-grounded, causal fixtures**, not with backtest optimization or generic CRT community conventions.

The current P0 contracts are structurally defined, but each still lacks one or more source-specific predicates:

- P0-01 Parent CRT / Candle-1 selector
- P0-02 KeyLevelSelector / ranking
- P0-03 H4/D1/W1 candle construction
- P0-04 Turtle Soup confirmation/reference lifecycle
- P0-05 Context direction resolver

## Primary fixture sources

### Source A — ROMEO-2025-LIVE
`CRT live tape-reading session`

- YouTube ID: `1EK-LMwgJ3c`
- official Romeo Telegram direct post + pin
- independently indexed metadata: 2025-07-01 / 43:42
- first-party follow-up says the move was outlined live beforehand

Priority: **highest** because it can support ex-ante information-set reconstruction.

### Source B — ROMEO-2026-LIVE-02
`CRT live tape-reading session (2)`

- YouTube ID: `Pmmx41M7KhA`
- official Romeo Telegram direct post + pin
- exact publication date/duration to verify

Priority: high for **cross-session stability testing** after Source A fixtures are extracted.

### Source C — original Episode examples
Use only where the chart/frame makes the decision state visible before outcome:
- 2024 CRT foundation
- Episode 4 Candle Anatomy
- Episode 5 Key Level
- Episode 7 Candle 3
- Episode 8 Failure
- Episode 9 Connecting the dots

## Fixture-evidence hierarchy

1. **First-party real-time/live declaration with timestamped chart**
2. First-party video chart example where pre-event state is visible
3. First-party Telegram/X chart posted before outcome
4. Indexed transcript/summary supporting interpretation
5. Community derivative material — **lead generation only; never rule closure**

No P0 blocker may be closed from level 5 evidence.

## Current closure matrix

| Blocker | Resolved contract | Exact missing predicate | Fixture target | Current status |
|---|---|---|---|---|
| P0-03 | NY wall-clock model; D1 midnight NY; W1 Sunday 17:00 NY | exact H4 anchors + venue policy | visible H4 timestamps in live charts across >=2 instruments/sessions | OPEN |
| P0-01 | parent selected before LTF patterns; immutable closed range; ambiguity fails closed | Candle-1 eligibility + nesting/ownership/expiry | predeclared parent with competing candles visible | OPEN |
| P0-02 | key level before LTF; destination vs reaction roles; pre-level patterns rejected | exact type registry + ranking + reach/consumption | level marked before touch plus negative fake level examples | OPEN |
| P0-05 | HTF direction precedes SMT/entry; aligned-only v0.1; unknown fails closed | owning timeframe + exact close/wick rule + conflict resolver | direction declared before move with HTF chart visible | OPEN |
| P0-04 | prior extreme + strict excursion + failed continuation; sweep != trade | eligible reference + exact confirmation + timeout + consumption | accepted vs rejected sweeps in same contextual framework | OPEN |

## Important lead that is NOT promoted

Secondary CRT communities commonly use specific four-hour anchor sets, including references to 9PM/1AM/5AM CRTs. These may help identify timestamps to inspect in Romeo's charts, but they are **not Romeo-primary evidence** and are therefore recorded only as a search lead.

The project must not close P0-03 by copying community schedules.

## Fixture annotation protocol

For every candidate frame/example, capture:

```text
FIXTURE ID
SOURCE / VIDEO ID
SOURCE TIMESTAMP
INSTRUMENT
CHART TIMEZONE (if visible)
OBSERVATION TIME t
DATA KNOWN AT t
PARENT CANDIDATES VISIBLE AT t
SELECTED PARENT + REASON GIVEN
KEY-LEVEL CANDIDATES VISIBLE AT t
SELECTED KEY LEVEL + ROLE
DIRECTION STATE + EVIDENCE
REFERENCE EXTREME
EXCURSION STATE
CONFIRMATION STATE
EXPECTED ENGINE DECISION AT t
OUTCOME (AUDIT ONLY)
CONFIDENCE
OPEN QUESTIONS
```

## Causal replay rule

The reviewer must be able to stop the source at timestamp `t` and independently reconstruct the engine state without seeing later frames.

A fixture is rejected if it requires statements such as:

```text
"this must have been Candle 1 because Candle 3 later expanded"
"this was the key level because price later reversed there"
"this was bearish because the week eventually closed down"
"this sweep was Turtle Soup because the target later hit"
```

## Minimum closure set

Each P0 blocker needs at minimum:

- 5 positive fixtures
- 5 negative/counterexample fixtures
- at least 2 instruments where applicable
- at least 2 distinct dates/sessions
- no contradictions left unexplained
- deterministic acceptance criteria written before any backtest

P0-03 additionally requires DST/provider tests once exact anchors are evidenced.

## Current findings from source registration

### FP-001 — live-session source identity
**Status:** VERIFIED source identity

Romeo's official public channel directly posted and pinned `1EK-LMwgJ3c` as `CRT live tape-reading session`.

### FP-002 — ex-ante fixture quality
**Status:** HIGH CONFIDENCE

Romeo's official follow-up says the move was outlined live beforehand in the prior video. This supports using the source to test causal preselection rather than only retrospective annotation.

### FP-003 — second independent live stream exists
**Status:** VERIFIED source identity

Romeo later directly posted and pinned `Pmmx41M7KhA` as `CRT live tape-reading session (2)`.

This gives the project a second source to test rule stability and avoid fitting P0 semantics to a single example set.

## What this pass does NOT claim

No live-session rule has been extracted merely from the existence/title of the video.

Specifically, this pass does **not** claim:
- any exact H4 anchor;
- any exact parent selector;
- any exact key-level type;
- any exact direction formula;
- any exact Turtle Soup close-back rule.

Those require direct frame/transcript evidence.

## Next extraction order

1. **ROMEO-2025-LIVE: H4/calendar frames** — attempt P0-03 first.
2. Same source: predeclared parent/key level/direction snapshot.
3. Same source: accepted and rejected Turtle Soup events.
4. Cross-check identical predicates in `ROMEO-2026-LIVE-02`.
5. Use Episodes 4/5/7/8/9 only to reconcile specific ambiguities revealed by live fixtures.

## Promotion gate

A P0 blocker moves from `PARTIALLY_RESOLVED` to `CLOSED_FOR_V0.1` only when:

```text
source-specific predicate deterministic
AND positive fixtures pass
AND negative fixtures pass
AND no look-ahead required
AND no unresolved contradiction on active path
```

Until then:

```text
P0 UNKNOWN
   ↓
NO VALIDATION / NO EXECUTABLE SIGNAL
```
