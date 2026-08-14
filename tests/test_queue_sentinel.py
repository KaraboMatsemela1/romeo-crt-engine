from datetime import UTC, datetime, timedelta

from romeo_crt_engine.queue_sentinel import (
    claim_is_stale,
    classify_checks,
    classify_pr,
    is_explicitly_ready_issue,
    parse_active_claim,
)


def test_checks_pending_when_missing_or_running():
    assert classify_checks([]) == "CI_PENDING"
    assert classify_checks([{"status": "in_progress", "conclusion": None}]) == "CI_PENDING"


def test_checks_failure_has_priority():
    checks = [{"status": "completed", "conclusion": "failure"}]
    assert classify_checks(checks) == "CI_FAILED"


def test_green_pr_is_ready_only_when_mergeable_and_review_clear():
    checks = [{"status": "completed", "conclusion": "success"}]
    assert (
        classify_pr(draft=False, mergeable=True, checks=checks, changes_requested=False)
        == "READY_TO_MERGE"
    )
    assert (
        classify_pr(draft=True, mergeable=True, checks=checks, changes_requested=False)
        == "REVIEW_PENDING"
    )
    assert (
        classify_pr(draft=False, mergeable=True, checks=checks, changes_requested=True)
        == "REVIEW_PENDING"
    )


def test_latest_claim_is_cleared_by_terminal_record():
    comments = [
        {
            "body": (
                "CLAIMED_BY: ChatGPT\nCLAIMED_AT: 2026-08-14T18:21:00Z\n"
                "BRANCH: agent/45-nonblocking-ci-lanes"
            )
        },
        {"body": "RESULT: COMPLETE\nPR: #47"},
    ]
    assert parse_active_claim(comments) is None


def test_explicit_ready_detection_is_conservative():
    assert is_explicitly_ready_issue("Task", "## Dependency\nNone. Safe to execute now.")
    assert not is_explicitly_ready_issue("[BLOCKED] Task", "## Dependency\nNone")


def test_stale_claim_requires_48_hours_and_inactive_branch():
    now = datetime(2026, 8, 14, 18, 0, tzinfo=UTC)
    claim = {
        "agent": "ChatGPT",
        "at": "2026-08-12T17:00:00Z",
        "branch": "agent/1-example",
    }
    assert claim_is_stale(claim, branch_updated_at=now - timedelta(hours=49), now=now)
    assert not claim_is_stale(claim, branch_updated_at=now - timedelta(hours=1), now=now)
