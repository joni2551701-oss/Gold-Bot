"""GoldBot Core Owner Monitoring Alpha, TASK 7 -- platform_layer/telegram/owner/monitoring_commands.py tests."""

from unittest.mock import MagicMock, patch

from decision_layer.decision_logger.decision_logger import DecisionLogger
from core_layer.health_monitor.error_monitor import ErrorMonitor
from core_layer.health_monitor.models import DecisionPipelineEntry, SignalHealth, SystemHealth
from platform_layer.telegram.owner.monitoring_commands import (
    get_daily_report,
    get_errors_report,
    get_health_report,
    get_market_report,
    get_pipeline_report,
    get_signals_report,
    get_status_report,
)
from platform_layer.telegram.owner.provider_commands import ProviderCommandResult


def _system_health(**overrides):
    defaults = dict(status="RUNNING", uptime_seconds=90.0, data_connection="1/1 ONLINE", database_status="OK")
    defaults.update(overrides)
    return SystemHealth(**defaults)


def test_get_status_report_returns_provider_command_result():
    with patch("platform_layer.telegram.owner.monitoring_commands.get_system_health_snapshot", return_value=_system_health()):
        result = get_status_report()
    assert isinstance(result, ProviderCommandResult)
    assert result.success is True


def test_get_status_report_includes_status_and_uptime():
    with patch("platform_layer.telegram.owner.monitoring_commands.get_system_health_snapshot", return_value=_system_health()):
        result = get_status_report()
    assert "RUNNING" in result.message
    assert "1m 30s" in result.message


def test_get_status_report_shows_na_for_missing_last_scan():
    with patch("platform_layer.telegram.owner.monitoring_commands.get_system_health_snapshot", return_value=_system_health(last_scan=None)):
        result = get_status_report()
    assert "N/A" in result.message


def test_get_status_report_includes_last_error_when_present():
    with patch("platform_layer.telegram.owner.monitoring_commands.get_system_health_snapshot", return_value=_system_health(last_error="boom")):
        result = get_status_report()
    assert "boom" in result.message


def test_get_status_report_never_raises_on_failure():
    with patch("platform_layer.telegram.owner.monitoring_commands.get_system_health_snapshot", side_effect=Exception("fail")):
        result = get_status_report()
    assert result.success is False


def test_get_health_report_delegates_to_system_commands():
    expected = ProviderCommandResult(success=True, message="diagnostic text")
    with patch("platform_layer.telegram.owner.monitoring_commands.get_system_health", return_value=expected) as mocked:
        result = get_health_report()
    mocked.assert_called_once()
    assert result is expected


def test_get_market_report_returns_provider_command_result():
    with patch("platform_layer.telegram.owner.monitoring_commands.get_market_health") as mocked:
        mocked.return_value = MagicMock(symbol="XAUUSD", last_price=None, last_update=None, data_source_status="ONLINE", latency_ms=10.0)
        result = get_market_report()
    assert isinstance(result, ProviderCommandResult)
    assert "XAUUSD" in result.message


def test_get_market_report_shows_na_for_missing_latency():
    with patch("platform_layer.telegram.owner.monitoring_commands.get_market_health") as mocked:
        mocked.return_value = MagicMock(symbol="XAUUSD", last_price=None, last_update=None, data_source_status="UNKNOWN", latency_ms=None)
        result = get_market_report()
    assert "Latency: N/A" in result.message


def test_get_market_report_never_raises_on_failure():
    with patch("platform_layer.telegram.owner.monitoring_commands.get_market_health", side_effect=Exception("fail")):
        result = get_market_report()
    assert result.success is False


def test_get_signals_report_shows_counts():
    health = SignalHealth(total_signals=8, buy_count=5, sell_count=3, none_count=0, average_confidence=0.78)
    with patch("platform_layer.telegram.owner.monitoring_commands.get_signal_health", return_value=health):
        result = get_signals_report()
    assert "BUY: 5" in result.message
    assert "SELL: 3" in result.message
    assert "78%" in result.message


def test_get_signals_report_never_raises_on_failure():
    with patch("platform_layer.telegram.owner.monitoring_commands.get_signal_health", side_effect=Exception("fail")):
        result = get_signals_report()
    assert result.success is False


def test_get_errors_report_shows_no_errors_message_when_empty():
    with patch.object(ErrorMonitor, "get_error_counts", return_value={}):
        result = get_errors_report()
    assert "No errors recorded." in result.message


def test_get_errors_report_shows_counts_by_type():
    with patch.object(ErrorMonitor, "get_error_counts", return_value={"API timeout": 2, "Data error": 0}):
        result = get_errors_report()
    assert "API timeout: 2" in result.message
    assert "Data error: 0" in result.message


def test_get_errors_report_never_raises_on_failure():
    with patch.object(ErrorMonitor, "get_error_counts", side_effect=Exception("fail")):
        result = get_errors_report()
    assert result.success is False


def test_get_pipeline_report_shows_no_entries_message_when_empty():
    with patch.object(DecisionLogger, "get_recent_entries", return_value=()):
        result = get_pipeline_report()
    assert "No decision pipeline entries recorded yet." in result.message


def test_get_pipeline_report_shows_criteria_and_decision():
    entry = DecisionPipelineEntry(
        timestamp="2026-01-01T00:00:00Z", symbol="XAUUSD", timeframe="M15",
        criteria_met=("STRUCTURE_ALIGNED",), criteria_total=5, decision="NO TRADE", reason="FVG failed",
    )
    with patch.object(DecisionLogger, "get_recent_entries", return_value=(entry,)):
        result = get_pipeline_report()
    assert "STRUCTURE_ALIGNED: PASS" in result.message
    assert "4 criteria FAIL" in result.message
    assert "Decision: NO TRADE" in result.message
    assert "Reason: FVG failed" in result.message


def test_get_pipeline_report_never_raises_on_failure():
    with patch.object(DecisionLogger, "get_recent_entries", side_effect=Exception("fail")):
        result = get_pipeline_report()
    assert result.success is False


def test_get_daily_report_composes_system_signals_and_errors():
    signals = SignalHealth(total_signals=3, buy_count=2, sell_count=1, none_count=0, average_confidence=0.5)
    with patch("platform_layer.telegram.owner.monitoring_commands.get_system_health_snapshot", return_value=_system_health()), \
         patch("platform_layer.telegram.owner.monitoring_commands.get_signal_health", return_value=signals), \
         patch.object(ErrorMonitor, "get_error_counts", return_value={"API timeout": 1}):
        result = get_daily_report()
    assert "GoldBot Daily Report" in result.message
    assert "BUY: 2" in result.message
    assert "1" in result.message


def test_get_daily_report_never_raises_on_failure():
    with patch("platform_layer.telegram.owner.monitoring_commands.get_system_health_snapshot", side_effect=Exception("fail")):
        result = get_daily_report()
    assert result.success is False


def test_all_report_functions_never_raise_regardless_of_input():
    """A blanket smoke test: every report function must return a ProviderCommandResult, never propagate."""
    for fn in (get_status_report, get_health_report, get_market_report, get_signals_report, get_errors_report, get_pipeline_report, get_daily_report):
        result = fn()
        assert isinstance(result, ProviderCommandResult)
