"""ReplayMetrics -- counters for a replay session (module 8)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ReplayMetrics:
    frames_replayed: int = 0
    events_replayed: int = 0
    speed: float = 1.0
    lag_seconds: float = 0.0
    duration_seconds: float = 0.0

    def as_dict(self) -> dict:
        return {
            "frames_replayed": self.frames_replayed,
            "events_replayed": self.events_replayed,
            "speed": self.speed,
            "lag_seconds": round(self.lag_seconds, 6),
            "duration_seconds": round(self.duration_seconds, 6),
        }
