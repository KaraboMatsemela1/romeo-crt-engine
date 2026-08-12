# Video Analysis — ROMEO-2025-S9

## Metadata
- Title: CRT secrets ep.9: Connecting the dots
- URL: https://www.youtube.com/watch?v=2sxdsgcIeYA
- Published: unresolved in this pass
- Duration: unresolved in this pass
- Creator: Romeo / @Romeotpt
- Analyst/date: ChatGPT / 2026-08-12
- Evidence pass: 1

## Evidence quality

Romeo's official Telegram directly posts the exact YouTube ID `2sxdsgcIeYA` and explicitly says Episode 9 answers three questions: which entry models to use, how to use SMT correctly while trading, and how to frame a trade logically. This gives strong first-party provenance for the source identity and intended scope of the episode.

The detailed semantic extraction in this pass uses an indexed AI-generated YouTube summary because a first-party YouTube transcript was not directly accessible in the research environment. Therefore all strategy semantics remain `PROVISIONAL` until checked against the original video/audio or an authoritative transcript.

Publication date and duration are deliberately left unresolved rather than inferred from Telegram chronology.

## Relevance
- CRT relevance: critical
- Primary concepts: end-to-end trade framing, higher-timeframe narrative, key-level/liquidity context, SMT, Model #1, true MSS, Turtle Soup, stop placement, targets, time exits, price exits
- Main engineering value: reconciles Episodes 1–8 into the first candidate end-to-end decision pipeline

## Source-backed / summary-backed observations

| ID | Observation | Evidence type | Confidence |
|---|---|---|---|
| DOT-O01 | Romeo's official Telegram says Episode 9 answers which entry models to use, how to use SMT correctly, and how to frame a trade logically. | First-party Telegram | High |
| DOT-O02 | The indexed summary frames trade preparation as a stack: higher-timeframe candle/narrative → daily/liquidity context → market profile/high-low behavior → lower-timeframe entry model. | Indexed Episode 9 summary | High |
| DOT-O03 | The indexed summary says the public execution family is narrowed to Model #1 or true market structure shift. | Indexed Episode 9 summary | High |
| DOT-O04 | Model #1 is treated as a specific candle, not a broad multi-candle zone; in the bearish example a close below that candle is important and a retrace back into it can precede continuation. | Indexed Episode 9 summary | Medium-High |
| DOT-O05 | True MSS is described using an observable lower-timeframe sequence involving a low, higher low, and a break above a relevant high in the bullish example, after contextual SMT. | Indexed Episode 9 summary | Medium-High |
| DOT-O06 | SMT is filtered by higher-timeframe direction: bullish SMT is sought in bullish HTF context and bearish SMT in bearish HTF context. | Indexed Episode 9 summary | High |
| DOT-O07 | The Bitcoin/Ethereum example uses one market taking a low while the other does not as the SMT relationship. | Indexed Episode 9 summary | High |
| DOT-O08 | Stop placement in the demonstrated bullish framework is tied below the Turtle Soup low / structural invalidation extreme rather than an arbitrary fixed distance. | Indexed Episode 9 summary | High |
| DOT-O09 | The demonstrated target includes previous-day high; the summary also says exits may be driven by time or by price. | Indexed Episode 9 summary | Medium-High |
| DOT-O10 | Romeo's workflow expects reactions around old liquidity pools and FVG/imbalance context rather than assuming straight-line movement. | Indexed Episode 9 summary | Medium-High |
| DOT-O11 | The episode references a London-session execution example and a Tuesday-to-Wednesday daily slice, showing that timing belongs in the trade frame. | Indexed Episode 9 summary | Medium |
| DOT-O12 | Romeo's Telegram instruction to watch Episode 9 multiple times and its explicit scope indicate this is intended as a reconciliation/operational lecture rather than a new isolated pattern. | First-party Telegram | High |

## Primary conclusion: strategy execution is context-first, entry-model-last

Episode 9 gives the clearest current ordering:

```text
HIGHER-TIMEFRAME NARRATIVE
        ↓
PARENT CRT / CANDLE STATE
        ↓
KEY LEVEL / LIQUIDITY CONTEXT
        ↓
TARGET + DIRECTION STATE
        ↓
SMT / MANIPULATION CONTEXT
        ↓
ENTRY MODEL
   ├── MODEL #1
   └── TRUE MSS
        ↓
STRUCTURAL STOP
        ↓
TIME / PRICE TARGET MANAGEMENT
        ↓
RISK ENGINE
```

