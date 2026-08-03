"""
Backtesting Layer — Data Feed Abstraction (Phase 60.2: Backtesting
Engine, TASK 2).

IDataFeed is the one seam between "where candles come from" and
everything that builds a signal from them. Per the Director's own
rule: no `if backtest: ... else: ...` branch anywhere -- a caller that
only knows `IDataFeed.get_candles(count)` cannot tell whether it is
running live or replayed.

Reuse-audit finding (Phase 60.2, TASK 1): `strategies/`/`signal_layer/signal_engine/signal_engine.py`
already only depend on `context.context_orchestrator.ContextSnapshot`,
never on a candle source directly -- they were already source-agnostic
before this phase. The actual seam requiring an abstraction is one
level up: `core/pipeline.py`'s live `market_data` stage calls
`data_layer.live_data.market_data.MarketDataNormalizer.get_candles(symbol, interval,
outputsize)`, while `backtesting/replay_feed.ReplayFeed.window(size)`
(Phase 60.1) is the replayed equivalent. `IDataFeed` unifies exactly
these two into one interface, so `backtesting_layer/backtest_engine/backtest_engine.py`
(TASK 3) builds context the same way regardless of which one backs it.
"""

from abc import ABC, abstractmethod
from typing import List

from backtesting_layer.replay_engine.replay_feed import ReplayFeed
from data_layer.live_data.market_data import MarketDataNormalizer
from data_layer.providers.twelve_data_client import Candle


class IDataFeed(ABC):
    """The only method a context-builder needs: the most recent `count` candles as of the feed's current position."""

    @abstractmethod
    def get_candles(self, count: int) -> List[Candle]:
        ...


class LiveDataFeed(IDataFeed):
    """Wraps the same MarketDataNormalizer.get_candles() call core/pipeline.py's own live market_data stage already makes -- no new fetch logic."""

    def __init__(self, data_normalizer: MarketDataNormalizer, symbol: str, interval: str):
        self.data_normalizer = data_normalizer
        self.symbol = symbol
        self.interval = interval

    def get_candles(self, count: int) -> List[Candle]:
        return self.data_normalizer.get_candles(self.symbol, self.interval, count)


class ReplayDataFeed(IDataFeed):
    """Wraps a backtesting.replay_feed.ReplayFeed's window() -- the last `count` candles up to and including the feed's current cursor (Phase 60.1)."""

    def __init__(self, replay_feed: ReplayFeed):
        self.replay_feed = replay_feed

    def get_candles(self, count: int) -> List[Candle]:
        return self.replay_feed.window(count)
