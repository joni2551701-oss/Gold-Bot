"""
market/ facade — empty-state behaviour (TASK-CORE-005).

Proves the façade never raises for missing data: a None or empty context
yields an all-empty MarketData with honest defaults (UNKNOWN / None /
empty), and its MarketSnapshot serialises cleanly. Missing data must be
a defined shape, never an exception.
"""

from types import SimpleNamespace

from data_layer.live_data.market.liquidity_state import LiquidityState
from data_layer.live_data.market.market_data import MarketSnapshot
from data_layer.live_data.market.market_manager import MarketManager
from data_layer.live_data.market.market_structure import MarketStructureView
from data_layer.live_data.market.regime_state import RegimeState
from data_layer.live_data.market.trend_state import TrendState
from data_layer.live_data.market.volatility_state import VolatilityLevel


def test_none_context_yields_empty_marketdata():
    data = MarketManager().build_market_data(None, symbol="XAUUSD", timeframe="M15")
    assert data.symbol == "XAUUSD"
    assert data.timeframe == "M15"
    assert data.price is None
    assert data.candle_count == 0
    assert data.trend is TrendState.UNKNOWN
    assert data.volatility is VolatilityLevel.UNKNOWN
    assert data.structure == MarketStructureView()
    assert data.liquidity == LiquidityState()
    assert data.regime == RegimeState()


def test_empty_schema_falls_back_to_unknown_symbol():
    data = MarketManager().build_market_data(SimpleNamespace())
    assert data.symbol == "UNKNOWN"
    assert data.timeframe == "UNKNOWN"


def test_empty_marketdata_snapshot_serialises():
    data = MarketManager().build_market_data(None, symbol="XAUUSD", timeframe="M15")
    snap = MarketSnapshot.from_market_data(data)
    d = snap.to_dict()
    assert d["symbol"] == "XAUUSD"
    assert d["price"] is None
    assert d["trend"] == TrendState.UNKNOWN.value
    assert d["regime"] == "UNKNOWN"
    assert d["candle_count"] == 0
    assert d["bos"] is False and d["order_block"] is False


def test_current_is_none_before_any_update():
    mgr = MarketManager()
    assert mgr.current() is None
    assert mgr.current_snapshot() is None
