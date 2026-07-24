"""
Backtesting Layer — Replay Session (Phase 60.1: Historical Replay
Engine Foundation, TASK 2).

ReplaySession is one replay run's identity and state -- who it is
(`session_id`), what it's replaying (`config`), and where it currently
stands (`state`, `candles_total`, `candles_replayed`, timestamps).
Deliberately holds no candle data or cursor logic of its own --
candle traversal is `replay_feed.py`'s job (TASK 4), timing/pacing is
`replay_clock.py`'s job (TASK 3); a session is the record both are
tracked against, not a third implementation of either.

Mutable by design (unlike this codebase's usual frozen-dataclass-plus-factory
convention) -- a session's whole purpose is to track a moving
position over its own lifetime, the same "in-memory holder" posture
`configuration.runtime_state.RuntimeStateCache` already established
for a different kind of mutable state. `to_result()` is the one-way
bridge to the immutable `ReplayResult` snapshot (`replay_models.py`)
a caller actually reads.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional

from backtesting.replay_models import ReplayConfig, ReplayResult, ReplayState


class ReplaySession:
    """One replay run. Never touches the database or a candle list directly -- replay_engine.py owns loading/wiring, this class only tracks state."""

    def __init__(self, config: ReplayConfig, candles_total: int = 0):
        self.session_id: str = str(uuid.uuid4())
        self.config: ReplayConfig = config
        self.state: ReplayState = ReplayState.PENDING
        self.candles_total: int = candles_total
        self.candles_replayed: int = 0
        self.started_at: Optional[datetime] = None
        self.finished_at: Optional[datetime] = None

    def mark_running(self) -> None:
        if self.started_at is None:
            self.started_at = datetime.now(timezone.utc)
        self.state = ReplayState.RUNNING

    def mark_paused(self) -> None:
        self.state = ReplayState.PAUSED

    def mark_stopped(self) -> None:
        self.state = ReplayState.STOPPED
        self.finished_at = datetime.now(timezone.utc)

    def mark_finished(self) -> None:
        self.state = ReplayState.FINISHED
        self.finished_at = datetime.now(timezone.utc)

    def record_progress(self, candles_replayed: int) -> None:
        """Called by replay_engine.py after each step() -- never decreases (a rewind changes the feed's cursor, not this counter's high-water mark)."""
        self.candles_replayed = max(self.candles_replayed, candles_replayed)

    def to_result(self) -> ReplayResult:
        return ReplayResult(
            symbol=self.config.symbol,
            timeframe=self.config.timeframe,
            state=self.state,
            candles_total=self.candles_total,
            candles_replayed=self.candles_replayed,
            speed=self.config.speed,
            started_at=self.started_at,
            finished_at=self.finished_at,
        )
