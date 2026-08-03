"""GoldBot Core Owner Monitoring Alpha, TASK 6 -- core_layer/health_monitor/error_monitor.py tests."""

from unittest.mock import MagicMock

from database_layer.audit_log.monitoring_models import create_error_event_entry
from core_layer.health_monitor.error_monitor import ErrorMonitor
from core_layer.health_monitor.models import ErrorEvent, ErrorSeverity


def _repository(row=None, rows=None):
    repository = MagicMock()
    repository.record_error.return_value = row or create_error_event_entry(
        "system_monitor", "API timeout", "connection timed out", "ERROR",
    )
    repository.get_recent_errors.return_value = rows or []
    return repository


def test_capture_returns_error_event():
    monitor = ErrorMonitor(repository=_repository())
    event = monitor.capture("system_monitor", "API timeout", "connection timed out")
    assert isinstance(event, ErrorEvent)


def test_capture_relays_module_error_type_message():
    monitor = ErrorMonitor(repository=_repository())
    event = monitor.capture("system_monitor", "API timeout", "connection timed out")
    assert event.module == "system_monitor"
    assert event.error_type == "API timeout"
    assert event.message == "connection timed out"


def test_capture_default_severity_is_error():
    row = create_error_event_entry("m", "t", "msg", "ERROR")
    monitor = ErrorMonitor(repository=_repository(row=row))
    event = monitor.capture("m", "t", "msg")
    assert event.severity == ErrorSeverity.ERROR


def test_capture_relays_custom_severity():
    row = create_error_event_entry("m", "t", "msg", "CRITICAL")
    monitor = ErrorMonitor(repository=_repository(row=row))
    event = monitor.capture("m", "t", "msg", severity=ErrorSeverity.CRITICAL)
    assert event.severity == ErrorSeverity.CRITICAL


def test_capture_never_raises_on_database_failure():
    repository = MagicMock()
    repository.record_error.side_effect = Exception("boom")
    monitor = ErrorMonitor(repository=repository)
    result = monitor.capture("m", "t", "msg")
    assert result is None


def test_capture_updates_system_monitor_last_error():
    from core_layer.health_monitor.system_monitor import DEFAULT_MONITOR
    monitor = ErrorMonitor(repository=_repository())
    monitor.capture("system_monitor", "API timeout", "unique marker message")
    assert DEFAULT_MONITOR.get_health().last_error == "unique marker message"


def test_get_recent_errors_returns_sequence():
    monitor = ErrorMonitor(repository=_repository())
    errors = monitor.get_recent_errors()
    assert isinstance(errors, tuple)


def test_get_recent_errors_empty_when_nothing_captured():
    monitor = ErrorMonitor(repository=_repository(rows=[]))
    assert monitor.get_recent_errors() == ()


def test_get_recent_errors_relays_rows():
    row = create_error_event_entry("data_feed", "Data error", "gap detected", "WARNING")
    monitor = ErrorMonitor(repository=_repository(rows=[row]))
    errors = monitor.get_recent_errors()
    assert len(errors) == 1
    assert errors[0].module == "data_feed"
    assert errors[0].severity == ErrorSeverity.WARNING


def test_get_recent_errors_never_raises_on_database_failure():
    repository = MagicMock()
    repository.get_recent_errors.side_effect = Exception("boom")
    monitor = ErrorMonitor(repository=repository)
    assert monitor.get_recent_errors() == ()


def test_get_error_counts_groups_by_error_type():
    rows = [
        create_error_event_entry("m1", "API timeout", "msg1", "ERROR"),
        create_error_event_entry("m2", "API timeout", "msg2", "ERROR"),
        create_error_event_entry("m3", "Data error", "msg3", "WARNING"),
    ]
    monitor = ErrorMonitor(repository=_repository(rows=rows))
    counts = monitor.get_error_counts()
    assert counts == {"API timeout": 2, "Data error": 1}


def test_get_error_counts_empty_dict_when_no_errors():
    monitor = ErrorMonitor(repository=_repository(rows=[]))
    assert monitor.get_error_counts() == {}


def test_get_error_counts_respects_hours_window():
    repository = _repository(rows=[])
    monitor = ErrorMonitor(repository=repository)
    monitor.get_error_counts(hours=1)
    repository.get_recent_errors.assert_called_with(hours=1, limit=200)


def test_error_monitor_default_construction_never_raises():
    assert ErrorMonitor() is not None


def test_capture_never_computes_a_trading_verdict():
    from dataclasses import fields
    field_names = {f.name for f in fields(ErrorEvent)}
    forbidden = {"signal", "decision", "verdict"}
    assert field_names.isdisjoint(forbidden)


def test_error_severity_has_four_members():
    assert len(list(ErrorSeverity)) == 4


def test_error_severity_members():
    values = {m.value for m in ErrorSeverity}
    assert values == {"INFO", "WARNING", "ERROR", "CRITICAL"}
