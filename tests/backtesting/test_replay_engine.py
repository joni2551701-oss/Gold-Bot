"""
Phase 60.1, TASK 5 -- backtesting/replay_engine.py tests. Real SQLite
(tests/conftest.py's autouse fresh_database fixture) -- no mocks.
"""

from datetime import datetime, timezone

from backtesting.replay_engine import ReplayEngine
from backtesting.replay_models import ReplayConfig
from database.raw_candle_models import create_raw_candle
from database.raw_candle_repository import RawCandleRepository


def _seed_candles(n=5, symbol="XAUUSD", timeframe="M15"):
    repo = RawCandleRepository()
    for i in range(n):
        repo.save_candle(create_raw_candle(
            symbol=symbol, timeframe=timeframe,
            timestamp=datetime(2026, 1, 1, i, tzinfo=timezone.utc),
            open=2000.0 + i, high=2005.0 + i, low=1995.0 + i, close=2001.0 + i,
            provider="twelvedata",
        ))
    return repo


def _config(**overrides):
    defaults = dict(
        symbol="XAUUSD", timeframe="M15",
        start=datetime(2026, 1, 1, 0, tzinfo=timezone.utc),
        end=datetime(2026, 1, 1, 23, tzinfo=timezone.utc),
    )
    defaults.update(overrides)
    return ReplayConfig(**defaults)


def test_engine_loads_candles_in_the_configured_range():
    _seed_candles(5)
    engine = ReplayEngine(_config())
    assert engine.candles_total == 5


def test_engine_produces_the_same_candle_type_live_data_uses():
    _seed_candles(1)
    engine = ReplayEngine(_config())
    engine.clock.play()
    candle = engine.step()

    from data.twelve_data_client import Candle
    assert isinstance(candle, Candle)


def test_step_does_not_advance_before_play():
    _seed_candles(3)
    engine = ReplayEngine(_config())
    result = engine.step()
    assert result is None
    assert engine.candles_replayed == 0


def test_step_advances_one_candle_per_step_at_default_speed():
    _seed_candles(3)
    engine = ReplayEngine(_config())
    engine.clock.play()

    first = engine.step()
    second = engine.step()

    assert first != second
    assert engine.candles_replayed == 2


def test_step_advances_by_speed():
    _seed_candles(6)
    engine = ReplayEngine(_config(speed=3.0))
    engine.clock.play()

    engine.step()

    assert engine.candles_replayed == 3


def test_is_finished_true_after_consuming_all_candles():
    _seed_candles(2)
    engine = ReplayEngine(_config())
    engine.clock.play()

    assert engine.is_finished is False
    engine.step()
    engine.step()
    assert engine.is_finished is True


def test_engine_marks_clock_finished_when_exhausted():
    from backtesting.replay_models import ReplayState
    _seed_candles(1)
    engine = ReplayEngine(_config())
    engine.clock.play()

    engine.step()

    assert engine.clock.state == ReplayState.FINISHED


def test_seek_moves_both_clock_and_feed():
    _seed_candles(5)
    engine = ReplayEngine(_config())

    candle = engine.seek(2)

    assert engine.clock.position == 2
    assert engine.feed.cursor == 2
    assert candle == engine.feed.candles[2]


def test_engine_only_loads_candles_within_the_configured_window():
    repo = _seed_candles(5)
    repo.save_candle(create_raw_candle(
        symbol="XAUUSD", timeframe="M15",
        timestamp=datetime(2026, 2, 1, tzinfo=timezone.utc),
        open=1.0, high=2.0, low=0.5, close=1.5, provider="twelvedata",
    ))

    engine = ReplayEngine(_config())

    assert engine.candles_total == 5
