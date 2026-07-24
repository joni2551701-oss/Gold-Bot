"""
Replay log for the Event Bus (v1.1 Phase 1, module 7).

Records published events for late-subscriber replay, governed by a
pluggable ReplayPolicy (DD amendment 5): RingBuffer (count-bounded) or
TimeBased (age-bounded); Persistent is a future policy. This is the
bus-level substrate Module 8 (Replay) builds on.

This module never imports from any layer above data/.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections import deque
from datetime import datetime, timedelta
from typing import Deque, List, Optional, Callable

from data.events.event_model import Event, EventType


class ReplayPolicy(ABC):
    """Governs how much history the replay log retains."""

    @abstractmethod
    def enforce(self, log: "Deque[Event]", now: Optional[datetime]) -> None:
        """Evict from `log` (in place) to satisfy the policy."""
        raise NotImplementedError


class RingBufferPolicy(ReplayPolicy):
    """Keep at most `capacity` most-recent events."""

    def __init__(self, capacity: int = 1000):
        if capacity <= 0:
            raise ValueError("capacity must be > 0")
        self._capacity = capacity

    def enforce(self, log, now=None):
        while len(log) > self._capacity:
            log.popleft()


class TimeBasedPolicy(ReplayPolicy):
    """Keep events newer than `window` (needs event timestamps + now)."""

    def __init__(self, window_seconds: float):
        self._window = timedelta(seconds=window_seconds)

    def enforce(self, log, now):
        if now is None:
            return
        cutoff = now - self._window
        while log and log[0].timestamp is not None and log[0].timestamp < cutoff:
            log.popleft()


class ReplayLog:
    """Bounded, policy-governed event history for replay."""

    def __init__(self, policy: Optional[ReplayPolicy] = None):
        self._policy = policy or RingBufferPolicy()
        self._log: Deque[Event] = deque()

    def record(self, event: Event, now: Optional[datetime] = None) -> None:
        self._log.append(event)
        self._policy.enforce(self._log, now or event.timestamp)

    def events(self, event_type: Optional[EventType] = None) -> List[Event]:
        if event_type is None:
            return list(self._log)
        return [e for e in self._log if e.type is event_type]

    def replay_to(self, handler: Callable[[Event], None],
                  event_type: Optional[EventType] = None) -> int:
        """Re-deliver recorded events (optionally filtered) to a handler."""
        count = 0
        for e in self.events(event_type):
            handler(e)
            count += 1
        return count

    def __len__(self) -> int:
        return len(self._log)
