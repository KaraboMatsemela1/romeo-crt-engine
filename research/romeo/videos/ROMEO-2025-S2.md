# Video Analysis — ROMEO-2025-S2

## Metadata
- Title: CRT secrets episode 2: The kiss of death
- URL: https://www.youtube.com/watch?v=FYr6J5pIDB4
- Published: 2025-07-31
- Duration: 21:56 (registry metadata; transcript ends ~21:49)
- Creator: Romeo / @Romeotpt
- Analyst/date: ChatGPT / 2026-08-12
- Evidence pass: 1

## Evidence quality

Romeo's official Telegram directly posted and pinned the exact YouTube video ID and described it as CRT Secrets episode 2. The same Telegram post also attached a `KOD.pdf`, establishing strong first-party provenance for the source identity.

The timestamped semantic extraction below uses an indexed transcript (Lilys.ai) because a first-party YouTube transcript was not directly accessible in the research environment. Therefore semantic rules remain `PROVISIONAL` until checked against the original video/audio or an authoritative transcript.

## Relevance
- CRT relevance: critical
- Setup variant: Kiss of Death (KOD) Turtle Soup
- Relationship to prior work: refinement of Turtle Soup within a CRT range
- Main engineering value: begins linking higher-timeframe range selection, targets, Turtle Soup, confluence, lower-timeframe Model #1 entry, and risk framing

## Source-backed observations

| ID | Timestamp | Observation | Confidence |
|---|---:|---|---|
| KOD-O01 | 01:49 | Romeo explicitly names the setup the `Kiss of Death Turtle Soup` and ranks it highly in his system. | High |
| KOD-O02 | 02:25–02:38 | Analysis begins from a specific candle; Romeo says the method trades candles rather than generic zones and says weekly/daily candles are a common focus. | High |
| KOD-O03 | 03:39 | Candle 1 / Candle 2 / Candle 3 are mapped to accumulation / manipulation / distribution. | High |
| KOD-O04 | 03:45 | The range of Candle 1 is selected; price Turtle Soups that range and then attacks the opposite side (bearish example: the low). | High |
| KOD-O05 | 04:02–04:37 | CRT is framed as a range-based way of reading price, not a visual pattern to trade blindly. | High |
| KOD-O06 | 05:45–06:10 | A daily CRT range is shown and then examined on the 1-hour; Romeo mentions multiple HTF/LTF combinations, but the exact canonical mapping is not fully clear from this transcript alone. | Medium-High |
| KOD-O07 | 06:12 | KOD is defined as the final Turtle Soup before the target is hit. | High |
| KOD-O08 | 06:42 | In the bearish example, CRT low is Target 2 and the 50% level is Target 1. | High |
| KOD-O09 | 06:42 | KOD is characterized as often producing a fast move into the target. | Medium-High |
| KOD-O10 | 07:29–09:06 | Romeo emphasizes the liquidity/failure logic more than the visual pattern; he distinguishes false breakouts/Turtle Soup from true breakouts. | High |
| KOD-O11 | 10:49–11:11 | Price breaks lower toward 50% and a reaction/bounce around 50% is described as usual in the example. | Medium-High |
| KOD-O12 | 14:27–14:41 | The bearish sequence is described as push higher/Turtle Soup → move to 50% → bounce → another push higher → final dump to the prior CRT low. | High |
| KOD-O13 | 17:39–17:57 | FVG above an old high (bearish) or below an old low (bullish) is presented as useful confluence, not as a standalone setup. | High |
| KOD-O14 | 18:08 | The lower-timeframe entry model for the KOD example is Model #1. | High |
| KOD-O15 | 18:44 | Risk is placed on the adverse side and reward toward the downside target in the bearish example; exact stop algorithm is not specified. | Medium |
| KOD-O16 | 19:07 | Romeo says he likes KOD in the lower 25% of the range, but also says it can occur as an OTE. Transcript wording is ambiguous and must be visually/directly verified before use. | Low-Medium |
| KOD-O17 | 19:44 | The bullish KOD is left as a reverse-engineering/backtesting exercise, implying structural symmetry but not giving a full explicit bullish rule set here. | Medium-High |
| KOD-O18 | 20:47–21:26 | Romeo recaps KOD in relation to CRT high/low and describes analysis as higher-timeframe candle shape plus lower-timeframe internal behaviour. | High |

## What KOD adds to the Turtle Soup primitive

The 2024 Turtle Soup lecture gave us the structural primitive:

```text
REFERENCE EXTREME
    ↓
EXCURSION / SWEEP
    ↓
FAILED CONTINUATION
    ↓
REVERSAL
```

