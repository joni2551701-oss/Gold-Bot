"""
market/ facade — MarketData / MarketSnapshot container shape (TASK-CORE-005).

Proves the aggregated container holds every projected state together,
exposes the fast reads consumers rely on (price/candle_count/
latest_candle), and serialises to a stable JSON-safe MarketSnapshot.
MarketData computes nothing itself -- it only carries the projections.
"""

from datetime import datetime, timezone
from types import SimpleNamespace

from data_layer.live_data.market.candle import Candle
from data_layer.live_data.market.current_price import MarketPrice
from data_layer.live_data.market.liquidity_state import LiquidityState
from data_layer.live_data.market.market_data import MarketData, MarketSnapshot
from data_layer.live_data.market.market_manager import MarketManager
from data_layer.live_data.market.market_structure import MarketStructureView
from data_layer.live_data.market.regime_state import RegimeState
from data_layer.live_data.market.session_state import SessionState
from data_layer.live_data.market.trend_state import TrendState
from data_layer.live_data.market.volatility_state import VolatilityLevel

# A deterministic non-weekend instant (Wed 2026-01-07 12:00 UTC).
_WEEKDAY = datetime(2026, 1, 7, 12, 0, tzinfo=timezone.utc)


def _schema(**over):
    base = dict(
        symbol="XAUUSD",
        timeframe="M15",
        timestamp=datetime(2026, 1, 7, 11, 45, tzinfo=timezone.utc),
        structure=SimpleNamespace(trend="BULLISH", bos=True, choch=False, swing_state="HH"),
        liquidity=SimpleNamespace(sweep_detected=True, liquidity_type="BUY_SIDE_LIQUIDITY"),
        zones=SimpleNamespace(order_block=True, fvg=False),
        session=SimpleNamespace(current_session="LONDON"),
        regime="TRENDING",
    )
    base.update(over)
    return SimpleNamespace(**base)


def test_market_data_defaults_are_a_valid_empty_view():
    data = MarketData(symbol="XAUUSD", timeframe="M15")
    assert data.price is None
    assert data.candle_count == 0
    assert data.latest_candle is None
    assert data.trend is TrendState.UNKNOWN
    assert data.volatility is VolatilityLevel.UNKNOWN
    assert isinstance(data.structure, MarketStructureView)
    assert isinstance(data.liquidity, LiquidityState)
    assert isinstance(data.session, SessionState)
    assert isinstance(data.regime, RegimeState)


def test_market_data_fast_reads():
    c1 = Candle("XAUUSD", "M15", _WEEKDAY, 2000, 2005, 1999, 2003)
    c2 = Candle("XAUUSD", "M15", _WEEKDAY, 2003, 2010, 2002, 2008)
    price = MarketPrice(symbol="XAUUSD", price=2008.0)
    data = MarketData(symbol="XAUUSD", timeframe="M15", current_price=price, candles=[c1, c2])
    assert data.price == 2008.0
    assert data.candle_count == 2
    assert data.latest_candle is c2


def test_manager_builds_full_marketdata_from_schema():
    mgr = MarketManager()
    data = mgr.build_market_data(_schema(), now=_WEEKDAY)
    assert data.symbol == "XAUUSD"
    assert data.timeframe == "M15"
    assert data.trend is TrendState.BULLISH
    assert data.structure.bos is True
    assert data.structure.order_block is True
    assert data.liquidity.sweep_detected is True
    assert data.liquidity.buy_side is True
    assert data.session.current_session == "LONDON"
    assert data.regime.regime == "TRENDING"
    assert data.volatility is VolatilityLevel.NORMAL


def test_snapshot_is_immutable_serialisable_summary():
    mgr = MarketManager()
    data = mgr.build_market_data(_schema(), now=_WEEKDAY)
    snap = MarketSnapshot.from_market_data(data)
    d = snap.to_dict()
    assert d["symbol"] == "XAUUSD"
    assert d["trend"] == TrendState.BULLISH.value
    assert d["regime"] == "TRENDING"
    assert d["bos"] is True
    assert d["order_block"] is True
    assert d["liquidity_sweep"] is True
    assert d["session"] == "LONDON"
    # JSON-safe: datetimes rendered as ISO strings.
    assert isinstance(d["created_at"], str)
    assert d["timestamp"] == data.timestamp.isoformat()


def test_manager_update_stores_current_view():
    mgr = MarketManager()
    assert mgr.current() is None
    assert mgr.current_snapshot() is None
    data = mgr.update(_schema(), now=_WEEKDAY)
    assert mgr.current() is data
    assert mgr.current_snapshot() is not None
    assert mgr.current_snapshot().symbol == "XAUUSD"
