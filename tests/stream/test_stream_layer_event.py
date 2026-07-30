"""TASK-CORE-004 -- StreamEvent format + MarketCandle adapter."""

from datetime import datetime, timezone

from data.providers.base_provider import MarketCandle
from stream.stream_event import StreamEvent


def _event(**kw):
    base = dict(symbol="XAUUSD", timeframe="M15", timestamp=datetime(2026, 1, 2, tzinfo=timezone.utc),
                open=2000.0, high=2010.0, low=1995.0, close=2005.0)
    base.update(kw)
    return StreamEvent(**base)


def test_event_has_all_required_fields():
    e = _event()
    for field in ("symbol", "timeframe", "timestamp", "open", "high", "low", "close",
                  "volume", "source", "provider"):
        assert hasattr(e, field)


def test_event_defaults():
    e = _event()
    assert e.volume is None
    assert e.source == "provider"
    assert e.provider is None


def test_to_dict_serializes_timestamp():
    e = _event()
    d = e.to_dict()
    assert d["timestamp"] == "2026-01-02T00:00:00+00:00"
    assert d["symbol"] == "XAUUSD"


def test_from_candle_maps_all_fields():
    ts = datetime(2026, 1, 2, 12, tzinfo=timezone.utc)
    candle = MarketCandle(symbol="XAUUSD", timeframe="M15", open=2000.0, high=2010.0,
                          low=1995.0, close=2005.0, timestamp=ts, volume=None, provider="twelvedata")
    e = StreamEvent.from_candle(candle, source="poll")
    assert e.symbol == "XAUUSD"
    assert e.close == 2005.0
    assert e.provider == "twelvedata"
    assert e.source == "poll"
    assert e.timestamp == ts


def test_from_candle_default_source():
    ts = datetime(2026, 1, 2, tzinfo=timezone.utc)
    candle = MarketCandle(symbol="XAUUSD", timeframe="M15", open=1.0, high=2.0,
                          low=0.5, close=1.5, timestamp=ts)
    e = StreamEvent.from_candle(candle)
    assert e.source == "provider"


def test_event_is_immutable():
    e = _event()
    try:
        e.close = 9999.0  # type: ignore[misc]
        assert False, "StreamEvent should be frozen"
    except Exception:
        pass
