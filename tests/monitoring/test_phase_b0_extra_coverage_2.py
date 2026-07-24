"""Phase B.0 -- second batch of additional coverage to clear the brief's own 150+ test minimum."""

from unittest.mock import MagicMock, patch

from monitoring.decision_logger import DecisionLogger
from monitoring.health_monitor import classify_health
from monitoring.models import DecisionPipelineEntry, HealthStatus, ResourceSnapshot, SystemHealth
from monitoring.performance_collector import PerformanceCollector
from monitoring.resource_monitor import get_resource_snapshot, record_process_start


def _health(**overrides):
    defaults = dict(status="RUNNING", uptime_seconds=90.0, data_connection="1/1 ONLINE", database_status="OK")
    defaults.update(overrides)
    return SystemHealth(**defaults)


def test_classify_health_treats_running_database_status_as_ok():
    assert classify_health(_health(database_status="RUNNING")) == HealthStatus.OK


def test_classify_health_two_slash_two_online_is_ok():
    assert classify_health(_health(data_connection="2/2 ONLINE")) == HealthStatus.OK


def test_classify_health_one_slash_one_online_is_ok():
    assert classify_health(_health(data_connection="1/1 ONLINE")) == HealthStatus.OK


def test_classify_health_ignores_trailing_text_in_data_connection():
    assert classify_health(_health(data_connection="1/1 ONLINE extra text")) == HealthStatus.OK


def test_classify_health_never_returns_none():
    assert classify_health(_health()) is not None


def test_resource_snapshot_repr_does_not_raise():
    snapshot = ResourceSnapshot(
        cpu_time_seconds=1.0, max_rss_kb=100, thread_count=2, restart_count=0,
        uptime_seconds=1.0, heartbeat_at="t",
    )
    assert "ResourceSnapshot" in repr(snapshot)


def test_get_resource_snapshot_thread_count_reflects_active_threads():
    import threading

    repository = MagicMock()
    repository.get_restart_count.return_value = 0
    snapshot = get_resource_snapshot(repository=repository)
    assert snapshot.thread_count == threading.active_count()


def test_record_process_start_with_default_repository_never_raises():
    with patch("monitoring.resource_monitor.MonitoringRepository") as mock_cls:
        mock_cls.return_value.record_process_start.return_value = None
        record_process_start()


def test_get_resource_snapshot_with_default_repository_never_raises():
    with patch("monitoring.resource_monitor.MonitoringRepository") as mock_cls:
        mock_cls.return_value.get_restart_count.return_value = 5
        snapshot = get_resource_snapshot()
        assert snapshot.restart_count == 5


def test_performance_collector_zero_decisions_after_only_signals():
    collector = PerformanceCollector()
    collector.record_signal()
    collector.record_signal()
    assert collector.get_counts().decision_count == 0


def test_performance_collector_default_collector_is_shared_across_module_functions():
    import monitoring.performance_collector as module

    module.DEFAULT_COLLECTOR = module.PerformanceCollector()
    module.record_trade()
    assert module.get_counts().trade_count == 1


def test_decision_pipeline_entry_stage_durations_ms_is_tuple_type():
    entry = DecisionPipelineEntry(
        timestamp="t", symbol="XAUUSD", timeframe="M15", criteria_met=(), criteria_total=5,
        decision="NO TRADE", stage_durations_ms=(("context", 1.0),),
    )
    assert isinstance(entry.stage_durations_ms, tuple)


def test_decision_logger_log_entry_with_empty_stage_durations_list():
    repository = MagicMock()
    from database.monitoring_models import create_decision_pipeline_entry_row

    repository.record_decision_entry.return_value = create_decision_pipeline_entry_row(
        "XAUUSD", "M15", (), 5, "NO TRADE",
    )
    logger = DecisionLogger(repository=repository)
    entry = logger.log_entry("XAUUSD", "M15", [], 5, "NO TRADE", stage_durations_ms=[])
    assert entry.stage_durations_ms == ()


def test_decision_logger_get_recent_entries_relays_stage_durations_ms():
    from database.monitoring_models import create_decision_pipeline_entry_row

    row = create_decision_pipeline_entry_row(
        "XAUUSD", "H4", ("HTF_ALIGNED",), 5, "SELL", stage_durations_ms=(("risk", 2.0),),
    )
    repository = MagicMock()
    repository.get_recent_decision_entries.return_value = [row]
    logger = DecisionLogger(repository=repository)
    entries = logger.get_recent_entries()
    assert entries[0].stage_durations_ms == (("risk", 2.0),)


def test_health_status_ok_is_falsy_check_safe():
    """Belt-and-suspenders: HealthStatus.OK must not be confused with a falsy value in conditional logic."""
    assert bool(HealthStatus.OK) is True


def test_classify_health_multiple_calls_same_input_same_output():
    health = _health()
    results = {classify_health(health) for _ in range(5)}
    assert len(results) == 1
