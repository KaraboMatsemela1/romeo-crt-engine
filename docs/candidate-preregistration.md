# Candidate preregistration

Issue #28 adds an outcome-blind, immutable Pydantic contract for future candidates. It is infrastructure only: it does not select a strategy, inspect historical counts/P&L, run a detector, or open OOS/CONFIRM.

Use `CandidatePrecommitment.from_untrusted(payload)` at the candidate-selection boundary. The contract requires:

- evidence and positive/negative fixture references;
- inherited, changed and excluded rule declarations;
- frozen universe, timeframes, calendar, timezone, provider and costs;
- strictly ordered DEV, OOS and CONFIRM reservations;
- activity floors of DEV ≥30, OOS ≥30 and CONFIRM ≥20;
- rejection of outcome-derived fields such as P&L, return, drawdown, expectancy and trade counts.

The actual candidate remains blocked by Issue #16. This module must not be used to create one until the candidate-selection gate is opened.
