"""
Market Layer — read-only market Facade (TASK-CORE-005).

═══════════════════════════════════════════════════════════════════════
UPPER-LAYER COMPONENT — NOT A DATA LAYER MEMBER (Owner ruling,
TASK-ARCH-101 Part 3).

Architectural clarification (Owner): **MarketProjection is NOT part of
the Data Layer.** It is an upper-layer component that CONSUMES the
outputs of the Data Layer (raw price) and GoldBot Core (`context/`'s
structure). The Data Layer works ONLY with raw market data and does not
know about Context/Strategy/Decision objects — verified in code
(`data/` imports none of them). This `market/` package reads
`context.snapshot.ContextSnapshotSchema` (Core output), which is exactly
why it cannot live in, and must not be folded into, `data/`.

Consequences of the ruling:
- The earlier TASK-ARCH-100 framing of `market/` as a "Data Layer legacy
  duplicate" to be migrated into `data/`/`MemoryReader` is WITHDRAWN —
  it was a mis-classification. `market/` is a distinct upper-layer
  component (it maps to the ecosystem's Application Services / market-
  view tier, not the Data Layer). It is NOT absorbed into `data/`.
- `market/` is NOT deleted and NOT DEPRECATED. It stays as the (current)
  home of the Market Projection capability until a proper upper-layer
  home is built.
- The only Data-Layer-migration-relevant coupling is that `market/`
  currently reads its price from the LEGACY `stream/` (`stream.CurrentPrice`);
  re-pointing that ONE dependency to the canonical current-price source
  is a small, separate item — it does not require moving the projection.

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
