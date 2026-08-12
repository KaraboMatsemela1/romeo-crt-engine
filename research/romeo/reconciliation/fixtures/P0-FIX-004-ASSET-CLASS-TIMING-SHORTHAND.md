# P0-FIX-004 — Asset-Class Timing Shorthand

**Class:** `CANDIDATE / TEXTUAL_TIMING_FIXTURE`  
**P0 targets:** P0-03 primarily; P0-02 secondarily  
**Source:** Romeo official Telegram  
**Doctrine:** `CRT_SECRETS_2025`

## First-party observation

Romeo publishes:

```text
Forex: 159159
Index futures: 26102610
Crypto: 12481248
```

The post explicitly separates three market classes.

## Causal fact available from source

At the time of the post, a learner can know that Romeo intends a repeating numeric schedule or sequence differentiated by market class.

No future outcome is needed to observe this.

## High-confidence decoding

The strings expand naturally into repeating 12-hour clock sequences:

```text
Forex         1,5,9,1,5,9
Index futures 2,6,10,2,6,10
Crypto        12,4,8,12,4,8
```

Corresponding 24-hour six-slot sequences:

```text
Forex:
01, 05, 09, 13, 17, 21

Index futures:
02, 06, 10, 14, 18, 22

Crypto:
00, 04, 08, 12, 16, 20
```

Independent secondary CRT publications reproduce the same asset-class clock grouping and explicitly describe the Forex and index sequences as 4-hour candle formation/timing schedules.

## Why fixture is not POSITIVE closure credit yet

The accessible Romeo text does not explicitly say:

```text
"these are the opening hours of my H4 CRT candles"
```

and does not state the timezone.

Therefore this fixture supports:

```text
H4_ANCHOR_SEQUENCE_INTERPRETATION = HIGH_CONFIDENCE
```

but not:

```text
P0_03 = CLOSED
```

## Candidate engine data

```python
TimingSequenceCandidate(
    asset_class="FOREX",
    local_hours=(1,5,9,13,17,21),
    semantic_role="LIKELY_H4_ANCHOR",
    timezone="UNKNOWN",
)

TimingSequenceCandidate(
    asset_class="INDEX_FUTURES",
    local_hours=(2,6,10,14,18,22),
    semantic_role="LIKELY_H4_ANCHOR",
    timezone="UNKNOWN",
)

TimingSequenceCandidate(
    asset_class="CRYPTO",
    local_hours=(0,4,8,12,16,20),
    semantic_role="LIKELY_H4_ANCHOR",
    timezone="UNKNOWN",
)
```

## Required upgrade evidence

To promote this fixture to P0 closure credit, obtain either:

- Romeo-primary textual/audio explanation of the numbers;
- a Romeo chart with known timezone whose H4 boundaries reproduce the sequence;
- repeated first-party market-class examples proving the same construction.

## Anti-overreach rule

Do not use secondary documentation to fill the missing timezone or claim the shorthand is verified Romeo H4 construction. Secondary sources corroborate the decoding; they do not replace first-party provenance for the final executable semantics.