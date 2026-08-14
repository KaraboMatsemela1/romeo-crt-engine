"""Read-only GitHub queue sentinel for autonomous work state classification."""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
from datetime import UTC, datetime, timedelta
from typing import Any

CLAIM_RE = re.compile(
    r"CLAIMED_BY:\s*(?P<agent>[^\n]+).*?CLAIMED_AT:\s*(?P<at>[^\n]+).*?BRANCH:\s*(?P<branch>[^\n]+)",
    re.DOTALL,
)
TERMINAL_MARKERS = (
    "RESULT: COMPLETE",
    "RESULT: BLOCKED",
    "RESULT: FAILED",
    "RELEASE_STALE_CLAIM",
)


def classify_checks(checks: list[dict[str, Any]]) -> str:
    """Return CI state from GitHub check-run records."""
    if not checks or any(check.get("status") != "completed" for check in checks):
        return "CI_PENDING"
    failing = {"failure", "cancelled", "timed_out", "action_required", "startup_failure"}
    if any(check.get("conclusion") in failing for check in checks):
        return "CI_FAILED"
    if all(check.get("conclusion") in {"success", "neutral", "skipped"} for check in checks):
        return "CI_GREEN"
    return "CI_PENDING"


def classify_pr(
    *,
    draft: bool,
    mergeable: bool | None,
    checks: list[dict[str, Any]],
    changes_requested: bool,
) -> str:
    """Classify a pull request without mutating repository state."""
    ci_state = classify_checks(checks)
    if ci_state != "CI_GREEN":
        return ci_state
    if draft or changes_requested:
        return "REVIEW_PENDING"
    if mergeable is True:
        return "READY_TO_MERGE"
    return "REVIEW_PENDING"


def parse_active_claim(comments: list[dict[str, Any]]) -> dict[str, str] | None:
    """Return the most recent claim unless a later terminal/release marker exists."""
    claim: dict[str, str] | None = None
    for comment in comments:
        body = str(comment.get("body", ""))
        if any(marker in body for marker in TERMINAL_MARKERS):
            claim = None
            continue
        match = CLAIM_RE.search(body)
        if match:
            claim = {key: value.strip() for key, value in match.groupdict().items()}
    return claim


def is_explicitly_ready_issue(title: str, body: str) -> bool:
    """Conservatively identify only issues explicitly documented as safe now."""
    text = f"{title}\n{body}".lower()
    if "[blocked]" in title.lower() or "current status\nblocked" in text:
        return False
    return (
        "dependency\nnone" in text
        or "safe to execute now" in text
        or "safe to implement now" in text
    )


def claim_is_stale(
    claim: dict[str, str], *, branch_updated_at: datetime | None, now: datetime
) -> bool:
    """Apply the 48-hour mechanical part of the canonical stale-claim rule."""
    claimed_at = datetime.fromisoformat(claim["at"].replace("Z", "+00:00"))
    cutoff = now - timedelta(hours=48)
    if claimed_at > cutoff:
        return False
    return branch_updated_at is not None and branch_updated_at <= cutoff


class GitHubClient:
    """Minimal read-only GitHub REST client using the workflow token."""

    def __init__(self, repo: str, token: str) -> None:
        self.repo = repo
        self.token = token

    def get(self, path: str) -> Any:
        request = urllib.request.Request(
            f"https://api.github.com/repos/{self.repo}{path}",
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self.token}",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        with urllib.request.urlopen(request, timeout=30) as response:  # noqa: S310
            return json.load(response)


def latest_changes_requested(reviews: list[dict[str, Any]]) -> bool:
    """Treat a latest CHANGES_REQUESTED review as pending until superseded."""
    latest_by_user: dict[str, str] = {}
    for review in reviews:
        user = str(review.get("user", {}).get("login", "unknown"))
        latest_by_user[user] = str(review.get("state", ""))
    return any(state == "CHANGES_REQUESTED" for state in latest_by_user.values())


def collect_snapshot(client: GitHubClient) -> dict[str, Any]:
    """Collect a conservative, read-only queue snapshot."""
    pull_rows: list[dict[str, Any]] = []
    for pr in client.get("/pulls?state=open&per_page=100"):
        number = int(pr["number"])
        detail = client.get(f"/pulls/{number}")
        sha = str(detail["head"]["sha"])
        checks = client.get(f"/commits/{sha}/check-runs?per_page=100").get("check_runs", [])
        reviews = client.get(f"/pulls/{number}/reviews?per_page=100")
        state = classify_pr(
            draft=bool(detail.get("draft")),
            mergeable=detail.get("mergeable"),
            checks=checks,
            changes_requested=latest_changes_requested(reviews),
        )
        pull_rows.append(
            {
                "number": number,
                "head_sha": sha,
                "state": state,
                "title": detail["title"],
            }
        )

    issue_rows: list[dict[str, Any]] = []
    now = datetime.now(UTC)
    for issue in client.get("/issues?state=open&per_page=100"):
        if "pull_request" in issue:
            continue
        number = int(issue["number"])
        comments = (
            client.get(f"/issues/{number}/comments?per_page=100")
            if issue.get("comments")
            else []
        )
        claim = parse_active_claim(comments)
        stale = False
        if claim:
            try:
                branch = client.get(f"/branches/{claim['branch']}")
                updated = datetime.fromisoformat(
                    branch["commit"]["commit"]["committer"]["date"].replace("Z", "+00:00")
                )
                stale = claim_is_stale(claim, branch_updated_at=updated, now=now)
            except Exception:  # noqa: BLE001
                stale = False
        issue_rows.append(
            {
                "number": number,
                "title": issue["title"],
                "claimed_by": claim["agent"] if claim else None,
                "stale_claim": stale,
                "explicitly_ready": is_explicitly_ready_issue(
                    issue["title"], issue.get("body") or ""
                ),
            }
        )
    return {"generated_at": now.isoformat(), "pull_requests": pull_rows, "issues": issue_rows}


def render_summary(snapshot: dict[str, Any]) -> str:
    """Render a compact Markdown summary for the Actions run."""
    lines = ["# Autonomous queue sentinel", "", "## Open pull requests"]
    pulls = snapshot["pull_requests"]
    if not pulls:
        lines.append("No open pull requests.")
    for pr in pulls:
        lines.append(f"- PR #{pr['number']}: **{pr['state']}** — {pr['title']}")
    lines.extend(["", "## Queue signals"])
    signals = [
        issue
        for issue in snapshot["issues"]
        if issue["stale_claim"] or (issue["explicitly_ready"] and not issue["claimed_by"])
    ]
    if not signals:
        lines.append("No new mechanical queue signals.")
    for issue in signals:
        if issue["stale_claim"]:
            lines.append(f"- Issue #{issue['number']}: stale claim candidate")
        elif issue["explicitly_ready"]:
            lines.append(f"- Issue #{issue['number']}: explicitly ready and unclaimed")
    return "\n".join(lines) + "\n"


def main() -> int:
    """Collect and write the sentinel snapshot and workflow summary."""
    repo = os.environ.get("GITHUB_REPOSITORY")
    token = os.environ.get("GITHUB_TOKEN")
    if not repo or not token:
        print("GITHUB_REPOSITORY and GITHUB_TOKEN are required", file=sys.stderr)
        return 2
    snapshot = collect_snapshot(GitHubClient(repo, token))
    with open("queue-sentinel.json", "w", encoding="utf-8") as handle:
        json.dump(snapshot, handle, indent=2, sort_keys=True)
        handle.write("\n")
    summary = render_summary(snapshot)
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as handle:
            handle.write(summary)
    else:
        print(summary, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
