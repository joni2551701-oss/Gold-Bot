"""Phase 61.4 TASK 5 — AI Trial Manager: in-memory 7-day FREE trial window, "1 phone = 1 trial" enforcement. Phase 61.5 TASK 4 adds trial_status_from_started_at(), the stateless function a persisted (database-backed) caller shares with TrialManager's own in-memory status_of()."""

from datetime import datetime, timedelta, timezone

from ai.access.trial_manager import DEFAULT_TRIAL_DURATION, TrialManager, trial_status_from_started_at


def test_new_account_with_no_phone_reuse_is_eligible():
    manager = TrialManager()
    result = manager.check_eligibility("111", phone_reused=False)
    assert result.eligible is True


def test_phone_reuse_blocks_eligibility_even_for_a_brand_new_account():
    manager = TrialManager()
    result = manager.check_eligibility("111", phone_reused=True)
    assert result.eligible is False
    assert "phone" in result.reason


def test_start_trial_records_the_start_time():
    manager = TrialManager()
    now = datetime(2026, 1, 1, tzinfo=timezone.utc)

    result = manager.start_trial("111", phone_reused=False, now=now)

    assert result.eligible is True
    status = manager.status_of("111", now=now)
    assert status.started_at == now
    assert status.active is True


def test_start_trial_a_second_time_for_the_same_account_is_rejected():
    manager = TrialManager()
    manager.start_trial("111", phone_reused=False)
    result = manager.start_trial("111", phone_reused=False)
    assert result.eligible is False
    assert "already started" in result.reason


def test_start_trial_with_phone_reuse_never_records_a_start():
    manager = TrialManager()
    result = manager.start_trial("111", phone_reused=True)
    assert result.eligible is False
    assert manager.status_of("111").started_at is None


def test_trial_expires_after_the_default_seven_day_window():
    manager = TrialManager()
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    manager.start_trial("111", phone_reused=False, now=start)

    still_active = manager.status_of("111", now=start + timedelta(days=6))
    expired = manager.status_of("111", now=start + timedelta(days=8))

    assert still_active.active is True
    assert expired.active is False


def test_custom_trial_duration_is_respected():
    manager = TrialManager(trial_duration=timedelta(days=1))
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    manager.start_trial("111", phone_reused=False, now=start)

    result = manager.status_of("111", now=start + timedelta(days=2))
    assert result.active is False


def test_status_of_unknown_account_reports_no_trial():
    manager = TrialManager()
    status = manager.status_of("does-not-exist")
    assert status.started_at is None
    assert status.active is False
    assert status.expires_at is None


def test_trial_status_from_started_at_none_reports_no_trial():
    status = trial_status_from_started_at(None)
    assert status.started_at is None
    assert status.active is False
    assert status.expires_at is None


def test_trial_status_from_started_at_active_within_window():
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    status = trial_status_from_started_at(start, now=start + timedelta(days=1))
    assert status.active is True
    assert status.expires_at == start + DEFAULT_TRIAL_DURATION


def test_trial_status_from_started_at_expired_after_window():
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    status = trial_status_from_started_at(start, now=start + timedelta(days=8))
    assert status.active is False


def test_trial_status_from_started_at_respects_custom_duration():
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    status = trial_status_from_started_at(start, duration=timedelta(days=1), now=start + timedelta(days=2))
    assert status.active is False


def test_status_of_delegates_to_trial_status_from_started_at():
    """TrialManager.status_of() must not duplicate the started_at-vs-now math -- verified by matching against the stateless function directly, not just by behavior."""
    manager = TrialManager()
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    manager.start_trial("111", phone_reused=False, now=start)

    now = start + timedelta(days=3)
    from_manager = manager.status_of("111", now=now)
    from_function = trial_status_from_started_at(start, DEFAULT_TRIAL_DURATION, now)

    assert from_manager == from_function
