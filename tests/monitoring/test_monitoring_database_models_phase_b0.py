"""Phase B.0 -- database/monitoring_models.py additions (DecisionPipelineEntryRow.stage_durations_ms, ProcessStartEntry) tests."""

from datetime import datetime

from database.monitoring_models import (
    ProcessStartEntry,
    create_decision_pipeline_entry_row,
    create_process_start_entry,
)


def test_create_decision_pipeline_entry_row_defaults_stage_durations_ms_to_empty_tuple():
    row = create_decision_pipeline_entry_row("XAUUSD", "M15", (), 5, "NO TRADE")
    assert row.stage_durations_ms == ()


def test_create_decision_pipeline_entry_row_relays_stage_durations_ms():
    row = create_decision_pipeline_entry_row(
        "XAUUSD", "M15", (), 5, "NO TRADE", stage_durations_ms=[("context", 4.2), ("signal", 1.1)],
    )
    assert row.stage_durations_ms == (("context", 4.2), ("signal", 1.1))


def test_create_decision_pipeline_entry_row_stamps_created_at():
    row = create_decision_pipeline_entry_row("XAUUSD", "M15", (), 5, "NO TRADE")
    assert isinstance(row.created_at, datetime)


def test_create_process_start_entry_returns_process_start_entry():
    entry = create_process_start_entry()
    assert isinstance(entry, ProcessStartEntry)


def test_create_process_start_entry_stamps_created_at():
    entry = create_process_start_entry()
    assert isinstance(entry.created_at, datetime)


def test_create_process_start_entry_is_deterministic_shape():
    a = create_process_start_entry()
    b = create_process_start_entry()
    assert a.created_at <= b.created_at
