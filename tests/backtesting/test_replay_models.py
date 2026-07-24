"""
Phase 60.1, TASK 2/7 -- backtesting/replay_models.py tests.
"""

from datetime import datetime, timezone

from backtesting.replay_models import ReplayConfig, ReplayResult, ReplayState, format_replay_report


def _config(**overrides):
    defaults = dict(
        symbol="XAUUSD", timeframe="M15",
        start=datetime(2026, 1, 1, tzinfo=timezone.utc),
        end=datetime(2026, 1, 2, tzinfo=timezone.utc),
    )
    defaults.update(overrides)
    return ReplayConfig(**defaults)


def test_replay_config_defaults_speed_to_one():
    assert _config().speed == 1.0


def test_replay_config_is_frozen():
    config = _config()
    try:
        config.speed = 2.0
        assert False, "ReplayConfig must be immutable"
    except AttributeError:
        pass


def test_replay_result_progress_is_zero_for_empty_dataset():
    result = ReplayResult(symbol="XAUUSD", timeframe="M15", state=ReplayState.PENDING, candles_total=0, candles_replayed=0, speed=1.0)
    assert result.progress == 0.0


def test_replay_result_progress_computes_ratio():
    result = ReplayResult(symbol="XAUUSD", timeframe="M15", state=ReplayState.RUNNING, candles_total=10, candles_replayed=3, speed=1.0)
    assert result.progress == 0.3


def test_replay_result_progress_never_exceeds_one():
    result = ReplayResult(symbol="XAUUSD", timeframe="M15", state=ReplayState.FINISHED, candles_total=10, candles_replayed=15, speed=1.0)
    assert result.progress == 1.0


def test_replay_result_finished_reflects_state():
    finished = ReplayResult(symbol="XAUUSD", timeframe="M15", state=ReplayState.FINISHED, candles_total=1, candles_replayed=1, speed=1.0)
    running = ReplayResult(symbol="XAUUSD", timeframe="M15", state=ReplayState.RUNNING, candles_total=1, candles_replayed=0, speed=1.0)
    assert finished.finished is True
    assert running.finished is False


def test_replay_result_duration_seconds_none_before_start():
    result = ReplayResult(symbol="XAUUSD", timeframe="M15", state=ReplayState.PENDING, candles_total=0, candles_replayed=0, speed=1.0)
    assert result.duration_seconds is None


def test_replay_result_duration_seconds_uses_finished_at_when_present():
    started = datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    finished = datetime(2026, 1, 1, 0, 1, 0, tzinfo=timezone.utc)
    result = ReplayResult(
        symbol="XAUUSD", timeframe="M15", state=ReplayState.FINISHED,
        candles_total=1, candles_replayed=1, speed=1.0,
        started_at=started, finished_at=finished,
    )
    assert result.duration_seconds == 60.0


def test_format_replay_report_never_raises_on_pending_state():
    result = ReplayResult(symbol="XAUUSD", timeframe="M15", state=ReplayState.PENDING, candles_total=0, candles_replayed=0, speed=1.0)
    text = format_replay_report(result)
    assert "XAUUSD" in text
    assert "PENDING" in text


def test_format_replay_report_includes_all_required_fields():
    result = ReplayResult(symbol="XAUUSD", timeframe="M15", state=ReplayState.RUNNING, candles_total=100, candles_replayed=25, speed=2.0)
    text = format_replay_report(result)
    assert "Dataset:" in text
    assert "State:" in text
    assert "Candles:" in text
    assert "Progress:" in text
    assert "Speed:" in text
    assert "Duration:" in text
    assert "Finished:" in text