Episode 2 adds a larger CRT journey around that primitive:

```text
HTF CANDLE-1 RANGE SELECTED
          ↓
CRT DIRECTION / OPPOSITE-SIDE TARGET EXISTS
          ↓
PRICE PROGRESSES THROUGH THE RANGE
          ↓
A LATE TURTLE-SOUP EVENT OCCURS
          ↓
OPTIONAL CONFLUENCE (e.g. FVG + OLD EXTREME)
          ↓
LTF MODEL #1 ENTRY CANDIDATE
          ↓
RISK CHECK
          ↓
TARGET 1: 50% (context-dependent)
TARGET 2: OPPOSITE CRT EXTREME
```

This is still a research abstraction, not production logic.

## Critical look-ahead-bias problem

Romeo's definition at 06:12 is semantically clear but algorithmically dangerous:

> KOD = the **final** Turtle Soup before the target is hit.

In historical data, it is trivial to label the last Turtle Soup before a target *after the fact*. In live trading, the system cannot know a Turtle Soup is the `final` one unless some real-time qualifying conditions distinguish it from earlier Turtle Soups.

Therefore the engine MUST NOT implement:

```python
kod = last_turtle_soup_before_target
```

because that directly leaks future knowledge into the signal.

The research task is to discover an ex-ante predicate such as:

```text
KOD_CANDIDATE =
    valid_crt_context
    AND target_pending
    AND qualifying_location
    AND qualifying_turtle_soup
    AND required_confluence
    AND valid_ltf_confirmation
```

The exact predicate is unresolved. Later episodes on `The Journey`, `Candle Anatomy`, `Key Level`, `SMT`, `Candle 3`, and `When does CRT fail?` are expected to supply missing context.

## Candidate rules created

### KOD-P001 — KOD is a Turtle Soup subtype
- Status: PROVISIONAL
- Category: taxonomy
- Human description: A Kiss of Death is not independent of Turtle Soup; it is a specialized Turtle Soup event within an active CRT journey.
- Evidence: KOD-O01, KOD-O07
- Deterministic status: taxonomy usable; executable predicate unresolved.

### KOD-P002 — Candle 1 defines the parent CRT range
- Status: PROVISIONAL
- Category: range
- Human description: The high/low of the selected Candle 1 define the parent range used to reason about the KOD journey.
- Evidence: KOD-O03, KOD-O04
- Blocker: exact Candle-1 selection rules remain unresolved.

### KOD-P003 — opposite-side CRT objective exists
- Status: PROVISIONAL
- Category: target/context
- Human description: In the bearish example, price Turtle Soups the high side and ultimately targets the CRT low; bullish is expected to mirror this but needs direct confirmation.
- Evidence: KOD-O04, KOD-O08, KOD-O12, KOD-O17
- Blocker: direction/context selector unresolved.

### KOD-P004 — 50% can be an intermediate objective
- Status: PROVISIONAL
- Category: target/management
- Human description: The 50% midpoint of the parent CRT range is presented as Target 1 in the bearish KOD example, with the opposite CRT extreme as Target 2.
- Evidence: KOD-O08, KOD-O11, KOD-O12
- Blocker: determine whether 50% is mandatory, optional, or setup-dependent across the corpus.

### KOD-P005 — KOD is late in an already-active CRT journey
- Status: PROVISIONAL
- Category: sequencing
- Human description: KOD is described as the final Turtle Soup before the active CRT's target is reached, so it cannot be classified without an already-defined parent CRT and pending objective.
- Evidence: KOD-O07, KOD-O12
- Blocker: requires ex-ante definition that avoids future leakage.

### KOD-P006 — pattern alone is insufficient
- Status: PROVISIONAL
- Category: context
- Human description: A visually similar sweep/reversal is not enough; the logic of the range, target and surrounding context must qualify it.
- Evidence: KOD-O05, KOD-O10
- Engineering implication: no image-pattern-only KOD classifier.

### KOD-P007 — FVG/old-extreme alignment is confluence
- Status: PROVISIONAL
- Category: confluence
- Human description: An FVG above an old high for bearish KOD, or below an old low for bullish KOD, is described as useful confluence.
- Evidence: KOD-O13
- Blocker: determine whether this is required, preferred, or merely optional.

### KOD-P008 — LTF Model #1 is an entry model
- Status: PROVISIONAL
- Category: entry
- Human description: Once KOD context exists, Model #1 on a lower timeframe is used as an entry model in the demonstrated setup.
- Evidence: KOD-O14
- Engineering implication: KOD detection and entry detection should be separate modules.

