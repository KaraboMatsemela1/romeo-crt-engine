# Video Analysis — ROMEO-2025-S5

## Metadata
- Title: CRT secrets ep.5: Key level
- URL: https://www.youtube.com/watch?v=p8UYOgVn1-g
- Published: 2025-08-17
- Duration: 17:59
- Creator: Romeo / @Romeotpt
- Analyst/date: ChatGPT / 2026-08-12
- Evidence pass: 1

## Evidence quality

Source identity, title, publication date and duration are corroborated by Glasp and Video Highlight. Romeo's official Telegram independently references CRT Secrets episode 5 and directly states that one can trade either the journey **to** a key level or the reaction **from** a key level.

Timestamped semantics below use indexed transcript/summary material because a first-party YouTube transcript was not directly accessible in the current environment. All rules therefore remain `PROVISIONAL` pending direct video/audio verification.

## Relevance
- CRT relevance: critical
- Main role: context and location filter
- Primary concepts: key level, higher-timeframe context, lower-timeframe behavior, journey-to-level vs reaction-from-level, fake bottom/top, KOD, true MSS, time + price
- Main engineering value: separates **location/context** from **entry pattern**, reducing pattern-first false positives

## Source-backed observations

| ID | Timestamp | Observation | Confidence |
|---|---:|---|---|
| KL-O01 | 04:49 | Romeo says key levels may be based on price or time and treats them as essential to successful trading. | High |
| KL-O02 | 06:01 | The problem space includes how to mark key levels, what types exist, how price reacts there, when they are reached, and what LTF behavior appears there. | High |
| KL-O03 | 08:36 | A key level is described as a price point where a bounce/reaction is expected; examples include counter-trend reactions and significant highs/lows. | High |
| KL-O04 | 11:05 | Two central questions are how LTF price behaves at HTF key levels and what trade opportunities exist at those levels. | High |
| KL-O05 | 12:13–13:47 | Price may form convincing reversal patterns/fake bottoms before the true key level is reached; Romeo warns against buying the apparent pattern prematurely. | High |
| KL-O06 | 13:47 | A KOD/Turtle-Soup-type event is described as part of the fake-bottom behavior before the later expansion from the true key level. | Medium-High |
| KL-O07 | 14:26 | Fake market-structure shifts can occur before/around key levels, so not every MSS-like event is valid confirmation. | High |
| KL-O08 | 15:06 | Two valid trade styles are explicitly separated: trade the journey **to** the key level, or trade the reaction **from** the key level. Romeo's Telegram later states both are valid. | High |
| KL-O09 | 15:51 | A `true` market-structure shift is associated with the actual key-level reaction; the indexed transcript describes a low-high-lower-low sequence followed by forceful break above the relevant high in the bullish example. | Medium-High |
| KL-O10 | transcript-level | Romeo links the true MSS to the key level **and the correct time**. Exact clock/session rules are not specified here. | High |
| KL-O11 | transcript-level | The episode mentions SMT alongside the true MSS example, but does not establish from this source alone whether SMT is mandatory. | Medium-High |
| KL-O12 | official Telegram | Romeo explicitly states: one can trade the journey of price to the key level or the reaction from the key level. | High / first-party |

## Core interpretation

Episode 5 turns `key_level` into a **context predicate** rather than an entry trigger.

The emerging architecture is:

```text
W1 → D1 → H4 CONTEXT / SELECTED PARENT CANDLE
                  ↓
          KEY LEVEL SELECTED
                  ↓
        TWO DISTINCT OPPORTUNITIES
          ┌───────┴────────┐
          ↓                ↓
 JOURNEY-TO-LEVEL     REACTION-FROM-LEVEL
          │                │
    path/target logic   wait for level hit
          │                ↓
          │          reject fake LTF setups
          │                ↓
          │          true confirmation at level
          │                ↓
          └──────────→ ENTRY MODEL
                           ↓
                       RISK ENGINE
```

This strongly argues against a system that simply scans for Turtle Soup / MSS / Model #1 everywhere on the chart.

## Important distinction: destination vs origin

A key level can play at least two different roles:

