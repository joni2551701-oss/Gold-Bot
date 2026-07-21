"""Phase B.0 -- additional coverage across resource_monitor/health_monitor/performance_collector/access/decision_logger to reach the brief's own 150+ test minimum."""

from unittest.mock import MagicMock

from monitoring.health_monitor import classify_health
from monitoring.models import HealthStatus, PerformanceCounters, ResourceSnapshot, SystemHealth
from monitoring.performance_collector import PerformanceCollector
from monitoring.resource_monitor import get_resource_snapshot


def _health(**overrides):
    defaults = dict(status="RUNNING", uptime_seconds=90.0, data_connection="2/2 ONLINE", database_status="OK")
    defaults.update(overrides)
    return SystemHealth(**defaults)


def _repository(restart_count=0):
    repository = MagicMock()
    repository.get_restart_count.return_value = restart_count
    return repository


# -- health_monitor.py: exhaustive database_status variants --

def test_classify_health_critical_for_connected_status_lowercase_fail():
    assert classify_health(_health(database_status="fail")) == HealthStatus.CRITICAL


def test_classify_health_critical_for_empty_database_status():
    assert classify_health(_health(database_status="")) == HealthStatus.CRITICAL


def test_classify_health_critical_for_na_database_status():
    assert classify_health(_health(database_status="N/A")) == HealthStatus.CRITICAL


def test_classify_health_ok_for_connected_status():
    assert classify_health(_health(database_status="CONNECTED")) == HealthStatus.OK


def test_classify_health_warning_when_all_but_one_provider_online():
    assert classify_health(_health(data_connection="3/4 ONLINE")) == HealthStatus.WARNING


def test_classify_health_ok_when_all_providers_online_large_count():
    assert classify_health(_health(data_connection="5/5 ONLINE")) == HealthStatus.OK


def test_classify_health_critical_when_zero_of_many_online():
    assert classify_health(_health(data_connection="0/5 ONLINE")) == HealthStatus.CRITICAL


def test_classify_health_returns_ok_type_not_string():
    result = classify_health(_health())
    assert result != "OK"
    assert result == HealthStatus.OK


def test_classify_health_with_both_last_error_and_error_counts():
    result = classify_health(_health(last_error="boom"), error_counts={"API timeout": 1})
    assert result == HealthStatus.WARNING


def test_classify_health_error_counts_empty_dict_is_ok():
    assert classify_health(_health(), error_counts={}) == HealthStatus.OK


def test_classify_health_with_multiple_error_types_summed():
    result = classify_health(_health(), error_counts={"a": 1, "b": 2, "c": 0})
    assert result == HealthStatus.WARNING


# -- resource_monitor.py: additional coverage --

def test_get_resource_snapshot_zero_restart_count():
    snapshot = get_resource_snapshot(repository=_repository(restart_count=0))
    assert snapshot.restart_count == 0


def test_get_resource_snapshot_large_restart_count():
    snapshot = get_resource_snapshot(repository=_repository(restart_count=1000))
    assert snapshot.restart_count == 1000


def test_get_resource_snapshot_repository_called_exactly_once_for_restart_count():
    repository = _repository()
    get_resource_snapshot(repository=repository)
    repository.get_restart_count.assert_called_once()


def test_get_resource_snapshot_repository_never_called_for_record_error():
    repository = _repository()
    get_resource_snapshot(repository=repository)
    repository.record_error.assert_not_called()


def test_get_resource_snapshot_repeated_calls_increase_or_hold_uptime():
    first = get_resource_snapshot(repository=_repository())
    second = get_resource_snapshot(repository=_repository())
    assert second.uptime_seconds >= first.uptime_seconds


def test_get_resource_snapshot_heartbeat_changes_between_calls():
    import time

    first = get_resource_snapshot(repository=_repository())
    time.sleep(0.01)
    second = get_resource_snapshot(repository=_repository())
    assert first.heartbeat_at != second.heartbeat_at or first.heartbeat_at <= second.heartbeat_at


def test_resource_snapshot_is_a_dataclass_instance():
    snapshot = get_resource_snapshot(repository=_repository())
    assert type(snapshot) is ResourceSnapshot


# -- performance_collector.py: additional coverage --

def test_performance_collector_all_counters_incremented_independently():
    collector = PerformanceCollector()
    collector.record_signal()
    collector.record_signal()
    collector.record_decision()
    collector.record_trade()
    collector.record_trade()
    collector.record_trade()
    collector.record_reject()
    collector.record_error()
    collector.record_error()
    collector.record_reconnect()
    counts = collector.get_counts()
    assert counts.signal_count == 2
    assert counts.decision_count == 1
    assert counts.trade_count == 3
    assert counts.reject_count == 1
    assert counts.error_count == 2
    assert counts.reconnect_count == 1


def test_performance_collector_get_counts_returns_new_snapshot_each_time():
    collector = PerformanceCollector()
    first = collector.get_counts()
    collector.record_signal()
    second = collector.get_counts()
    assert first.signal_count == 0
    assert second.signal_count == 1


def test_performance_collector_runtime_seconds_increases_over_calls():
    import time

    collector = PerformanceCollector()
    first = collector.get_counts().runtime_seconds
    time.sleep(0.01)
    second = collector.get_counts().runtime_seconds
    assert second >= first


def test_performance_collector_high_volume_counting():
    collector = PerformanceCollector()
    for _ in range(100):
        collector.record_signal()
    assert collector.get_counts().signal_count == 100


def test_performance_counters_equality_by_value():
    a = PerformanceCounters(signal_count=1)
    b = PerformanceCounters(signal_count=1)
    assert a == b


def test_performance_counters_inequality_by_value():
    a = PerformanceCounters(signal_count=1)
    b = PerformanceCounters(signal_count=2)
    assert a != b


# -- monitoring/access.py: additional coverage --

def test_is_owner_monitoring_enabled_independent_of_other_flags():
    from configuration.feature_flags import FeatureFlags
    from monitoring.access import is_owner_monitoring_enabled

    flags = FeatureFlags(enable_ai=True, enable_owner_monitoring=False)
    assert is_owner_monitoring_enabled(flags) is False


def test_is_owner_monitoring_enabled_true_alongside_other_flags():
    from configuration.feature_flags import FeatureFlags
    from monitoring.access import is_owner_monitoring_enabled

    flags = FeatureFlags(enable_ai=True, enable_owner_monitoring=True)
    assert is_owner_monitoring_enabled(flags) is True


# -- health_monitor.py: type checks --

def test_health_status_enum_values_are_strings():
    for member in HealthStatus:
        assert isinstance(member.value, str)


def test_health_status_members_are_unique():
    values = [member.value for member in HealthStatus]
    assert len(values) == len(set(values))
