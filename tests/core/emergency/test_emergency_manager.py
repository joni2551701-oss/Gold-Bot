"""
Phase 59.9, TASK 3/6 -- core_layer/emergency/emergency_manager.py tests.
Real repositories (SQLite, tests/conftest.py's autouse fresh_database
fixture) -- no mocks.
"""

from core_layer.emergency.emergency_manager import EmergencyManager
from core_layer.emergency.emergency_state import EmergencyState
from database_layer.audit_log.audit_log_repository import AuditLogRepository


def test_get_status_defaults_to_normal_when_never_recorded():
    manager = EmergencyManager()
    status = manager.get_status()
    assert status.state == EmergencyState.NORMAL


def test_activate_pause_transitions_to_paused():
    manager = EmergencyManager()

    result = manager.activate_pause(reason="daily loss limit")

    assert result.state == EmergencyState.PAUSED
    assert result.reason == "daily loss limit"
    assert manager.get_status().state == EmergencyState.PAUSED


def test_activate_kill_transitions_to_killed():
    manager = EmergencyManager()

    result = manager.activate_kill(reason="Daily loss limit reached", source="system")

    assert result.state == EmergencyState.KILLED
    assert manager.get_status().state == EmergencyState.KILLED


def test_activate_maintenance_transitions_to_maintenance():
    manager = EmergencyManager()

    result = manager.activate_maintenance(reason="system update", activated_by="owner")

    assert result.state == EmergencyState.MAINTENANCE
    assert result.activated_by == "owner"


def test_paused_to_normal_round_trip():
    manager = EmergencyManager()
    manager.activate_pause(reason="loss limit")

    result = manager.restore_normal(reason="manual restore")

    assert result.state == EmergencyState.NORMAL
    assert manager.get_status().state == EmergencyState.NORMAL


def test_normal_to_killed_round_trip():
    manager = EmergencyManager()
    assert manager.get_status().state == EmergencyState.NORMAL

    manager.activate_kill(reason="critical failure")

    assert manager.get_status().state == EmergencyState.KILLED


def test_history_survives_a_simulated_restart():
    first_manager = EmergencyManager()
    first_manager.activate_pause(reason="loss limit")
    first_manager.restore_normal()

    second_manager = EmergencyManager()
    assert second_manager.get_status().state == EmergencyState.NORMAL
    assert len(second_manager.repository.get_history()) == 2


def test_activate_kill_writes_a_kill_activated_audit_entry():
    manager = EmergencyManager()
    manager.activate_kill(reason="daily loss limit", activated_by="owner")

    entries = AuditLogRepository().get_recent()

    assert any(e.action == "KILL_ACTIVATED" and e.actor == "owner" for e in entries)


def test_activate_pause_writes_a_pause_activated_audit_entry():
    manager = EmergencyManager()
    manager.activate_pause(reason="drawdown warning")

    entries = AuditLogRepository().get_recent()

    assert any(e.action == "PAUSE_ACTIVATED" for e in entries)


def test_activate_maintenance_writes_a_maintenance_enabled_audit_entry():
    manager = EmergencyManager()
    manager.activate_maintenance(reason="system update")

    entries = AuditLogRepository().get_recent()

    assert any(e.action == "MAINTENANCE_ENABLED" for e in entries)


def test_restore_normal_writes_a_system_restored_audit_entry():
    manager = EmergencyManager()
    manager.activate_kill(reason="test")
    manager.restore_normal(reason="all clear")

    entries = AuditLogRepository().get_recent()

    assert any(e.action == "SYSTEM_RESTORED" for e in entries)


def test_source_defaults_to_system_when_no_actor_given():
    manager = EmergencyManager()
    result = manager.activate_pause(reason="automatic")
    assert result.source == "system"
