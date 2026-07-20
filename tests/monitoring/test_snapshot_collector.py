"""
GoldBot Core Owner Snapshot Reporter Alpha, TASK 2 --
monitoring/snapshot_collector.py tests. Extended for the v1.1
Operational Intelligence Upgrade, TASK 1-8.
"""

from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from monitoring.snapshot_collector import (
    DEFAULT_TIMEFRAME,
    _decision_breakdown,
    _decision_rows_today,
    _error_breakdown,
    _format_uptime,
    _last_signal_score,
    _last_signal_summary,
    _pipeline_activity,
    _pipeline_events_total,
    _telegram_status,
    collect_snapshot,
    next_check_time,
)
from monitoring.snapshot_models import OwnerSnapshot


def test_collect_snapshot_returns_owner_snapshot_instance():
    snap = collect_snapshot()
    assert isinstance(snap, OwnerSnapshot)


def test_collect_snapshot_never_raises_default_construction():
    collect_snapshot()  # must not raise


def test_collect_snapshot_status_ok_when_core_running_and_database_ok():
    with patch("monitoring.snapshot_collector.get_core_health") as mocked:
        mocked.return_value = MagicMock(status="RUNNING", database_status="OK", uptime_seconds=60.0)
        snap = collect_snapshot()
    assert snap.status == "OK"


def test_collect_snapshot_status_degraded_when_core_not_running():
    with patch("monitoring.snapshot_collector.get_core_health") as mocked:
        mocked.return_value = MagicMock(status="STOPPED", database_status="OK", uptime_seconds=60.0)
        snap = collect_snapshot()
    assert snap.status == "DEGRADED"


def test_collect_snapshot_status_degraded_when_database_not_ok():
    with patch("monitoring.snapshot_collector.get_core_health") as mocked:
        mocked.return_value = MagicMock(status="RUNNING", database_status="ERROR", uptime_seconds=60.0)
        snap = collect_snapshot()
    assert snap.status == "DEGRADED"


def test_collect_snapshot_core_health_failure_degrades_gracefully():
    with patch("monitoring.snapshot_collector.get_core_health", side_effect=Exception("boom")):
        snap = collect_snapshot()
    assert snap.core_status == "UNKNOWN"
    assert snap.database_status == "UNKNOWN"
    assert snap.uptime_info == "N/A"


def test_collect_snapshot_market_health_failure_degrades_gracefully():
    with patch("monitoring.snapshot_collector.get_market_health", side_effect=Exception("boom")):
        snap = collect_snapshot()
    assert snap.market_data_status == "UNKNOWN"


def test_collect_snapshot_error_counts_failure_defaults_to_zero():
    with patch("monitoring.snapshot_collector.ErrorMonitor") as mocked:
        mocked.return_value.get_error_counts.side_effect = Exception("boom")
        snap = collect_snapshot()
    assert snap.error_count == 0


def test_collect_snapshot_error_count_sums_all_types():
    with patch("monitoring.snapshot_collector.ErrorMonitor") as mocked:
        mocked.return_value.get_error_counts.return_value = {"API timeout": 2, "DB error": 1}
        snap = collect_snapshot()
    assert snap.error_count == 3


def test_collect_snapshot_signals_today_reads_signal_health():
    with patch("monitoring.snapshot_collector.get_signal_health") as mocked:
        mocked.return_value = MagicMock(total_signals=7)
        snap = collect_snapshot()
    assert snap.signals_today == 7


def test_collect_snapshot_signals_today_failure_defaults_to_zero():
    with patch("monitoring.snapshot_collector.get_signal_health", side_effect=Exception("boom")):
        snap = collect_snapshot()
    assert snap.signals_today == 0


def test_collect_snapshot_last_signal_none_when_no_signals():
    repo = MagicMock()
    repo.get_latest_signal.return_value = None
    snap = collect_snapshot(signal_repository=repo)
    assert snap.last_signal is None


def test_collect_snapshot_last_signal_formats_direction_and_time():
    repo = MagicMock()
    repo.get_latest_signal.return_value = {"direction": "BUY", "created_at": "2026-01-01T00:00:00"}
    snap = collect_snapshot(signal_repository=repo)
    assert snap.last_signal == "BUY @ 2026-01-01T00:00:00"


def test_collect_snapshot_never_calls_a_mutating_repository_method():
    repo = MagicMock()
    repo.get_latest_signal.return_value = None
    collect_snapshot(signal_repository=repo)
    repo.create_signal.assert_not_called()
    repo.update_signal_status.assert_not_called()


def test_collect_snapshot_timestamp_is_iso_format():
    snap = collect_snapshot()
    assert "T" in snap.timestamp


