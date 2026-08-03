"""
Phase 60.1, TASK 8 -- platform_layer/telegram/owner/replay_commands.py tests. Real
SQLite (tests/conftest.py's autouse fresh_database fixture) -- no
mocks. Each test constructs its own controller (module-level
_default_controller is deliberately not reset between tests -- session
IDs are UUIDs, so state never leaks across tests as a shared-name
collision).
"""

from datetime import datetime, timezone

from platform_layer.telegram.owner.replay_commands import replay_pause, replay_start, replay_status, replay_stop
from platform_layer.telegram.owner.provider_commands import ProviderCommandResult
from database_layer.market_repository.raw_candle_models import create_raw_candle
from database_layer.market_repository.raw_candle_repository import RawCandleRepository


def _seed_candles(n=3):
    repo = RawCandleRepository()
    for i in range(n):
        repo.save_candle(create_raw_candle(
            symbol="XAUUSD", timeframe="M15",
            timestamp=datetime(2026, 1, 1, i, tzinfo=timezone.utc),
            open=2000.0, high=2005.0, low=1995.0, close=2001.0,
            provider="twelvedata",
        ))


def _extract_session_id(message: str) -> str:
    return message.splitlines()[0].split("=", 1)[1]


def test_replay_start_returns_a_session_id():
    _seed_candles(3)
    result = replay_start("XAUUSD", "M15", datetime(2026, 1, 1, 0, tzinfo=timezone.utc), datetime(2026, 1, 1, 23, tzinfo=timezone.utc))
    assert isinstance(result, ProviderCommandResult)
    assert result.success is True
    assert "session_id=" in result.message


def test_replay_status_reports_the_started_session():
    _seed_candles(3)
    start_result = replay_start("XAUUSD", "M15", datetime(2026, 1, 1, 0, tzinfo=timezone.utc), datetime(2026, 1, 1, 23, tzinfo=timezone.utc))
    session_id = _extract_session_id(start_result.message)

    status = replay_status(session_id)

    assert status.success is True
    assert "RUNNING" in status.message


def test_replay_pause_transitions_the_session():
    _seed_candles(3)
    start_result = replay_start("XAUUSD", "M15", datetime(2026, 1, 1, 0, tzinfo=timezone.utc), datetime(2026, 1, 1, 23, tzinfo=timezone.utc))
    session_id = _extract_session_id(start_result.message)

    result = replay_pause(session_id)

    assert result.success is True
    assert "PAUSED" in result.message


def test_replay_stop_transitions_the_session():
    _seed_candles(3)
    start_result = replay_start("XAUUSD", "M15", datetime(2026, 1, 1, 0, tzinfo=timezone.utc), datetime(2026, 1, 1, 23, tzinfo=timezone.utc))
    session_id = _extract_session_id(start_result.message)

    result = replay_stop(session_id)

    assert result.success is True
    assert "STOPPED" in result.message


def test_replay_status_unknown_session_fails_honestly():
    result = replay_status("nonexistent-session-id")
    assert result.success is False


def test_replay_pause_unknown_session_fails_honestly():
    result = replay_pause("nonexistent-session-id")
    assert result.success is False