The entry model is deliberately near the end. The project must not scan Model #1 or MSS globally and then retrofit narrative afterward.

## Candidate rules created

### DOT-P001 — trade framing is top-down and context-first
- Status: PROVISIONAL / HIGH CONFIDENCE
- Category: orchestration
- Human description: A trade is framed by higher-timeframe narrative/candle state, liquidity/key-level context and current market state before lower-timeframe entry selection.
- Evidence: DOT-O01, DOT-O02
- Engineering implication: entry detectors consume a pre-qualified `TradeContext`; they do not create context themselves.

### DOT-P002 — first candidate entry families are Model #1 and true MSS
- Status: PROVISIONAL / HIGH CONFIDENCE
- Category: execution scope
- Human description: Episode 9 narrows the public entry decision to two families: Model #1 or true market structure shift.
- Evidence: DOT-O01, DOT-O03
- Engineering implication: CRT-v0.1 should not add generic FVG, breaker, order-block or arbitrary pattern entries unless separately specified and evidence-backed.

### DOT-P003 — Model #1 remains a specific-candle model
- Status: PROVISIONAL
- Category: entry
- Human description: Model #1 is anchored to a particular candle rather than an arbitrary zone; close behavior around that candle participates in confirmation.
- Evidence: DOT-O04
- Cross-source support: ROMEO-2025-S1
- Blocker: exact bullish/bearish eligibility, `thick` semantics and close predicate still require direct-source resolution.

### DOT-P004 — true MSS is context-qualified and structural
- Status: PROVISIONAL
- Category: entry / confirmation
- Human description: True MSS is not any generic break of structure; the demonstrated bullish sequence follows contextual SMT/liquidity behavior and then a specific lower-timeframe structural shift.
- Evidence: DOT-O05, DOT-O07
- Cross-source support: ROMEO-2025-S5, ROMEO-2025-S6
- Blocker: exact swing construction and the phrase `high that broke the low` require direct visual/transcript validation.

### DOT-P005 — SMT direction must align with HTF direction
- Status: PROVISIONAL / HIGH CONFIDENCE
- Category: cross-market filter
- Human description: Bullish SMT is sought under bullish higher-timeframe context and bearish SMT under bearish higher-timeframe context.
- Evidence: DOT-O06
- Cross-source support: ROMEO-2025-S8 directional-alignment filter
- Engineering implication: SMT does not independently choose direction; it is filtered by the already-established context direction.

### DOT-P006 — SMT remains context/confirmation, not direct entry
- Status: PROVISIONAL / HIGH CONFIDENCE
- Category: entry governance
- Human description: SMT contributes to trade framing, but execution still requires Model #1 or true MSS.
- Evidence: DOT-O01, DOT-O03, DOT-O05, DOT-O07
- Cross-source support: ROMEO-2025-S6, ROMEO-2025-S8
- Engineering implication: no `SMTEvent -> OrderIntent` path.

### DOT-P007 — stop is structural, beyond the Turtle Soup invalidation extreme
- Status: PROVISIONAL / HIGH CONFIDENCE
- Category: risk / invalidation
- Human description: In the demonstrated bullish framework, stop loss is placed below the Turtle Soup low rather than at an arbitrary fixed distance.
- Evidence: DOT-O08
- Engineering implication: stop calculation must reference the qualifying structural event and include execution buffer/slippage policy separately.
- Blocker: exact buffer beyond the extreme is not specified and must not be invented.

### DOT-P008 — exits may be price-based or time-based
- Status: PROVISIONAL
- Category: management
- Human description: Episode 9 permits trade exit logic based on reaching price objectives and/or time conditions.
- Evidence: DOT-O09, DOT-O11
- Engineering implication: eventual strategy spec needs separate `price_exit` and `time_exit` policies rather than assuming every trade remains open until one price target is hit.
- Blocker: exact time-exit rules remain unresolved.

### DOT-P009 — target must come from the pre-trade narrative
- Status: PROVISIONAL
- Category: target
- Human description: The demonstrated previous-day-high target is selected from surrounding narrative/liquidity context, not as a universal fixed target for every CRT.
- Evidence: DOT-O02, DOT-O09, DOT-O10
- Engineering implication: target selection belongs in `TradeContext` before order approval.

