"""
Phase 59.6, TASK 1 -- core/system_state.py tests.
"""

from datetime import datetime, timezone

from core.system_state import SystemState, SystemStateRecord, create_system_state_record


def test_system_state_has_exactly_five_values():
    assert {s.value for s in SystemState} == {"RUNNING", "VALIDATION", "MAINTENANCE", "PANIC", "READ_ONLY"}


def test_create_system_state_record_stamps_changed_at():
    record = create_system_state_record(SystemState.RUNNING)

    assert isinstance(record, SystemStateRecord)
    assert record.state == SystemState.RUNNING
    assert isinstance(record.changed_at, datetime)
    assert record.changed_at.tzinfo is not None


def test_create_system_state_record_accepts_changed_by_and_reason():
    record = create_system_state_record(SystemState.MAINTENANCE, changed_by="owner", reason="server upgrade")

    assert record.changed_by == "owner"
    assert record.reason == "server upgrade"


def test_create_system_state_record_defaults_are_none():
    record = create_system_state_record(SystemState.PANIC)

    assert record.changed_by is None
    assert record.reason is None


def test_system_state_record_is_frozen():
    record = create_system_state_record(SystemState.RUNNING)
    try:
        record.state = SystemState.PANIC
        assert False, "SystemStateRecord must be immutable"
    except AttributeError:
        pass


def test_each_state_constructs_a_record_without_raising():
    for state in SystemState:
        record = create_system_state_record(state)
        assert record.state == state


def test_default_record_now_is_utc():
    before = datetime.now(timezone.utc)
    record = create_system_state_record(SystemState.RUNNING)
    after = datetime.now(timezone.utc)

    assert before <= record.changed_at <= after
