# Validation Access Guard

`romeo_crt_engine.validation_guard` encodes the preregistered sequential-access rule as a fail-closed immutable state machine.

Canonical states:

```text
PRECOMMIT
  -> DEV_ALLOWED
  -> DEV_SEALED
  -> OOS_ALLOWED
  -> OOS_SEALED
  -> CONFIRM_ALLOWED
  -> COMPLETE
```

A terminal `REJECT`, `REVISE_AS_NEW_VERSION`, or `INSUFFICIENT_EVIDENCE` decision may close validation from `DEV_SEALED` or `OOS_SEALED` without opening later windows. `PROMOTE_TO_PAPER_CANDIDATE` is valid only after CONFIRM has been explicitly authorized and completed.

Every accepted transition appends an immutable audit record. Window-seal transitions require SHA-256 identities for the dataset, run, and report. CONFIRM access additionally requires an explicit eligibility decision plus its SHA-256 evidence identity.

The guard contains no P&L or strategy-selection logic. It exists only to prevent premature data/result access and to preserve a machine-readable access audit trail.

## CLI

Initialize a candidate-specific state file:

```bash
python -m romeo_crt_engine.validation_guard init validation-state.json CRT-EXAMPLE-v0.3
```

Apply a transition using an evidence JSON payload:

```bash
python -m romeo_crt_engine.validation_guard transition \
  validation-state.json DEV_ALLOWED \
  --evidence-json transition-evidence.json
```

Invalid or out-of-order transitions fail without rewriting the state file.

## Safety boundary

The guard never authorizes live trading. OOS and CONFIRM remain inaccessible until their predecessor seals and explicit entry conditions are satisfied. Existing Phase 6/6B historical outcomes remain immutable and are not consumed by this module or its tests.
