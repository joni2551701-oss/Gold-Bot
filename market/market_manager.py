"""
Market Layer — Market Manager (TASK-CORE-005).

MarketManager is the FACADE entry point of the market layer (Director
decision: market/ is the single Facade Layer for future chart/, ai/,
platform/, telegram/, monitoring/). It composes a MarketData /
MarketSnapshot view by READING two already-built inputs:

    - a context.snapshot.ContextSnapshotSchema (the market structure
      context/ already computed -- via context.snapshot.from_context_snapshot;
      FROZEN, never recomputed or modified here), and
    - the latest price from the Data Layer's data_layer.market_memory.MemoryReader
      (or an explicit MarketPrice), plus any recent candles.

Canonical dependencies (Owner ruling, TASK-ARCH-101 PART-03, Option
3A): MemoryReader (Data Layer market data) + ContextSnapshotSchema
(GoldBot Core context). No `stream/` dependency remains.

It performs NO market-structure math, NO signal, NO decision, NO risk,
NO execution, NO Telegram/chart rendering, and NO provider-API call. It
never reads .env or a secret. It keeps a small in-memory MarketState
(the latest MarketData + MarketSnapshot) so a consumer has one place to
read the current market view.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from market.candle import Candle
from market.current_price import MarketPrice, read_current_price
from market.liquidity_state import LiquidityState
from market.market_data import MarketData, MarketStateSnapshot
from market.market_structure import MarketStructureView
from market.regime_state import RegimeState
from market.session_state import SessionState
from market.trend_state import TrendState
from market.volatility_state import VolatilityLevel


@dataclass
class MarketState:
    """The latest market view the façade is holding -- last MarketData + its MarketSnapshot. Volatile; not history."""
    data: Optional[MarketData] = None
    snapshot: Optional[MarketStateSnapshot] = None


class MarketManager:
    """
    Stateless-by-default façade. build_market_data() projects a fresh
    MarketData from a context schema + price/candles; update() also
    stores it as the current MarketState. Never raises for a data-driven
    condition -- a None/empty context yields an all-empty MarketData.
    """

    def __init__(self) -> None:
        self._state = MarketState()

    @property
    def state(self) -> MarketState:
        return self._state

    def build_market_data(
        self,
        context_schema,
        *,
        symbol: Optional[str] = None,
        timeframe: Optional[str] = None,
        current_price: Optional[MarketPrice] = None,
        memory_reader=None,
        candles: Optional[List[Candle]] = None,
        now: Optional[datetime] = None,
    ) -> MarketData:
        """
        Project a MarketData from an already-built ContextSnapshotSchema.
        symbol/timeframe default to the schema's own values. The latest
        price is taken from `current_price` if given, else read from a
        `memory_reader` (data_layer.market_memory.MemoryReader) by symbol. Every state
        field is a READ-ONLY projection. Never raises.
        """
        sym = symbol or getattr(context_schema, "symbol", None) or "UNKNOWN"
        tf = timeframe or getattr(context_schema, "timeframe", None) or "UNKNOWN"

        price = current_price
        if price is None and memory_reader is not None:
            price = read_current_price(memory_reader, sym)

        return MarketData(
            symbol=sym,
            timeframe=tf,
            timestamp=getattr(context_schema, "timestamp", None),
            current_price=price,
            candles=list(candles) if candles else [],
            structure=MarketStructureView.from_context(context_schema),
            trend=TrendState.from_context(context_schema),
            liquidity=LiquidityState.from_context(context_schema),
            session=SessionState.from_context(context_schema, now=now),
            volatility=VolatilityLevel.from_context(context_schema),
            regime=RegimeState.from_context(context_schema),
        )

    def build_snapshot(self, context_schema, **kwargs) -> MarketStateSnapshot:
        """Project a MarketData and summarise it into an immutable MarketSnapshot. Accepts the same kwargs as build_market_data()."""
        data = self.build_market_data(context_schema, **kwargs)
        return MarketStateSnapshot.from_market_data(data)

    def update(self, context_schema, **kwargs) -> MarketData:
        """
        build_market_data() + store it (with its snapshot) as the current
        MarketState, and return the MarketData. The façade's single
        "refresh the current market view" call.
        """
        data = self.build_market_data(context_schema, **kwargs)
        self._state = MarketState(data=data, snapshot=MarketStateSnapshot.from_market_data(data))
        return data

    def current(self) -> Optional[MarketData]:
        """The last built MarketData, or None if update() hasn't run. Fast read for a consumer."""
        return self._state.data

    def current_snapshot(self) -> Optional[MarketStateSnapshot]:
        """The last built MarketSnapshot, or None. Fast serializable read for chart/ai/telegram/monitoring."""
        return self._state.snapshot
