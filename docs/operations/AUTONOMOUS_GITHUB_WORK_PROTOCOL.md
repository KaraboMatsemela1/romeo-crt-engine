# Autonomous GitHub Work Protocol

This protocol governs autonomous execution of the romeo-crt-engine backlog by Codex, Hermes, and other agents.

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
- If `main` moved before implementation, rebase or recreate the branch so the PR is based on current `main`.

## 3. Selecting the next task

After every merged task:

1. Refresh open issues and existing claims.
2. Exclude issues with an active claim from another agent.
3. Exclude issues whose explicit dependencies are false.
4. Exclude blocked issues even if their implementation would be useful.
5. Prefer governance and safety foundations before broker integrations or strategy work.
6. Verify the issue's safety boundary before claiming it.
7. Claim the selected issue, then create its branch from current `main`.

Issue #42 is the canonical queue. Its blocked labels and dependency statements are authoritative. Never infer that a blocked issue is ready from the existence of supporting infrastructure.

## 4. Stale claims

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

## 5. Implementation and safety gates

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

## 6. CI, review, and merge

Before merge:

1. Run the repository test and lint/type-check commands documented by the project.
2. Open the PR against `main`.
3. Wait for required CI checks to complete.
4. Inspect review threads, including resolved/unresolved state where available.
5. Fix actionable feedback and rerun CI.
6. Merge only when required CI is green and no unresolved actionable review thread remains.
7. Confirm the merge commit on `main`.

A passing local test is not a substitute for GitHub CI. If CI is unavailable or required checks fail, record the exact state and do not claim completion.

## 7. Completion and release records

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
