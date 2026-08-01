"""
market/ projection — current price via the canonical MemoryReader
(TASK-CORE-005; canonicalized TASK-ARCH-101 PART-03).

Proves read_current_price() reads the latest price from the Data
Layer's data.memory.MemoryReader (MA-002) -- NOT the DEPRECATED
stream/ -- and the projection threads that price into MarketData.
"""

from datetime import datetime, timezone
from types import SimpleNamespace

from data.memory import MarketMemoryRegistry, MemoryReader
from data.twelve_data_client import Candle

from market.current_price import MarketPrice, read_current_price
from market.market_manager import MarketManager
from market.ticker import Ticker

_WEEKDAY = datetime(2026, 1, 7, 12, 0, tzinfo=timezone.utc)


def _reader_with_price(symbol="XAUUSD", timeframe="M1", price=2010.5):
    """A real MemoryReader with one hydrated closed candle for `symbol`."""
    registry = MarketMemoryRegistry()
    registry.register(symbol)
    candle = Candle(timestamp=_WEEKDAY, open=price, high=price, low=price, close=price)
    registry.get(symbol).timeframe(timeframe).hydrate([candle])
    return MemoryReader(registry)


def test_reads_price_from_memory_reader():
    reader = _reader_with_price(price=2010.5)
    price = read_current_price(reader, "XAUUSD")
    assert isinstance(price, MarketPrice)
    assert price.symbol == "XAUUSD"
    assert price.price == 2010.5


def test_unknown_symbol_and_none_reader_return_none():
    reader = _reader_with_price()
    assert read_current_price(reader, "BTCUSDT") is None   # asset not registered
    assert read_current_price(None, "XAUUSD") is None


def test_manager_threads_memory_price_into_marketdata():
    reader = _reader_with_price(price=2033.0)
    schema = SimpleNamespace(symbol="XAUUSD", timeframe="M15", regime="TRENDING")
    data = MarketManager().build_market_data(schema, memory_reader=reader, now=_WEEKDAY)
    assert data.price == 2033.0


def test_explicit_current_price_takes_precedence_over_memory():
    reader = _reader_with_price(price=2000.0)
    explicit = MarketPrice(symbol="XAUUSD", price=2099.0)
    schema = SimpleNamespace(symbol="XAUUSD", timeframe="M15", regime="RANGE")
    data = MarketManager().build_market_data(
        schema, current_price=explicit, memory_reader=reader, now=_WEEKDAY)
    assert data.price == 2099.0


def test_ticker_adapts_from_market_price_and_is_none_safe():
    price = MarketPrice(symbol="XAUUSD", price=2010.5, provider="mt5")
    ticker = Ticker.from_market_price(price)
    assert ticker.symbol == "XAUUSD"
    assert ticker.price == 2010.5
    assert ticker.bid is None and ticker.ask is None
    assert Ticker.from_market_price(None) is None
