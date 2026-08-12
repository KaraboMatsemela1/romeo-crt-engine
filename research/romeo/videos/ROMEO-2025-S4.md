# Video Analysis — ROMEO-2025-S4

## Metadata
- Title: CRT secrets ep.4: Candle anatomy
- URL: https://www.youtube.com/watch?v=n2GF8kCpgVg
- Published: 2025-08-15
- Duration: 15:48
- Creator: Romeo / @Romeotpt
- Analyst/date: ChatGPT / 2026-08-12
- Evidence pass: 1

## Evidence quality

Romeo's official Telegram directly posted and pinned the exact YouTube video ID `n2GF8kCpgVg` and announced it as CRT Secrets episode 4, giving strong first-party provenance for source identity.

Timestamped semantic extraction uses indexed summaries from Video Highlight and YouTubeSummary because the current research environment could not retrieve a first-party YouTube transcript. Both are secondary/AI-generated summaries, so all strategy semantics remain `PROVISIONAL` until checked directly against the original video/audio or an authoritative transcript.

## Relevance
- CRT relevance: critical
- Primary concepts: candle anatomy, parent candle selection, open/close time, price path inside candle, permitted parent timeframes, fractality, pattern/context ordering
- Main engineering value: provides the first explicit initial **parent-timeframe scope** and establishes that candle identity/time boundaries must be selected before entry-pattern detection

## Source-backed observations

| ID | Timestamp | Observation | Confidence |
|---|---:|---|---|
| ANA-O01 | 00:00 | Romeo presents candle anatomy as foundational to CRT rather than an optional refinement. | High |
| ANA-O02 | 01:22–02:36 | Blind pattern trading without context/narrative is criticized; pattern recognition alone is insufficient. | High |
| ANA-O03 | 03:54 | The viewer is asked to reason about the candle itself before applying entry models. | Medium-High |
| ANA-O04 | 05:05 | A candle is described through its opening time, closing time, and price movement between those boundaries. | High |
| ANA-O05 | 06:06 | For the public foundational framework, Romeo tells traders to focus on 4-hour, Daily, and Weekly candles. | High |
| ANA-O06 | 06:06–07:10 | Larger candles such as Monthly / multi-month / yearly scales are presented as later/advanced extensions rather than the initial learning scope. | Medium-High |
| ANA-O07 | 07:10 | Candles are described as fractal: structurally similar across timeframes, while differing in how long they take to print. | High |
| ANA-O08 | 08:52 | The first decision in analysis should be which candle is being traded. | High |
| ANA-O09 | 13:24 | Lower timeframes can be studied for experience/observation, but Romeo cautions against turning that into excessive direct trading. | Medium-High |
| ANA-O10 | 14:08 | The timeframe/candle should be identified before looking for the technical pattern. | High |
| ANA-O11 | summary-level | A secondary summary describes directional examples as opening movement → Turtle Soup → CRT directional delivery; exact terminology/sequence needs direct verification. | Low-Medium |

## Core conclusion: `TradeCandle` must be a first-class object

This episode gives us a stronger data-model boundary than previous sources:

```text
SELECT TRADE CANDLE
      ↓
KNOW ITS OPEN TIME
KNOW ITS CLOSE TIME
KNOW CURRENT POSITION INSIDE ITS LIFECYCLE
      ↓
ESTABLISH CRT CONTEXT / NARRATIVE
      ↓
ONLY THEN SEARCH FOR ENTRY PATTERNS
```

The engine therefore should not begin from a generic lower-timeframe pattern and ask, "Which CRT could explain this?"

It should begin from an explicitly selected parent candle/range and ask, "What lower-timeframe behavior is occurring inside this known parent candle?"

## Initial parent-timeframe scope

Episode 4 gives the strongest current source support for constraining the first research/backtest universe to:

```text
PARENT / TRADE CANDLES
- H4
- D1
- W1
```

This does **not** yet mean execution must occur on those same timeframes. Episode 3 already supports HTF-context / LTF-execution separation.

The implication is:

```text
TradeCandle.timeframe ∈ {H4, D1, W1}
ExecutionTimeframe = unresolved mapping
```

for the initial public-system candidate.

Larger parent periods can be added later as a separate doctrine/version extension after the base engine is validated.

## Candle lifecycle model

The source supports treating a candle as a time-bounded object, not merely final OHLC values:

```text
TradeCandle
├── timeframe
├── open_time
├── close_time
├── open_price
├── high_so_far
├── low_so_far
├── current_price
├── elapsed_fraction
├── remaining_time
└── is_closed
```

After close, final fields become:

```text
high
low
close
body
upper_wick
lower_wick
range
```

However, **final high/low/close are unavailable before the candle closes**. Backtests must not use final candle anatomy to make earlier intrabar decisions.

## Critical anti-look-ahead consequence

A common implementation bug would be:

```python
# INVALID for an intrabar decision
if current_parent_candle.final_close < current_parent_candle.open:
    bearish_context = True
```

when the decision supposedly occurred before the parent candle closed.

The valid model must snapshot candle anatomy at decision time:

```text
CandleSnapshot(t)
├── open_price                    # known
├── high_so_far(t)                # known
├── low_so_far(t)                 # known
├── current_price(t)              # known
├── scheduled_close_time          # known
├── elapsed_time                  # known
└── final_close                   # UNKNOWN until close
```

This extends the look-ahead protections already identified for KOD and Candle 1/2/3 phase labels.

## Candidate rules created

### ANA-P001 — parent candle must be selected before entry pattern
- Status: PROVISIONAL
- Category: analysis ordering
- Human description: Decide which candle/timeframe is being traded before looking for Turtle Soup, Model #1, KOD, FVG or other technical patterns.
- Evidence: ANA-O02, ANA-O03, ANA-O08, ANA-O10
- Engineering implication: pattern detectors require a `parent_candle_id` / `crt_context_id` where applicable.

### ANA-P002 — candle anatomy includes time boundaries
- Status: PROVISIONAL
- Category: time / data model
- Human description: A candle is defined not only by price geometry but by its opening time, closing time, and price action between them.
- Evidence: ANA-O04
- Engineering implication: candle objects must use exchange/session-aware timestamps; OHLC alone is insufficient for CRT research.

### ANA-P003 — initial parent-candle whitelist is H4/D1/W1
- Status: PROVISIONAL
- Category: timeframe scope
- Human description: Romeo's foundational public guidance restricts the initial trade-candle focus to 4-hour, Daily, and Weekly candles.
- Evidence: ANA-O05, ANA-O08
- Engineering implication: Phase-2 candidate strategy should default to `{H4,D1,W1}` parent candles instead of parameter-sweeping every timeframe.

### ANA-P004 — larger parent candles are an advanced extension
- Status: PROVISIONAL / SCOPE
- Category: timeframe scope
- Human description: Monthly and larger multi-month/yearly candles are treated as later/advanced work rather than necessary for the initial model.
- Evidence: ANA-O06
- Engineering implication: exclude them from CRT-v0.1 unless later evidence makes them necessary.

### ANA-P005 — candle mechanics are fractal across timeframes
- Status: PROVISIONAL
- Category: timeframe architecture
- Human description: Candles share the same structural anatomy across timeframes, with the primary difference being elapsed clock time / data-print duration.
- Evidence: ANA-O07
- Engineering implication: use a generic candle/state implementation parameterized by timeframe rather than separate H4/D1/W1 algorithms.

### ANA-P006 — final candle anatomy cannot be used before close
- Status: ENGINEERING SAFETY INFERENCE
- Category: backtest integrity
- Human description: Because the candle is a time-evolving object, final high/low/close/body/wicks cannot qualify an earlier entry unless those values were already observable at that timestamp.
- Evidence basis: ANA-O04 plus general causal-data constraint
- Engineering implication: maintain timestamped candle snapshots for intrabar decisions.