1. **Destination key level** — price is moving *toward* it; the journey itself may be tradable.
2. **Reaction key level** — price reaches it and the level becomes the context for a reversal/expansion trade.

These must be separate strategy states because their direction, target logic and confirmation requirements differ.

## Candidate rules created

### KL-P001 — key level is context, not entry
- Status: PROVISIONAL
- Category: context
- Human description: A key level defines meaningful location/time context; the system still needs lower-timeframe confirmation or journey logic to trade it.
- Evidence: KL-O01, KL-O04, KL-O05
- Engineering implication: `KeyLevelDetector` must not emit executable orders directly.

### KL-P002 — key levels can be price-based or time-based
- Status: PROVISIONAL
- Category: context/time
- Human description: Romeo explicitly distinguishes key levels based on price and time.
- Evidence: KL-O01, KL-O02
- Blocker: exact taxonomy/calculation for both types is unresolved.

### KL-P003 — HTF key level governs LTF interpretation
- Status: PROVISIONAL
- Category: timeframe hierarchy
- Human description: Lower-timeframe patterns/entries are interpreted relative to a higher-timeframe key level.
- Evidence: KL-O04, KL-O05
- Engineering implication: every LTF signal candidate should retain `distance_to_key_level`, `key_level_id`, and `key_level_timeframe` where applicable.

### KL-P004 — pre-level reversal patterns may be traps
- Status: PROVISIONAL
- Category: invalidation/filter
- Human description: Convincing LTF reversal patterns can form before price reaches the actual key level and should not automatically be treated as the real reversal.
- Evidence: KL-O05, KL-O07
- Engineering implication: add a `level_reached`/`location_valid` gate before qualifying reaction trades.

### KL-P005 — journey-to-level and reaction-from-level are separate setup families
- Status: PROVISIONAL
- Category: setup taxonomy
- Human description: Romeo explicitly permits trading the move into a key level and the move away from a key level as two distinct opportunities.
- Evidence: KL-O08, KL-O12
- Engineering implication: implement separate research labels/state machines, not one bidirectional generic `key_level_trade`.

### KL-P006 — true MSS must be contextualized at the level
- Status: PROVISIONAL
- Category: confirmation
- Human description: A valid/true MSS is associated with the actual key-level interaction, while MSS-like patterns before the key level may be fake.
- Evidence: KL-O05, KL-O07, KL-O09
- Blocker: exact deterministic true-MSS predicate remains unresolved.

### KL-P007 — correct time participates in true reaction qualification
- Status: PROVISIONAL
- Category: time
- Human description: Romeo links the real market-structure shift to the key level and the correct time.
- Evidence: KL-O10
- Engineering implication: location alone is insufficient; eventual `KeyLevelReaction` state must include a timing gate.
- Blocker: exact time windows are unresolved.

### KL-P008 — KOD may appear as a pre-level trap
- Status: PROVISIONAL
- Category: KOD/context
- Human description: The episode associates KOD/Turtle-Soup behavior with a false bottom/top before the eventual key-level reaction.
- Evidence: KL-O05, KL-O06
- Research consequence: `KOD` may have more than one functional role across the corpus; do not assume every KOD is the final same-direction continuation setup described in Episode 2 without reconciling context.

### KL-P009 — SMT is associated with high-quality confirmation but role unresolved
- Status: PROVISIONAL
- Category: confluence
- Human description: SMT appears alongside the true-MSS example at the key level.
- Evidence: KL-O11
- Blocker: Episode 6 must determine whether SMT is required, optional, directional, or a failure filter.

## Critical cross-source tension: KOD semantics

Episode 2 describes KOD as the **final Turtle Soup before the target is reached**.

Episode 5's bullish key-level narrative places a KOD/Turtle-Soup-like fake bottom **before** the real low/key-level reaction.

These may be fully compatible if the episodes are speaking about different parent journeys or nesting levels. For example:

```text
HTF journey toward key level
    └── LTF KOD / fake reversal event before destination

then

HTF key level reached
    └── new reaction journey begins
```

But this MUST be reconciled. The engine cannot currently define one global `KOD` predicate.

