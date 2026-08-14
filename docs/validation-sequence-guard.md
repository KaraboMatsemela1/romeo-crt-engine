# Validation sequence guard

The `ValidationGuard` is a fail-closed, outcome-independent state machine for the
DEV → OOS → CONFIRM access sequence.

Allowed order:

`PRECOMMIT → DEV_ALLOWED → DEV_SEALED → OOS_ALLOWED → OOS_SEALED → CONFIRM_ALLOWED → COMPLETE`

Opening OOS requires a sealed DEV transition. Opening CONFIRM requires a sealed
OOS transition plus an explicit promotion-eligibility decision. Every sealed or
promoted transition requires both a dataset hash and a run hash, which are retained
in an immutable audit tuple.

The guard does not load market data, inspect outcomes, run a detector, calculate
P&L, or authorize paper/live execution. It only controls future callers that
request validation-window access. Existing historical OOS/CONFIRM artifacts are
not accessed by this implementation.
