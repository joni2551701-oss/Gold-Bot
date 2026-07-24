"""
ReplayClock -- virtual time for the Replay Engine (v1.1 Phase 1, module 8).

Holds a virtual "now" advanced by `advance(real_dt)` scaled by speed
(1x, 2x, 5x, 10x, ...), seekable, and switchable between REPLAY and LIVE.
The engine derives ALL timing from this clock (never wall-clock), so
replay is deterministic and speed-controllable.

This module never imports from any layer above data/.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from data.memory.candle_record import MemoryMode


class ReplayClock:
    def __init__(self, start: datetime, speed: float = 1.0):
        self._now = self._utc(start)
        self._speed = self._valid_speed(speed)
        self._mode = MemoryMode.REPLAY

    def mode(self) -> MemoryMode:
        return self._mode

    def now(self) -> datetime:
        return self._now

    def speed(self) -> float:
        return self._speed

    def set_speed(self, speed: float) -> None:
        self._speed = self._valid_speed(speed)

    def advance(self, real_dt: timedelta) -> datetime:
        """Advance virtual time by real_dt scaled by speed (REPLAY only)."""
        if self._mode is MemoryMode.REPLAY:
            self._now = self._now + timedelta(
                seconds=real_dt.total_seconds() * self._speed)
        return self._now

    def seek(self, when: datetime) -> None:
        self._now = self._utc(when)

    def switch_live(self, real_now: datetime) -> None:
        """Hand off to live: virtual time becomes real time."""
        self._mode = MemoryMode.LIVE
        self._now = self._utc(real_now)

    @staticmethod
    def _valid_speed(speed: float) -> float:
        if speed <= 0:
            raise ValueError("speed must be > 0")
        return float(speed)

    @staticmethod
    def _utc(dt: datetime) -> datetime:
        if not isinstance(dt, datetime) or dt.tzinfo is None:
            raise ValueError("clock time must be timezone-aware (UTC)")
        return dt.astimezone(timezone.utc)
