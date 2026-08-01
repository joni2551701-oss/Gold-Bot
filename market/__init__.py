"""
Market Layer — read-only market Facade (TASK-CORE-005).

═══════════════════════════════════════════════════════════════════════
LEGACY (NON-CANONICAL) — TASK-ARCH-100, Owner decisions 1 & 2.

The Owner has designated `data/` as the canonical Data Layer. This
`market/` package is NON-CANONICAL and no new consumer should be built
on it. HOWEVER, its read-only context→market-state projection facade
(trend/liquidity/session/volatility/regime/structure views over
`context.snapshot.ContextSnapshotSchema`) is a UNIQUE capability that
the canonical `data/` layer has NO equivalent for today (TASK-ARCH-100
Step 7). It is therefore NOT deleted, NOT DEPRECATED, and its migration
target is an OPEN Migration Proposal awaiting Owner approval — it must
not be moved into `data/` without that approval. See
`docs/governance/collaboration/TASK-ARCH-100.md` (Step 7).

Note: the projection snapshot class formerly named `MarketSnapshot`
here is now `MarketStateSnapshot` (TASK-ARCH-100 Step 8) so the single
canonical `MarketSnapshot` is `data.market_data.MarketSnapshot`; a
backward-compatible `MarketSnapshot` alias is retained.
═══════════════════════════════════════════════════════════════════════

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
from market.market_data import MarketData, MarketStateSnapshot, MarketSnapshot
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
    "MarketStateSnapshot",
    "MarketSnapshot",  # backward-compat alias of MarketStateSnapshot (TASK-ARCH-100 Step 8)
    "MarketState",
    "MarketManager",
]
