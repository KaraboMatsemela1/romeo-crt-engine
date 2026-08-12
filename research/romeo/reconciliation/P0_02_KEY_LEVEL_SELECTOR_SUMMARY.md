# P0-02 Reconciliation Summary

Status: `PARTIALLY_RESOLVED`

Core resolved contract:

- key level is context, never a direct entry;
- higher-timeframe context must exist before lower-timeframe interpretation;
- key-level role is predeclared as `DESTINATION` or `REACTION_ORIGIN`;
- reaction-from-level setups must reject pre-level lower-timeframe reversal structures;
- key-level selection is frozen causally before outcome;
- ambiguous key-level selection fails closed.

Still blocking:

- exact price-level taxonomy;
- exact time-level taxonomy;
- W1/D1/H4 ranking/conflict resolution;
- exact `reached` predicate;
- consumed/invalidated/superseded semantics;
- exact timing qualification.

First-candidate recommendation: once direct evidence closes the taxonomy/ranking gap, prefer `REACTION_FROM_KEY_LEVEL` as the first executable key-level family because the public Episode-5 evidence provides a clear negative fixture class: convincing LTF reversal before the true key level must be rejected.

See `P0_02_KEY_LEVEL_SELECTOR.md` for the full evidence reconciliation and acceptance criteria.
