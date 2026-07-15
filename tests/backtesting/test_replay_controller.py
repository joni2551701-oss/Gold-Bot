"""
Phase 60.1, TASK 6 -- backtesting/replay_controller.py tests. Real
SQLite (tests/conftest.py's autouse fresh_database fixture) -- no
mocks.
"""

from datetime import datetime, timezone

from backtesting.replay_controller import ReplayController
from backtesting.replay_models import ReplayConfig, ReplayState
from database.raw_candle_models import create_raw_candle
from database.raw_candle_repository import RawCandleRepository


def _seed_candles(n=5):
    repo = RawCandleRepository()
    for i in range(n):
        repo.save_candle(create_raw_candle(
            symbol="XAUUSD", timeframe="M15",
            timestamp=datetime(2026, 1, 1, i, tzinfo=timezone.utc),
            open=2000.0, high=2005.0, low=1995.0, close=2001.0,
            provider="twelvedata",
        ))


def _config(**overrides):
    defaults = dict(
        symbol="XAUUSD", timeframe="M15",
        start=datetime(2026, 1, 1, 0, tzinfo=timezone.utc),
        end=datetime(2026, 1, 1, 23, tzinfo=timezone.utc),
    )
    defaults.update(overrides)
    return ReplayConfig(**defaults)


def test_start_creates_a_running_session():
    _seed_candles(3)
    controller = ReplayController()

    session = controller.start(_config())

    assert session.state == ReplayState.RUNNING
    assert session.candles_total == 3


def test_pause_transitions_a_running_session():
    _seed_candles(3)
    controller = ReplayController()
    session = controller.start(_config())

    paused = controller.pause(session.session_id)

    assert paused.state == ReplayState.PAUSED


def test_resume_transitions_a_paused_session_back_to_running():
    _seed_candles(3)
    controller = ReplayController()
    session = controller.start(_config())
    controller.pause(session.session_id)

    resumed = controller.resume(session.session_id)

    assert resumed.state == ReplayState.RUNNING


def test_stop_transitions_to_stopped():
    _seed_candles(3)
    controller = ReplayController()
    session = controller.start(_config())

    stopped = controller.stop(session.session_id)

    assert stopped.state == ReplayState.STOPPED


def test_restart_keeps_the_same_session_id():
    _seed_candles(3)
    controller = ReplayController()
    session = controller.start(_config())
    original_id = session.session_id
    controller.step(session.session_id)

    restarted = controller.restart(session.session_id)

    assert restarted.session_id == original_id
    assert restarted.candles_replayed == 0
    assert restarted.state == ReplayState.RUNNING


def test_step_advances_the_underlying_engine():
    _seed_candles(3)
    controller = ReplayController()
    session = controller.start(_config())

    candle = controller.step(session.session_id)

    assert candle is not None
    status = controller.get_status(session.session_id)
    assert status.candles_replayed == 1


def test_step_returns_none_for_unknown_session():
    controller = ReplayController()
    assert controller.step("nonexistent") is None


def test_pause_returns_none_for_unknown_session():
    controller = ReplayController()
    assert controller.pause("nonexistent") is None


def test_get_status_reflects_finished_state_once_exhausted():
    _seed_candles(1)
    controller = ReplayController()
    session = controller.start(_config())

    controller.step(session.session_id)
    status = controller.get_status(session.session_id)

    assert status.state == ReplayState.FINISHED
    assert status.finished is True


def test_get_status_unknown_session_returns_none():
    controller = ReplayController()
    assert controller.get_status("nonexistent") is None
