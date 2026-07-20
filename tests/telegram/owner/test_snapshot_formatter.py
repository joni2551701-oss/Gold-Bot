"""GoldBot Core Owner Snapshot Reporter Alpha, TASK 3 -- telegram/owner/snapshot_formatter.py tests."""

from monitoring.snapshot_models import OwnerSnapshot
from telegram.owner.snapshot_formatter import format_snapshot


def _snapshot(**overrides):
    defaults = dict(
        timestamp="2026-01-01T20:00:00+00:00",
        status="OK",
        core_status="RUNNING",
        database_status="OK",
        telegram_status="OK",
        market_data_status="ONLINE",
        last_signal="BUY @ 2026-01-01T19:55:00",
        error_count=0,
        uptime_info="15h 20m",
        signals_today=3,
    )
    defaults.update(overrides)
    return OwnerSnapshot(**defaults)


def test_format_snapshot_returns_string():
    assert isinstance(format_snapshot(_snapshot()), str)


def test_format_snapshot_contains_goldbot_snapshot_header():
    assert "GoldBot Snapshot" in format_snapshot(_snapshot())


def test_format_snapshot_contains_formatted_time():
    assert "20:00 UTC" in format_snapshot(_snapshot())


def test_format_snapshot_contains_core_status():
    assert "RUNNING" in format_snapshot(_snapshot())


def test_format_snapshot_contains_database_status():
    message = format_snapshot(_snapshot(database_status="OK"))
    assert "Database:" in message
    assert "OK" in message


def test_format_snapshot_contains_market_data_status():
    message = format_snapshot(_snapshot(market_data_status="ONLINE"))
    assert "Market Data:" in message
    assert "ONLINE" in message


def test_format_snapshot_contains_signals_today_count():
    message = format_snapshot(_snapshot(signals_today=3))
    assert "Signals Today:" in message
    assert "3" in message


def test_format_snapshot_contains_error_count():
    message = format_snapshot(_snapshot(error_count=2))
    assert "Errors:" in message
    assert "2" in message


def test_format_snapshot_contains_runtime():
    message = format_snapshot(_snapshot(uptime_info="15h 20m"))
    assert "Runtime:" in message
    assert "15h 20m" in message


def test_format_snapshot_shows_na_for_missing_last_signal():
    message = format_snapshot(_snapshot(last_signal=None))
    assert "N/A" in message


def test_format_snapshot_shows_last_signal_when_present():
    message = format_snapshot(_snapshot(last_signal="SELL @ 2026-01-01T18:00:00"))
    assert "SELL @ 2026-01-01T18:00:00" in message


def test_format_snapshot_uses_green_marker_when_status_ok():
    message = format_snapshot(_snapshot(status="OK"))
    assert "\U0001F7E2" in message


def test_format_snapshot_uses_yellow_marker_when_status_degraded():
    message = format_snapshot(_snapshot(status="DEGRADED"))
    assert "\U0001F7E1" in message


def test_format_snapshot_shows_telegram_status():
    message = format_snapshot(_snapshot(telegram_status="OK"))
    assert "Telegram:" in message


def test_format_snapshot_unknown_status_gets_question_icon():
    message = format_snapshot(_snapshot(core_status="SOMETHING_NEW"))
    assert "❓" in message


def test_format_snapshot_never_raises_on_malformed_timestamp():
    message = format_snapshot(_snapshot(timestamp="not-a-timestamp"))
    assert "not-a-timestamp" in message
