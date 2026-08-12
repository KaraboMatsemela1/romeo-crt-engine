# Video Analysis — ROMEO-2024-TS

## Metadata
- Title: What is turtle soup?
- URL: https://www.youtube.com/watch?v=U-gNCwbGtTI
- Published: 2024-03-06
- Duration: 21:28
- Creator: Romeo / @Romeotpt
- Analyst/date: ChatGPT / 2026-08-12
- Evidence pass: 1

## Evidence quality

The source identity and metadata are corroborated by Glasp and Video Highlight. The current research environment could not access a first-party YouTube transcript directly. Timestamped semantics below come from indexed transcript/summary material and therefore remain `PROVISIONAL` until checked against the original video/audio or an authoritative transcript.

## Relevance
- CRT relevance: critical foundation
- Primary concepts: Turtle Soup, old highs/lows, false breakout/breakdown, liquidity, reversal, higher-timeframe context, risk management
- Setup role: foundational price-delivery primitive used throughout later CRT material

## Source-backed observations

| ID | Timestamp | Observation | Confidence |
|---|---:|---|---|
| TS-O01 | 00:00 | Romeo introduces this as the first part of a six-video public Turtle Soup series. | High |
| TS-O02 | 01:17 | The series scope includes what Turtle Soup is, how it is traded, and when it occurs; timing is presented as important. | Medium-High |
| TS-O03 | 06:29 | Turtle Soup is framed as a false breakout/breakdown around prior highs/lows. | High |
| TS-O04 | 11:06 | Bearish case: an old high is the reference liquidity level. | High |
| TS-O05 | 11:43 | Price trades above the old high, triggering short stops and attracting breakout longs before a reversal lower. | High |
| TS-O06 | 13:57 | The characteristic behaviour is described as a stab through an old high/low followed by reversal. | High |
| TS-O07 | 15:18 | Bullish case is the inverse: liquidity exists below an old low and new shorts can be trapped. | High |
| TS-O08 | 15:54 | Price trades below an established low and then reverses higher. | High |
| TS-O09 | 17:37 | Romeo explicitly separates learning the concept, repeatedly observing it, and only then trading it. | High |
| TS-O10 | 20:23 | Market profiles, higher-timeframe price action, entry-model variants, and risk management are stated as necessary surrounding context. | High |

## Candidate semantics

### Turtle Soup — structural definition

A **Turtle Soup event** is provisionally defined as a failed excursion beyond a previously established price extreme that is followed by movement in the opposite direction.

Bearish structural skeleton:

```text
OLD_HIGH_IDENTIFIED
        ↓
PRICE_TRADES_ABOVE_OLD_HIGH
        ↓
BREAKOUT / STOP LIQUIDITY IS ENGAGED
        ↓
PRICE_FAILS TO CONTINUE HIGHER
        ↓
REVERSAL LOWER
```

Bullish structural skeleton:

```text
OLD_LOW_IDENTIFIED
        ↓
PRICE_TRADES_BELOW_OLD_LOW
        ↓
BREAKDOWN / STOP LIQUIDITY IS ENGAGED
        ↓
PRICE_FAILS TO CONTINUE LOWER
        ↓
REVERSAL HIGHER
```

This is **not yet an executable algorithm**, because the source pass does not establish precise definitions for `old high/low`, the minimum excursion, the confirmation event, timing, entry, stop, target, or failure timeout.

## Candidate rules created

### TS-P001 — prior extreme is required
- Status: PROVISIONAL
- Category: setup prerequisite
- Human description: A Turtle Soup setup references an existing prior high or low; a random reversal without a reference extreme is not enough.
- Evidence: TS-O03, TS-O04, TS-O07
- Implementation status: BLOCKED pending formal definition of eligible old high/low.

### TS-P002 — bearish liquidity excursion
- Status: PROVISIONAL
- Category: manipulation / liquidity
- Human description: Bearish Turtle Soup requires price to trade above a qualifying prior high before reversing lower.
- Evidence: TS-O04, TS-O05
- Implementation status: BLOCKED pending excursion and confirmation semantics.

