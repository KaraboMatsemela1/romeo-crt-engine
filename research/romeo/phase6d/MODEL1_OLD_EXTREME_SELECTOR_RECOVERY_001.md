# Phase 6D — Model #1 Old-Extreme Selector Recovery 001

**Date:** 2026-08-15  
**Tracking:** Issue #91  
**Baseline:** Recovery 007 + `MINIMUM_MISSING_FIELD_CLOSURE_001.md`  
**Mode:** bounded first-party evidence recovery  
**Disposition:** `NO_SELECTOR_RULE_FOUND`

## Decision

The bounded first-party material does **not** define a deterministic rule for selecting the qualifying `old high` / `old low` used by `MODEL_1_GEOMETRY` when more than one prior extreme is available.

A direct first-party Romeo clarification materially narrows one bearish reaction/reference subtype to an **old CRTH**, but it does not establish that Model #1 universally selects an old CRTH, does not define what makes a CRTH `old`, does not rank multiple eligible CRTHs/highs, and does not provide an explicit bullish old-CRTL mirror. Therefore this clarification is `PARTIAL_SELECTOR_CONTEXT`, not a Model #1 selector closure.

```text
MODEL_1_OLD_EXTREME_SELECTOR = NO_SELECTOR_RULE_FOUND
PARTIAL_SELECTOR_CONTEXT     = OLD_CRTH_BEARISH_REFERENCE_SUBTYPE
MODEL_1_EXACT_PREDICATE      = STRONG_PARTIAL
INDEPENDENT_CLOSURE_AUDIT    = NOT_READY
ISSUE_16                     = KEEP_BLOCKED
ISSUE_37                     = MUST_NOT_START
```

No candidate, detector/count, P&L/backtest, OOS/CONFIRM, paper, shadow, live or broker action is authorized by this report.

## Bounded evidence checked

### Recovery 007 — Model #1 direct timed text

`ROMEO-2025-S1` 10:18–10:56 directly supports a sweep into an `old high`, selection of the sweep candle, and a close below that candle as a bearish trigger. The admitted record explicitly leaves the old-high selector undefined.

`ROMEO-2025-S1` 15:05–15:41 directly supports the stated bullish/bearish old-high/old-low symmetry, but the qualifying extreme remains undefined.

`ROMEO-2025-S9` 02:02–02:58 directly supports that Model #1 is anchored to the one specific candle that liquidated the old high rather than an arbitrary multi-candle zone. It still does not algorithmically identify which old high is the relevant target when several prior highs exist.

The Recovery 007 Model #1 evidence therefore establishes the event *after* a qualifying old extreme has been chosen; it does not establish the selector that chooses the extreme.

### Direct first-party bearish reference clarification

Romeo's official Telegram channel, exact post locator:

- `https://t.me/officialRomeotpt/6615`
- official public channel index: `https://t.me/s/officialRomeotpt/6615`

The post states the ideal bearish reaction as a candle opening, then price stabbing into an **old CRTH**, then dumping.

Safe credit:

```text
BEARISH REACTION / TURTLE-SOUP REFERENCE SUBTYPE:
    OLD_CRTH = FIRST_PARTY_SUPPORTED
```

This matches the repository's existing `CLAR-TS-001` / `P0-FIX-002` treatment and narrows the broader `old high` vocabulary for at least one bearish reaction class.

It does **not** safely establish:

- `MODEL_1_OLD_HIGH = OLD_CRTH` universally;
- what makes a CRTH `old` or fresh/eligible;
- which timeframe owns the CRTH;
- how the parent CRT that produced CRTH is selected;
- how to rank several old CRTHs/highs;
- whether a consumed/revisited CRTH remains eligible;
- an explicit bullish `old CRTL` mirror for Model #1;
- expiry or invalidation of the reference.

## Existing corpus reconciliation

The existing first-party clarification record already preserves the dependency:

```text
PARENT CRT SELECTED
    ↓
CRTH / CRTL EXIST
    ↓
OLD CRTH MAY BECOME A BEARISH REACTION REFERENCE
```

That dependency is useful, but it moves the unresolved choice one level upstream: a deterministic Model #1 implementation still needs to know which parent CRT / old extreme owns the setup and how an `old` reference is selected among alternatives.

The older Episode-1 analysis explicitly retained the open question: how are old highs/lows selected when several liquidity levels exist? Recovery 007 did not close that question.

## Search-hypothesis disposition

The bounded corpus search tested whether first-party evidence explicitly bound the Model #1 old extreme to a nearest, protected, structural, session, candle-range, liquidity, key-level, CRTH/CRTL, or other source-defined selector. Those labels were search hypotheses only.

Result:

```text
DIRECT_MODEL1_SELECTOR_RULE_FOUND = false
OLD_CRTH_BEARISH_CONTEXT_FOUND    = true
MODEL1_TO_OLD_CRTH_BINDING_FOUND  = false
MULTIPLE_EXTREME_RANKING_FOUND    = false
OLD_REFERENCE_LIFECYCLE_FOUND     = false
```

No generic ICT/SMC convention is substituted for the missing selector.

## Two-engineer test

Given the same OHLC history containing multiple prior highs, two independent engineers could still choose different `old high` references while remaining consistent with the admitted Romeo wording.

Therefore:

```text
TWO_ENGINEER_TEST = FAIL
```

The Model #1 `EXACT_PREDICATE` cannot advance to `CLOSING` from this bounded pass.

## Exact next first-party question

Do not launch another broad corpus sweep. The unresolved semantic can be asked directly and narrowly:

> For Model #1, when several prior highs or lows exist, which exact level qualifies as the `old high` / `old low`? Is the reference specifically an old CRTH/CRTL from the paired higher-timeframe parent, and if so, what makes that CRTH/CRTL `old`, still eligible, and preferred when more than one exists?

A first-party answer must define selection/ownership sufficiently for two engineers to identify the same level from the same information set. Otherwise this field remains open.

## Next research priority after this bounded route

Because the selector remains unresolved, repeated mining of the same Model #1 passages is not justified. The next independent Model #1 closure debt from `MINIMUM_MISSING_FIELD_CLOSURE_001.md` is the **trigger-versus-retrace execution contract**: determine whether the close beyond the sweep candle is itself executable entry, whether a retrace is required/optional, or whether Romeo teaches distinct versioned execution paths.

That next task must remain evidence-only and must not use outcomes to choose between interpretations.

## Final disposition

```text
RESULT                         = NO_SELECTOR_RULE_FOUND
NEW_CLOSING_FIELD_EVIDENCE     = 0
MODEL_1_GEOMETRY               = STRONG_PARTIAL / KEEP_BLOCKED
INDEPENDENT_CLOSURE_AUDIT      = NOT_READY
ISSUE_16                       = BLOCKED_NO_VERIFIED_PREDICATE_CLOSURE
ISSUE_37                       = MUST_NOT_START
CANDIDATE_CREATION             = NOT_AUTHORIZED
DETECTOR_ACTIVITY              = NOT_AUTHORIZED
BACKTEST_PNL                   = NOT_AUTHORIZED
OOS_CONFIRM                    = UNOPENED
PAPER_EXECUTION                = NOT_AUTHORIZED
```

This report changes research prioritization only. It does not change any project gate.