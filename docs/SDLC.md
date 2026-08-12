# Software Delivery Lifecycle

## Standard change flow

Issue/research question -> branch -> implementation/research artifact -> tests -> docs -> PR -> review -> merge.

## A change must include

- stated intent/hypothesis
- affected modules/rules
- tests or evidence
- compatibility/migration notes if needed
- strategy-version impact assessment
- risk impact assessment

## Strategy-critical changes

Any modification to validity, entry, exit, stop, target, time/session, position sizing, feature transformation, or ML decision threshold requires explicit strategy/model versioning and revalidation at the appropriate level.
