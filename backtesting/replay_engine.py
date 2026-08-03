"""
Backtesting Layer — Replay Engine (Phase 60.1: Historical Replay
Engine Foundation, TASK 5).

Composes, rather than reimplements, three already-built pieces:
    database.raw_candle_repository.RawCandleRepository  -- persistence (Phase 59.3/59.5, +TASK 1's get_candles_range())
    backtesting.replay_clock.ReplayClock                 -- timing/pacing (TASK 3)
    backtesting.replay_feed.ReplayFeed                    -- candle traversal (TASK 4)

ReplayEngine is the only piece that touches the database -- it loads
the configured window once at construction (`RawCandle` rows,
converted to `data_layer.providers.twelve_data_client.Candle` so `ReplayFeed` hands out
the exact type live data already uses) and then drives `ReplayClock`
and `ReplayFeed` together on each `step()`. It never calls
`strategies/`, `signals/`, `decision/`, or `risk/` -- this phase
replaces only the data source, per the Director's own explicit rule;
what a caller does with the `Candle` a `step()` returns is entirely
outside this module.
"""

from typing import Optional

from backtesting.replay_clock import ReplayClock
from backtesting.replay_feed import ReplayFeed
from backtesting.replay_models import ReplayConfig
from data_layer.providers.twelve_data_client import Candle
from database.raw_candle_repository import RawCandleRepository
from database.raw_candle_models import RawCandle


def _to_candle(raw: RawCandle) -> Candle:
    return Candle(timestamp=raw.timestamp, open=raw.open, high=raw.high, low=raw.low, close=raw.close)


class ReplayEngine:
    """One engine per replay run -- owns its own ReplayClock/ReplayFeed, loads its own candle window once."""

    def __init__(self, config: ReplayConfig, raw_candle_repository: Optional[RawCandleRepository] = None):
        self.config = config
        repository = raw_candle_repository or RawCandleRepository()
        raw_candles = repository.get_candles_range(
            config.symbol, config.timeframe, config.start, config.end, provider=config.provider
        )
        candles = [_to_candle(rc) for rc in raw_candles]

        self.feed = ReplayFeed(candles)
        self.clock = ReplayClock(speed=config.speed)

    @property
    def candles_total(self) -> int:
        return self.feed.total

    @property
    def candles_replayed(self) -> int:
        return self.feed.cursor + 1

    @property
    def is_finished(self) -> bool:
        """
        `ReplayFeed.is_exhausted` alone is already correct for both
        cases: False before any step on a non-empty feed (cursor=-1,
        total>0 -> -1 >= total-1 is False), True once every candle is
        consumed, and True immediately for a genuinely empty candle
        list (cursor=-1, total=0 -> -1 >= -1). A previous extra `and
        self.feed.cursor >= 0` guard here made an empty-dataset replay
        infinite-loop forever instead: with zero candles,
        `ReplayFeed.jump()` always clamps back to cursor=-1 (there is
        no valid index >= 0 to reach), so that extra condition could
        never become True and BacktestEngine.run() (Phase 60.2) would
        spin forever on any symbol/timeframe with no stored candles.
        Found via Phase 60.2's own test suite, fixed here rather than
        worked around in the caller.
        """
        return self.feed.is_exhausted

    def step(self) -> Optional[Candle]:
        """
        Advances the clock (which moves by `int(speed)` positions when
        RUNNING) and the feed together, then returns the feed's new
        current candle. A no-op (returns the current candle unchanged)
        when the clock isn't RUNNING (PENDING/PAUSED/STOPPED/FINISHED) --
        same "step() only moves time forward while playing" contract a
        real player would have, without this phase needing a thread.
        """
        if not self.clock.is_running:
            return self.feed.current_candle()

        target_position = self.clock.advance()
        candle = self.feed.jump(target_position)

        if self.feed.is_exhausted:
            self.clock.finish()

        return candle

    def seek(self, index: int) -> Optional[Candle]:
        """Jumps both clock and feed to the same position, keeping them in sync (ReplayClock.seek()'s own docstring names this engine's responsibility)."""
        self.clock.seek(index)
        return self.feed.jump(index)
