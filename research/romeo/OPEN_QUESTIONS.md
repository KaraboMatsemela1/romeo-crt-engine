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
- Is Episode 5's pre-key-level KOD the same semantic subtype as Episode 2's final-Turtle-Soup KOD, or are these nested roles at different parent journeys?

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
- Episode 6 suggests AMD order may not be rigid; what exact alternative sequences are valid and how are they identified causally?

## Candle 3

- Is `Candle 2 closed` sufficient to label the next candle `Candle 3`, or must Candle 1/2 first satisfy a complete CRT predicate?
- Does Candle-3 execution occur literally at the parent Candle-3 open, or only after lower-timeframe confirmation after that open?
- What exact event turns `C3_ELIGIBLE` into `C3_ENTRY_CONFIRMED`?
- Must Candle 3 open from a particular side of the Candle-2 range or key level?
- Is a local Turtle Soup mandatory for Candle 3, or can SMT fully substitute for local manipulation evidence?
- If SMT substitutes for Turtle Soup, which instrument must show the actual Candle-3 confirmation?
- What exact relation between Candle-3 open and the key level is required?
- Is 50% primarily an expected entry retracement, a target, a reaction point, or different roles in different setup families?
- How should `near 50%` be quantified without curve fitting?
- What exact regime condition allows shallower-than-50% retracement?
- Does strong trend change only entry retracement depth, or also target/stop logic?
- What specific pre-entry conditions make a Candle-3 CRT likely to fail versus succeed?
- Does reaching 50% before Candle 3 begins strengthen, weaken, complete, or invalidate the intended setup?
- What happens if Candle 3 opens but no valid LTF confirmation appears before the parent candle closes?
- Can a valid CRT journey terminate as `NO_SIGNAL` without being labeled a failed strategy setup?
- Which target is primary for Candle 3: 50%, Candle-1 extreme, parent key level, pending HTF target, or setup-specific hierarchy?
- What exact event completes Candle 3 successfully?
- What exact event invalidates Candle 3 before entry?
- What exact event invalidates Candle 3 after entry?
- Does Episode 8 supersede any Episode-7 Candle-3 assumptions?

## Key levels

- What exact structures qualify as Romeo price key levels?
- What exact structures qualify as time key levels?
- Are old highs/lows always valid key levels or only under additional context?
- How are multiple W1 → D1 → H4 key levels ranked when they conflict or overlap?
- What numerical tolerance defines `at the key level`?
- Does a touch, wick through, body trade-through, or candle close mark a level as reached?
- What event marks a key level as consumed or invalidated?
- Can a destination key level become a reaction-origin key level immediately after being reached?
- For `journey-to-key-level` trades, what exact event supplies entry and where does the position exit relative to the level?
- For `reaction-from-key-level` trades, must price first hit/purge the level before any LTF confirmation can qualify?
- What separates the fake MSS before the key level from the true MSS at the level?
- Does the true MSS require a specific time window as well as the price level?
- Is SMT mandatory for identifying the real key-level reaction or only additional confluence?
- Does key-level type determine which entry models are legal?

## SMT / cross-market context

- What does `SMT` expand to in Romeo's own terminology?
- What exact pair/group registry does Romeo use for ES/NQ/Dow, Gold/Silver, BTC/ETH and FX/DXY?
- For each pair/group, is the expected relationship correlated, inverse, or context-dependent?
- Which market is `the one that takes` and which is `the one that doesn't`, and what directional inference follows?
- Does the non-take represent weakness, strength, or only divergence until confirmation?
- What corresponding high/low definition is used across the pair?
- What synchronization window is valid between the two markets' reference events?
- Is a wick through sufficient, or must a close beyond the corresponding level occur?
- What happens when both instruments take the level?
- What happens when neither instrument takes the level?
- Is SMT required only at key levels, or can it qualify the journey toward a key level?
- Is SMT mandatory for any CRT setup family, or always optional context/confluence?
- Can SMT fully substitute for a local Turtle Soup? Under exactly what conditions?
- Is SMT an entry confirmation, manipulation detector, target selector, failure filter, or multiple roles depending on state?
- Does true MSS need to form on the primary instrument, the comparison instrument, or either?
- Which instrument's Model #1 is used for actual execution?
- How is the instrument to trade selected after SMT appears?
- How do different market sessions and holidays affect pair validity?
- How stale may one market's data be before SMT becomes `UNKNOWN`?
- How does Episode 8 use SMT as a CRT failure condition?
- What does Episode 9 refine about `correct SMT usage`?
- Does SMT alter the Candle 2 → Candle 3 transition?

## Context / liquidity

- What liquidity levels are required vs optional?
- How is higher-timeframe direction/context established?
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
- How do we prevent a key level from being labeled `important` only because a future reversal later occurred there?
- How do we define destination/reaction roles ex ante rather than from the completed path?
- How do we prevent pair-selection hindsight by fixing SMT relationships before the signal timestamp?
- How do we ensure both instruments are compared using data available at the same causal timestamp?
- How do we prevent stale/missing comparison data from becoming a false SMT non-take?
- How are differing session calendars normalized without fabricating cross-market observations?
- How are corresponding highs/lows chosen without selecting the pair of extremes that looks best after the outcome?
- How do we prevent final Candle-3 direction/high/low/close from being used at Candle-3 open?
- How do we separate `C3_ELIGIBLE`, `C3_ENTRY_CONFIRMED`, `C3_NO_SIGNAL`, and `C3_FAILED` without using future outcomes to label earlier states?

## Corpus/versioning

- Which 2024 foundation rules were refined, superseded or narrowed by 2025 CRT Secrets?
- Which 2025 rules were refined or superseded by 2026 CRTology?
- Should the engine support distinct doctrine versions instead of silently merging all public teaching into one strategy?
