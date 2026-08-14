from romeo_crt_engine.spec_audit import AuditInput, AuditStatus, audit


def passing_input(**overrides):
    values = {
        "future_d1_h1_used": False,
        "unfinished_candle_ohlc_used": False,
        "retrospective_parent_selection": False,
        "date_window_immutable": True,
        "cost_config_immutable": True,
        "hashes_bound": True,
        "same_bar_policy_declared": True,
        "gap_policy_declared": True,
        "quarantined_windows_excluded": True,
        "spec_matches_code": True,
    }
    return AuditInput(**(values | overrides))


def test_clean_candidate_passes_every_check():
    report = audit(passing_input())
    assert report.status is AuditStatus.PASS
    assert len(report.findings) == 10


def test_future_information_fails_audit():
    report = audit(passing_input(future_d1_h1_used=True))
    assert report.status is AuditStatus.FAIL
    assert any(f.check == "future_d1_h1_use" and f.status is AuditStatus.FAIL for f in report.findings)


def test_unfinished_candle_and_spec_mismatch_fail():
    report = audit(
        passing_input(
            unfinished_candle_ohlc_used=True,
            spec_matches_code=False,
        )
    )
    assert report.status is AuditStatus.FAIL
    failed = {f.check for f in report.findings if f.status is AuditStatus.FAIL}
    assert failed == {"unfinished_candle_ohlc", "spec_matches_code"}
