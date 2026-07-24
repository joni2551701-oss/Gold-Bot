"""Phase B.0 -- telegram/owner/monitoring_commands.py additions (get_performance_report, /owner_status resource+health lines) tests."""

from unittest.mock import patch

from monitoring.models import HealthStatus, PerformanceCounters, ResourceSnapshot, SystemHealth
from telegram.owner.monitoring_commands import get_performance_report, get_status_report
from telegram.owner.provider_commands import ProviderCommandResult


def _system_health(**overrides):
    defaults = dict(status="RUNNING", uptime_seconds=90.0, data_connection="1/1 ONLINE", database_status="OK")
    defaults.update(overrides)
    return SystemHealth(**defaults)


def _resource_snapshot(**overrides):
    defaults = dict(
        cpu_time_seconds=1.5, max_rss_kb=2048, thread_count=4,
        restart_count=2, uptime_seconds=90.0, heartbeat_at="2026-01-01T00:00:00Z",
    )
    defaults.update(overrides)
    return ResourceSnapshot(**defaults)


def test_get_performance_report_returns_provider_command_result():
    with patch("telegram.owner.monitoring_commands.is_owner_monitoring_enabled", return_value=True), \
         patch("telegram.owner.monitoring_commands.get_performance_counts", return_value=PerformanceCounters(signal_count=3)):
        result = get_performance_report()
    assert isinstance(result, ProviderCommandResult)
    assert result.success is True


def test_get_performance_report_shows_counts():
    counts = PerformanceCounters(signal_count=3, decision_count=2, trade_count=1, reject_count=1, error_count=0, reconnect_count=1)
    with patch("telegram.owner.monitoring_commands.is_owner_monitoring_enabled", return_value=True), \
         patch("telegram.owner.monitoring_commands.get_performance_counts", return_value=counts):
        result = get_performance_report()
    assert "Signals: 3" in result.message
    assert "Decisions: 2" in result.message
    assert "Trades: 1" in result.message
    assert "Rejects: 1" in result.message
    assert "Reconnects: 1" in result.message


def test_get_performance_report_disabled_when_flag_off():
    with patch("telegram.owner.monitoring_commands.is_owner_monitoring_enabled", return_value=False):
        result = get_performance_report()
    assert result.success is False


def test_get_performance_report_never_raises_on_failure():
    with patch("telegram.owner.monitoring_commands.is_owner_monitoring_enabled", return_value=True), \
         patch("telegram.owner.monitoring_commands.get_performance_counts", side_effect=Exception("fail")):
        result = get_performance_report()
    assert result.success is False


def test_get_status_report_omits_resource_lines_when_flag_off():
    with patch("telegram.owner.monitoring_commands.get_system_health_snapshot", return_value=_system_health()), \
         patch("telegram.owner.monitoring_commands.is_owner_monitoring_enabled", return_value=False):
        result = get_status_report()
    assert "Overall health" not in result.message
    assert "Resources:" not in result.message


def test_get_status_report_includes_overall_health_when_flag_on():
    with patch("telegram.owner.monitoring_commands.get_system_health_snapshot", return_value=_system_health()), \
         patch("telegram.owner.monitoring_commands.is_owner_monitoring_enabled", return_value=True), \
         patch("telegram.owner.monitoring_commands.classify_health", return_value=HealthStatus.OK), \
         patch("telegram.owner.monitoring_commands.get_resource_snapshot", return_value=_resource_snapshot()):
        result = get_status_report()
    assert "Overall health: OK" in result.message


def test_get_status_report_includes_resource_line_when_flag_on():
    with patch("telegram.owner.monitoring_commands.get_system_health_snapshot", return_value=_system_health()), \
         patch("telegram.owner.monitoring_commands.is_owner_monitoring_enabled", return_value=True), \
         patch("telegram.owner.monitoring_commands.classify_health", return_value=HealthStatus.OK), \
         patch("telegram.owner.monitoring_commands.get_resource_snapshot", return_value=_resource_snapshot()):
        result = get_status_report()
    assert "Threads 4" in result.message
    assert "Restarts 2" in result.message


def test_get_status_report_resource_line_shows_na_for_missing_cpu_ram():
    snapshot = _resource_snapshot(cpu_time_seconds=None, max_rss_kb=None)
    with patch("telegram.owner.monitoring_commands.get_system_health_snapshot", return_value=_system_health()), \
         patch("telegram.owner.monitoring_commands.is_owner_monitoring_enabled", return_value=True), \
         patch("telegram.owner.monitoring_commands.classify_health", return_value=HealthStatus.OK), \
         patch("telegram.owner.monitoring_commands.get_resource_snapshot", return_value=snapshot):
        result = get_status_report()
    assert "CPU N/A" in result.message
    assert "RAM N/A" in result.message


def test_get_status_report_still_includes_original_lines_when_flag_on():
    """Additive only: the pre-existing lines must never be removed."""
    with patch("telegram.owner.monitoring_commands.get_system_health_snapshot", return_value=_system_health()), \
         patch("telegram.owner.monitoring_commands.is_owner_monitoring_enabled", return_value=True), \
         patch("telegram.owner.monitoring_commands.classify_health", return_value=HealthStatus.OK), \
         patch("telegram.owner.monitoring_commands.get_resource_snapshot", return_value=_resource_snapshot()):
        result = get_status_report()
    assert "RUNNING" in result.message
    assert "1m 30s" in result.message


def test_get_status_report_never_raises_when_resource_snapshot_fails():
    with patch("telegram.owner.monitoring_commands.get_system_health_snapshot", return_value=_system_health()), \
         patch("telegram.owner.monitoring_commands.is_owner_monitoring_enabled", return_value=True), \
         patch("telegram.owner.monitoring_commands.classify_health", side_effect=Exception("fail")):
        result = get_status_report()
    assert result.success is False
