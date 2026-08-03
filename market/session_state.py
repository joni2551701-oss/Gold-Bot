"""
Market Layer — Session State projection (TASK-CORE-005).

SessionState is a READ-ONLY projection combining the trading session
context/ already classified (context.session -> ContextSnapshotSchema.
session.current_session) with the canonical Data Layer weekend clock
(`data_layer.live_data.market_calendar.is_weekend`, TASK-ARCH-101 Part 2) -- so
the projection's session view agrees with the canonical live-stream
weekend/pause behaviour. Re-pointed off the now-DEPRECATED
`stream.stream_mode` (TASK-ARCH-101 PART-03, Owner-approved L1
migration). It performs NO session classification of its own.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from data_layer.live_data.market_calendar import is_weekend


@dataclass(frozen=True)
class SessionState:
    """
    current_session: context's own Session label (e.g. "LONDON",
        "NEW_YORK", "ASIA") or None.
    is_weekend: from stream.stream_mode.is_weekend -- the same clock the
        stream layer pauses on, so "OFF_SESSION"/"WEEKEND_WAIT" reads
        consistently across layers.
    """
    current_session: Optional[str] = None
    is_weekend: bool = False

    @classmethod
    def from_context(cls, context_schema, now: Optional[datetime] = None) -> "SessionState":
        """
        Project from an already-built context.snapshot.ContextSnapshotSchema
        .session plus the shared weekend clock (`now` optional, defaults
        to real UTC -- injectable for replay/tests). Never recomputes a
        session; empty context -> current_session None.
        """
        info = getattr(context_schema, "session", None)
        current = getattr(info, "current_session", None) if info else None
        return cls(current_session=current, is_weekend=is_weekend(now))

    @property
    def label(self) -> str:
        """A single human label: the weekend wins over any stale session tag, else the session, else OFF_SESSION."""
        if self.is_weekend:
            return "WEEKEND_WAIT"
        return self.current_session or "OFF_SESSION"