### DOT-P010 — Episode 9 closes the SMT execution-governance loop, but not all pair semantics
- Status: RESEARCH GOVERNANCE
- Category: corpus reconciliation
- Human description: Episode 9 confirms SMT should be directionally filtered and followed by an approved entry model, but exact pair polarity/reference synchronization still requires explicit source-backed relationship definitions.
- Evidence: DOT-O01, DOT-O06, DOT-O07
- Engineering implication: keep the versioned SMT relationship registry and synchronized replay constraints from Episode 6.

## Reconciled end-to-end candidate flow

The first serious CRT-v0.1 research candidate can now be expressed as:

```text
1. BUILD CAUSAL MARKET STATE
   - normalized W1 → D1 → H4 hierarchy
   - valid candle boundaries / timezone
   - no future parent-candle OHLC

2. ESTABLISH HTF NARRATIVE
   - parent CRT selected
   - context direction known
   - target state known

3. SELECT KEY LEVEL / LIQUIDITY CONTEXT
   - destination or reaction-origin role
   - level reached/not reached state
   - incomplete CRT filter

4. CANDLE-3 GATE
   - Candle 2 completed
   - Candle 3 opened
   - setup still eligible

5. FAILURE FILTERS
   - direction aligned
   - Target 1 / 50% state not misread
   - no confirmed SMT conflict against intended target
   - CRT completeness acceptable

6. MANIPULATION / CROSS-MARKET STATE
   - local Turtle Soup and/or qualifying SMT evidence
   - SMT direction filtered by HTF context

7. ENTRY MODEL
   - Model #1
     OR
   - true MSS

8. STRUCTURAL INVALIDATION
   - stop beyond qualifying Turtle Soup / structural extreme
   - no arbitrary fixed-pip stop invented from source gaps

9. TARGET / EXIT
   - price objective from narrative
   - optional later target stages
   - time exit if strategy version defines it

10. INDEPENDENT RISK ENGINE
   - position sizing
   - max exposure
   - portfolio/daily loss controls
```

This is not yet frozen. Several predicates remain unresolved.

## True MSS candidate semantics — use caution

The indexed summary describes the bullish true-MSS example roughly as:

```text
contextual bullish SMT
      ↓
low forms
      ↓
higher low forms
      ↓
price breaks above the relevant high that caused/broke the prior low
      ↓
true MSS candidate
      ↓
entry inside the shift range
```

The wording is not precise enough to code safely from text alone. The project must not substitute a generic ICT/BOS algorithm and call it Romeo's true MSS.

Required direct-source questions:

- Which exact high is the reference high?
- Does the break require wick or close?
- What qualifies the prior low/high as structural?
- What is the exact entry zone after the shift?
- Is an FVG required in that zone?
- Must SMT exist first, or can true MSS qualify without SMT in other setup families?

## Model #1 candidate semantics — current reconciliation

Across Episodes 1 and 9, Model #1 continues to look like a **specific candle-based initiation/entry model**, not a broad zone.

Current safe abstraction:

```text
QUALIFYING MODEL-1 CANDLE
      ↓
REQUIRED CLOSE / DISPLACEMENT CONDITION
      ↓
RETRACE INTO MODEL-1 AREA
      ↓
ENTRY CANDIDATE
```

Still unresolved:

- exact qualifying candle body/wick geometry
- what `thick` means numerically, if anything
- whether FVG is required or only confluence
- exact close threshold
- exact retrace entry price
- exact bullish inverse

Therefore Model #1 remains blocked for deterministic implementation until direct visual/source reconciliation is complete.

## Stop-loss model emerging

Episode 9 provides the clearest stop reference to date:

```text
BULLISH QUALIFYING TURTLE SOUP
    reference_low = turtle_soup_low
    stop_reference = below(reference_low)

BEARISH mirror hypothesis
    reference_high = turtle_soup_high
    stop_reference = above(reference_high)
```

Only the bullish example is considered directly supported in this pass. The bearish mirror remains a symmetry hypothesis until explicitly verified.

The project must separate:

```text
strategy stop reference
from
execution buffer
```

Example design:

```python
StructuralStop(
    reference_type="TURTLE_SOUP_EXTREME",
    reference_price=...,
    side="BELOW" | "ABOVE",
    buffer_policy="UNRESOLVED",
)
```

Do not optimize the buffer before the source rule is frozen.

## Exit model emerging

Episode 9 implies two different exit dimensions:

```text
PRICE EXIT
- target derived from narrative/liquidity
- example: previous-day high
- CRT T1/T2 framework remains relevant from earlier episodes

TIME EXIT
- exit because the valid trading/time window has ended or the trade thesis expires in time
```

