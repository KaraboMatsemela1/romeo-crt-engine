# Video Analysis — ROMEO-2025-S3

## Metadata
- Title: CRT secrets ep.3: The journey
- URL: https://www.youtube.com/watch?v=_oiwm8_id8c
- Published: 2025-08-04
- Duration: 21:01 (registry metadata)
- Creator: Romeo / @Romeotpt
- Analyst/date: ChatGPT / 2026-08-12
- Evidence pass: 1

## Evidence quality

Romeo's official Telegram directly posted, announced, and pinned the exact YouTube ID `_oiwm8_id8c`, giving strong first-party provenance for the source identity.

The timestamped semantic extraction below uses indexed AI-generated video summaries (Video Highlight and YouTubeSummary) because a first-party YouTube transcript was not directly accessible in the current research environment. These services explicitly warn that generated summaries may contain inaccuracies. Therefore all trading semantics remain `PROVISIONAL` until directly checked against the original audio/video or an authoritative transcript.

One concrete summary error was observed: Video Highlight expands `CRT` as `Candle Reversal Techniques` in one bullet, while Romeo's foundational corpus and this project establish CRT as `Candle Range Theory`. This reinforces the rule that third-party summaries may support discovery/evidence triangulation but cannot independently promote a rule to `VERIFIED`.

## Relevance
- CRT relevance: critical
- Primary concepts: Candle 1/2/3 journey, higher-timeframe context, lower-timeframe execution, Turtle Soup, true market structure shift, Model #1, Kiss of Death, targets, timing
- Main engineering value: starts defining the **state progression** of an active CRT rather than describing isolated patterns

## Source-backed observations

| ID | Timestamp | Observation | Confidence |
|---|---:|---|---|
| JRN-O01 | 00:41 | Romeo recommends that learners initially focus on Candle 3 rather than trying to trade every stage. | High |
| JRN-O02 | 01:21–01:56 | All three candles may be tradable, but Candle 2 is treated as materially harder/riskier; waiting for Candle 3 is emphasized for less experienced traders. | High |
| JRN-O03 | 02:31 | The lesson explicitly focuses on the journey from Candle 2 into Candle 3. | High |
| JRN-O04 | 03:13 | Two-timeframe analysis is emphasized: higher timeframe for context/bias, lower timeframe for entry/execution detail. | High |
| JRN-O05 | 05:10–05:46 | Account blow-ups while trading Candle 2 are attributed to poor risk management; learners are encouraged to observe/tape-read Candle 2 while practicing Candle 3. | High |
| JRN-O06 | 06:49 | Candle 1 is associated with accumulation within the three-candle sequence. | High |
| JRN-O07 | 10:20 | The journey includes recurring concepts such as Turtle Soup, Model #1, a breaker / true market-structure-shift concept, and Kiss of Death. | Medium-High |
| JRN-O08 | 11:58 | The episode presents a true market structure shift as a recurring component inside CRT. Exact deterministic semantics are not established by the available summary. | Medium-High |
| JRN-O09 | 12:34 | Time is flagged as a later/important dimension of CRT; this episode does not provide a complete numeric timing model. | Medium-High |
| JRN-O10 | 12:48 | The CRT journey is framed as progression from accumulation through manipulation toward target delivery. | High |
| JRN-O11 | 13:32 | A weekly CRT example previously called publicly is used as practical evidence rather than only a schematic example. | Medium-High |
| JRN-O12 | 14:10 | In a bullish journey example, lower-timeframe observations before the higher-timeframe high target include Turtle Soup at the low, true MSS, Model #1, and Kiss of Death. | High |
| JRN-O13 | 16:21 | Lower-timeframe signals/confirmation are expected before entry rather than entering purely from the higher-timeframe candle label. | High |
| JRN-O14 | summary-level | Target types described include attacking high/low liquidity and rebalancing an imbalance/gap; 50% and old highs appear in the example path. | Medium |
| JRN-O15 | summary-level | A `time meets price` idea is associated with reversal timing, but no deterministic clock/session rule is provided here. | Medium |

## Central interpretation: CRT is a journey/state machine

The strongest architectural contribution of Episode 3 is that CRT should not be modeled as a static chart pattern. It is better represented as a **stateful journey** in which a parent higher-timeframe range progresses through recognizable phases and exposes lower-timeframe execution opportunities.

Provisional high-level model:

