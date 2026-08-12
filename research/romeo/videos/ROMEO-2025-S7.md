# Video Analysis — ROMEO-2025-S7

## Metadata
- Title: CRT secrets ep.7: Candle 3
- URL: https://www.youtube.com/watch?v=h7NCST2wPw8
- Published: 2025-09-21
- Duration: 25:31
- Creator: Romeo / @Romeotpt
- Analyst/date: ChatGPT / 2026-08-12
- Evidence pass: 1

## Evidence quality

Romeo's official Telegram directly posted the exact YouTube ID `h7NCST2wPw8`, announced Episode 7, and then posted a follow-up snippet framed around the question: `When will the CRT you want to trade fail vs succeed?` This provides strong first-party provenance for the source identity and confirms that failure/success discrimination is part of the episode's intended content.

Publication date and duration are independently indexed by Glasp and Video Highlight as 2025-09-21 and 25:31.

The detailed semantic extraction in this pass uses an indexed AI-generated summary because a first-party YouTube transcript was not directly accessible in the current research environment. Therefore all trading rules remain `PROVISIONAL` until directly verified against the original video/audio or an authoritative transcript.

## Relevance
- CRT relevance: critical
- Primary concepts: Candle 3, Candle 2 close, distribution phase, key-level dependence, Turtle Soup, OTE/50%, target progression, timeframe nesting, failure/success conditions
- Main engineering value: provides the first practical boundary for when Candle 3 may become eligible in real time and sharpens the first candidate setup family for backtesting

## Source-backed / summary-backed observations

| ID | Observation | Evidence type | Confidence |
|---|---|---|---|
| C3-O01 | Romeo's official Telegram identifies this as Episode 7 and separately highlights the question of when a CRT will fail versus succeed. | First-party Telegram | High |
| C3-O02 | Candle 3 is presented as the primary/safer phase for learners to trade, consistent with Episode 3. | Indexed Episode 7 summary + cross-source Episode 3 | High |
| C3-O03 | The summary states Candle 2 should be allowed to complete/close before Candle 3 is traded. | Indexed Episode 7 summary | High |
| C3-O04 | The summary frames the open of Candle 3 as the temporal start of the tradeable distribution phase after Candle 2 closes. | Indexed Episode 7 summary | Medium-High |
| C3-O05 | Candle 3 must be interpreted together with a valid key level; trading Candle 3 without key-level context is explicitly criticized as a beginner mistake. | Indexed Episode 7 summary | High |
| C3-O06 | Turtle Soup/liquidity manipulation remains part of the setup logic around Candle 3, but not as a context-free trigger. | Indexed Episode 7 summary | High |
| C3-O07 | The summary presents OTE/Fibonacci context around Candle 3 and gives 50% as an important expected level in an OTE-entry case. | Indexed Episode 7 summary | Medium-High |
| C3-O08 | If price approaches but does not reach 50% and instead gives Turtle Soup at the key level, Romeo adapts rather than insisting price must first touch 50%. | Indexed Episode 7 summary | High |
| C3-O09 | Strong trend conditions may produce shallower retracement than 50%; the summary says lower Fibonacci levels may be respected instead. | Indexed Episode 7 summary | Medium |
| C3-O10 | The summary says trades should be thought of as nested inside candles rather than fixed trader labels such as scalp/swing; higher/lower timeframe nesting remains central. | Indexed Episode 7 summary | High |
| C3-O11 | A daily CRT inside a weekly framework is used as an example, with the move framed toward completion of the parent candle objective. | Indexed Episode 7 summary | Medium-High |
| C3-O12 | When Candle 3 does not produce the expected entry, the instruction is to journal/observe rather than force a trade. | Indexed Episode 7 summary | High |

## Primary conclusion: Candle 3 is a gated state, not an ordinal label

The safe implementation interpretation is:

```text
PARENT CRT EXISTS
      ↓
CANDLE 2 IS ACTIVE
      ↓
WAIT — NO CANDLE-3 SIGNAL YET
      ↓
CANDLE 2 CLOSES
      ↓
CANDLE 3 OPENS
      ↓
KEY-LEVEL / TARGET CONTEXT VALID?
      ↓
LIQUIDITY / TURTLE-SOUP / CONFIRMATION STATE
      ↓
CANDLE-3 ENTRY CANDIDATE
      ↓
INDEPENDENT RISK ENGINE
```

The opening of Candle 3 appears to be a **necessary temporal boundary**, not sufficient evidence for entry by itself.

## Why this matters for look-ahead safety

A naive historical implementation might label three completed candles and then assume the third candle was always known to be `distribution` from its first tick.

That is unsafe.

At the first timestamp of Candle 3, the engine may know:

- Candle 1 history
- Candle 2 final OHLC, because Candle 2 has closed
- Candle 3 open price and opening timestamp
- higher-timeframe/key-level state known at that timestamp

