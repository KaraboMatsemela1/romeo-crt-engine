# AGENTS.md — AI Agent Operating Contract

This file governs any AI/coding/research agent working in this repository.

## Priority order

1. Safety and capital-protection constraints
2. `PROJECT_BIBLE.md`
3. Frozen strategy specification under `strategy/`
4. ADRs
5. Tests
6. Implementation
7. Exploratory research notes

If implementation conflicts with the frozen spec, do not silently “fix” the spec in code. Raise the mismatch.

## Before coding

- Read `PROJECT_BIBLE.md`.
- Read `docs/ROADMAP.md` and current `STATUS.md`.
- Read relevant ADRs.
- Read `docs/operations/AUTONOMOUS_GITHUB_WORK_PROTOCOL.md` before claiming autonomous work.
- Use GitHub Issue #42 as the canonical shared execution queue.
- Determine whether the requested work is research, infrastructure, strategy logic, validation, risk, or execution.
- Identify the applicable quality gate.
- Do not implement unresolved Romeo concepts as facts.

## Multi-agent coordination

ChatGPT Work, Codex, Hermes, and other agents share the same GitHub claim/dependency protocol. Never maintain a separate hidden backlog that bypasses Issue #42.

- Claim before implementation and immediately refetch issue comments to resolve claim races.
- Never work an issue with an earlier valid active claim from another agent.
- Follow the bounded work-in-flight rules for CI/review wait states.
- Recheck claim ownership before opening a PR.
- Use a closing keyword such as `Closes #<n>` only when the PR actually satisfies that issue's definition of done. For bounded research/recovery/follow-up work against a standing blocked gate, use `Related to #<n>` (or another non-closing reference) so the gate cannot be auto-closed prematurely.
- After merge, record completion and immediately return to the shared queue.

Hermes-specific continuous execution and bootstrap instructions are defined in `docs/operations/HERMES_EXECUTION_PROFILE.md`.

## Research-agent rules

- Preserve exact source provenance.
- Separate explicit statements from inference.
- Record contradictions.
- Assign confidence honestly.
- Never fabricate a source/timestamp.
- Put unknowns in `research/romeo/OPEN_QUESTIONS.md`.
- A profitable-looking interpretation is not evidence that the interpretation is correct.

## Coding-agent rules

- Keep core strategy logic deterministic.
- Add tests with every behavior change.
- Do not introduce look-ahead.
- Do not access future-confirmed features at decision time.
- Keep risk logic independent from signal logic.
- Keep broker/execution code behind interfaces.
- Use idempotent order intents.
- Fail closed on stale/invalid/missing critical inputs.
- Store no credentials in source control.
- Update docs when behavior/contracts change.

## Quant-agent rules

- Record all experiment assumptions.
- Keep exploratory and confirmatory tests separate.
- Freeze a candidate before evaluating final OOS data.
- Report negative results.
- Include costs.
- Always provide trade count and drawdown with return metrics.
- Perform sensitivity analysis; do not report only the best parameter point.
- Challenge apparent edge for leakage, overfit, regime dependence, and selection bias.

## ML-agent rules

- ML may rank valid deterministic setups initially; it may not create arbitrary live trades.
- Use time-aware validation.
- Compare against a simple baseline.
- Track model/data/feature versions.
- Candidate models do not enter production directly.

## Live-trading restriction

`LIVE_TRADING_AUTHORIZED = false` until the project owner explicitly changes governance after all gates. Agents must not add credentials, activate broker live mode, or bypass paper/shadow environments merely because code exists.

## Definition of done

A task is not done until applicable tests pass, docs are updated, assumptions are recorded, and no unresolved safety/strategy ambiguity is hidden.