### ANA-P007 — lower timeframe is observational/execution detail, not the analysis anchor
- Status: PROVISIONAL
- Category: timeframe hierarchy
- Human description: Lower timeframes are useful for studying and executing the internal journey, but analysis should remain anchored to the selected parent candle.
- Evidence: ANA-O09; cross-source ROMEO-2025-S3
- Engineering implication: avoid free-floating LTF signal generation without a parent context for the first CRT candidate.

### ANA-P008 — pattern quality is conditional on narrative/context
- Status: PROVISIONAL
- Category: setup qualification
- Human description: A technically recognizable pattern is not automatically tradable; it must be evaluated inside the chosen candle's CRT context.
- Evidence: ANA-O02, ANA-O10
- Engineering implication: pattern detector output should be `candidate event`, not `trade signal`.

## Revised hierarchical architecture

Episodes 1–4 now support this research architecture:

```text
CALENDAR / TIME ENGINE
        ↓
TRADE-CANDLE SELECTOR
(H4 / D1 / W1 initially)
        ↓
PARENT CANDLE LIFECYCLE STATE
        ↓
CRT JOURNEY / DIRECTION / TARGET STATE
        ↓
LTF INTERNAL EVENTS
(Turtle Soup / true MSS / Model #1 / KOD)
        ↓
ENTRY QUALIFICATION
        ↓
INDEPENDENT RISK ENGINE
```

This is materially different from the typical bot architecture of scanning every bar for visual setups.

## Deterministic calendar requirement

A 4H, Daily or Weekly candle is meaningless unless its boundaries are reproducible.

Before Phase 3 data ingestion is considered trusted, the system must define:

- canonical timezone for market/session candles
- DST behavior
- broker/data-provider candle-boundary differences
- weekend/holiday handling
- asset-class-specific session boundaries
- whether Romeo's `4H` means a specific New York/London anchored 4H schedule or provider-native 4H bars

This is now a **strategy-critical requirement**, not data plumbing.

## What this episode does NOT establish

Do not guess:

- exact canonical timezone for H4/D1/W1 candle construction
- exact H4 opening times
- exact meaning of Daily open for each asset class
- whether FX, indices, metals and crypto use identical candle boundaries
- exact HTF→LTF mapping
- exact live definitions of Candle 1/2/3
- body/wick thresholds
- `thick candle` thresholds
- whether candle color at close establishes bias
- exact use of candle open as support/resistance or entry reference
- precise meaning of the summary-level `open dump/pump → Turtle Soup → CRT` sequence
- exact entry or stop rules

## New questions created

1. What timezone/session anchors Romeo's 4H candles?
2. What exact 4H start times are valid?
3. What is Romeo's canonical Daily candle open/close?
4. What is the canonical Weekly open/close?
5. Are candle boundaries different across Forex, indices, metals and crypto?
6. Can an active parent candle be selected at its open, or only after some internal event develops?
7. How does the open price participate in Candle 1/2/3 state transitions?
8. What exact intrabar information allows Candle 2 manipulation to be recognized before the candle completes?
9. How is the execution timeframe derived from H4 vs D1 vs W1 parent candles?
10. What candle-shape information is actually used versus merely descriptive?
11. What makes Romeo's `thick candle` deterministic?

## Research consequence

Episode 4 resolves one major architectural question: the initial CRT engine should **not** be timeframe-agnostic at the strategy level. It can be generic in implementation, but CRT-v0.1 should intentionally scope its parent candle universe to H4/D1/W1 until evidence justifies expansion.

It also upgrades the time/calendar engine from infrastructure to **core strategy logic**.

The next source, `ROMEO-2025-S5 — Key level`, is the correct next blocker because choosing the parent candle is still not enough: we need to know **where** within market context a candle/range interaction is meaningful and which price/time levels qualify the journey.

## Promotion decision

No `ANA-Pxxx` strategy rule is promoted to `VERIFIED` yet.

`ANA-P006` is adopted as an engineering anti-look-ahead constraint regardless of future doctrine changes: no historical decision may consume candle information that was not available at its decision timestamp.
