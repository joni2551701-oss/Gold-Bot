"""TASK-CORE-004 -- CurrentPrice: latest-value store, no history."""

from datetime import datetime, timezone

from data_layer.live_data.stream.current_price import CurrentPrice
from data_layer.live_data.stream.stream_event import StreamEvent


def test_set_and_get():
    cp = CurrentPrice()
    cp.set("XAUUSD", 2005.0, datetime(2026, 1, 2, tzinfo=timezone.utc), "twelvedata")
    point = cp.get("XAUUSD")
    assert point is not None
    assert point.price == 2005.0
    assert point.provider == "twelvedata"


def test_price_of():
    cp = CurrentPrice()
    cp.set("XAUUSD", 2005.0)
    assert cp.price_of("XAUUSD") == 2005.0


def test_missing_symbol_returns_none():
    cp = CurrentPrice()
    assert cp.get("NONE") is None
    assert cp.price_of("NONE") is None


def test_overwrite_keeps_no_history():
    cp = CurrentPrice()
    cp.set("XAUUSD", 2000.0)
    cp.set("XAUUSD", 2010.0)
    # Only the latest is retained -- no history.
    assert cp.price_of("XAUUSD") == 2010.0
    assert len(cp.all()) == 1


def test_update_from_event_uses_close():
    cp = CurrentPrice()
    e = StreamEvent(symbol="XAUUSD", timeframe="M15",
                    timestamp=datetime(2026, 1, 2, tzinfo=timezone.utc),
                    open=2000.0, high=2010.0, low=1995.0, close=2007.5, provider="twelvedata")
    cp.update_from_event(e)
    assert cp.price_of("XAUUSD") == 2007.5


def test_all_and_clear():
    cp = CurrentPrice()
    cp.set("XAUUSD", 2000.0)
    cp.set("BTCUSDT", 50000.0)
    assert set(cp.all().keys()) == {"XAUUSD", "BTCUSDT"}
    cp.clear()
    assert cp.all() == {}
