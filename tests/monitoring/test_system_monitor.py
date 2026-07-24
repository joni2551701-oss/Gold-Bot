"""GoldBot Core Owner Monitoring Alpha, TASK 2 -- monitoring/system_monitor.py tests."""

from unittest.mock import MagicMock

from monitoring.models import SystemHealth
from monitoring.provider_health import ProviderHealthReport, ProviderHealthStatus
from monitoring.system_monitor import SystemMonitor, get_health, record_error, record_scan


def _admin_service(database="OK"):
    admin_service = MagicMock()
    admin_service.get_system_status.return_value = MagicMock(database=database)
    return admin_service


def _registry(reports):
    registry = MagicMock()
    return registry, reports


def test_get_health_returns_system_health():
    monitor = SystemMonitor()
    health = monitor.get_health(admin_service=_admin_service())
    assert isinstance(health, SystemHealth)


def test_get_health_relays_database_status():
    monitor = SystemMonitor()
    health = monitor.get_health(admin_service=_admin_service(database="OK"))
    assert health.database_status == "OK"


def test_get_health_relays_database_failure_status():
    monitor = SystemMonitor()
    health = monitor.get_health(admin_service=_admin_service(database="FAIL"))
    assert health.database_status == "FAIL"


def test_get_health_status_is_running():
    monitor = SystemMonitor()
    health = monitor.get_health(admin_service=_admin_service())
    assert health.status == "RUNNING"


def test_get_health_never_raises_on_admin_service_failure():
    monitor = SystemMonitor()
    broken_admin_service = MagicMock()
    broken_admin_service.get_system_status.side_effect = Exception("boom")
    health = monitor.get_health(admin_service=broken_admin_service)
    assert health.database_status == "N/A"


def test_get_health_never_raises_on_registry_failure(monkeypatch):
    monitor = SystemMonitor()

    def _raise(*args, **kwargs):
        raise Exception("registry boom")

    monkeypatch.setattr("monitoring.system_monitor.check_registry_health", _raise)
    health = monitor.get_health(admin_service=_admin_service())
    assert health.data_connection == "N/A"


def test_get_health_data_connection_counts_online(monkeypatch):
    monitor = SystemMonitor()
    reports = [
        ProviderHealthReport(provider_name="a", status=ProviderHealthStatus.ONLINE, latency_ms=1.0),
        ProviderHealthReport(provider_name="b", status=ProviderHealthStatus.OFFLINE, latency_ms=1.0),
    ]
    monkeypatch.setattr("monitoring.system_monitor.check_registry_health", lambda registry: reports)
    health = monitor.get_health(admin_service=_admin_service())
    assert health.data_connection == "1/2 ONLINE"


def test_uptime_seconds_increases():
    monitor = SystemMonitor()
    first = monitor.uptime_seconds()
    second = monitor.uptime_seconds()
    assert second >= first


def test_uptime_seconds_never_negative():
    monitor = SystemMonitor()
    assert monitor.uptime_seconds() >= 0.0


def test_record_scan_sets_last_scan():
    monitor = SystemMonitor()
    monitor.record_scan("2026-01-01T00:00:00Z")
    health = monitor.get_health(admin_service=_admin_service())
    assert health.last_scan == "2026-01-01T00:00:00Z"


def test_record_scan_defaults_to_now_when_no_timestamp_given():
    monitor = SystemMonitor()
    monitor.record_scan()
    health = monitor.get_health(admin_service=_admin_service())
    assert health.last_scan is not None
    assert health.last_scan != ""


def test_last_scan_none_before_record_scan_called():
    monitor = SystemMonitor()
    health = monitor.get_health(admin_service=_admin_service())
    assert health.last_scan is None


def test_record_error_sets_last_error():
    monitor = SystemMonitor()
    monitor.record_error("something broke")
    health = monitor.get_health(admin_service=_admin_service())
    assert health.last_error == "something broke"


def test_last_error_none_before_record_error_called():
    monitor = SystemMonitor()
    health = monitor.get_health(admin_service=_admin_service())
    assert health.last_error is None


def test_record_error_never_raises_on_none_message():
    monitor = SystemMonitor()
    monitor.record_error(None)
    health = monitor.get_health(admin_service=_admin_service())
    assert health.last_error is None


def test_module_level_get_health_uses_default_monitor():
    health = get_health(admin_service=_admin_service())
    assert isinstance(health, SystemHealth)


def test_module_level_record_scan_and_record_error_never_raise():
    record_scan("2026-02-02T00:00:00Z")
    record_error("module-level error")


def test_two_monitor_instances_are_independent():
    a = SystemMonitor()
    b = SystemMonitor()
    a.record_scan("2026-03-03T00:00:00Z")
    health_a = a.get_health(admin_service=_admin_service())
    health_b = b.get_health(admin_service=_admin_service())
    assert health_a.last_scan == "2026-03-03T00:00:00Z"
    assert health_b.last_scan is None


def test_system_monitor_default_construction_never_raises():
    assert SystemMonitor() is not None


def test_get_health_never_computes_a_trading_verdict():
    """Rule: Monitoring never decides a trade -- SystemHealth carries no verdict-shaped field."""
    from dataclasses import fields
    field_names = {f.name for f in fields(SystemHealth)}
    forbidden = {"signal", "decision", "verdict", "direction"}
    assert field_names.isdisjoint(forbidden)
