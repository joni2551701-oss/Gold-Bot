"""
Market Layer — Market Data container + Snapshot (TASK-CORE-005).

MarketData is the single container that unifies every market view the
façade exposes: symbol/timeframe/current price/candles plus the
structure, trend, liquidity, session, volatility and regime states.
Every one of those states is a READ-ONLY projection of stream/ + the
already-computed context/ output (see each state module) -- MarketData
holds them together, it does not compute any of them.

MarketSnapshot is the immutable, serializable, point-in-time summary of
a MarketData (primitives only) -- the shape a future chart/, AI/,
telegram/ or monitoring/ consumer serializes. Both are data views: no
signal, decision, risk, execution, or provider-API logic.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional

from market.candle import Candle
from market.current_price import MarketPrice
from market.liquidity_state import LiquidityState
from market.market_structure import MarketStructureView
from market.regime_state import RegimeState
from market.session_state import SessionState
from market.trend_state import TrendState
from market.volatility_state import VolatilityLevel


@dataclass(frozen=True)
class MarketData:
    """
    The aggregated market view. Defaults make an all-empty MarketData a
    valid "no data yet" state (never raises to construct). Consumers
    read; they never expect MarketData to have computed anything itself.
    """
    symbol: str
    timeframe: str
    timestamp: Optional[datetime] = None
    current_price: Optional[MarketPrice] = None
    candles: List[Candle] = field(default_factory=list)
    structure: MarketStructureView = field(default_factory=MarketStructureView)
    trend: TrendState = TrendState.UNKNOWN
    liquidity: LiquidityState = field(default_factory=LiquidityState)
    session: SessionState = field(default_factory=SessionState)
    volatility: VolatilityLevel = VolatilityLevel.UNKNOWN
    regime: RegimeState = field(default_factory=RegimeState)

    @property
    def price(self) -> Optional[float]:
        """The latest float price, or None -- the fast read every consumer wants."""
        return self.current_price.price if self.current_price else None

    @property
    def candle_count(self) -> int:
        return len(self.candles)

    @property
    def latest_candle(self) -> Optional[Candle]:
        return self.candles[-1] if self.candles else None


@dataclass(frozen=True)
class MarketStateSnapshot:
    """
    Immutable, serializable point-in-time summary of a MarketData --
    primitives only, safe to JSON/transport to any consumer. Built via
    from_market_data(); carries candle_count rather than the candle list.

    Renamed from `MarketSnapshot` (TASK-ARCH-100 Step 8, Owner decision
    3): the canonical class literally named `MarketSnapshot` is now
    `data_layer.live_data.market_data.MarketSnapshot` (a multi-timeframe candle
    container -- a different shape from this market-state projection).
    A backward-compatible `MarketSnapshot = MarketStateSnapshot` alias
    is kept at the bottom of this module so existing importers of
    `market.market_data.MarketSnapshot` keep working (no delete, per
    the Owner's no-DELETE rule).
    """
    symbol: str
    timeframe: str
    created_at: datetime
    timestamp: Optional[datetime] = None
    price: Optional[float] = None
    trend: str = TrendState.UNKNOWN.value
    regime: str = "UNKNOWN"
    volatility: str = VolatilityLevel.UNKNOWN.value
    session: str = "OFF_SESSION"
    swing_state: Optional[str] = None
    bos: bool = False
    choch: bool = False
    order_block: bool = False
    fvg: bool = False
    liquidity_sweep: bool = False
    liquidity_type: Optional[str] = None
    candle_count: int = 0

    @classmethod
    def from_market_data(cls, data: MarketData, created_at: Optional[datetime] = None) -> "MarketStateSnapshot":
        """Summarise a MarketData into an immutable snapshot of primitives. Never raises."""
        return cls(
            symbol=data.symbol,
            timeframe=data.timeframe,
            created_at=created_at or datetime.now(timezone.utc),
            timestamp=data.timestamp,
            price=data.price,
            trend=data.trend.value,
            regime=data.regime.regime,
            volatility=data.volatility.value,
            session=data.session.label,
            swing_state=data.structure.swing_state,
            bos=data.structure.bos,
            choch=data.structure.choch,
            order_block=data.structure.order_block,
            fvg=data.structure.fvg,
            liquidity_sweep=data.liquidity.sweep_detected,
            liquidity_type=data.liquidity.liquidity_type,
            candle_count=data.candle_count,
        )

    def to_dict(self) -> dict:
        """JSON-safe dict -- datetimes rendered as ISO-8601 strings."""
        return {
            "symbol": self.symbol,
            "timeframe": self.timeframe,
            "created_at": self.created_at.isoformat(),
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "price": self.price,
            "trend": self.trend,
            "regime": self.regime,
            "volatility": self.volatility,
            "session": self.session,
            "swing_state": self.swing_state,
            "bos": self.bos,
            "choch": self.choch,
            "order_block": self.order_block,
            "fvg": self.fvg,
            "liquidity_sweep": self.liquidity_sweep,
            "liquidity_type": self.liquidity_type,
            "candle_count": self.candle_count,
        }


# Backward-compatibility alias (TASK-ARCH-100 Step 8, Owner decision 3 +
# no-DELETE rule). The projection snapshot's canonical name is now
# `MarketStateSnapshot`; `MarketSnapshot` here is the SAME object under
# its old name so existing `from market.market_data import MarketSnapshot`
# importers keep working. The only class literally *defined* as
# `MarketSnapshot` in the repository is now the canonical
# `data_layer.live_data.market_data.MarketSnapshot`. This alias is a compatibility shim,
# not a second class definition.
MarketSnapshot = MarketStateSnapshot