It does **not** know:

- Candle 3 final high
- Candle 3 final low
- Candle 3 final close
- Candle 3 eventual direction
- whether Candle 3 ultimately succeeds or fails

Therefore `CANDLE_3_OPEN` may unlock eligibility, but later distribution behavior must still be observed causally.

## Candidate rules created

### C3-P001 — Candle 2 must be complete before Candle 3 is actionable
- Status: PROVISIONAL / HIGH CONFIDENCE
- Category: time / phase transition
- Human description: The engine must not use Candle-3 execution logic while Candle 2 is still active; Candle 2 close is a gating boundary.
- Evidence: C3-O03, C3-O04
- Engineering implication: `CANDLE_2_CLOSED` should be an explicit state transition event.

### C3-P002 — Candle 3 open begins eligibility, not automatic entry
- Status: PROVISIONAL
- Category: phase transition
- Human description: Candle 3 begins after Candle 2 closes, but its open does not itself constitute a trade signal.
- Evidence: C3-O04, C3-O05, C3-O06
- Engineering implication: distinguish `C3_ELIGIBLE` from `C3_ENTRY_CONFIRMED`.

### C3-P003 — Candle 3 requires key-level context
- Status: PROVISIONAL / HIGH CONFIDENCE
- Category: context
- Human description: Candle 3 should not be traded as a standalone ordinal pattern; it must be anchored to a valid key-level/narrative context.
- Evidence: C3-O05
- Cross-source support: ROMEO-2025-S5
- Engineering implication: Candle-3 detector consumes a `KeyLevelState` rather than emitting orders independently.

### C3-P004 — liquidity/manipulation evidence remains relevant
- Status: PROVISIONAL
- Category: manipulation
- Human description: Turtle Soup/liquidity behavior remains part of Candle-3 qualification, but exact mandatory/optional status depends on later reconciliation with SMT and Episode 8 failure rules.
- Evidence: C3-O06, C3-O08
- Cross-source support: ROMEO-2025-S6

### C3-P005 — 50% is important but must not be forced
- Status: PROVISIONAL
- Category: location / target / entry context
- Human description: 50% is an important OTE-related level in the demonstrated framework, but price need not always touch 50% before a valid Candle-3 trade can occur.
- Evidence: C3-O07, C3-O08, C3-O09
- Engineering implication: never encode `price_must_touch_50 = True` globally.

### C3-P006 — key-level Turtle Soup can override waiting for exact 50%
- Status: PROVISIONAL
- Category: adaptive qualification
- Human description: If price is near the expected retracement area but produces qualifying Turtle Soup at a valid key level, Romeo may act without requiring an exact 50% print.
- Evidence: C3-O08
- Blocker: exact `near 50%` tolerance and qualifying Turtle Soup semantics unresolved.

### C3-P007 — strong-trend state may alter retracement depth
- Status: HYPOTHESIS / MEDIUM CONFIDENCE
- Category: regime
- Human description: Strong trend conditions may produce shallower retracements than the 50% expectation.
- Evidence: C3-O09
- Engineering implication: do not hard-code one Fibonacci retracement threshold before regime/context evidence is resolved.

### C3-P008 — Candle 3 should remain nested in a parent timeframe hierarchy
- Status: PROVISIONAL
- Category: timeframe architecture
- Human description: Candle-3 execution belongs inside a larger candle/context hierarchy; the example of Daily CRT inside Weekly context reinforces nested-candle analysis.
- Evidence: C3-O10, C3-O11
- Engineering implication: every Candle-3 candidate must carry `parent_context_timeframe` and `trade_candle_timeframe`.

### C3-P009 — missed/absent Candle 3 is a no-trade outcome
- Status: PROVISIONAL / HIGH CONFIDENCE
- Category: no-trade governance
- Human description: If the expected Candle-3 entry does not materialize, the correct action is to journal and move on, not force an alternative trade.
- Evidence: C3-O12
- Engineering implication: `NO_SIGNAL` is a valid terminal state for a candidate journey.

### C3-P010 — failure/success discrimination belongs inside Candle-3 qualification
- Status: PROVISIONAL / RESEARCH DIRECTIVE
- Category: invalidation
- Human description: Romeo's own Telegram specifically advertises Episode 7 as teaching when the CRT being traded will fail versus succeed; the engine therefore needs explicit pre-entry/early-state failure features rather than assuming every Candle 3 is valid.
- Evidence: C3-O01
- Blocker: Episode 8 is expected to formalize the failure taxonomy and must be reconciled before freezing this predicate.

## Candidate Candle-3 state machine

