"""
Phase 59.3, TASK 2 -- database_layer/market_repository/raw_candle_repository.py and
raw_candle_models.py tests. Extended by Phase 59 Real Market
Validation Foundation, TASK 3 (from_market_candle()/
save_market_candles() -- the MarketCandle bridge). Each test gets its
own fresh, isolated SQLite file (tests/conftest.py's autouse
fresh_database fixture).
"""

from datetime import datetime, timezone

import pytest

from database_layer.market_repository.raw_candle_models import create_raw_candle, from_market_candle
from database_layer.market_repository.raw_candle_repository import RawCandleRepository
from data_layer.providers.base_provider import MarketCandle
from data_layer.providers.twelve_data_provider import TwelveDataProvider
from data_layer.providers.twelve_data_client import Candle


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


# --- Phase 59 Real Market Validation Foundation, TASK 3: MarketCandle bridge ---

def _market_candle(provider="twelvedata", ts=None):
    return MarketCandle(
        symbol="XAUUSD", timeframe="M15",
        open=2000.0, high=2005.0, low=1995.0, close=2001.0,
        timestamp=ts or datetime(2026, 1, 1, tzinfo=timezone.utc),
        volume=None, provider=provider,
    )


def test_from_market_candle_copies_every_field():
    market_candle = _market_candle()

    raw = from_market_candle(market_candle)

    assert raw.symbol == "XAUUSD"
    assert raw.timeframe == "M15"
    assert raw.open == 2000.0
    assert raw.provider == "twelvedata"
    assert raw.volume is None


def test_from_market_candle_override_provider_takes_precedence():
    market_candle = _market_candle(provider="twelvedata")

    raw = from_market_candle(market_candle, provider="override_provider")

    assert raw.provider == "override_provider"


def test_from_market_candle_raises_without_any_provider():
    market_candle = _market_candle(provider=None)

    with pytest.raises(ValueError):
        from_market_candle(market_candle)


def test_save_market_candles_round_trips_through_the_repository():
    repo = RawCandleRepository()
    candles = [_market_candle(ts=datetime(2026, 1, 1, tzinfo=timezone.utc))]

    inserted = repo.save_market_candles(candles)

    assert inserted == 1
    saved = repo.get_candles("XAUUSD", "M15")
    assert saved[0].provider == "twelvedata"


def test_save_market_candles_deduplicates_like_save_candles():
    repo = RawCandleRepository()
    candles = [_market_candle(ts=datetime(2026, 1, 1, tzinfo=timezone.utc))]

    repo.save_market_candles(candles)
    inserted_again = repo.save_market_candles(candles)

    assert inserted_again == 0


def test_save_market_candles_accepts_a_provider_override():
    repo = RawCandleRepository()
    candles = [_market_candle(provider=None, ts=datetime(2026, 1, 1, tzinfo=timezone.utc))]

    inserted = repo.save_market_candles(candles, provider="twelvedata")

    assert inserted == 1


# --- Phase 60.1 (Historical Replay Engine, TASK 1 reuse audit): get_candles_range() ---

def test_get_candles_range_filters_by_date_bounds():
    repo = RawCandleRepository()
    t1 = datetime(2026, 1, 1, 0, 0, tzinfo=timezone.utc)
    t2 = datetime(2026, 1, 2, 0, 0, tzinfo=timezone.utc)
    t3 = datetime(2026, 1, 3, 0, 0, tzinfo=timezone.utc)
    repo.save_candle(_candle(ts=t1))
    repo.save_candle(_candle(ts=t2))
    repo.save_candle(_candle(ts=t3))

    result = repo.get_candles_range("XAUUSD", "M15", start=t1, end=t2)

    assert [c.timestamp for c in result] == [t1, t2]


def test_get_candles_range_is_chronologically_ascending():
    repo = RawCandleRepository()
    t1 = datetime(2026, 1, 1, tzinfo=timezone.utc)
    t2 = datetime(2026, 1, 2, tzinfo=timezone.utc)
    repo.save_candle(_candle(ts=t2))
    repo.save_candle(_candle(ts=t1))

    result = repo.get_candles_range("XAUUSD", "M15", start=t1, end=t2)

    assert [c.timestamp for c in result] == [t1, t2]


def test_get_candles_range_filters_by_provider_when_specified():
    repo = RawCandleRepository()
    ts = datetime(2026, 1, 1, tzinfo=timezone.utc)
    repo.save_candle(_candle(ts=ts, provider="twelvedata"))
    repo.save_candle(_candle(ts=ts, provider="binance"))

    result = repo.get_candles_range("XAUUSD", "M15", start=ts, end=ts, provider="binance")

    assert len(result) == 1
    assert result[0].provider == "binance"


def test_get_candles_range_empty_result_returns_empty_list_not_none():
    t1 = datetime(2026, 1, 1, tzinfo=timezone.utc)
    t2 = datetime(2026, 1, 2, tzinfo=timezone.utc)
    repo = RawCandleRepository()
    assert repo.get_candles_range("NONEXISTENT", "M15", start=t1, end=t2) == []


def test_get_candles_range_excludes_candles_outside_the_window():
    repo = RawCandleRepository()
    before = datetime(2025, 12, 31, tzinfo=timezone.utc)
    inside = datetime(2026, 1, 1, tzinfo=timezone.utc)
    after = datetime(2026, 1, 5, tzinfo=timezone.utc)
    repo.save_candle(_candle(ts=before))
    repo.save_candle(_candle(ts=inside))
    repo.save_candle(_candle(ts=after))

    result = repo.get_candles_range("XAUUSD", "M15", start=datetime(2026, 1, 1, tzinfo=timezone.utc), end=datetime(2026, 1, 2, tzinfo=timezone.utc))

    assert [c.timestamp for c in result] == [inside]


def test_twelvedataprovider_output_round_trips_into_raw_candles(monkeypatch):
    """End-to-end: TwelveDataProvider's real (mocked) get_candles() output saves cleanly -- MT5 is never touched anywhere in this path."""
    provider = TwelveDataProvider()
    monkeypatch.setattr(
        provider.client, "fetch_candles",
        lambda *a, **k: [Candle(timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc), open=2000.0, high=2005.0, low=1995.0, close=2001.0)],
    )

    market_candles = provider.get_candles("XAUUSD", "M15", 10)
    assert market_candles[0].provider == "twelvedata"  # Phase 59.3 TASK 1's own stamping

    repo = RawCandleRepository()
    inserted = repo.save_market_candles(market_candles)

    assert inserted == 1
    saved = repo.get_candles("XAUUSD", "M15", provider="twelvedata")
    assert len(saved) == 1
    assert saved[0].open == 2000.0
