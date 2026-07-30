"""
Market Layer — read-only market Facade (TASK-CORE-005).

market/ is the single READ-ONLY facade over the market view. It does
NOT compute market structure -- the real detection (swing/HH/HL/BOS/
CHoCH/order-block/FVG/liquidity/regime/session) lives in context/ and
is FROZEN and untouched (Director decision). market/ READS the
already-built context.snapshot.ContextSnapshotSchema plus stream/'s
current price and aggregates them into one MarketData / MarketSnapshot /
MarketState view for future chart/, ai/, platform/, telegram/, and
monitoring/ consumers.

    config.py -> data/providers/ (FROZEN) -> stream/ -> [context/ computes]
                                                     \-> market/ (this facade) -> consumers

No signal/decision/risk/execution/UI/chart logic. No .env read, no
secret. Not wired into core/pipeline.py -- foundation posture, same as
the other foundation layers. See market/README.md.
"""

from market.candle import Candle
from market.current_price import MarketPrice, read_current_price
from market.liquidity_state import LiquidityState
from market.market_data import MarketData, MarketSnapshot
from market.market_manager import MarketManager, MarketState
from market.market_structure import MarketStructureView
from market.orderbook import OrderBook, OrderBookLevel
from market.regime_state import RegimeState
from market.session_state import SessionState
from market.ticker import Ticker
from market.trend_state import TrendState
from market.volatility_state import VolatilityLevel

__all__ = [
    "Candle",
    "Ticker",
    "OrderBook",
    "OrderBookLevel",
    "MarketPrice",
    "read_current_price",
    "TrendState",
    "LiquidityState",
    "SessionState",
    "VolatilityLevel",
    "RegimeState",
    "MarketStructureView",
    "MarketData",
    "MarketSnapshot",
    "MarketState",
    "MarketManager",
]
