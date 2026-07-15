"""
Phase 59.3, TASK 2 -- database/raw_candle_repository.py and
raw_candle_models.py tests. Each test gets its own fresh, isolated
SQLite file (tests/conftest.py's autouse fresh_database fixture).
"""

from datetime import datetime, timezone

from database.raw_candle_models import create_raw_candle
from database.raw_candle_repository import RawCandleRepository


def _candle(symbol="XAUUSD", timeframe="M15", ts=None, provider="twelvedata"):
    return create_raw_candle(
        symbol=symbol, timeframe=timeframe,
        timestamp=ts or datetime(2026, 1, 1, tzinfo=timezone.utc),
        open=2000.0, high=2005.0, low=1995.0, close=2001.0,
        provider=provider,
    )


def test_save_candle_returns_true_on_first_insert():
    repo = RawCandleRepository()
    assert repo.save_candle(_candle()) is True


def test_save_candle_returns_false_on_exact_duplicate():
    repo = RawCandleRepository()
    candle = _candle()
    repo.save_candle(candle)
    assert repo.save_candle(candle) is False


def test_same_window_different_provider_is_not_a_duplicate():
    """UNIQUE(symbol, timeframe, timestamp, provider) -- provider is part of the identity."""
    repo = RawCandleRepository()
    ts = datetime(2026, 1, 1, tzinfo=timezone.utc)
    assert repo.save_candle(_candle(ts=ts, provider="twelvedata")) is True
    assert repo.save_candle(_candle(ts=ts, provider="binance")) is True
    assert repo.count_candles("XAUUSD", "M15") == 2


def test_get_candles_returns_chronologically_ascending():
    repo = RawCandleRepository()
    t1 = datetime(2026, 1, 1, 0, 0, tzinfo=timezone.utc)
    t2 = datetime(2026, 1, 1, 0, 15, tzinfo=timezone.utc)
    t3 = datetime(2026, 1, 1, 0, 30, tzinfo=timezone.utc)
    repo.save_candle(_candle(ts=t3))
    repo.save_candle(_candle(ts=t1))
    repo.save_candle(_candle(ts=t2))

    result = repo.get_candles("XAUUSD", "M15")

    assert [c.timestamp for c in result] == [t1, t2, t3]


def test_get_candles_filters_by_symbol_and_timeframe():
    repo = RawCandleRepository()
    repo.save_candle(_candle(symbol="XAUUSD", timeframe="M15"))
    repo.save_candle(_candle(symbol="EURUSD", timeframe="M15"))
    repo.save_candle(_candle(symbol="XAUUSD", timeframe="H1"))

    result = repo.get_candles("XAUUSD", "M15")

    assert len(result) == 1
    assert result[0].symbol == "XAUUSD"
    assert result[0].timeframe == "M15"


def test_get_candles_filters_by_provider_when_specified():
    repo = RawCandleRepository()
    ts = datetime(2026, 1, 1, tzinfo=timezone.utc)
    repo.save_candle(_candle(ts=ts, provider="twelvedata"))
    repo.save_candle(_candle(ts=ts, provider="binance"))

    result = repo.get_candles("XAUUSD", "M15", provider="binance")

    assert len(result) == 1
    assert result[0].provider == "binance"


def test_get_candles_empty_result_returns_empty_list_not_none():
    repo = RawCandleRepository()
    assert repo.get_candles("NONEXISTENT", "M15") == []


def test_save_candles_batch_returns_inserted_count():
    repo = RawCandleRepository()
    t1 = datetime(2026, 1, 1, 0, 0, tzinfo=timezone.utc)
    t2 = datetime(2026, 1, 1, 0, 15, tzinfo=timezone.utc)
    candles = [_candle(ts=t1), _candle(ts=t2), _candle(ts=t1)]  # last is a duplicate of the first

    inserted = repo.save_candles(candles)

    assert inserted == 2


def test_volume_none_is_preserved_not_coerced():
    repo = RawCandleRepository()
    repo.save_candle(_candle())
    result = repo.get_candles("XAUUSD", "M15")
    assert result[0].volume is None


def test_raw_candle_dataclass_is_frozen():
    candle = _candle()
    try:
        candle.close = 9999.0
        assert False, "RawCandle must be immutable"
    except AttributeError:
        pass


def test_create_raw_candle_stamps_created_at():
    candle = _candle()
    assert isinstance(candle.created_at, datetime)
    assert candle.created_at.tzinfo is not None
