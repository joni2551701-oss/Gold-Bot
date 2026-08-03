"""
Phase 59.9, TASK 5 -- core_layer/emergency/maintenance.py tests.
"""

from datetime import datetime

from core_layer.emergency.maintenance import MaintenanceMode, disable_maintenance, enable_maintenance


def test_enable_maintenance_sets_enabled_true():
    mode = enable_maintenance(reason="system update", owner="owner")

    assert mode.enabled is True
    assert mode.reason == "system update"
    assert mode.owner == "owner"
    assert isinstance(mode.started_at, datetime)


def test_disable_maintenance_sets_enabled_false():
    mode = disable_maintenance(owner="owner")

    assert mode.enabled is False
    assert mode.reason is None
    assert mode.started_at is None


def test_maintenance_mode_is_frozen():
    mode = MaintenanceMode(enabled=True)
    try:
        mode.enabled = False
        assert False, "MaintenanceMode must be immutable"
    except AttributeError:
        pass
