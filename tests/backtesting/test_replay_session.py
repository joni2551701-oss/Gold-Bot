"""
Phase 60.1, TASK 2 -- backtesting_layer/replay_controller/replay_session.py tests.
"""

from datetime import datetime, timezone

from backtesting_layer.replay_engine.replay_models import ReplayConfig, ReplayState
from backtesting_layer.replay_controller.replay_session import ReplaySession


def _config():
    return ReplayConfig(
        symbol="XAUUSD", timeframe="M15",
        start=datetime(2026, 1, 1, tzinfo=timezone.utc),
        end=datetime(2026, 1, 2, tzinfo=timezone.utc),
    )


def test_new_session_starts_pending():
    session = ReplaySession(_config())
    assert session.state == ReplayState.PENDING
    assert session.started_at is None


def test_session_id_is_unique_per_instance():
    a = ReplaySession(_config())
    b = ReplaySession(_config())
    assert a.session_id != b.session_id


def test_mark_running_stamps_started_at_once():
    session = ReplaySession(_config())
    session.mark_running()
    first_started = session.started_at
    assert session.state == ReplayState.RUNNING
    assert first_started is not None

    session.mark_paused()
    session.mark_running()
    assert session.started_at == first_started


def test_mark_stopped_stamps_finished_at():
    session = ReplaySession(_config())
    session.mark_running()
    session.mark_stopped()
    assert session.state == ReplayState.STOPPED
    assert session.finished_at is not None


def test_mark_finished_stamps_finished_at():
    session = ReplaySession(_config())
    session.mark_running()
    session.mark_finished()
    assert session.state == ReplayState.FINISHED
    assert session.finished_at is not None


def test_record_progress_never_decreases():
    session = ReplaySession(_config(), candles_total=10)
    session.record_progress(5)
    session.record_progress(2)
    assert session.candles_replayed == 5


def test_to_result_reflects_current_state():
    session = ReplaySession(_config(), candles_total=10)
    session.mark_running()
    session.record_progress(4)

    result = session.to_result()

    assert result.symbol == "XAUUSD"
    assert result.candles_total == 10
    assert result.candles_replayed == 4
    assert result.state == ReplayState.RUNNING
