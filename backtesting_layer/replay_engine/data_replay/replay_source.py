"""
Replay data sources (v1.1 Phase 1, module 8).

`ReplayDataSource` abstracts where replay frames come from -- snapshots
(module 6), historical data (module 5), or future remote/simulation
sources. A Frame is a timeframe-tagged candle at a point in time.

Future time sources (amendment 6): `SimulationSource` is the base for
SyntheticSource / ScenarioSource / Monte-Carlo generators the Training
module will use -- they subclass ReplayDataSource without changing
anything above it.

This module never imports from any layer above data/.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from data_layer.providers.twelve_data_client import Candle
from data_layer.historical_data.historical_provider import HistoricalProvider


@dataclass(frozen=True)
class Frame:
    timeframe: str
    candle: Candle

    @property
    def timestamp(self) -> datetime:
        return self.candle.timestamp


class ReplayDataSource(ABC):
    @abstractmethod
    def timeline(self, asset: str) -> Tuple[Optional[datetime], Optional[datetime]]:
        """(start, end) of available data, or (None, None) if empty."""
        raise NotImplementedError

    @abstractmethod
    def frames(self, asset: str, start: Optional[datetime] = None,
               end: Optional[datetime] = None) -> List[Frame]:
        """Time-ordered frames in [start, end] (inclusive of start)."""
        raise NotImplementedError


class SnapshotReplaySource(ReplayDataSource):
    """Replays from decoded snapshot candles (module 6)."""

    def __init__(self, frames_by_timeframe: Dict[str, List[Candle]]):
        self._by_tf = {tf: sorted(cs, key=lambda c: c.timestamp)
                       for tf, cs in frames_by_timeframe.items()}

    def _all(self) -> List[Frame]:
        out = [Frame(tf, c) for tf, cs in self._by_tf.items() for c in cs]
        return sorted(out, key=lambda f: f.timestamp)

    def timeline(self, asset):
        frames = self._all()
        if not frames:
            return (None, None)
        return (frames[0].timestamp, frames[-1].timestamp)

    def frames(self, asset, start=None, end=None):
        return [f for f in self._all()
                if (start is None or f.timestamp >= start)
                and (end is None or f.timestamp <= end)]


class HistoricalReplaySource(ReplayDataSource):
    """Replays from a HistoricalProvider (module 5) for one timeframe."""

    def __init__(self, provider: HistoricalProvider, timeframe: str,
                 start: datetime, end: datetime):
        self._provider = provider
        self._tf = timeframe
        self._start = start
        self._end = end

    def timeline(self, asset):
        return (self._start, self._end)

    def frames(self, asset, start=None, end=None):
        s = start or self._start
        e = end or self._end
        candles = self._provider.fetch_range(asset, self._tf, s, e)
        return [Frame(self._tf, c)
                for c in sorted(candles, key=lambda c: c.timestamp)]


class SimulationSource(ReplayDataSource):
    """
    Base for future generated sources (amendment 6): SyntheticSource,
    ScenarioSource, Monte-Carlo, AI-generated market. Subclasses implement
    `frames()`/`timeline()`. Present now so the Training module can plug in
    later without changing the Replay Engine.
    """
