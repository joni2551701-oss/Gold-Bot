"""
Backtesting Layer — Replay Models (Phase 60.1: Historical Replay
Engine Foundation, TASK 2/7).

Reuse-first, per the Director's own Phase 60.1 brief and CLAUDE.md's
Module Reuse Principle: no new top-level `market/` package -- Replay
lives inside `backtesting/` because it is a service over existing
Historical Data (`database.raw_candle_repository.RawCandleRepository`,
Phase 59.3/59.5), not a new business domain of its own. This module
holds the pure value types every other `backtesting/replay_*.py` file
shares; TASK 7 (Replay Report) is folded into this file rather than
given its own module -- `format_replay_report()` is a small, tightly
coupled formatter over `ReplayResult`, the same "extend, don't add a
file" instinct the Module Reuse Principle asks for at the package's
own internal scope, not just the repo's.

Foundation only: nothing in `core/pipeline.py`, `strategies/`,
`signals/`, `decision/`, `risk/`, or `execution/` reads this module.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class ReplayState(Enum):
    """
    PENDING: constructed, not yet started.
    RUNNING: actively advancing.
    PAUSED: temporarily halted, resumable.
    STOPPED: halted by an explicit stop() -- not resumable (see
        replay_controller.py's restart() for starting over instead).
    FINISHED: reached the end of the configured candle range.
    """
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    STOPPED = "STOPPED"
    FINISHED = "FINISHED"


@dataclass(frozen=True)
class ReplayConfig:
    """
    What to replay. `start`/`end` bound the historical window (fed to
    `database.raw_candle_repository.RawCandleRepository.get_candles_range()`,
    Phase 60.1's own additive extension to that repository). `speed`
    is candles consumed per `ReplayEngine.step()` call (2.0 = two
    candles per step, 0.5 = one candle every two steps) -- a
    deterministic, manually-stepped notion of speed, not a wall-clock
    timer; this phase builds no background thread or scheduler.
    """
    symbol: str
    timeframe: str
    start: datetime
    end: datetime
    provider: Optional[str] = None
    speed: float = 1.0


@dataclass(frozen=True)
class ReplayResult:
    """
    A point-in-time snapshot of one replay session -- valid whether
    the session is still running (a progress report) or has reached
    FINISHED/STOPPED (a final report). `progress`/`finished` are
    derived, not stored twice.
    """
    symbol: str
    timeframe: str
    state: ReplayState
    candles_total: int
    candles_replayed: int
    speed: float
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None

    @property
    def progress(self) -> float:
        """0.0-1.0. 0.0 for an empty dataset (never divides by zero)."""
        if self.candles_total <= 0:
            return 0.0
        return min(1.0, self.candles_replayed / self.candles_total)

    @property
    def finished(self) -> bool:
        return self.state == ReplayState.FINISHED

    @property
    def duration_seconds(self) -> Optional[float]:
        """Wall-clock seconds this session has been open. None until started_at is set."""
        if self.started_at is None:
            return None
        end = self.finished_at or datetime.now(self.started_at.tzinfo)
        return (end - self.started_at).total_seconds()


def format_replay_report(result: ReplayResult) -> str:
    """
    TASK 7 -- the future `/replay_status` command's payload (see
    telegram/owner/replay_commands.py). Never raises: every field on
    ReplayResult is either always-present or already None-safe via its
    own property.
    """
    duration = result.duration_seconds
    lines = [
        f"Dataset: {result.symbol} {result.timeframe}",
        f"State: {result.state.value}",
        f"Candles: {result.candles_replayed}/{result.candles_total}",
        f"Progress: {result.progress:.1%}",
        f"Speed: {result.speed}x",
        f"Duration: {duration:.1f}s" if duration is not None else "Duration: not started",
        f"Finished: {result.finished}",
    ]
    return "\n".join(lines)
