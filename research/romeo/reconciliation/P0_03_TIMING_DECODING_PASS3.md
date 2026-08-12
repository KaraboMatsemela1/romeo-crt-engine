# P0-03 Timing Decoding — Pass 3

**Candidate:** `CRT-C3-ALIGNED-v0.1-DRAFT`  
**Doctrine snapshot:** `CRT_SECRETS_2025`  
**Status:** HIGH-CONFIDENCE INTERPRETATION / P0-03 STILL OPEN  
**Date:** 2026-08-12

## First-party source

Romeo's official Telegram posts the compact asset-class notation:

```text
Forex: 159159
Index futures: 26102610
Crypto: 12481248
```

This appears in the same public teaching period as CRT Secrets Episodes 4 and 5.

## Most likely decoding

The string naturally expands in 12-hour clock repetition as six 4-hour anchors:

```text
Forex:
01:00, 05:00, 09:00, 13:00, 17:00, 21:00

Index futures:
02:00, 06:00, 10:00, 14:00, 18:00, 22:00

Crypto:
00:00, 04:00, 08:00, 12:00, 16:00, 20:00
```

In shorthand:

```text
Forex         = 1 / 5 / 9
Index futures = 2 / 6 / 10
Crypto        = 12 / 4 / 8
```

## Independent secondary corroboration

Independent CRT material reproduces the same interpretation:

- Forex 4H: 1am / 5am / 9am
- index futures 4H: 2am / 6am / 10am
- crypto: 4 / 8 / 12

This corroboration is useful for decoding Romeo's compact first-party notation, but it is not itself accepted as Romeo doctrine.

## Evidence classification

The project may now classify:

```text
asset_class_h4_anchor_pattern = HIGH_CONFIDENCE_INTERPRETATION
```

but NOT yet:

```text
asset_class_h4_calendar = VERIFIED
```

because Romeo's accessible first-party post does not explicitly state:

1. that the numbers are H4 candle open times;
2. the timezone;
3. whether they represent candle construction or only high-probability formation/purge times;
4. venue/maintenance treatment;
5. DST semantics for this exact shorthand.

## Candidate calendar representation

```python
AssetClassH4AnchorDraft(
    forex_local_hours=(1, 5, 9, 13, 17, 21),
    index_futures_local_hours=(2, 6, 10, 14, 18, 22),
    crypto_local_hours=(0, 4, 8, 12, 16, 20),
    timezone="UNRESOLVED_FOR_THIS_RULE",
    meaning="LIKELY_H4_CANDLE_ANCHORS",
    evidence_status="HIGH_CONFIDENCE_INTERPRETATION",
)
```

## Relationship to existing New York evidence

P0-03 already has high-confidence evidence that Romeo uses New York wall-clock references for Daily and Weekly construction.

That makes `America/New_York` the leading candidate timezone for this shorthand, but the project will not promote the H4 notation to a NY-local executable calendar until a Romeo-primary source explicitly links the numeric sequence to that timezone or a chart fixture reproduces it unambiguously.

## Important scope consequence

P0-03 is narrower than before:

```text
BEFORE PASS 3
exact H4 anchors = completely unknown

AFTER PASS 3
asset-class anchor sequences = high-confidence decoded
exact timezone/semantic role = blocking
```

## Acceptance path to close P0-03

Need at least one of:

1. direct Romeo text/video saying the sequence represents 4H candle times and naming timezone;
2. a directly inspectable Romeo chart whose H4 bars reproduce the decoded sequence with known chart timezone;
3. multiple first-party fixtures across asset classes that eliminate competing interpretations.

Then validate:

- FX against `01/05/09/13/17/21`;
- index futures against `02/06/10/14/18/22`;
- crypto against `00/04/08/12/16/20`;
- DST behavior;
- futures maintenance windows;
- provider reconstruction.

## Current disposition

```text
P0-03 = PARTIALLY_RESOLVED
H4 sequence interpretation = materially narrowed
strategy freeze = BLOCKED
```

No provider-native bars should be authorized merely because they happen to match the candidate sequence.