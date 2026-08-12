# Video Analysis — ROMEO-2025-S1

## Metadata
- Title: CRT secrets ep.1: One CRT model for life
- URL: https://www.youtube.com/watch?v=T7udbrWlARI
- Published: 2025-06-16
- Duration: 30:58
- Analyst/date: ChatGPT / 2026-08-12
- Evidence status: **PROVISIONAL — official Telegram corroborates video ID/title; technical extraction currently depends on indexed transcript/summary**

## Relevance
- CRT relevance: Critical. This episode appears to formalize `Model #1`, selectivity, timeframe mapping and time filters.
- Setup variants discussed: bearish/bullish Model #1, FVG-enhanced Model #1, weekly timing example

## Candidate terminology
| Term | Timestamp | Provisional meaning | Confidence |
|---|---:|---|---|
| Model #1 bearish | ~10:45 / 20:24 | A selected thick up-close candle penetrates an old high; short confirmation occurs when price closes below that selected candle. | High |
| Model #1 bullish | later inverse example | Symmetric structure using a down-close candle through an old low, with confirmation by a close above. | Medium-High |
| Thick candle | ~10:45+ | Qualitative candle-selection requirement; exact body/range threshold is not yet defined. | High that term matters; Low on formula |
| FVG enhancement | ~21:01 | FVG associated with Model #1 is presented as increasing probability, apparently not always required. | Medium-High |
| Time > price | ~23:11 | Timing/context can override otherwise attractive price patterns. | High |

## Explicit candidate rules
| Candidate rule ID | Candidate rule | Timestamp | Confidence |
|---|---|---:|---|
| CRT-P010 | Bearish Model #1 begins with a qualifying up-close candle that trades into/through an old high. | ~10:45 / 20:24 | High |
| CRT-P011 | Bearish Model #1 confirmation requires a close below the selected model candle. | ~15:23 / 19:24 / 20:24 | High |
| CRT-P012 | Bullish Model #1 is the directional inverse around an old low and down-close model candle. | inverse example | Medium-High |
| CRT-P013 | Model #1 is a single-candle object, not an arbitrary multi-candle zone. | ~19:12 | High |
| CRT-P014 | Trade selection must be selective; not every visually similar candle is a valid Model #1 candidate. | 11:28–14:51 / 21:41+ | High |
| CRT-P015 | FVG may act as a probability enhancer for Model #1 rather than the core definition itself. | ~21:01 | Medium-High |
| CRT-P016 | Time context is a required setup dimension and can invalidate a pattern that is acceptable on price alone. | ~23:11+ | High |

## Timeframe mapping hypothesis
Indexed summaries of this episode report a mapping such as:
- Monthly context → Daily Model #1
- Weekly context → 4H Model #1
- Daily context → 1H Model #1

**Status: PROVISIONAL.** Before coding, confirm whether these are strict mappings, examples, or beginner defaults; also determine the exact ratio/relationship for additional timeframe pairs.

## Entry / stop / target / invalidation
- Entry: close confirmation across the Model #1 candle is strongly supported by indexed transcript material.
- Stop: indexed summaries refer to stop placement around the model/entry high or low, but exact structural placement is unresolved.
- Targets: prior/old lows for bearish and highs for bullish are referenced; target ordering and relationship to the parent CRT 50% target need reconciliation.
- Invalidation: lack of qualifying close, incorrect candle selection, or wrong time/context appear important; exact hard invalidation still unresolved.

## Open questions
1. Quantify `thick` candle mathematically: body/range ratio, ATR-relative threshold, percentile, or purely contextual?
2. Does `stab into an old high/low` require wick penetration, body penetration, or any trade beyond the level?
3. Must the model candle itself close back inside/outside the old high/low?
4. What exact candle provides confirmation: the next candle or any later candle?
5. Is FVG optional, preferred, or mandatory for specific subtypes?
6. What exact stop is used if the confirmation candle makes a new extreme?
7. How are old highs/lows selected when several liquidity levels exist?
8. Are the published timeframe mappings hard constraints or educational defaults?
9. What exact weekly time windows distinguish fake vs real weekly high/low?

## Promotion decision
No strategy rule is `VERIFIED` yet. The Model #1 semantics are strong enough to prioritize direct-source verification and fixture extraction next.
