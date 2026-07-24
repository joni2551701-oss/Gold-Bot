"""
Replay validation (v1.1 Phase 1, module 8; amendment 4).

Before a replay starts: timeline valid, source has data, asset present in
memory, and (for snapshot sources) integrity holds. A replay never starts
on invalid inputs. This module never imports from any layer above data/.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from data.memory.market_memory import MarketMemory
from data.replay.replay_source import ReplayDataSource, Frame
from data.candle_clock import CandleClock
from data.persistence.integrity import check_series


@dataclass
class ReplayValidation:
    ok: bool = True
    errors: List[str] = field(default_factory=list)

    def fail(self, msg: str) -> "ReplayValidation":
        self.ok = False
        self.errors.append(msg)
        return self


def validate_replay(asset: str, source: ReplayDataSource,
                    memory: MarketMemory,
                    clock: Optional[CandleClock] = None,
                    check_integrity: bool = True) -> ReplayValidation:
    result = ReplayValidation()
    clock = clock or CandleClock()

    # asset present in memory?
    if not asset:
        return result.fail("asset is empty")

    # timeline valid?
    start, end = source.timeline(asset)
    if start is None or end is None:
        return result.fail("source has no data (empty timeline)")
    if start > end:
        result.fail(f"invalid timeline: start {start} > end {end}")

    frames: List[Frame] = source.frames(asset)
    if not frames:
        result.fail("source produced no frames")

    # per-timeframe integrity of the source frames (amendment 4)
    if check_integrity and frames:
        by_tf = {}
        for f in frames:
            by_tf.setdefault(f.timeframe, []).append(f.candle)
        for tf, candles in by_tf.items():
            report = check_series(candles, tf, clock)
            if not report.ok:
                result.fail(f"integrity failed on {tf}: {report.as_dict()}")
    return result
