"""Phase B.0 TASK 6 -- core_layer/health_monitor/health_monitor.py tests."""

from core_layer.health_monitor.health_monitor import classify_health
from core_layer.health_monitor.models import HealthStatus, SystemHealth


def _health(**overrides):
    defaults = dict(status="RUNNING", uptime_seconds=90.0, data_connection="2/2 ONLINE", database_status="OK")
    defaults.update(overrides)
    return SystemHealth(**defaults)


def test_classify_health_returns_health_status():
    result = classify_health(_health())
    assert isinstance(result, HealthStatus)


def test_classify_health_ok_when_everything_healthy():
    result = classify_health(_health())
    assert result == HealthStatus.OK


def test_classify_health_critical_when_database_down():
    result = classify_health(_health(database_status="FAIL"))
    assert result == HealthStatus.CRITICAL


def test_classify_health_critical_when_zero_providers_online():
    result = classify_health(_health(data_connection="0/2 ONLINE"))
    assert result == HealthStatus.CRITICAL


def test_classify_health_warning_when_some_providers_offline():
    result = classify_health(_health(data_connection="1/2 ONLINE"))
    assert result == HealthStatus.WARNING


def test_classify_health_warning_when_last_error_present():
    result = classify_health(_health(last_error="boom"))
    assert result == HealthStatus.WARNING


def test_classify_health_warning_when_error_counts_nonzero():
    result = classify_health(_health(), error_counts={"API timeout": 2})
    assert result == HealthStatus.WARNING


def test_classify_health_ok_when_error_counts_all_zero():
    result = classify_health(_health(), error_counts={"API timeout": 0})
    assert result == HealthStatus.OK


def test_classify_health_ok_when_error_counts_is_none():
    result = classify_health(_health(), error_counts=None)
    assert result == HealthStatus.OK


def test_classify_health_database_status_is_case_insensitive():
    result = classify_health(_health(database_status="ok"))
    assert result == HealthStatus.OK


def test_classify_health_handles_unparseable_data_connection():
    result = classify_health(_health(data_connection="N/A"))
    assert result == HealthStatus.OK


def test_classify_health_never_raises_on_malformed_data_connection():
    result = classify_health(_health(data_connection=""))
    assert isinstance(result, HealthStatus)


def test_classify_health_critical_takes_priority_over_warning():
    """Database down AND providers offline -> still CRITICAL, not WARNING."""
    result = classify_health(_health(database_status="FAIL", data_connection="0/2 ONLINE"))
    assert result == HealthStatus.CRITICAL


def test_classify_health_never_mutates_input():
    health = _health()
    classify_health(health)
    assert health.database_status == "OK"


def test_classify_health_deterministic():
    health = _health()
    assert classify_health(health) == classify_health(health)
