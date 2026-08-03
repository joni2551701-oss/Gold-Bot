"""
market/ facade — MarketManager façade lifecycle (TASK-CORE-005).

Proves the façade's small in-memory MarketState: build_market_data() is
stateless (does not store), update() stores the latest MarketData +
MarketSnapshot, and a second update() replaces the first (volatile, not
history).
"""

from datetime import datetime, timezone
from types import SimpleNamespace

from data_layer.live_data.market.market_data import MarketData, MarketSnapshot
from data_layer.live_data.market.market_manager import MarketManager, MarketState

_WEEKDAY = datetime(2026, 1, 7, 12, 0, tzinfo=timezone.utc)


def _schema(regime="TRENDING", symbol="XAUUSD"):
    return SimpleNamespace(symbol=symbol, timeframe="M15", regime=regime)


def test_build_does_not_store_state():
    mgr = MarketManager()
    mgr.build_market_data(_schema(), now=_WEEKDAY)
    assert mgr.current() is None
    assert mgr.state == MarketState()


def test_update_stores_data_and_snapshot():
    mgr = MarketManager()
    data = mgr.update(_schema(), now=_WEEKDAY)
    assert isinstance(data, MarketData)
    assert isinstance(mgr.state.snapshot, MarketSnapshot)
    assert mgr.current() is data
    assert mgr.current_snapshot() is mgr.state.snapshot


def test_second_update_replaces_first_no_history():
    mgr = MarketManager()
    mgr.update(_schema(symbol="XAUUSD"), now=_WEEKDAY)
    second = mgr.update(_schema(symbol="EURUSD"), now=_WEEKDAY)
    assert mgr.current() is second
    assert mgr.current().symbol == "EURUSD"


def test_marketstate_default_is_empty():
    st = MarketState()
    assert st.data is None
    assert st.snapshot is None