### KOD-P009 — HTF context and LTF execution are distinct
- Status: PROVISIONAL
- Category: timeframe architecture
- Human description: Parent CRT/KOD context is read from a higher timeframe and lower-timeframe structure is used for execution.
- Evidence: KOD-O02, KOD-O06, KOD-O14, KOD-O18
- Blocker: exact timeframe-mapping table still needs direct verification.

### KOD-P010 — KOD location may matter
- Status: UNRESOLVED / LOW CONFIDENCE
- Category: range location
- Human description: Romeo appears to state a preference for KOD in the lower 25% of the range, while allowing an OTE alternative.
- Evidence: KOD-O16
- Blocker: transcript wording/location appears counterintuitive for the bearish example and MUST be checked visually/directly before any implementation.

## Candidate bearish state machine

```text
WAIT_FOR_PARENT_CRT
        ↓
CANDLE_1_RANGE_SELECTED
        ↓
BEARISH_CRT_OBJECTIVE_PENDING
        ↓
PRICE_PROGRESSING_TOWARD_LOW
        ↓
WAIT_FOR_KOD_CONTEXT
        ↓
QUALIFYING_UPSIDE_TURTLE_SOUP
        ↓
OPTIONAL_CONFLUENCE_CHECK
        ↓
WAIT_FOR_LTF_MODEL_1
        ↓
ENTRY_CANDIDATE
        ↓
RISK_ENGINE
        ↓
T1 / T2 MANAGEMENT
```

Every transition containing `QUALIFYING`, `OBJECTIVE`, or `MODEL_1` remains blocked until later evidence resolves its deterministic definition.

## Explicit non-rules / causal claims

Romeo describes market makers as intentionally creating liquidity pools and trapping participants. Those are causal interpretations. The trading engine does not need to assume or prove actor intent.

We will model observable quantities only:

- candle/range geometry
- old highs/lows
- excursions
- closes
- target location
- timeframe relationships
- FVG geometry if retained
- subsequent price movement

This preserves testability.

## What this source does NOT yet establish

Do not guess:

- exact deterministic Candle-1 selector
- exact meaning of a `pending CRT`
- objective rule that chooses bullish vs bearish CRT
- whether the first Turtle Soup must occur at the parent CRT high/low
- exact conditions that make a Turtle Soup the KOD in real time
- whether 50% is always Target 1
- whether FVG confluence is required
- exact lower-timeframe mapping for each HTF
- Model #1 deterministic definition (tracked separately)
- exact stop placement
- exact entry price
- exact risk/reward requirement
- exact `lower 25%` / OTE location rule
- exact time/session filters
- exact bullish KOD mirror rules

## Questions created for later episodes

1. What observable, real-time property distinguishes the `final` Turtle Soup from prior Turtle Soups?
2. What makes a parent CRT `pending`?
3. How do we select Candle 1 without hindsight?
4. What determines the intended opposite-side CRT target?
5. Is the 50% objective mandatory, and what changes after price has already reached 50%?
6. Is FVG + old-high/old-low alignment required or optional?
7. Is Model #1 mandatory for KOD execution or just the example entry model?
8. What is the exact HTF→LTF alignment?
9. What did `lower 25%` mean in the visual example, and is that rule directional?
10. What invalidates a KOD candidate before entry?

## Links to later evidence

- ROMEO-2025-S3 — `The Journey`: expected to clarify sequence and target progression.
- ROMEO-2025-S4 — `Candle Anatomy`: expected to clarify candle/timeframe semantics.
- ROMEO-2025-S5 — `Key Level`: expected to clarify where Turtle Soup/KOD is allowed to form.
- ROMEO-2025-S6 — `SMT`: expected to clarify confirmation/confluence.
- ROMEO-2025-S7 — `Candle 3`: expected to clarify distribution phase.
- ROMEO-2025-S8 — `When does CRT fail?`: expected to clarify 50%, direction and invalidation.
- ROMEO-2025-S9 — `Connecting the dots`: expected to reconcile full execution.

## Promotion decision

**No KOD-Pxxx rule is promoted to `VERIFIED`.**

However, the modular architecture is becoming clearer:

```text
PARENT CRT CONTEXT
      ↓
TURTLE SOUP / KOD CONTEXT
      ↓
CONFLUENCE
      ↓
LTF ENTRY MODEL
      ↓
INDEPENDENT RISK
      ↓
TARGET MANAGEMENT
```

The most important blocker is now the ex-ante KOD classifier needed to prevent look-ahead bias.
