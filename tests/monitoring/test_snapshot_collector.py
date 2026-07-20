"""GoldBot Core Owner Snapshot Reporter Alpha, TASK 2 -- monitoring/snapshot_collector.py tests."""

from unittest.mock import MagicMock, patch

from monitoring.snapshot_collector import (
    _format_uptime,
    _last_signal_summary,
    _telegram_status,
    collect_snapshot,
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
