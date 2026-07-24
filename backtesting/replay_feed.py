"""
Backtesting Layer — Replay Feed (Phase 60.1: Historical Replay Engine
Foundation, TASK 4).

ReplayFeed hands out `data.twelve_data_client.Candle` objects -- the
exact type `data.market_data.MarketDataNormalizer.get_candles()`
already returns to the live pipeline -- one at a time, from an
in-memory list loaded once at construction (`replay_engine.py`, TASK 5,
owns the load). This is the reuse-audit finding this phase's brief
asked for: Strategy/Context consume `List[Candle]` today regardless of
source, so a `ReplayFeed` that also produces `Candle` means nothing
downstream of it needs to change to accept replayed data later -- the
Director's own "LIVE Provider -> Strategy / REPLAY Feed -> Strategy,
same code either way" requirement, satisfied by matching the existing
type rather than inventing a new one.

Foundation only: nothing constructs a ReplayFeed from
core/pipeline.py, strategies/, or signals/ in this phase.
"""

from typing import List, Optional

from data.twelve_data_client import Candle


class ReplayFeed:
    """
    Cursor-based access over a fixed, already-loaded candle list.
    `cursor` starts at -1 (before the first candle) -- `current_candle()`
    is None until the first `next_candle()` call, same "nothing shown
    until advanced" posture as a video player before pressing play.
    """

    def __init__(self, candles: List[Candle]):
        self.candles: List[Candle] = candles
        self.cursor: int = -1

    @property
    def total(self) -> int:
        return len(self.candles)

    @property
    def is_exhausted(self) -> bool:
        return self.cursor >= len(self.candles) - 1

    def current_candle(self) -> Optional[Candle]:
        if 0 <= self.cursor < len(self.candles):
            return self.candles[self.cursor]
        return None

    def next_candle(self) -> Optional[Candle]:
        """Advances the cursor by one and returns the new current candle -- None (cursor left unchanged) once exhausted."""
        if self.is_exhausted:
            return None
        self.cursor += 1
        return self.current_candle()

    def previous_candle(self) -> Optional[Candle]:
        """Retreats the cursor by one -- None (cursor left unchanged) if already at or before the first candle."""
        if self.cursor <= 0:
            return None
        self.cursor -= 1
        return self.current_candle()

    def jump(self, index: int) -> Optional[Candle]:
        """Moves the cursor directly to `index`, clamped to [-1, total-1]. Returns the resulting current candle (None if index == -1)."""
        self.cursor = max(-1, min(index, len(self.candles) - 1))
        return self.current_candle()

    def window(self, size: int) -> List[Candle]:
        """The last `size` candles up to and including the cursor -- the same fixed-size-window shape MarketDataNormalizer.get_candles(outputsize=N) already returns for live data. Fewer than `size` if the cursor hasn't advanced that far yet; empty before the first next_candle() call."""
        if self.cursor < 0:
            return []
        start = max(0, self.cursor - size + 1)
        return self.candles[start:self.cursor + 1]
