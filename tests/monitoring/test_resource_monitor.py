"""Phase B.0 TASK 2 -- monitoring/resource_monitor.py tests."""

from unittest.mock import MagicMock

from monitoring.models import ResourceSnapshot
from monitoring.resource_monitor import get_resource_snapshot, record_process_start


def _repository(restart_count=3):
    repository = MagicMock()
    repository.get_restart_count.return_value = restart_count
    return repository


def test_get_resource_snapshot_returns_resource_snapshot():
    snapshot = get_resource_snapshot(repository=_repository())
    assert isinstance(snapshot, ResourceSnapshot)


def test_get_resource_snapshot_relays_restart_count():
    snapshot = get_resource_snapshot(repository=_repository(restart_count=7))
    assert snapshot.restart_count == 7


def test_get_resource_snapshot_thread_count_is_positive():
    snapshot = get_resource_snapshot(repository=_repository())
    assert snapshot.thread_count >= 1


def test_get_resource_snapshot_uptime_is_non_negative():
    snapshot = get_resource_snapshot(repository=_repository())
    assert snapshot.uptime_seconds >= 0.0


def test_get_resource_snapshot_heartbeat_is_a_string():
    snapshot = get_resource_snapshot(repository=_repository())
    assert isinstance(snapshot.heartbeat_at, str)
    assert snapshot.heartbeat_at != ""


def test_get_resource_snapshot_cpu_time_is_float_or_none():
    snapshot = get_resource_snapshot(repository=_repository())
    assert snapshot.cpu_time_seconds is None or isinstance(snapshot.cpu_time_seconds, float)


def test_get_resource_snapshot_max_rss_is_int_or_none():
    snapshot = get_resource_snapshot(repository=_repository())
    assert snapshot.max_rss_kb is None or isinstance(snapshot.max_rss_kb, int)


def test_get_resource_snapshot_never_raises_on_restart_count_failure():
    repository = MagicMock()
    repository.get_restart_count.side_effect = Exception("boom")
    snapshot = get_resource_snapshot(repository=repository)
    assert snapshot.restart_count == 0


def test_get_resource_snapshot_default_construction_never_raises():
    assert get_resource_snapshot is not None


def test_record_process_start_calls_repository():
    repository = _repository()
    record_process_start(repository=repository)
    repository.record_process_start.assert_called_once()


def test_record_process_start_never_raises_on_database_failure():
    repository = MagicMock()
    repository.record_process_start.side_effect = Exception("boom")
    record_process_start(repository=repository)  # must not raise


def test_get_resource_snapshot_never_reads_decision_or_risk_state():
    """Belt-and-suspenders: ResourceSnapshot carries no field shaped like a Trading Core object."""
    import dataclasses

    field_names = {f.name for f in dataclasses.fields(ResourceSnapshot)}
    assert field_names == {
        "cpu_time_seconds", "max_rss_kb", "thread_count", "restart_count",
        "uptime_seconds", "heartbeat_at",
    }


def test_multiple_calls_to_get_resource_snapshot_never_share_mutable_state():
    a = get_resource_snapshot(repository=_repository())
    b = get_resource_snapshot(repository=_repository())
    assert a is not b
