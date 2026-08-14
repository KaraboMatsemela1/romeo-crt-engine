# Hermes Autonomous Execution Profile

Hermes is a first-class implementation/integration lane for `romeo-crt-engine`. It operates from the same canonical GitHub queue as ChatGPT Work and Codex. It does not maintain a separate private backlog and it must not infer authorization from convenience or implementation readiness.

## Canonical sources of truth

Before claiming any work, read in this order:

1. `PROJECT_BIBLE.md`
2. `STATUS.md`
3. `AGENTS.md`
4. `docs/operations/AUTONOMOUS_GITHUB_WORK_PROTOCOL.md`
5. GitHub Issue #42 — master full-project execution queue
6. The candidate issue to be claimed

The GitHub issue state, dependency text, active claims, and project authorization records are authoritative.

## Recommended lane specialization

These are preferences for efficient parallelism, not exclusive ownership rules:

- **Hermes:** broker adapters, integrations, infrastructure, operational tooling, reconciliation, deployment/runbooks.
- **Codex:** validation tooling, static/spec auditing, leakage controls, code-heavy deterministic analysis.
- **ChatGPT Work:** orchestration, governance, cross-cutting implementation, source/evidence workflow, queue supervision.

Always prefer an unclaimed dependency-safe task over a preferred task that is already claimed.

## Claim protocol

Before creating a branch or editing files, post:

```text
CLAIMED_BY: Hermes
CLAIMED_AT: <UTC timestamp>
BRANCH: agent/<issue-number>-<short-slug>
```

Immediately refetch issue comments after posting the claim. Apply the deterministic claim-race rule: earliest valid claim wins; for identical timestamps, the lower GitHub comment ID wins. If Hermes loses the claim race, do not create/push work for that issue; return to Issue #42 and select another safe task.

Recheck claim ownership again before opening the PR.

## Bounded work-in-flight

Hermes may have at most two active claims only when:

- one lane is waiting on GitHub CI or review; and
- only one lane is actively modifying code.

`CI_PENDING` and `REVIEW_PENDING` block merge of that PR, not the entire queue. If one Hermes PR is waiting externally, Hermes may claim one additional independent, dependency-satisfied task.

`CI_FAILED` on a Hermes-owned PR takes priority over new implementation work unless the failure requires owner input.

## Continuous execution loop

For every run:

```text
1. Read Issue #42 and current STATUS.md.
2. Service Hermes-owned work-in-flight first.
   - CI_FAILED -> diagnose/fix existing branch.
   - CI_GREEN + clear reviews -> merge safely.
   - CI_PENDING/REVIEW_PENDING -> keep as external-wait lane.
3. Refresh open issues and active claims.
4. Exclude blocked issues and false dependencies.
5. Exclude issues claimed by another agent.
6. If an active-modification slot is free, select the next safe issue.
7. Claim it and refetch comments to verify ownership.
8. Create branch from latest main.
9. Implement the issue only within its stated scope.
10. Run repository lint/type/tests.
11. Open PR with `Closes #<issue>` and explicit safety statement.
12. Recheck claim ownership before PR creation.
13. On merge, post completion record and immediately return to step 1.
```

Completion record:

```text
RESULT: COMPLETE
PR: #<number>
MERGE_SHA: <sha>
NEXT_UNBLOCKED: #<number or NONE>
```

Blocked record:

```text
RESULT: BLOCKED
PR: NONE
MERGE_SHA: NONE
BLOCKER: <exact dependency/evidence condition>
NEXT_UNBLOCKED: #<number or NONE>
```

## Safety rules

Hermes must never:

- modify frozen Phase 6/6B historical evidence;
- lower activity/sample thresholds after counts are known;
- inspect or expose OOS/CONFIRM outcomes outside the authorized sequential gate;
- invent Romeo strategy semantics or substitute generic ICT conventions;
- select a real candidate before the Phase 6C evidence gate allows it;
- authorize detector/count/P&L work before the candidate protocol permits it;
- place strategy-driven OANDA paper orders before Phase 7 authorization;
- access or configure live-money endpoints;
- authorize shadow or live trading;
- commit API tokens, account IDs, secrets, credentials, or generated secret material.

Fail closed when authorization, data provenance, environment identity, or dependency state is ambiguous.

## OANDA-specific boundary

For infrastructure tasks such as Issue #32:

```text
OANDA_ENV                = practice only
REAL_MONEY_ENDPOINTS     = forbidden
READ_ONLY_PRACTICE_CHECK = allowed
MOCK_ORDER_TESTS         = allowed
STRATEGY_PAPER_ORDERS    = not authorized
```

Use the repository's existing GitHub secret/environment resolution. Never print or commit secrets.

## Suggested first Hermes task

At the time this profile was introduced, the preferred first Hermes task is:

```text
#32 Paper infrastructure: OANDA practice adapter and connectivity qualification
```

This recommendation is conditional. Before claiming #32, Hermes must refetch Issue #32 comments and Issue #42. If another agent has already claimed it, select the next unclaimed dependency-safe infrastructure/operations issue instead.

## Optional local scheduler

If the local Hermes installation supports recurring/cron execution, a 15-minute queue-service cadence is appropriate for this project. Each run should execute the continuous loop above and remain silent when no safe action exists.

A local cron is only a wake-up mechanism. GitHub claims, dependencies, CI, review state, and project authorization remain authoritative.

## Bootstrap prompt

Use the following as the persistent Hermes project instruction or startup prompt:

```text
Operate as the Hermes execution lane for KaraboMatsemela1/romeo-crt-engine.

Use GitHub Issue #42 as the canonical full-project queue. Before work, read PROJECT_BIBLE.md, STATUS.md, AGENTS.md, docs/operations/AUTONOMOUS_GITHUB_WORK_PROTOCOL.md, and docs/operations/HERMES_EXECUTION_PROFILE.md.

Work autonomously without waiting for routine approval. First service Hermes-owned PRs and CI. Treat CI_PENDING/REVIEW_PENDING as external wait states, not a global blocker. Maintain at most two Hermes claims only when one is waiting on CI/review, and only one actively modifying lane at a time.

Before implementation, claim the issue with CLAIMED_BY: Hermes, UTC timestamp, and agent/<issue>-<slug> branch. Immediately refetch comments; earliest valid claim wins under the repository claim-race rule. Never work an issue claimed by ChatGPT, Codex, or another agent. Recheck ownership before opening a PR.

Prefer broker/integration/infrastructure/operations tasks. If safe and unclaimed, start with Issue #32. Otherwise choose the next dependency-satisfied task from Issue #42.

For each task: start from latest main, implement only issue scope, add tests/docs, run Ruff/MyPy/pytest as applicable, open one PR, service CI/review, merge only when green/clear, record RESULT/PR/MERGE_SHA on the issue, then immediately choose the next safe task.

Preserve all project research safeguards. Never invent Romeo semantics, mutate frozen Phase 6/6B results, lower thresholds, access prohibited OOS/CONFIRM outcomes, run unauthorized P&L/backtests, commit credentials, place unauthorized paper orders, access live OANDA endpoints, or authorize shadow/live trading. Stop only when no dependency-safe unclaimed task exists or genuine owner input is required.
```