```text
CANDLE_1 / ACCUMULATION RANGE
          ↓
CANDLE_2 / MANIPULATION PHASE
          ↓
DIRECTIONAL INTENT / TARGET PATH EMERGES
          ↓
LOWER-TIMEFRAME TURTLE SOUP
          ↓
TRUE-MSS / STRUCTURE CONFIRMATION
          ↓
MODEL #1 OR OTHER ENTRY MODEL
          ↓
JOURNEY CONTINUES
          ↓
KOD CANDIDATE LATE IN JOURNEY
          ↓
TARGET DELIVERY
          ↓
CANDLE_3 / DISTRIBUTION EXPRESSION
```

Important: ordering of every lower-timeframe component is not yet fully established. The diagram is a research hypothesis based on the episode's narrative, not a frozen algorithm.

## Relationship to the KOD look-ahead problem

Episode 2 defined KOD retrospectively as the final Turtle Soup before target. Episode 3 helps narrow the search for an ex-ante classifier by showing KOD as one event **within an already-defined higher-timeframe journey** and by placing it alongside lower-timeframe confirmation concepts before target delivery.

This suggests that the KOD classifier should not inspect Turtle Soup events globally. It should operate only inside an active parent CRT state:

```text
if not parent_crt.active:
    KOD = impossible

if parent_crt.target_already_reached:
    KOD = impossible

if not journey_stage_is_late_enough:
    KOD = unlikely / invalid

if qualifying_turtle_soup and qualifying_ltf_context:
    KOD_CANDIDATE = true
```

The unresolved problem is `journey_stage_is_late_enough`. Later episodes must define that state using only information available at the signal timestamp.

## Candidate rules created

### JRN-P001 — CRT must be modeled as stateful progression
- Status: PROVISIONAL
- Category: architecture / setup sequencing
- Human description: A CRT is a progression through phases and target delivery, not merely a single visual candlestick pattern.
- Evidence: JRN-O03, JRN-O10, JRN-O12
- Engineering implication: use explicit state transitions and timestamps; do not classify setups from a static screenshot alone.

### JRN-P002 — higher-timeframe context and lower-timeframe execution are separate layers
- Status: PROVISIONAL
- Category: timeframe architecture
- Human description: The higher timeframe determines the parent CRT context/journey while lower timeframes provide execution evidence.
- Evidence: JRN-O04, JRN-O12, JRN-O13
- Engineering implication: signal objects must retain both `context_timeframe` and `execution_timeframe`.

### JRN-P003 — Candle 3 is the preferred initial execution phase
- Status: PROVISIONAL / PEDAGOGICAL
- Category: setup selection
- Human description: Romeo recommends Candle 3 as the safer starting focus for learners; Candle 2 is materially more advanced.
- Evidence: JRN-O01, JRN-O02, JRN-O05
- Engineering implication: the first backtestable strategy candidate should likely prioritize Candle-3 setups before attempting Candle-2 trading, unless later evidence contradicts this.
- Note: this is a teaching/risk-selection recommendation, not yet a proof that Candle 3 has superior expectancy.

### JRN-P004 — Candle 1 is the accumulation anchor
- Status: PROVISIONAL
- Category: range / phase
- Human description: Candle 1 acts as the accumulation phase/anchor of the parent CRT journey.
- Evidence: JRN-O06, JRN-O10
- Blocker: exact Candle-1 selection predicate remains unresolved.

### JRN-P005 — lower-timeframe Turtle Soup participates in the journey
- Status: PROVISIONAL
- Category: liquidity / confirmation
- Human description: Turtle Soup appears on the lower timeframe as part of the internal path of a parent CRT.
- Evidence: JRN-O07, JRN-O12
- Engineering implication: Turtle Soup detector should accept parent-CRT context rather than operating only as an isolated global signal.

### JRN-P006 — true MSS is a recurring CRT component
- Status: PROVISIONAL
- Category: confirmation / structure
- Human description: Romeo presents a `true market structure shift` as a recurring component of CRT progression.
- Evidence: JRN-O07, JRN-O08, JRN-O12
- Blocker: exact structural predicate is unresolved and must not be substituted with a generic retail MSS algorithm.

### JRN-P007 — Model #1 can serve as LTF execution within an active journey
- Status: PROVISIONAL
- Category: entry
- Human description: Model #1 is observed on the lower timeframe within the active CRT journey before target delivery.
- Evidence: JRN-O07, JRN-O12, JRN-O13
- Engineering implication: keep `journey context` and `entry model` separate.

### JRN-P008 — KOD is journey-dependent
- Status: PROVISIONAL
- Category: sequencing
- Human description: Kiss of Death belongs late in the path toward a parent CRT target rather than being a context-free Turtle Soup label.
- Evidence: JRN-O07, JRN-O12; cross-source support ROMEO-2025-S2
- Blocker: real-time late-stage predicate remains unresolved.

