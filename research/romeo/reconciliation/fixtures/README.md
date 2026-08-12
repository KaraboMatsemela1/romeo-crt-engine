# P0 Fixture Index

**Doctrine:** `CRT_SECRETS_2025`  
**Candidate:** `CRT-C3-ALIGNED-v0.1-DRAFT`  
**Purpose:** causal, chart-grounded closure evidence for P0 blockers.

## Fixture statuses

- `PRECOMMITMENT_ONLY` — proves thesis existed before outcome but does not expose enough chart state to close alpha rules.
- `RULE_CLARIFICATION` — first-party statement narrows a rule/subtype but is not itself a fully reconstructable causal trade fixture.
- `CANDIDATE` — chart state is partially recoverable; not yet sufficient for closure.
- `POSITIVE` — source-grounded accepted example with causal state fully annotated.
- `NEGATIVE` — source-grounded rejected/counterexample with causal state fully annotated.
- `REJECTED` — fixture contaminated by hindsight, ambiguous source identity, or insufficient information.

## Current fixtures

| Fixture | Source | Class | P0 closure credit | Notes |
|---|---|---|---|---|
| `P0-FIX-001` | `ROMEO-2025-LIVE` / `1EK-LMwgJ3c` | `PRECOMMITMENT_ONLY` | none | First-party Telegram proves the live thesis preceded the later outcome commentary; chart-level P0 fields remain unavailable through current interface. |
| `P0-FIX-002` | Romeo official Telegram / NQ clarification | `RULE_CLARIFICATION` | partial P0-04 | Romeo explicitly describes bearish ideal reaction as candle open → stab into an old CRTH → dump. Safely adds `OLD_CRTH` as a source-backed bearish Turtle Soup reference subtype; does not resolve oldness, confirmation, expiry, consumption or bullish mirror. |

## Required closure coverage

Each active P0 blocker should ultimately have at least five positive and five negative/counterexample fixtures, with causal information sets and source timestamps.

Rule-clarification fixtures can narrow domain taxonomies, but they do **not** replace the positive/negative causal chart fixtures required for final closure.

### P0-01 Parent CRT
Need competing parent candidates plus the source-specific selection/expiry decision.

### P0-02 Key Level
Need candidate levels, selected level/role, reach state and rejected pre-level patterns.

### P0-03 Calendar
Need visible chart timestamps/timezone sufficient to reproduce H4/D1/W1 construction across instruments/sessions.

### P0-04 Turtle Soup
Need selected reference extreme, strict excursion, confirmation or rejection, timeout/consumption behavior.

Current direct taxonomy progress:
- bearish `OLD_CRTH` = source-backed eligible subtype candidate;
- generic old-high/old-low registry remains open;
- bullish `OLD_CRTL` remains unpromoted until directly supported.

### P0-05 Context Direction
Need direction declared before outcome plus the exact timeframe and close/wick evidence used to derive it.

## Evidence discipline

Outcomes may be stored only as audit fields. They may never be used to fill missing pre-trade fields.

If a chart/source cannot be frozen at time `t` and reconstructed independently without seeing later outcome, it does not receive causal P0 closure credit.
