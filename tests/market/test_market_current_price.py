"""
market/ facade — current price integration with stream/ (TASK-CORE-005).

Proves read_current_price() REUSES the existing
stream.current_price.CurrentPrice store (no re-implementation, per the
Director's "duplicate logic qat'iyan taqiqlanadi") and the façade
threads that price into MarketData, without importing stream internals
beyond the public read API.
"""

from datetime import datetime, timezone
from types import SimpleNamespace

from stream.current_price import CurrentPrice

from market.current_price import MarketPrice, read_current_price
from market.market_manager import MarketManager
from market.ticker import Ticker

_WEEKDAY = datetime(2026, 1, 7, 12, 0, tzinfo=timezone.utc)


def test_reads_price_from_stream_current_price():
    store = CurrentPrice()
    store.set("XAUUSD", 2010.5, timestamp=_WEEKDAY, provider="twelvedata")
    price = read_current_price(store, "XAUUSD")
    assert isinstance(price, MarketPrice)
    assert price.symbol == "XAUUSD"
    assert price.price == 2010.5
    assert price.provider == "twelvedata"


def test_unknown_symbol_and_none_store_return_none():
    store = CurrentPrice()
    assert read_current_price(store, "XAUUSD") is None
    assert read_current_price(None, "XAUUSD") is None


def test_manager_threads_stream_price_into_marketdata():
    store = CurrentPrice()
    store.set("XAUUSD", 2033.0, timestamp=_WEEKDAY)
    schema = SimpleNamespace(symbol="XAUUSD", timeframe="M15", regime="TRENDING")
    data = MarketManager().build_market_data(schema, stream_current_price=store, now=_WEEKDAY)
    assert data.price == 2033.0


def test_explicit_current_price_takes_precedence_over_stream():
    store = CurrentPrice()
    store.set("XAUUSD", 2000.0)
    explicit = MarketPrice(symbol="XAUUSD", price=2099.0)
    schema = SimpleNamespace(symbol="XAUUSD", timeframe="M15", regime="RANGE")
    data = MarketManager().build_market_data(
        schema, current_price=explicit, stream_current_price=store, now=_WEEKDAY)
    assert data.price == 2099.0


def test_ticker_adapts_from_market_price_and_is_none_safe():
    price = MarketPrice(symbol="XAUUSD", price=2010.5, provider="mt5")
    ticker = Ticker.from_market_price(price)
    assert ticker.symbol == "XAUUSD"
    assert ticker.price == 2010.5
    assert ticker.bid is None and ticker.ask is None
    assert Ticker.from_market_price(None) is None