### JRN-P009 — target delivery is part of CRT state
- Status: PROVISIONAL
- Category: target
- Human description: A CRT journey has an intended destination such as a high/low liquidity objective or rebalancing objective; target state influences which journey phase is active.
- Evidence: JRN-O10, JRN-O12, JRN-O14
- Blocker: target hierarchy and selection algorithm are unresolved.

### JRN-P010 — time must become a first-class input
- Status: PROVISIONAL
- Category: time
- Human description: Time is treated as part of understanding when price reverses/progresses, not merely metadata attached to a price setup.
- Evidence: JRN-O09, JRN-O15
- Engineering implication: eventual feature/state model must retain timezone-safe session/calendar context.
- Blocker: exact Romeo timing rules require later evidence.

## Candidate data model emerging from Episodes 1–3

```text
CRTContext
├── context_timeframe
├── parent_candle_id
├── range_high
├── range_low
├── midpoint_50
├── direction                 # unresolved selector
├── phase                     # C1/C2/C3 semantics unresolved in detail
├── target_primary
├── target_secondary
├── target_status
└── created_at / state timestamps

JourneyEvent
├── timestamp
├── execution_timeframe
├── event_type
│   ├── TURTLE_SOUP
│   ├── TRUE_MSS
│   ├── MODEL_1
│   └── KOD_CANDIDATE
├── reference_level
├── evidence
└── parent_crt_id
```

This is a research data model only. Fields whose semantics are unresolved must not be used to generate live orders.

## Important implementation boundary: no hindsight phase labels

The system must distinguish two tasks:

1. **Retrospective annotation** — after a completed sequence, label Candle 1/2/3 and the journey for research.
2. **Live inference** — at time `t`, determine which states are inferable using only data available through `t`.

A completed historical chart makes phase labels obvious. A valid backtester must not use completed Candle-3 information to decide an entry that allegedly occurred during Candle 2.

Every phase transition therefore requires an `information_available_at` test.

## Target taxonomy hypothesis

Episode 3's summary material describes two broad objective families:

```text
A. LIQUIDITY OBJECTIVE
   → attack a prior high / low

B. REBALANCING OBJECTIVE
   → fill/rebalance an imbalance or gap
```

The project should treat this only as a provisional taxonomy until direct transcript/video confirmation and later episodes clarify priority/order.

## What this source does NOT yet establish

Do not guess:

- exact live predicate for Candle 1, Candle 2, or Candle 3
- exact moment the system may declare Candle 2 manipulation complete
- whether Turtle Soup → true MSS → Model #1 is a mandatory ordered chain
- exact definition of `true market structure shift`
- exact breaker semantics
- whether Model #1 is always present or merely common
- exact ex-ante condition identifying KOD
- exact target hierarchy
- exact relationship between 50% and old-high/old-low objectives
- exact HTF→LTF mapping table
- exact time/session rules
- exact stop placement or risk/reward requirement
- whether all CRT variants use the same internal journey

## New questions created

1. What event moves a parent CRT from `ACCUMULATION` to `MANIPULATION` in real time?
2. What event moves it from `MANIPULATION` to `DISTRIBUTION` / Candle 3?
3. Is Candle 3 defined by calendar position, price behavior, confirmation, or a combination?
4. Is the lower-timeframe sequence Turtle Soup → true MSS → Model #1 → KOD ordered, optional, or overlapping?
5. What exactly is `true MSS`, and how is it distinguished from a fake MSS?
6. What makes a journey `late enough` for a KOD candidate without knowing the future target hit?
7. Can the 50% interaction be used as a causal state boundary for KOD qualification?
8. How is the target objective selected before the move begins?
9. What are the canonical HTF/LTF pairs?
10. Which timing features define `time meets price`?

## Research consequence

Episode 3 materially strengthens the decision to implement the strategy as a **hierarchical state machine**:

```text
HIGHER-TIMEFRAME CRT STATE
          ↓
LOWER-TIMEFRAME JOURNEY EVENTS
          ↓
ENTRY-MODEL CONFIRMATION
          ↓
INDEPENDENT RISK ENGINE
```

The next source, `ROMEO-2025-S4 — Candle anatomy`, is now the highest-value blocker because it should help define the candle/phase mechanics and timeframe semantics needed to make these states deterministic.

## Promotion decision

**No JRN-Pxxx rule is promoted to `VERIFIED`.**

The evidence is sufficient to refine the research architecture and candidate state model, but not yet to produce a look-ahead-safe executable CRT state machine.