### TS-P003 — bullish liquidity excursion
- Status: PROVISIONAL
- Category: manipulation / liquidity
- Human description: Bullish Turtle Soup requires price to trade below a qualifying prior low before reversing higher.
- Evidence: TS-O07, TS-O08
- Implementation status: BLOCKED pending excursion and confirmation semantics.

### TS-P004 — breakout failure is part of the concept
- Status: PROVISIONAL
- Category: confirmation
- Human description: The excursion alone does not define a completed trade setup; continuation must fail and price must begin moving away from the swept extreme.
- Evidence: TS-O03, TS-O05, TS-O06, TS-O08
- Implementation status: BLOCKED because exact failure/confirmation event is unresolved.

### TS-P005 — higher-timeframe context matters
- Status: PROVISIONAL
- Category: context
- Human description: Turtle Soup should not be treated as a context-free visual pattern; higher-timeframe price action is part of the decision framework.
- Evidence: TS-O10
- Implementation status: BLOCKED pending later market-profile/context lectures.

### TS-P006 — multiple entry models exist
- Status: PROVISIONAL
- Category: execution
- Human description: Turtle Soup is a structural event that may have multiple entry models rather than one universal entry trigger.
- Evidence: TS-O10
- Implementation status: intentionally deferred to later sources.

### TS-P007 — risk management remains independent
- Status: PROVISIONAL
- Category: risk
- Human description: Strategy win-rate claims do not remove the need for explicit risk management.
- Evidence: TS-O10
- Engineering implication: keep the risk engine independent from setup detection.

## What this source does NOT yet establish

The following must not be guessed from this lecture:

- exact algorithmic definition of an `old high` or `old low`
- whether equal highs/lows count
- minimum age of the reference extreme
- minimum sweep distance
- maximum sweep distance
- wick-only vs body-close conditions
- whether a close back inside the prior range is mandatory
- exact entry trigger
- exact stop-loss placement
- exact target-selection rule
- required session/time window
- how long after the sweep reversal must occur
- permitted instruments/timeframes
- whether SMT is required or optional
- relationship to Model #1 / Kiss of Death

## State-machine candidate

The safest implementation abstraction currently supported by the evidence is:

```text
WAITING_FOR_CONTEXT
        ↓
REFERENCE_EXTREME_SELECTED
        ↓
WAITING_FOR_EXCURSION
        ↓
EXTREME_SWEPT
        ↓
WAITING_FOR_FAILURE_CONFIRMATION
        ↓
TURTLE_SOUP_CONFIRMED
```

`TURTLE_SOUP_CONFIRMED` must remain undefined in code until later sources establish the required confirmation semantics.

## Contradictions / tensions

- The indexed material characterizes Turtle Soup broadly as false breakout/breakdown behaviour, while later Romeo material appears to add stricter time, candle, context and entry-model requirements. Treat the 2024 definition as foundational rather than automatically equivalent to every 2025/2026 CRT setup.
- Romeo's market-maker/algorithm explanations are causal claims about market behaviour. The engine does not need to prove those causal claims to test the observable price pattern. Implementation should encode observable conditions, not unverifiable intent.

## Research consequences

This lecture establishes **Turtle Soup as a reusable structural primitive**, not yet a complete trading strategy. Later CRT sources should be analyzed as potential selectors/confirmers around this primitive:

```text
CONTEXT / TIME
      ↓
REFERENCE RANGE OR EXTREME
      ↓
TURTLE SOUP EVENT
      ↓
ENTRY MODEL / CONFIRMATION
      ↓
TARGET / INVALIDATION
```

## Next linked sources

1. ROMEO-2024-CRT — determine how Turtle Soup sits inside Candle Range Theory.
2. ROMEO-2025-S1 — determine Model #1 relationship to Turtle Soup.
3. ROMEO-2025-S2 — determine Kiss of Death as an entry/refinement model.
4. ROMEO-2025-S3/S4 — resolve candle journey/anatomy and timeframe semantics.
5. ROMEO-2025-S5 — resolve key-level/reference-extreme selection.
6. ROMEO-2025-S8 — resolve failure/invalidation rules.

## Promotion decision

**Do not promote any TS-Pxxx rule to VERIFIED yet.**

The source is sufficient to establish a research model and vocabulary, but not a deterministic production rule set.