```text
WAIT_FOR_PARENT_CONTEXT
        ↓
PARENT_CRT_SELECTED
        ↓
KEY_LEVEL_IDENTIFIED
        ↓
CANDLE_2_ACTIVE
        ↓
WAIT_FOR_CANDLE_2_CLOSE
        ↓
CANDLE_2_CLOSED
        ↓
CANDLE_3_OPENED
        ↓
C3_ELIGIBLE
        ↓
CHECK LOCATION / TARGET STATE
        ↓
CHECK MANIPULATION EVIDENCE
   ├── LOCAL TURTLE SOUP
   └── SMT / CROSS-MARKET EVIDENCE (if allowed)
        ↓
CHECK CONFIRMATION
        ↓
C3_ENTRY_CANDIDATE
        ↓
RISK ENGINE
        ↓
TARGET MANAGEMENT
```

The exact `CHECK CONFIRMATION` predicate remains unresolved.

## OTE / 50% caution

The indexed summary describes Candle 3 using OTE/Fibonacci language and emphasizes 50%, but also explicitly says the trader should adapt if a valid key-level Turtle Soup appears before an exact 50% touch.

Therefore the first implementation must model 50% as a **state/feature**, not a mandatory global equality condition:

```python
RetracementState(
    parent_range_high,
    parent_range_low,
    midpoint_50,
    current_retracement_fraction,
    touched_50,
    near_50,
    key_level_interaction,
    regime_state,
)
```

`near_50` must remain undefined until source evidence or a separately governed quantitative hypothesis sets a tolerance.

## Timeframe-scope caution

The indexed Episode 7 summary mentions Weekly, Daily, Monthly, 4H and even 1H in different contexts. Episode 4 established the initial public parent whitelist `{H4, D1, W1}` for this project and we use `W1 → D1 → H4` when expressing top-down hierarchy.

Do **not** expand the first candidate strategy to Monthly or 1H parent candles from this summary alone. Record those as later/advanced scope until direct-source verification and strategy versioning justify inclusion.

## Cross-source reconciliation

### Episode 3
- Candle 3 is the preferred learning/trading phase.
- Episode 7 strengthens this with a causal boundary: Candle 2 must complete first.

### Episode 5
- Key level is context, not entry.
- Episode 7 reinforces that Candle 3 without a key level is invalid/low quality.

### Episode 6
- Local Turtle Soup may not always be the only manipulation evidence if SMT supplies the cross-market role.
- Episode 7 does not yet resolve whether every valid Candle 3 requires local Turtle Soup.

### Episode 8
- Must provide the formal failure filters needed to decide when an apparent Candle 3 should be rejected.

## What this source does NOT yet establish

Do not guess:

- exact deterministic definition of Candle 1
- exact deterministic definition of Candle 2
- whether Candle 2 manipulation must be wick-based, close-based or cross-market
- exact Candle-3 entry trigger after the open
- whether entry occurs literally at Candle-3 open or only after LTF confirmation
- exact key-level selection hierarchy
- exact OTE/Fibonacci anchor definition used in every setup
- exact `near 50%` tolerance
- exact regime definition for `strong trend`
- exact stop-loss placement
- exact target hierarchy and partial-management rules
- exact no-trade/failure conditions
- exact role of SMT within Candle 3
- exact canonical execution timeframe beneath W1/D1/H4

## New questions created

1. Is `Candle 2 closed` sufficient to label the next candle `Candle 3`, or must the prior sequence first satisfy an explicit CRT predicate?
2. Does Candle-3 entry occur at the parent candle open, or only after an LTF confirmation that occurs after that open?
3. What exact event turns `C3_ELIGIBLE` into `C3_ENTRY_CONFIRMED`?
4. Is Turtle Soup mandatory for Candle 3, or can SMT fully substitute for it?
5. What exact key-level relation is required at Candle-3 open?
6. Is the 50% level an entry expectation, a target, a reaction point, or different roles in different setup families?
7. How is `near 50%` quantified without overfitting?
8. What exactly defines the strong-trend exception to 50% retracement?
9. What are the explicit pre-entry failure conditions teased in Episode 7?
10. What does Episode 8 add or supersede regarding Candle-3 failure?

## Research consequence

Episode 7 gives the project its clearest candidate for the **first backtestable strategy family**:

```text
CANDLE-3 REACTION/EXPANSION CANDIDATE
    + valid parent CRT
    + valid key level
    + Candle 2 completed
    + Candle 3 opened
    + causal manipulation evidence
    + causal confirmation
    + explicit failure filters
```

We are still missing the final two pieces needed before formalizing that candidate:

1. explicit failure/invalidation taxonomy — Episode 8
2. full execution reconciliation, including SMT — Episode 9

## Promotion decision

**No C3-Pxxx rule is promoted to `VERIFIED`.**

However, `Candle 2 close → Candle 3 eligibility` and `Candle 3 requires key-level context` are now high-confidence candidate constraints for the first CRT-v0.1 setup family, pending direct-source verification and Episode 8/9 reconciliation.
