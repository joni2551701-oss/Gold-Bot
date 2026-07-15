"""
Phase 59.9, TASK 1 -- core/emergency/emergency_state.py tests.
"""

from datetime import datetime

from core.emergency.emergency_state import (
    EmergencyState,
    EmergencyStateRecord,
    create_emergency_state_record,
)


def test_emergency_state_has_five_values():
    assert {s.value for s in EmergencyState} == {"NORMAL", "WARNING", "PAUSED", "KILLED", "MAINTENANCE"}


def test_create_emergency_state_record_stamps_timestamps():
    record = create_emergency_state_record(EmergencyState.KILLED, reason="daily loss limit")

    assert record.state == EmergencyState.KILLED
    assert record.reason == "daily loss limit"
    assert isinstance(record.created_at, datetime)
    assert record.created_at.tzinfo is not None
    assert record.updated_at == record.created_at


def test_create_emergency_state_record_defaults_source_to_system():
    record = create_emergency_state_record(EmergencyState.NORMAL)
    assert record.source == "system"


def test_create_emergency_state_record_accepts_owner_source():
    record = create_emergency_state_record(EmergencyState.PAUSED, activated_by="owner", source="owner")
    assert record.source == "owner"
    assert record.activated_by == "owner"


def test_emergency_state_record_is_frozen():
    record = create_emergency_state_record(EmergencyState.NORMAL)
    try:
        record.state = EmergencyState.KILLED
        assert False, "EmergencyStateRecord must be immutable"
    except AttributeError:
        pass


def test_expires_at_defaults_to_none():
    record = create_emergency_state_record(EmergencyState.MAINTENANCE)
    assert record.expires_at is None


def test_expires_at_can_be_set():
    from datetime import timezone
    expiry = datetime(2026, 1, 1, tzinfo=timezone.utc)
    record = create_emergency_state_record(EmergencyState.PAUSED, expires_at=expiry)
    assert record.expires_at == expiry
