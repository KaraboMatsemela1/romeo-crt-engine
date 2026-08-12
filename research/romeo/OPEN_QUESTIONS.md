# Open Strategy Questions

These must be answered from evidence or deliberately scoped out before freezing the first strategy candidate.

## Turtle Soup primitive

- What exact conditions make a previous high/low an eligible Turtle Soup reference extreme?
- Do equal highs/lows count, and how should clusters be handled?
- Is there a minimum age or minimum separation for the old high/low?
- Must price merely trade beyond the extreme, or must a wick/body/close condition occur?
- Is there a minimum or maximum sweep distance?
- Is a close back inside the reference range required?
- What precisely confirms failure of continuation after the sweep?
- How many bars may elapse between sweep and confirmation?
- When is a swept extreme considered invalid/consumed?
- Are there multiple Turtle Soup variants that need separate formal specifications?
- What time/session conditions turn a generic liquidity sweep into a valid Romeo Turtle Soup trade?

## CRT range and timeframe semantics

- What is the exact CRT range definition?
- What candles/timeframes are permitted to define the range?
- How is a CRT candle selected versus ignored?
- How does a higher-timeframe CRT map deterministically to lower-timeframe Turtle Soup behaviour?
- How are inside bars, overlapping ranges and nested CRTs handled?
- What exactly is the role of the 50% level: target, reaction zone, invalidation/failure filter, or multiple roles?
- What makes a parent CRT `active` or `pending` before the target is reached?
- What determines bullish versus bearish CRT direction in real time?
- What event moves a parent CRT from `ACCUMULATION` into `MANIPULATION`?
- What event moves a parent CRT from `MANIPULATION` into `DISTRIBUTION` / Candle 3?
- Is Candle 3 defined by calendar position, price behavior, confirmation, or a combination?
- What are the canonical higher-timeframe → lower-timeframe pairs?
- Episode 4 scopes initial parent candles to H4/D1/W1; what exact evidence defines the execution timeframe beneath each one?
- Can a parent candle be selected immediately at its open, or only after some internal structure/event appears?
- What candle-shape properties are actually strategy inputs versus descriptive observations?

## Kiss of Death

- What observable ex-ante conditions distinguish a KOD candidate from earlier Turtle Soups before the target is hit?
- How do we avoid defining KOD retrospectively as `the final Turtle Soup before target`, which would create look-ahead bias?
- What makes a CRT journey `late enough` for KOD qualification using only information available at that time?
- Can interaction with the CRT 50% level act as a causal journey-stage boundary for KOD qualification?
- Must KOD occur after price has already interacted with the CRT 50% level?
- Is the demonstrated sequence `first Turtle Soup → 50% → bounce → KOD → opposite extreme` mandatory or merely one example?
- What exactly did Romeo mean by preferring KOD in the `lower 25%` of the range, and how does that map directionally for bearish/bullish setups?
- Is KOD allowed at OTE instead of the 25% location, and what is the exact OTE definition used here?
- Is FVG aligned with an old high/low mandatory, preferred, or optional confluence?
- Is lower-timeframe Model #1 mandatory for KOD execution or only one supported entry model?
- What invalidates a KOD candidate before lower-timeframe entry confirmation?
- What is the exact bullish mirror of the bearish KOD sequence?

## Journey / phase progression

- Is the lower-timeframe sequence `Turtle Soup → true MSS → Model #1 → KOD` mandatory, optional, overlapping, or example-specific?
- What exactly is Romeo's `true market structure shift`, and how is it distinguished from a fake/ordinary MSS?
- What is the exact breaker concept mentioned alongside true MSS?
- Can Model #1 occur multiple times within one parent CRT journey?
- Can Turtle Soup occur multiple times before Candle 3 and, if so, how should events be ranked?
- How is `target pending` represented in real time without hindsight?
- What objective families exist: liquidity targets, imbalance/rebalancing targets, 50% targets, or others?
- What hierarchy chooses the primary target before entry?
- Does every CRT variant share one journey state machine, or do multiple setup-specific state machines exist?
- How does the selected parent candle's open price influence phase progression?
- What intrabar evidence lets the engine infer Candle 2 manipulation before the parent candle has closed?

## Context / liquidity

- What liquidity levels are required vs optional?
- How is higher-timeframe direction/context established?
- What exact hierarchy determines a valid key level?
- Is SMT required, optional confirmation, or a failure filter depending on setup type?
- What explicit no-trade conditions exist?

## Entry / confirmation

- What exact event confirms entry?
- Is displacement required? If so, how is it measured?
- What exactly constitutes Romeo's `true market structure shift`?
- What is the deterministic definition of Model #1?
- What makes a candle `thick` or otherwise eligible for Model #1?
- Are FVGs required or probability enhancers only?

## Invalidation / exit

- What invalidates a candidate before entry?
- Where is stop loss placed for each entry model?
- How is the target selected?
- Are partials/breakeven/trailing part of the methodology?
- When is `Candle 3` considered complete or failed?

## Time / markets / candle construction

- What sessions/trading windows are valid?
- What does Romeo mean operationally when saying time is more important than price?
- What exact features define `time meets price`?
- What timezone/session anchor defines Romeo's H4 candles?
- What exact H4 start times are valid?
- What is the canonical Daily candle open/close?
- What is the canonical Weekly candle open/close?
- Do Forex, indices, metals and crypto require different candle-boundary calendars?
- How is DST handled for all parent and execution candles?
- Which instrument classes and timeframe combinations are in scope?
- Are H4/D1/W1 boundaries provider-native, New-York anchored, London anchored, or otherwise normalized?

## Backtesting / information-set safety

- For each phase label, what information was actually available at timestamp `t`?
- Which retrospective labels are allowed for research annotation but prohibited as live signal inputs?
- How do we ensure Candle 3 completion is not used to justify an entry that occurred during Candle 2?
- How do we ensure KOD is never labeled from knowledge of the future target hit?
- How do we ensure final parent-candle high/low/close/body/wicks are never used for an intrabar decision before those values existed?
- What minimum event granularity is required to reconstruct candle snapshots faithfully: ticks, 1m bars, or another base interval?
- How are provider bar-boundary discrepancies detected and prevented from changing CRT labels silently?

## Corpus/versioning

- Which 2024 foundation rules were refined, superseded or narrowed by 2025 CRT Secrets?
- Which 2025 rules were refined or superseded by 2026 CRTology?
- Should the engine support distinct doctrine versions instead of silently merging all public teaching into one strategy?
