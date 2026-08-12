# Video Analysis — ROMEO-2025-LIVE

## Metadata
- Title: CRT live tape-reading session
- URL: https://www.youtube.com/watch?v=1EK-LMwgJ3c
- Published: 2025-07-01
- Duration: 43:42
- Creator: Romeo / @Romeotpt
- Analyst/date: ChatGPT / 2026-08-12
- Evidence pass: P0 fixture-source registration

## Evidence quality

Romeo's official Telegram directly posted and pinned the exact YouTube ID `1EK-LMwgJ3c` and described it as a `CRT live tape-reading session`, giving first-party provenance for source identity.

The same official feed subsequently said the move had been `outlined live beforehand in yesterday's video` and rejected a `maybe up maybe down` framing. This makes the source particularly valuable for causal fixture construction because the thesis/context was publicly stated before the later outcome post.

Video Highlight independently indexes the video as published 2025-07-01 with duration 43:42, but also explicitly warns that its generated summaries may contain inaccuracies.

At the time of this pass, a reliable indexed full transcript or directly inspectable frame sequence for this exact video was not available through the research interface. Therefore **no new trading-rule semantics are promoted from the live session in this file**. The source is registered as a priority visual/causal fixture source.

## Why this source matters more than a completed-chart lecture

A completed historical chart can encourage hindsight selection:

```text
see winner
  ↓
choose parent candle
  ↓
choose key level
  ↓
call the right direction
  ↓
label the successful Turtle Soup
```

The live tape-reading source can instead support:

```text
information available at t0
  ↓
predeclared context / expectation
  ↓
observable subsequent events
  ↓
outcome
```

That is exactly the evidence structure required to close P0 rules without look-ahead bias.

## P0 fixture objectives

### P0-03 — Candle calendar
Capture visual frames where:
- the chart timeframe is visible;
- H4 candle timestamps/open boundaries are visible;
- instrument/venue is identifiable;
- local chart timezone can be inferred or directly shown.

Target evidence:
```text
exact H4 anchor sequence
+ instrument/session policy
```

### P0-01 — Parent CRT / Candle-1 selector
For each setup discussed live, record:
- when the parent candle/range is first identified;
- what competing nearby candles existed at that timestamp;
- why the selected candle was preferred;
- whether C1/C2/C3 are consecutive;
- nested/inside/overlapping range treatment;
- when the parent expires or is superseded.

### P0-02 — KeyLevelSelector
Capture:
- which level is marked before price reaches it;
- level source/timeframe;
- whether the level is price/time/composite;
- role: `DESTINATION` or `REACTION_ORIGIN`;
- competing levels visible at selection time;
- exact reach event;
- pre-level fake structures that are rejected.

### P0-05 — Context direction
Record the exact evidence Romeo uses before declaring direction:
- owning timeframe;
- close vs wick relationship;
- target/draw relationship;
- how conflicting W1/D1/H4 states are treated;
- timestamp at which direction becomes known.

### P0-04 — Turtle Soup
Capture both accepted and rejected examples:
- selected old high/low;
- age/type of reference;
- excursion beyond reference;
- exact confirmation event;
- time between sweep and confirmation;
- what would constitute true breakout rather than Turtle Soup;
- whether reference remains reusable afterward.

## Fixture schema

Every extracted fixture should be stored with an immutable information set:

```python
P0Fixture(
    fixture_id,
    source_id="ROMEO-2025-LIVE",
    instrument,
    chart_timezone,
    context_timeframe,
    execution_timeframe,
    observation_timestamp,
    parent_candidates_visible,
    selected_parent_id,
    key_level_candidates_visible,
    selected_key_level_id,
    context_direction_at_t,
    turtle_soup_state_at_t,
    screenshot_or_timestamp_reference,
    source_statement,
    expected_engine_decision,
    outcome_for_audit_only,
)
```

`outcome_for_audit_only` must never participate in candidate selection.

## Required fixture classes

### Positive
At least five examples where the live source establishes enough pre-event information to reproduce:
1. parent selection;
2. key-level selection;
3. direction;
4. sweep/failure state;
5. accepted downstream decision.

### Negative
At least five examples including:
1. plausible but non-selected parent candle;
2. plausible but non-selected key level;
3. pre-level fake reversal;
4. sweep without qualifying confirmation;
5. direction/time/context conflict;
6. setup that ends `NO_SIGNAL`.

## Current promotion decision

This pass **confirms source identity and causal fixture value only**.

It does NOT yet close:
- H4 anchors;
- Candle-1 eligibility;
- key-level taxonomy/ranking;
- direction resolver;
- Turtle Soup confirmation.

No P0 alpha predicate is promoted to `VERIFIED` from this file.

## Additional high-value source discovered

Romeo's official Telegram later posted and pinned a second public source:

- `CRT live tape-reading session (2)`
- YouTube ID: `Pmmx41M7KhA`

That source should be added as a second fixture stream after session 1, especially for checking whether the same P0 predicates remain stable across time and markets rather than fitting one lecture.