Recommended research representation:

```text
KODEvent
├── parent_crt_id
├── parent_journey_direction
├── role
│   ├── CONTINUATION_KOD
│   └── PRE_KEY_LEVEL_TRAP   # provisional taxonomy
├── key_level_id
├── timestamp
└── evidence
```

Do not code the role taxonomy into production until later sources confirm whether these are genuinely distinct variants.

## Key-level state model candidate

```text
KEY_LEVEL_DISCOVERED
        ↓
CLASSIFY_ROLE
  ├── DESTINATION
  └── REACTION_ORIGIN
        ↓
TRACK_DISTANCE / TIME
        ↓
IF DESTINATION:
    evaluate journey-to-level opportunities

IF REACTION_ORIGIN:
    reject premature pattern signals
    wait for level interaction
    wait for time qualification
    wait for true confirmation
        ↓
ENTRY_CANDIDATE
```

## Data model implications

```text
KeyLevel
├── id
├── source_timeframe
├── level_type           # price/time taxonomy unresolved
├── price                # nullable for pure time level
├── time_window          # nullable until time rules resolved
├── direction_context    # unresolved
├── role                 # destination / reaction-origin / unresolved
├── created_at
├── valid_from
├── invalidated_at
└── evidence

SignalContext
├── parent_crt_id
├── key_level_id
├── distance_to_key_level
├── level_reached
├── time_qualified
├── ltf_event
└── information_available_at
```

## What this source does NOT yet establish

Do not guess:

- complete list of Romeo key-level types
- exact algorithm for marking a key level
- whether old highs/lows alone are always key levels
- whether FVG/OB/OTE are accepted key levels in this CRT version
- exact ranking when multiple HTF levels overlap
- exact W1 → D1 → H4 level-propagation hierarchy
- precise distance threshold for `at the key level`
- whether touching, wicking through, or closing through the level counts as reached
- exact time-window rule associated with each level
- deterministic true-MSS definition
- whether SMT is mandatory
- whether KOD in this episode is the same subtype as Episode 2's KOD
- exact entry/stop/target for either key-level setup family

## New research questions

1. What exact structures are valid price key levels in Romeo's system?
2. What are valid time key levels?
3. How are overlapping W1/D1/H4 key levels ranked?
4. What does `at the key level` mean numerically?
5. What event marks a key level as reached/consumed/invalidated?
6. Can a key level change role from destination to reaction origin after being reached?
7. What separates a fake MSS before the level from the true MSS at the level?
8. Is the true MSS valid only when price reaches the level at a specific time?
9. How does SMT interact with key-level confirmation?
10. Is Episode 5's KOD a nested/pre-level KOD variant distinct from Episode 2's continuation KOD?
11. For a journey-to-level trade, what provides entry and what is the exact target endpoint?
12. Which higher timeframe owns the key level when W1/D1/H4 levels conflict?

## Architecture consequence

Episode 5 materially changes the detector ordering. The engine should eventually evaluate:

```text
1. WHAT PARENT CANDLE / JOURNEY ARE WE TRADING?
2. WHERE IS THE RELEVANT KEY LEVEL?
3. IS PRICE TRAVELING TO IT OR REACTING FROM IT?
4. HAS THE REQUIRED LOCATION/TIME STATE OCCURRED?
5. WHAT LTF EVENT IS PRESENT?
6. IS IT TRUE CONFIRMATION OR A PREMATURE/FAKE PATTERN?
7. ONLY THEN: ENTRY + RISK
```

This ordering should prevent a large class of pattern-first false positives.

## Next source

`ROMEO-2025-S6 — CRT secrets ep.6: SMT` is the next evidence target because Episode 5 explicitly introduces SMT alongside the true key-level market-structure shift. Episode 6 should help determine whether SMT is a required confirmation, optional confluence, asset-selection mechanism, or failure filter.

## Promotion decision

**No KL-Pxxx rule is promoted to VERIFIED.**

However, `journey-to-key-level` versus `reaction-from-key-level` is now a strong source-backed setup taxonomy and should be preserved as separate research labels.
