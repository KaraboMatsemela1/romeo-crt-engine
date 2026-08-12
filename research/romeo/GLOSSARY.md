# CRT Glossary

No glossary term is assumed verified until source evidence is added. `PROVISIONAL` means the concept is source-backed enough for research use but not yet deterministic/production-safe.

| Term | Working definition | Status | Evidence |
|---|---|---|---|
| CRT | Candle Range Theory; broader formal definition still being established from the corpus. | PROVISIONAL | ROMEO-2024-CRT |
| Range | A bounded price interval; Romeo's CRT foundation appears to treat a candle itself as a range, but exact eligible-range semantics remain unresolved. | PROVISIONAL | ROMEO-2024-CRT |
| Liquidity | Observable trading interest/stops associated with reference highs/lows and other later-defined levels. Do not encode assumptions about participant intent. | PROVISIONAL | ROMEO-2024-TS 06:29–15:54 |
| Old high / old low | A previously established price extreme used as the reference level for a Turtle Soup event. Eligibility criteria remain unresolved. | PROVISIONAL | ROMEO-2024-TS 06:29, 11:06, 15:18 |
| Turtle Soup | Failed excursion beyond a qualifying prior high/low followed by movement in the opposite direction. Exact confirmation and timing rules remain unresolved. | PROVISIONAL | ROMEO-2024-TS 06:29–15:54 |
| Sweep / manipulation | Price trades beyond a qualifying reference extreme. A sweep alone is not yet sufficient to define a completed Turtle Soup setup. | PROVISIONAL | ROMEO-2024-TS 11:43, 13:57, 15:54 |
| False breakout / breakdown | A move beyond a prior reference high/low that does not sustain continuation and instead reverses. | PROVISIONAL | ROMEO-2024-TS 06:29–15:54 |
| Confirmation | The observable event that establishes failure of continuation and makes a setup actionable. Exact Romeo semantics remain unresolved. | UNRESOLVED | ROMEO-2024-TS identifies the need conceptually; later sources required |
| Model #1 | Romeo's later candle-specific setup/entry model. Deterministic definition not yet frozen. | PROVISIONAL | ROMEO-2025-S1 |
| Kiss of Death (KOD) | A specialized Turtle Soup occurring late in an active CRT journey; Romeo defines it as the final Turtle Soup before the target is hit. This definition is not directly implementable without ex-ante qualifying conditions because using `final` retrospectively would introduce look-ahead bias. | PROVISIONAL | ROMEO-2025-S2 01:49, 06:12 |
| Candle 1 / 2 / 3 | Provisional CRT sequence mapped to accumulation / manipulation / distribution. Episode 3 reinforces this as a stateful journey, but exact live transition predicates remain unresolved. | PROVISIONAL | ROMEO-2025-S2 03:39; ROMEO-2025-S3 02:31, 06:49, 12:48 |
| CRT journey | Stateful progression of a parent higher-timeframe CRT from range/accumulation through manipulation toward target delivery, with lower-timeframe events used for execution. | PROVISIONAL | ROMEO-2025-S3 02:31–16:21 |
| True MSS | Romeo's `true market structure shift`, presented as a recurring lower-timeframe CRT component. Exact deterministic definition is unresolved and must not be replaced by a generic market-structure-shift algorithm. | PROVISIONAL | ROMEO-2025-S3 10:20–14:10 |
| CRT 50% | Midpoint of the parent CRT range; used as Target 1 / reaction area in the demonstrated bearish KOD journey. Mandatory/optional status remains unresolved. | PROVISIONAL | ROMEO-2025-S2 06:42, 10:49–11:11 |
| Opposite CRT extreme | The opposite boundary of the selected parent CRT range; demonstrated as Target 2 in the bearish KOD example and part of the journey's destination logic. | PROVISIONAL | ROMEO-2025-S2 06:42, 14:27–14:41; ROMEO-2025-S3 |
| FVG confluence | Fair Value Gap aligned around an old extreme; presented as useful KOD confluence, not yet established as mandatory. | PROVISIONAL | ROMEO-2025-S2 17:39–17:57 |
| HTF context / LTF execution | Higher timeframe supplies parent CRT context/journey; lower timeframe supplies entry/confirmation evidence. Exact timeframe-pair mapping remains unresolved. | PROVISIONAL | ROMEO-2025-S3 03:13, 14:10, 16:21 |
| Key level | Context/reference level used to select meaningful price interactions; exact hierarchy and calculation pending. | UNRESOLVED | ROMEO-2025-S5 pending |
| SMT | Cross-market/correlated-market divergence concept used as later CRT context/confirmation; exact required/optional role pending. | UNRESOLVED | ROMEO-2025-S6 pending |
