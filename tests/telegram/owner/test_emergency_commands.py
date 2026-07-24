"""
Phase 59.9, TASK 7 -- telegram/owner/emergency_commands.py tests.
Real repositories (SQLite, tests/conftest.py's autouse fresh_database
fixture) -- no mocks.
"""

from telegram.owner.emergency_commands import (
    get_emergency_status,
    kill_system,
    maintenance_on,
    pause_system,
    restore_system,
)
from telegram.owner.provider_commands import ProviderCommandResult


def test_get_emergency_status_defaults_to_normal():
    result = get_emergency_status()
    assert isinstance(result, ProviderCommandResult)
    assert result.success is True
    assert "NORMAL" in result.message


def test_kill_system_returns_killed_state():
    result = kill_system(actor="owner", reason="daily loss limit")

    assert result.success is True
    assert "KILLED" in result.message
    assert "daily loss limit" in result.message


def test_pause_system_returns_paused_state():
    result = pause_system(actor="owner", reason="drawdown warning")

    assert result.success is True
    assert "PAUSED" in result.message


def test_maintenance_on_returns_maintenance_state():
    result = maintenance_on(actor="owner", reason="system update")

    assert result.success is True
    assert "MAINTENANCE" in result.message


def test_restore_system_returns_normal_state():
    kill_system(actor="owner", reason="test")

    result = restore_system(actor="owner", reason="all clear")

    assert result.success is True
    assert "NORMAL" in result.message


def test_get_emergency_status_reflects_the_latest_action():
    pause_system(actor="owner", reason="loss limit")

    result = get_emergency_status()

    assert "PAUSED" in result.message
