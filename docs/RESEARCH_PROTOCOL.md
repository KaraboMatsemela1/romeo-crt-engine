# Romeo Research Protocol

## Objective
Convert public educational material into a traceable strategy knowledge base without confusing interpretation with fact.

## Per-source workflow

1. Register source in `research/romeo/SOURCE_REGISTRY.csv`.
2. Save transcript/notes metadata; do not commit copyrighted full transcripts if licensing/terms do not permit it.
3. Analyze with `VIDEO_ANALYSIS_TEMPLATE.md`.
4. Extract each candidate rule using `RULE_TEMPLATE.md`.
5. Add new terms to `GLOSSARY.md`.
6. Add unresolved ambiguity to `OPEN_QUESTIONS.md`.
7. Link examples/counterexamples by stable IDs.
8. Reconcile against previous rules and record contradictions.
9. Only then update the draft strategy spec.

## Evidence discipline

Distinguish:
- explicit rule stated by source
- repeated demonstration
- analyst inference
- quantitative hypothesis

Never invent a missing parameter because it improves a backtest.

## Reconciliation

When sources conflict:
- preserve both citations
- note chronology/context
- test whether they describe different setup variants
- mark rule unresolved until evidence supports a scoped interpretation
