"""
ReplayController -- drives ONE running replay session (v1.1 Phase 1,
module 8). Per SRP (amendment 5) the controller only runs a session;
ReplayManager (replay_manager.py) creates/ends them.

Controls time and data flow into MarketMemory (via a sink, source=REPLAY)
and emits REPLAY.* events on the bus (amendment 2). Enforces the state
machine (amendment 1). No Strategy/Chart/Decision logic; not wired into
core/pipeline.py (Trading Safety).

This module never imports from any layer above data/.
"""

from __future__ import annotations

import itertools
from datetime import datetime, timedelta
from typing import Optional, List

from core_layer.logger.logger import setup_logger
from data.memory.market_memory import MarketMemory
from data.memory.candle_record import CandleSource, MemoryMode
from data.replay.replay_state import ReplayState, assert_transition
from data.replay.replay_session import ReplaySession
from data.replay.replay_clock import ReplayClock
from data.replay.replay_source import ReplayDataSource, Frame
from data.replay.replay_metrics import ReplayMetrics
from data.events.event_bus import EventBus
from data.events.event_model import Event, EventType

logger = setup_logger("ReplayController")


class MemoryReplaySink:
    """Writes replay frames into MarketMemory as source=REPLAY."""

    def __init__(self, memory: MarketMemory):
        self._memory = memory

    def deliver(self, frame: Frame) -> None:
        if self._memory.has_timeframe(frame.timeframe):
            self._memory.timeframe(frame.timeframe).merge_closed(
                [frame.candle], source=CandleSource.REPLAY)

    def reset_all(self) -> None:
        for tf in self._memory.timeframes():
            self._memory.timeframe(tf).hydrate([])   # clear for rebuild


class ReplayController:
    def __init__(self, session: ReplaySession, source: ReplayDataSource,
                 memory: MarketMemory, clock: Optional[ReplayClock] = None,
                 bus: Optional[EventBus] = None,
                 sink: Optional[MemoryReplaySink] = None):
        self._session = session
        self._source = source
        self._memory = memory
        self._clock = clock or ReplayClock(session.start, session.speed)
        self._bus = bus
        self._sink = sink or MemoryReplaySink(memory)
        self._frames: List[Frame] = source.frames(session.asset)
        self._idx = 0
        self._metrics = ReplayMetrics(speed=session.speed)
        self._eid = itertools.count(1)
        # LOADED
        self._memory.set_mode(MemoryMode.REPLAY)
        self._to(ReplayState.LOADED)
        self._session.position = session.start

    # -- state / events -------------------------------------------------
    @property
    def state(self) -> ReplayState:
        return self._session.state

    def _to(self, dst: ReplayState) -> None:
        assert_transition(self._session.state, dst)
        self._session.state = dst

    def _emit(self, event_type: EventType) -> None:
        if self._bus is None:
            return
        self._bus.publish(Event(
            type=event_type, payload=self._session.session_id,
            asset=self._session.asset, event_id=f"rp{next(self._eid)}",
            timestamp=self._clock.now(), source="ReplayController",
            correlation_id=self._session.session_id))
        self._metrics.events_replayed += 1

    # -- controls -------------------------------------------------------
    def play(self) -> None:
        self._to(ReplayState.PLAYING)
        self._emit(EventType.REPLAY_STARTED)

    def pause(self) -> None:
        self._to(ReplayState.PAUSED)
        self._emit(EventType.REPLAY_PAUSED)

    def resume(self) -> None:
        self._to(ReplayState.PLAYING)
        self._emit(EventType.REPLAY_RESUMED)

    def set_speed(self, speed: float) -> None:
        self._clock.set_speed(speed)
        self._session.speed = speed
        self._metrics.speed = speed
        self._emit(EventType.REPLAY_SPEED_CHANGED)

    def tick(self, real_dt: timedelta) -> None:
        """Advance the clock by speed and deliver all now-due frames."""
        if self._session.state is not ReplayState.PLAYING:
            return
        now = self._clock.advance(real_dt)
        while self._idx < len(self._frames) and \
                self._frames[self._idx].timestamp <= now:
            self._deliver(self._frames[self._idx])
            self._idx += 1
        self._session.position = now
        if self._idx >= len(self._frames):
            self._to(ReplayState.FINISHED)
            self._emit(EventType.REPLAY_FINISHED)

    def step_forward(self, n: int = 1) -> int:
        """Deliver the next `n` frames (frame-precise); returns delivered."""
        delivered = 0
        for _ in range(n):
            if self._idx >= len(self._frames):
                break
            frame = self._frames[self._idx]
            self._deliver(frame)
            self._idx += 1
            self._clock.seek(frame.timestamp)
            self._session.position = frame.timestamp
            delivered += 1
        if self._idx >= len(self._frames) and \
                self._session.state in (ReplayState.PLAYING, ReplayState.PAUSED):
            self._to(ReplayState.FINISHED)
            self._emit(EventType.REPLAY_FINISHED)
        return delivered

    def seek(self, when: datetime) -> None:
        """Rebuild memory up to `when` (supports step-back)."""
        self._sink.reset_all()
        self._idx = 0
        for frame in self._frames:
            if frame.timestamp <= when:
                self._deliver(frame)
                self._idx += 1
            else:
                break
        self._clock.seek(when)
        self._session.position = when
        self._session.frame_index = self._idx
        self._emit(EventType.REPLAY_SEEKED)

    def step_back(self, n: int = 1) -> None:
        target_idx = max(0, self._idx - n)
        if target_idx == 0:
            when = self._session.start
        else:
            when = self._frames[target_idx - 1].timestamp
        self.seek(when)

    def transition_to_live(self, real_now: datetime) -> None:
        """Seamless Replay -> LIVE (no restart): mode + clock switch."""
        self._to(ReplayState.LIVE)
        self._memory.set_mode(MemoryMode.LIVE)
        self._clock.switch_live(real_now)
        self._emit(EventType.REPLAY_LIVE_TRANSITION)

    def metrics(self) -> ReplayMetrics:
        return self._metrics

    def _deliver(self, frame: Frame) -> None:
        self._sink.deliver(frame)
        self._metrics.frames_replayed += 1
