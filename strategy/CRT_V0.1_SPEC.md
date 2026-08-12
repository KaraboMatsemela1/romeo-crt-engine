# CRT v0.1 Strategy Specification

**Status:** DRAFT / NOT FROZEN / NOT VERIFIED  
**Live trading:** NOT AUTHORIZED

This file will become the first deterministic candidate only after the Romeo corpus has been researched and reconciled.

## Scope

- Instruments: UNRESOLVED
- Context timeframes: UNRESOLVED
- Execution timeframes: UNRESOLVED
- Sessions: UNRESOLVED
- Setup variants: UNRESOLVED

## State machine

```text
WAIT_FOR_CONTEXT
 -> RANGE_IDENTIFIED
 -> WAIT_FOR_LIQUIDITY_EVENT
 -> LIQUIDITY_EVENT_DETECTED
 -> WAIT_FOR_CONFIRMATION
 -> CONFIRMED
 -> RISK_CHECK
 -> ENTER
 -> MANAGE_POSITION
 -> EXIT
```

Each transition remains unimplemented until rule definitions are evidence-backed.

## Rule register

| Rule ID | Category | Status | Description |
|---|---|---|---|
| CRT-001 | Range | UNRESOLVED | Pending corpus research |
| CRT-002 | Liquidity | UNRESOLVED | Pending corpus research |
| CRT-003 | Sweep | UNRESOLVED | Pending corpus research |
| CRT-004 | Context | UNRESOLVED | Pending corpus research |
| CRT-005 | Confirmation | UNRESOLVED | Pending corpus research |
| CRT-006 | Entry | UNRESOLVED | Pending corpus research |
| CRT-007 | Stop | UNRESOLVED | Pending corpus research |
| CRT-008 | Target | UNRESOLVED | Pending corpus research |
| CRT-009 | Invalidation | UNRESOLVED | Pending corpus research |
| CRT-010 | Session/time | UNRESOLVED | Pending corpus research |

## Freeze checklist

- [ ] All required rule IDs linked to source evidence
- [ ] Explicit vs inferred logic marked
- [ ] Critical ambiguity resolved or excluded
- [ ] Positive examples exist
- [ ] Negative examples exist
- [ ] Machine-readable fixtures exist
- [ ] Rule tests defined
- [ ] Independent strategy review completed
- [ ] Version freeze commit/tag created
