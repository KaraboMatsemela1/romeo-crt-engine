# Order and position state

This module provides deterministic, broker-independent order records, transition events,
client-order-id binding, monotonic fill validation, and fail-closed reconciliation.

An order may not silently change identity, regress state, overfill, or become complete
without an accepted terminal broker state. Reconciliation returns MATCH only when order
and position state agree; missing or divergent broker state returns MISMATCH.

The module is persistence-ready: records and immutable event tuples can be serialized by
a later adapter, but this issue does not connect to a broker or place paper/live orders.