The exact time-exit predicate is unresolved and must not be approximated from the example alone.

## Important architectural consequence: TradePlan becomes first-class

The engine should construct an immutable candidate plan before risk approval:

```python
TradePlan(
    timestamp,
    strategy_version,
    instrument,
    direction,
    context_timeframe,
    trade_candle_timeframe,
    execution_timeframe,
    parent_crt_id,
    key_level_id,
    context_direction,
    smt_state,
    manipulation_state,
    entry_model,          # MODEL_1 or TRUE_MSS
    entry_reference,
    stop_reference,
    price_targets,
    time_exit_policy,
    evidence_ids,
)
```

The risk engine then decides whether this plan may become an order.

This preserves the intended architecture:

```text
RESEARCH / CONTEXT / STRATEGY
            ↓
        TRADE PLAN
            ↓
        RISK ENGINE
            ↓
        ORDER INTENT
            ↓
         EXECUTION
```

## Anti-look-ahead requirements added by Episode 9

1. **HTF narrative must exist before the entry.** Do not use future weekly/daily closes to justify an earlier LTF trade.
2. **SMT must be known causally across synchronized markets.** Episode 6 safeguards remain mandatory.
3. **Entry model must trigger after context exists.** Do not scan a winning Model #1/MSS first and retrospectively discover context.
4. **Stop reference must exist at order time.** Do not use the eventual lowest low/highest high of the finished move.
5. **Target must be selected before outcome.** Do not choose previous-day high, 50%, CRT extreme or another level based on which one happened to be reached.
6. **Time exit policy must be frozen before testing.** Do not exit at the historically best timestamp.

## What Episode 9 materially resolves

Compared with the previous open-question set, Episode 9 gives the strongest evidence so far for:

- context first, entry last
- Model #1 / true MSS as the two public entry families
- SMT filtered by HTF direction
- SMT not being a direct entry
- structural Turtle-Soup-extreme stop reference
- target chosen from trade narrative
- price-based and time-based exit dimensions

## What remains unresolved after Episode 9

- exact Model #1 deterministic geometry
- exact true MSS structural algorithm
- exact HTF/LTF mapping for every parent timeframe
- exact key-level marking hierarchy
- exact SMT pair registry and polarity semantics
- whether local Turtle Soup is mandatory when SMT is present
- exact stop buffer
- exact price-entry location after true MSS
- exact time-exit windows
- exact session/candle anchors
- exact Target 1/Target 2 hierarchy by setup family
- exact incomplete-CRT predicate
- exact KOD ex-ante classifier
- exact Candle-1/Candle-2 selection algorithm

## First CRT-v0.1 strategy-candidate boundary

Episode 9 is enough to justify drafting, but **not freezing**, a first strategy candidate with the following scope:

```text
SETUP FAMILY:
    directionally aligned Candle-3 CRT

CONTEXT:
    W1 → D1 → H4 hierarchy
    valid parent CRT
    valid key level
    untouched/appropriate target state

FILTERS:
    no countertrend setup
    no confirmed SMT conflict
    no incomplete/unknown CRT

MANIPULATION:
    local Turtle Soup and/or explicitly validated SMT path

ENTRY:
    Model #1 OR true MSS

STOP:
    structural Turtle Soup extreme reference

EXIT:
    narrative-defined price target
    time-exit policy only when separately frozen
```

Because the key entry predicates remain partly unresolved, this candidate is `DRAFT / BLOCKED`, not ready for broad backtesting.

## Next research task

`ROMEO-2025-S10 — A clean close` should be analyzed next for corpus completeness and any clarification on close semantics, key-level selection, draw-on-liquidity, journaling or discipline.

After Episode 10, the project should perform a **Phase 1 reconciliation pass** across Episodes 1–10 rather than immediately coding. That pass should produce:

1. a contradiction matrix,
2. evidence-status table,
3. unresolved blockers ranked by implementation impact,
4. draft `CRT_STRATEGY_SPEC.md`,
5. known-example fixture list,
6. explicit `DO NOT IMPLEMENT YET` list.

## Promotion decision

**No DOT-Pxxx rule is promoted to VERIFIED.**

Episode 9 is the strongest integration source so far and is sufficient to draft the end-to-end decision model, but direct visual/transcript verification is still required before deterministic entry/stop/exit rules are frozen.
