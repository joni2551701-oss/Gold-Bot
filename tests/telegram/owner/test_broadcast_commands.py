"""Phase 63.0 TASK 7 — Owner Broadcast Commands. Foundation only -- not registered in OWNER_COMMANDS, not wired into command_router/handlers, every function reports NOT IMPLEMENTED."""

from telegram.owner.broadcast_commands import (
    BroadcastCommandResult,
    broadcast_disable,
    broadcast_enable,
    broadcast_provider,
    broadcast_status,
)


def test_broadcast_status_is_not_implemented():
    result = broadcast_status()
    assert isinstance(result, BroadcastCommandResult)
    assert result.success is False
    assert "NOT IMPLEMENTED" in result.message


def test_broadcast_provider_is_not_implemented():
    result = broadcast_provider("youtube")
    assert result.success is False
    assert "NOT IMPLEMENTED" in result.message


def test_broadcast_enable_is_not_implemented():
    result = broadcast_enable("youtube")
    assert result.success is False
    assert "NOT IMPLEMENTED" in result.message


def test_broadcast_disable_is_not_implemented():
    result = broadcast_disable("youtube")
    assert result.success is False
    assert "NOT IMPLEMENTED" in result.message


def test_broadcast_commands_are_not_registered_in_owner_commands():
    from telegram.commands import OWNER_COMMANDS
    for command in ("broadcast_status", "broadcast_provider", "broadcast_enable", "broadcast_disable"):
        assert command not in OWNER_COMMANDS


def test_broadcast_commands_have_no_dispatch_handler():
    from telegram import handlers
    for command in ("broadcast_status", "broadcast_provider", "broadcast_enable", "broadcast_disable"):
        assert getattr(handlers, f"{command}_handler", None) is None
