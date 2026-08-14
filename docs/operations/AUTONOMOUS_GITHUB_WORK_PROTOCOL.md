# Autonomous GitHub Work Protocol

This protocol governs autonomous execution of the romeo-crt-engine backlog by Codex, Hermes, ChatGPT, and other agents.

## 1. Claim before work

Before creating a branch or changing files, add a top-level comment to the issue:

```text
CLAIMED_BY: <agent-name>
CLAIMED_AT: <UTC timestamp>
BRANCH: agent/<issue-number>-<short-name>
```

A claim is active until the agent posts a completion, blocked, failed, or explicit release comment. Another agent must not work an actively claimed issue.

Claims are coordination metadata, not evidence that the task is unblocked. The agent must independently verify the issue dependencies and repository status.

## 2. Branch and pull request convention

- Start from the latest `main`.
- Use exactly one primary branch and one PR per issue.
- Branch format: `agent/<issue-number>-<short-name>`.
- PR title format: `Issue #<number>: <imperative change>`.
- The PR body must link the issue with `Closes #<number>`, summarize safety impact, list tests, and state that no prohibited historical/OOS/CONFIRM outcome access occurred.
- Do not reuse a branch for a different issue.
- If `main` moved before implementation, rebase or recreate the branch so the PR is based on current `main` before merge when required.

## 3. Work states and bounded concurrency

Every claimed issue/PR is classified into one of these states:

```text
IMPLEMENTING
CI_PENDING
CI_FAILED
REVIEW_PENDING
READY_TO_MERGE
BLOCKED
COMPLETE
```

State meaning:

- `IMPLEMENTING`: the agent is actively changing the issue branch.
- `CI_PENDING`: required GitHub checks are still running or queued.
- `CI_FAILED`: a required check failed and needs diagnosis/fix unless owner input is required.
- `REVIEW_PENDING`: CI is green but required review/actionable thread resolution is incomplete.
- `READY_TO_MERGE`: required CI is green and no unresolved actionable review thread remains.
- `BLOCKED`: an explicit dependency, evidence gate, permission, or owner decision prevents further safe progress.
- `COMPLETE`: the PR is merged and the issue completion record is posted.

`CI_PENDING` and `REVIEW_PENDING` block only that PR's merge. They do **not** block the entire queue.

Each agent may hold at most two active claims, and only when exactly one claim is in an external wait state (`CI_PENDING` or `REVIEW_PENDING`). At most one claim per agent may be `IMPLEMENTING` at a time. The second issue must be dependency-satisfied, unclaimed by another agent, and branch-independent.

`CI_FAILED` has priority over starting new implementation work for that agent unless the failure cannot be resolved without owner input.

## 4. Selecting the next task

On every autonomous run, and after every merge:

1. Refresh Issue #42, open issues, active claims, open PRs, CI results, and review threads.
2. Service the agent's existing work-in-flight first:
   - fix `CI_FAILED` work;
   - merge `READY_TO_MERGE` work;
   - record exact blockers for genuinely `BLOCKED` work.
3. Exclude issues with an active claim from another agent.
4. Exclude issues whose explicit dependencies are false.
5. Exclude blocked issues even if their implementation would be useful.
6. If the agent has one claim waiting in `CI_PENDING` or `REVIEW_PENDING`, it may claim one additional independent ready issue.
7. Prefer governance and safety foundations before broker integrations or strategy work.
8. Verify the issue's safety boundary before claiming it.
9. Claim the selected issue, then create its branch from current `main`.

Issue #42 is the canonical queue. Its blocked labels and dependency statements are authoritative. Never infer that a blocked issue is ready from the existence of supporting infrastructure.

## 5. Stale claims

A claim is stale when all of the following are true:

- no completion, blocked, failed, or release update exists;
- the claimed branch has had no commit for 48 hours; and
- the issue has not received a progress update for 48 hours.

A later agent may not silently take over a stale claim. It must first comment:

```text
RELEASE_STALE_CLAIM:
PREVIOUS_BRANCH: <branch>
REASON: no commit or progress for 48h
NEW_AGENT: <agent-name>
```

If the original agent resumes, it must either continue on the same branch or explicitly release the claim. When a claim is ambiguous, stop and ask the project owner rather than guessing.

## 6. Implementation and safety gates

Before coding, read `AGENTS.md`, `PROJECT_BIBLE.md`, `STATUS.md`, the relevant roadmap/checklist, and the issue dependencies.

Every behavior change must include tests and documentation. Agents must:

- preserve Phase 6/6B historical results;
- avoid look-ahead and future-confirmed data;
- keep OOS and CONFIRM closed except through the sequential-access protocol;
- keep candidate creation outcome-free and gated;
- keep broker execution disabled until the Phase-7 authorization issue succeeds;
- keep live trading unauthorized;
- fail closed for missing or invalid safety inputs;
- never commit credentials or secrets.

If a dependency or required evidence is missing, do not implement around it. Post `RESULT: BLOCKED` with the exact dependency and immediately return to the selection procedure.

## 7. CI, review, and merge

Before merge:

1. Run the repository test and lint/type-check commands documented by the project.
2. Open the PR against `main`.
3. Classify the PR as `CI_PENDING` until required checks complete.
4. While that PR is `CI_PENDING`, another independent task may proceed only under the bounded-concurrency rule in Section 3.
5. If CI fails, classify `CI_FAILED`, diagnose the exact failure, and prioritize the fix before new implementation work unless owner input is required.
6. If CI passes, inspect review threads, including resolved/unresolved state where available.
7. If actionable review remains, classify `REVIEW_PENDING`, address it, and rerun CI as needed.
8. When CI is green and no unresolved actionable review remains, classify `READY_TO_MERGE` and merge using the expected head SHA where available.
9. Confirm the merge commit on `main`.
10. If another PR merged while an independent branch was waiting, refresh/rebase/recreate that branch as required before merge.

A passing local test is not a substitute for GitHub CI. A pending or failed CI state is not permission to claim completion.

## 8. Unattended continuity

A single Work/Codex/ChatGPT invocation is not treated as a permanent daemon. Long-running continuity is provided by scheduled orchestration that periodically revisits Issue #42 and current PR state.

The scheduled queue runner must:

- service existing failed/green PRs before claiming new work;
- treat `CI_PENDING`/`REVIEW_PENDING` as external wait states rather than a global stop;
- respect other agents' active claims;
- preserve the two-claim/one-active-modification bound;
- make no repository change when no safe action is available.

A lightweight GitHub Actions sentinel may shorten mechanical state-detection latency, but it must not perform strategy reasoning, mutate strategy rules, open OOS/CONFIRM, place orders, or authorize paper/live trading.

## 9. Completion and release records

After merge, comment on the issue:

```text
RESULT: COMPLETE
PR: #<number>
MERGE_SHA: <sha>
NEXT_UNBLOCKED: #<issue-number or NONE>
```

For a blocked task:

```text
RESULT: BLOCKED
PR: NONE
MERGE_SHA: NONE
BLOCKER: <exact dependency or evidence condition>
NEXT_UNBLOCKED: #<issue-number or NONE>
```

For a failed task, include the failing command/check and preserve the branch for diagnosis:

```text
RESULT: FAILED
PR: #<number or NONE>
MERGE_SHA: NONE
FAILURE: <exact failure>
NEXT_UNBLOCKED: #<issue-number or NONE>
```

The master issue and `STATUS.md`/README progress view must be updated when a gate materially changes. Never mark an issue complete merely because a branch or PR exists.