def test_format_uptime_seconds_only():
    assert _format_uptime(45) == "45s"


def test_format_uptime_minutes_and_seconds():
    assert _format_uptime(125) == "2m 5s"


def test_format_uptime_hours_and_minutes():
    assert _format_uptime(3725) == "1h 2m"


def test_telegram_status_ok_when_token_present(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456789:AAFakeToken0000000000000000000")
    assert _telegram_status() == "OK"


def test_telegram_status_not_configured_when_token_missing(monkeypatch):
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    assert _telegram_status() == "NOT_CONFIGURED"


def test_last_signal_summary_handles_repository_failure():
    repo = MagicMock()
    repo.get_latest_signal.side_effect = Exception("boom")
    assert _last_signal_summary(repo) is None


def test_collect_snapshot_default_symbol_is_xauusd():
    from monitoring.snapshot_collector import DEFAULT_SYMBOL

    assert DEFAULT_SYMBOL == "XAUUSD"


def test_collect_snapshot_market_health_uses_configured_provider():
    with patch("monitoring.snapshot_collector.get_market_health") as mocked:
        mocked.return_value = MagicMock(data_source_status="ONLINE")
        collect_snapshot(provider_name="twelvedata")
    _, kwargs = mocked.call_args
    assert kwargs["provider_name"] == "twelvedata"


# v1.1 TASK 1 -- Pipeline Activity

def test_decision_rows_today_handles_repository_failure():
    repo = MagicMock()
    repo.get_signals_today.side_effect = Exception("boom")
    assert _decision_rows_today(repo) == []


def test_pipeline_activity_no_runs_today():
    runs, last_at, status = _pipeline_activity([])
    assert runs == 0
    assert last_at is None
    assert status == "NO_RUNS_TODAY"


def test_pipeline_activity_reports_latest_row():
    rows = [
        {"created_at": "2026-01-01T10:00:00", "ai_decision": "REJECT"},
        {"created_at": "2026-01-01T12:00:00", "ai_decision": "APPROVE"},
    ]
    runs, last_at, status = _pipeline_activity(rows)
    assert runs == 2
    assert last_at == "2026-01-01T12:00:00"
    assert status == "SUCCESS"


def test_collect_snapshot_pipeline_runs_today_reflects_signal_rows():
    repo = MagicMock()
    repo.get_signals_today.return_value = [{"created_at": "2026-01-01T10:00:00", "ai_decision": "APPROVE"}]
    repo.get_latest_signal.return_value = None
    snap = collect_snapshot(signal_repository=repo)
    assert snap.pipeline_runs_today == 1
    assert snap.pipeline_last_status == "SUCCESS"


# v1.1 TASK 2/3 -- Signal Intelligence + Decision Engine

def test_decision_breakdown_counts_approved_and_rejected():
    rows = [
        {"ai_decision": "APPROVE", "confidence_score": 0.8, "risk_status": "PASSED", "strategy_name": "FVG_STRATEGY"},
        {"ai_decision": "REJECT", "confidence_score": 0.4, "risk_status": "BLOCKED", "strategy_name": "AMD_STRATEGY"},
        {"ai_decision": "NO_TRADE", "confidence_score": 0.3, "risk_status": "BLOCKED", "strategy_name": "AMD_STRATEGY"},
    ]
    approved, rejected, breakdown, avg_confidence, risk_pass_rate = _decision_breakdown(rows)
    assert approved == 1
    assert rejected == 2
    assert breakdown == "AMD: 2, FVG: 1"
    assert avg_confidence == 50.0
    assert risk_pass_rate == 33.3


def test_decision_breakdown_empty_rows_returns_zeros():
    approved, rejected, breakdown, avg_confidence, risk_pass_rate = _decision_breakdown([])
    assert approved == 0
    assert rejected == 0
    assert breakdown == ""
    assert avg_confidence == 0.0
    assert risk_pass_rate == 0.0


def test_decision_breakdown_strips_strategy_suffix():
    rows = [{"strategy_name": "LIQUIDITY_SWEEP_STRATEGY", "ai_decision": "APPROVE", "risk_status": "PASSED"}]
    _, _, breakdown, _, _ = _decision_breakdown(rows)
    assert breakdown == "LIQUIDITY_SWEEP: 1"


def test_last_signal_score_converts_confidence_to_percentage():
    repo = MagicMock()
    repo.get_latest_signal.return_value = {"confidence_score": 0.82}
    assert _last_signal_score(repo) == 82


def test_last_signal_score_none_when_no_signal():
    repo = MagicMock()
    repo.get_latest_signal.return_value = None
    assert _last_signal_score(repo) is None


def test_last_signal_score_handles_repository_failure():
    repo = MagicMock()
    repo.get_latest_signal.side_effect = Exception("boom")
    assert _last_signal_score(repo) is None


def test_collect_snapshot_decision_total_matches_row_count():
    repo = MagicMock()
    repo.get_signals_today.return_value = [
        {"created_at": "2026-01-01T10:00:00", "ai_decision": "APPROVE", "confidence_score": 0.9, "risk_status": "PASSED"},
    ]
    repo.get_latest_signal.return_value = None
    snap = collect_snapshot(signal_repository=repo)
    assert snap.decision_total == 1
    assert snap.decision_approved == 1
    assert snap.decision_avg_confidence_pct == 90.0


# v1.1 TASK 4 -- AI Layer Monitoring (always honest zero/NO_DATA)

def test_collect_snapshot_ai_status_is_always_no_data():
    snap = collect_snapshot()
    assert snap.ai_status == "NO_DATA"
    assert snap.ai_requests_today == 0


# v1.1 TASK 5 -- Market Data Monitoring Upgrade

def test_collect_snapshot_market_fields_reflect_configuration():
    with patch("monitoring.snapshot_collector.get_market_health") as mocked:
        mocked.return_value = MagicMock(data_source_status="ONLINE")
        snap = collect_snapshot(symbol="XAUUSD", provider_name="twelvedata")
    assert snap.market_provider == "twelvedata"
    assert snap.market_symbol == "XAUUSD"
    assert snap.market_timeframe == DEFAULT_TIMEFRAME
    assert snap.market_candles_configured > 0


# v1.1 TASK 6 -- Error Intelligence

def test_error_breakdown_counts_by_severity():
    critical_event = MagicMock(severity=MagicMock(value="CRITICAL"), module="Core", timestamp="2026-01-01T10:00:00")
    warning_event = MagicMock(severity=MagicMock(value="WARNING"), module="Market", timestamp="2026-01-01T09:00:00")
    with patch("monitoring.snapshot_collector.ErrorMonitor") as mocked:
        mocked.return_value.get_recent_errors.return_value = [critical_event, warning_event]
        critical, warning, last_module, last_time = _error_breakdown()
    assert critical == 1
    assert warning == 1
    assert last_module == "Core"
    assert last_time == "2026-01-01T10:00:00"


def test_error_breakdown_empty_when_no_errors():
    with patch("monitoring.snapshot_collector.ErrorMonitor") as mocked:
        mocked.return_value.get_recent_errors.return_value = []
        critical, warning, last_module, last_time = _error_breakdown()
    assert critical == 0
    assert warning == 0
    assert last_module is None
    assert last_time is None


def test_error_breakdown_handles_failure():
    with patch("monitoring.snapshot_collector.ErrorMonitor") as mocked:
        mocked.return_value.get_recent_errors.side_effect = Exception("boom")
        critical, warning, last_module, last_time = _error_breakdown()
    assert (critical, warning, last_module, last_time) == (0, 0, None, None)


# v1.1 TASK 7 -- System Runtime Metrics

def test_next_check_time_rounds_up_to_next_boundary():
    now = datetime(2026, 1, 1, 18, 3, tzinfo=timezone.utc)
    assert next_check_time(now) == "18:15 UTC"


def test_next_check_time_exactly_on_boundary_advances_a_full_interval():
    now = datetime(2026, 1, 1, 18, 15, tzinfo=timezone.utc)
    assert next_check_time(now) == "18:30 UTC"


def test_collect_snapshot_sets_runtime_next_check():
    snap = collect_snapshot()
    assert snap.runtime_next_check is not None
    assert "UTC" in snap.runtime_next_check


# v1.1 TASK 8 -- Database Statistics

def test_pipeline_events_total_handles_failure():
    with patch("monitoring.snapshot_collector.MonitoringRepository", side_effect=Exception("boom")):
        assert _pipeline_events_total() == 0


def test_pipeline_events_total_counts_recent_entries():
    with patch("monitoring.snapshot_collector.MonitoringRepository") as mocked:
        mocked.return_value.get_recent_decision_entries.return_value = [MagicMock(), MagicMock()]
        assert _pipeline_events_total() == 2


def test_collect_snapshot_db_signals_total_matches_today_rows():
    repo = MagicMock()
    repo.get_signals_today.return_value = [{"created_at": "2026-01-01T10:00:00", "ai_decision": "APPROVE"}]
    repo.get_latest_signal.return_value = None
    snap = collect_snapshot(signal_repository=repo)
    assert snap.db_signals_total == 1
