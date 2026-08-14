# Queue Sentinel

The queue sentinel is a read-only GitHub Actions workflow that runs every 15 minutes to shorten mechanical state-detection latency for the autonomous execution queue.

It classifies open pull requests into the canonical states documented in `AUTONOMOUS_GITHUB_WORK_PROTOCOL.md`, identifies mechanically stale claim candidates, and surfaces explicitly ready unclaimed issues when the issue text makes readiness safe to infer.

The sentinel is intentionally not a coding agent. It does not merge pull requests, push fixes, alter strategy semantics, inspect protected OOS/CONFIRM outcomes, place broker orders, or change paper/live authorization.

The hourly ChatGPT Queue Runner remains responsible for reasoning-heavy actions such as diagnosing CI failures, selecting dependency-safe work, reviewing PR state, merging green changes, and updating Issue #42.

Canonical workflow:

```text
.github/workflows/queue-sentinel.yml
```

Machine-readable output is written to `queue-sentinel.json` inside the workflow run and the human-readable state is added to the GitHub Actions step summary.

Security boundary:

```text
contents       read
issues         read
pull-requests  read
checks         read
```

Only the default GitHub Actions token is used. No repository or broker secrets are required.
