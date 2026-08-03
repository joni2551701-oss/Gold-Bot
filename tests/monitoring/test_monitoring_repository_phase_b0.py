"""Phase B.0 -- database_layer/audit_log/monitoring_repository.py additions (stage_durations_ms persistence, record_process_start/get_restart_count) tests."""

import os

import pytest

from config import Config
from database_layer.audit_log.monitoring_repository import (
    MonitoringRepository,
    _deserialize_stage_durations,
    _serialize_stage_durations,
)


def test_serialize_stage_durations_empty():
    assert _serialize_stage_durations(()) == ""


def test_serialize_stage_durations_single_stage():
    assert _serialize_stage_durations((("context", 4.2),)) == "context:4.2"


def test_serialize_stage_durations_multiple_stages():
    result = _serialize_stage_durations((("context", 4.2), ("signal", 1.1)))
    assert result == "context:4.2,signal:1.1"


def test_deserialize_stage_durations_empty_string():
    assert _deserialize_stage_durations("") == ()


def test_deserialize_stage_durations_single_stage():
    assert _deserialize_stage_durations("context:4.2") == (("context", 4.2),)


def test_deserialize_stage_durations_multiple_stages():
    result = _deserialize_stage_durations("context:4.2,signal:1.1")
    assert result == (("context", 4.2), ("signal", 1.1))


def test_serialize_then_deserialize_round_trips():
    original = (("context", 4.2), ("signal", 1.1), ("ai", 812.0))
    assert _deserialize_stage_durations(_serialize_stage_durations(original)) == original


@pytest.fixture
def repository(tmp_path, monkeypatch):
    db_path = os.path.join(str(tmp_path), "phase_b0_monitoring_test.db")
    monkeypatch.setattr(Config, "DB_PATH", db_path)
    return MonitoringRepository()


def test_record_decision_entry_persists_stage_durations_ms(repository):
    repository.record_decision_entry(
        "XAUUSD", "M15", ("STRUCTURE_ALIGNED",), 5, "NO TRADE", "FVG failed",
        stage_durations_ms=(("context", 4.2), ("signal", 1.1)),
    )
    entries = repository.get_recent_decision_entries()
    assert entries[0].stage_durations_ms == (("context", 4.2), ("signal", 1.1))


def test_record_decision_entry_defaults_stage_durations_ms_to_empty(repository):
    repository.record_decision_entry("XAUUSD", "M15", (), 5, "NO TRADE")
    entries = repository.get_recent_decision_entries()
    assert entries[0].stage_durations_ms == ()


def test_record_process_start_returns_process_start_entry(repository):
    from database_layer.audit_log.monitoring_models import ProcessStartEntry

    entry = repository.record_process_start()
    assert isinstance(entry, ProcessStartEntry)


def test_get_restart_count_starts_at_zero(repository):
    assert repository.get_restart_count() == 0


def test_get_restart_count_increments_after_record_process_start(repository):
    repository.record_process_start()
    assert repository.get_restart_count() == 1


def test_get_restart_count_after_three_starts(repository):
    repository.record_process_start()
    repository.record_process_start()
    repository.record_process_start()
    assert repository.get_restart_count() == 3


def test_record_process_start_never_updates_existing_rows(repository):
    repository.record_process_start()
    repository.record_process_start()
    assert repository.get_restart_count() == 2
