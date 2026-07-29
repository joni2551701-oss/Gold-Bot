"""
market/ facade — Candle / Ticker / OrderBook read models (TASK-CORE-005).

Proves the thin read adapters copy upstream values verbatim (no OHLCV
recompute, no fabricated bid/ask/volume) and adapt from a stream event
or a provider candle using public attributes only.
"""

from datetime import datetime, timezone
from types import SimpleNamespace

from market.candle import Candle
from market.orderbook import OrderBook
from market.ticker import Ticker

_TS = datetime(2026, 1, 7, 12, 0, tzinfo=timezone.utc)


def test_candle_from_stream_event():
    event = SimpleNamespace(symbol="XAUUSD", timeframe="M15", timestamp=_TS,
                            open=2000, high=2010, low=1999, close=2008,
                            volume=12.0, provider="twelvedata")
    c = Candle.from_stream_event(event)
    assert (c.open, c.high, c.low, c.close) == (2000, 2010, 1999, 2008)
    assert c.volume == 12.0
    assert c.provider == "twelvedata"
    d = c.to_dict()
    assert d["timestamp"] == _TS.isoformat()


def test_candle_from_provider_candle_without_volume():
    candle = SimpleNamespace(symbol="XAUUSD", timeframe="M15", timestamp=_TS,
                             open=1.0, high=2.0, low=0.5, close=1.5)
    c = Candle.from_provider_candle(candle)
    assert c.volume is None  # never fabricated
    assert c.provider is None


def test_ticker_from_stream_event_uses_close():
    event = SimpleNamespace(symbol="XAUUSD", close=2008.0, timestamp=_TS, provider="mt5")
    t = Ticker.from_stream_event(event)
    assert t.price == 2008.0
    assert t.bid is None and t.ask is None


def test_orderbook_from_levels_orders_and_bests():
    ob = OrderBook.from_levels(
        "XAUUSD",
        bids=[(2000.0, 1.0), (1999.0, 2.0)],
        asks=[(2001.0, 1.5), (2002.0, 3.0)],
        timestamp=_TS, provider="depthsrc",
    )
    assert ob.best_bid.price == 2000.0
    assert ob.best_ask.price == 2001.0
    assert ob.is_empty is False
    assert ob.provider == "depthsrc"
