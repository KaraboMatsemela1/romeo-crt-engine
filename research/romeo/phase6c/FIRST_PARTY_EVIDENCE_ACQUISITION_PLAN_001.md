# Phase 6C — Bounded First-Party Evidence Acquisition Plan 001

**Date:** 2026-08-14  
**Mode:** research-only  
**Outcome surface:** first-party source acquisition only  
**Candidate creation:** prohibited  
**Detector / count / P&L / OOS / CONFIRM:** prohibited

## Objective

Run one bounded, direct-source acquisition pass against the highest-leverage entries in `research/romeo/SOURCE_REGISTRY.csv` that could close a currently held deterministic predicate. Do not use secondary summaries as verification and do not infer missing semantics from generic ICT/SMT/CRT conventions.

## Bound

- Maximum sources: **6**.
- Per source: one direct source availability check plus one first-party channel/index search for the exact missing predicate.
- Secondary sources may not close a predicate.
- If no verified first-party source closes a complete candidate-readiness predicate, stop Phase 6C acquisition, mark Issue #16 `BLOCKED`, and do not create a candidate.

## Acquisition matrix

| Priority | Source ID / URL | Availability | Provenance | Exact unresolved predicate | Bounded next action | Result |
|---:|---|---|---|---|---|---|
| 1 | `ROMEO-2026-CRTOLOGY-01` — https://www.youtube.com/watch?v=4DZWbCzEvhM | Video identity is public; direct technical transcript/captions not capturable through the current public route | First-party Romeo Telegram directly links the exact video and identifies it as `CRTology episode 1: SS` | Explicit meaning of `SS`; exact causal predicate; information-availability time; confirmation/invalidation/expiry | Fetch exact YouTube source; search Romeo's first-party Telegram for `SS`/Episode-1 technical clarification; accept only direct causal language | **NO CLOSURE** — identity/provenance confirmed, technical predicate still unavailable |
| 2 | `ROMEO-2025-S6` — https://www.youtube.com/watch?v=3IWgc52Dqsg | Exact YouTube title/page is publicly identifiable; technical transcript not exposed through the current direct route | Registered first-party source; Romeo Telegram explicitly states SMT can play the role expected from a local Turtle Soup and points back to Episode 6 | Correlated/inverse polarity; corresponding extreme; leg ownership; synchronization; exact SMT-for-TS substitution; confirmation/invalidation/expiry | Fetch exact YouTube page; search Romeo Telegram for direct take/non-take polarity and ownership language | **PARTIAL ONLY / NO CLOSURE** — substitution role reconfirmed; executable semantics still incomplete |
| 3 | `ROMEO-2025-S9` — https://www.youtube.com/watch?v=2sxdsgcIeYA | Video identity public; direct watch route was rate-limited/unavailable for technical transcript capture | Romeo Telegram directly links the exact video and states it answers entry models, correct SMT use, and logical trade framing | Model #1 exact geometry; true-MSS algorithm; SMT ownership interaction; structural stop buffer; time-exit rule | Fetch exact source; search Romeo Telegram for direct entry-geometry / true-MSS / SMT implementation language | **NO CLOSURE** — scope is first-party confirmed, exact deterministic rules not captured |
| 4 | `ROMEO-2024-TS` — https://www.youtube.com/watch?v=U-gNCwbGtTI | Registered source identity; direct technical transcript/video extraction unavailable in this pass | First-party Romeo source in project registry; Romeo Telegram repeatedly identifies Turtle Soup as his core concept and shows qualitative examples | Exact Turtle Soup confirmation event; qualifying old-high/old-low eligibility; confirmation timing; expiry | Fetch exact source; search Romeo Telegram for a direct definition of a `proper Turtle Soup entry` and causal confirmation rule | **NO CLOSURE** — qualitative examples found, no complete confirmation predicate |
| 5 | `ROMEO-2025-S5` — https://www.youtube.com/watch?v=p8UYOgVn1-g | Public registered video identity; existing evidence pass available, direct new technical capture not obtained | Romeo Telegram directly restates Episode-5 doctrine: trade the journey to a key level or the reaction from it | Deterministic key-level selector/hierarchy; price-vs-time ownership; arrival/reaction confirmation; fake-MSS discrimination | Search first-party Romeo posts for exact key-level marking or ranking rule tied to Episode 5 | **NO CLOSURE** — journey/reaction taxonomy reconfirmed; selector remains unresolved |
| 6 | `ROMEO-2026-TG-TIME-TS-6361` — https://t.me/officialRomeotpt/6361 | Direct first-party text is publicly capturable | Romeo official Telegram | Exact time selector: eligible weekday/session/key time, timezone/DST anchor, owning timeframe, hard filter vs context, confirmation timing, expiry | Re-read direct post and adjacent first-party temporal statements; require explicit executable calendar/time predicate | **PARTIAL ONLY / NO CLOSURE** — Time + Turtle Soup core doctrine confirmed; executable temporal selector absent |

## First-party acquisition findings

Direct first-party material obtained or reconfirmed in this pass supports these doctrine facts only:

```text
EPISODE_9_INTENDED_TO_ANSWER_ENTRY_MODEL_AND_SMT_USAGE = true
SMT_CAN_SOMETIMES_FULFILL_EXPECTED_LOCAL_TS_ROLE       = true
TIME_AND_TURTLE_SOUP_ARE_CORE_CRT_COMPONENTS           = true
KEY_LEVEL_HAS_JOURNEY_AND_REACTION_USE_CASES            = true
```

None of those statements, alone or together, closes all candidate-readiness fields for a new deterministic signal path.

## Candidate-readiness check

Required for any Phase 6C executable delta:

```text
DIRECT_FIRST_PARTY_EVIDENCE          = sufficient
EXACT_PREDICATE                      = defined
INFORMATION_AVAILABILITY_TIME        = defined
DIRECTION/TIMEFRAME_OWNERSHIP        = defined
CONFIRMATION/INVALIDATION/EXPIRY     = defined where applicable
POSITIVE_AND_NEGATIVE_FIXTURES       = obtainable without hindsight
DATA_REQUIREMENTS                    = known
NO_OUTCOME_BASED_SELECTION           = true
```

Observed after this bounded acquisition pass:

```text
candidate_ready_rows = 0
verified predicate closures = 0
```

## Decision

```text
PHASE6C_ACQUISITION_RESULT = BLOCKED_NO_VERIFIED_PREDICATE_CLOSURE
NEW_ALPHA_CANDIDATE        = NOT_SELECTED
ALPHA_IMPLEMENTATION       = NOT_AUTHORIZED
DETECTOR_ACTIVITY          = NOT_AUTHORIZED
BACKTEST_PNL               = NOT_AUTHORIZED
V0_1_OOS_CONFIRM           = UNOPENED
PHASE_7                    = BLOCKED
```

## Re-entry condition

Do not resume Phase 6C acquisition until at least one of these becomes directly available:

1. a verified new first-party CRTology episode with technical content;
2. direct captions/transcript/technical frames for Episode 1, Episode 6, Episode 9, or the original Turtle Soup video;
3. a first-party Romeo text/chart post that explicitly defines one held predicate including causal timing/ownership/confirmation semantics.

No scheduled monitoring, detector execution, count access, backtest, P&L, OOS, CONFIRM, parameter tuning, threshold changes, or candidate implementation is authorized by this record.
