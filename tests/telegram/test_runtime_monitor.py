"""
GoldBot Core Telegram Runtime Activation Alpha, TASK 4/8 --
telegram/runtime_monitor.py tests. Constructs its own
TelegramRuntimeMonitor() instance for isolation everywhere except the
module-level free-function tests, which intentionally exercise the
shared DEFAULT_RUNTIME_MONITOR singleton (matching
core_layer/health_monitor/system_monitor.py's own test convention).
"""

from dataclasses import fields

import core_layer.health_monitor.system_monitor as system_monitor_module
from telegram.runtime_monitor import (
    DEFAULT_RUNTIME_MONITOR,
    TelegramRuntimeMonitor,
    TelegramRuntimeStatus,
    get_status,
    record_connected,
    record_error,
    record_heartbeat,
)


def test_new_monitor_starts_disconnected():
    monitor = TelegramRuntimeMonitor()
    status = monitor.get_status()
    assert status.status == "DISCONNECTED"


def test_new_monitor_starts_with_no_ping():
    monitor = TelegramRuntimeMonitor()
    assert monitor.get_status().last_ping is None


def test_new_monitor_starts_with_zero_errors():
    monitor = TelegramRuntimeMonitor()
    assert monitor.get_status().errors == 0


def test_new_monitor_uptime_is_non_negative():
    monitor = TelegramRuntimeMonitor()
    assert monitor.get_status().uptime_seconds >= 0.0


def test_record_connected_flips_status():
    monitor = TelegramRuntimeMonitor()
    monitor.record_connected()
    assert monitor.get_status().status == "CONNECTED"


def test_record_connected_idempotent():
    monitor = TelegramRuntimeMonitor()
    monitor.record_connected()
    monitor.record_connected()
    assert monitor.get_status().status == "CONNECTED"


def test_record_heartbeat_sets_last_ping_with_explicit_timestamp():
    monitor = TelegramRuntimeMonitor()
    monitor.record_heartbeat(timestamp="2026-01-01T00:00:00Z")
    assert monitor.get_status().last_ping == "2026-01-01T00:00:00Z"


def test_record_heartbeat_defaults_to_iso_timestamp():
    monitor = TelegramRuntimeMonitor()
    monitor.record_heartbeat()
    last_ping = monitor.get_status().last_ping
    assert last_ping is not None
    assert "T" in last_ping  # ISO 8601 shape


def test_record_heartbeat_overwrites_previous_ping():
    monitor = TelegramRuntimeMonitor()
    monitor.record_heartbeat(timestamp="2026-01-01T00:00:00Z")
    monitor.record_heartbeat(timestamp="2026-01-02T00:00:00Z")
    assert monitor.get_status().last_ping == "2026-01-02T00:00:00Z"


def test_record_error_increments_error_count():
    monitor = TelegramRuntimeMonitor()
    monitor.record_error("boom")
    assert monitor.get_status().errors == 1


def test_record_error_accumulates_across_calls():
    monitor = TelegramRuntimeMonitor()
    monitor.record_error("first")
    monitor.record_error("second")
    monitor.record_error("third")
    assert monitor.get_status().errors == 3


def test_record_error_relays_into_monitoring_system_monitor():
    """Cross-module wiring: a Telegram runtime error surfaces in /owner_status's last_error too."""
    monitor = TelegramRuntimeMonitor()
    monitor.record_error("connection dropped")
    assert system_monitor_module.get_health().last_error == "connection dropped"


def test_record_error_never_raises_when_relay_fails(monkeypatch):
    import telegram.runtime_monitor as runtime_monitor_module

    def failing_relay(message):
        raise RuntimeError("relay unreachable")

    monkeypatch.setattr(runtime_monitor_module, "_record_core_error", failing_relay)

    monitor = TelegramRuntimeMonitor()
    monitor.record_error("boom")  # must not raise
    assert monitor.get_status().errors == 1


def test_uptime_seconds_is_monotonically_non_decreasing():
    monitor = TelegramRuntimeMonitor()
    first = monitor.uptime_seconds()
    second = monitor.uptime_seconds()
    assert second >= first


def test_two_monitor_instances_are_independent():
    a = TelegramRuntimeMonitor()
    b = TelegramRuntimeMonitor()
    a.record_connected()
    a.record_error("only on a")
    assert b.get_status().status == "DISCONNECTED"
    assert b.get_status().errors == 0


def test_get_status_returns_telegram_runtime_status_instance():
    monitor = TelegramRuntimeMonitor()
    assert isinstance(monitor.get_status(), TelegramRuntimeStatus)


def test_telegram_runtime_status_is_frozen():
    status = TelegramRuntimeStatus(status="CONNECTED", last_ping=None, errors=0, uptime_seconds=0.0)
    try:
        status.status = "DISCONNECTED"
        assert False, "expected FrozenInstanceError"
    except Exception:
        pass


def test_telegram_runtime_status_field_names_match_brief():
    field_names = {f.name for f in fields(TelegramRuntimeStatus)}
    assert field_names == {"status", "last_ping", "errors", "uptime_seconds"}


def test_telegram_runtime_status_never_computes_a_trading_verdict():
    """Belt-and-suspenders: this is connection-runtime observability, never a signal/decision object."""
    field_names = {f.name for f in fields(TelegramRuntimeStatus)}
    forbidden = {"signal", "decision", "verdict", "direction"}
    assert field_names.isdisjoint(forbidden)


def test_module_level_record_connected_updates_shared_singleton():
    record_connected()
    assert get_status().status == "CONNECTED"


def test_module_level_record_heartbeat_updates_shared_singleton():
    record_heartbeat(timestamp="2026-05-05T05:05:05Z")
    assert get_status().last_ping == "2026-05-05T05:05:05Z"


def test_module_level_record_error_updates_shared_singleton():
    before = get_status().errors
    record_error("shared singleton error")
    assert get_status().errors == before + 1


def test_default_runtime_monitor_is_a_telegram_runtime_monitor_instance():
    assert isinstance(DEFAULT_RUNTIME_MONITOR, TelegramRuntimeMonitor)
