"""
Market Layer — Session State projection (TASK-CORE-005).

SessionState is a READ-ONLY projection combining the trading session
context/ already classified (context.session -> ContextSnapshotSchema.
session.current_session) with stream/'s weekend clock
(stream.stream_mode.is_weekend) -- so the market façade's session view
agrees with the stream layer's weekend/pause behaviour (Director:
"stream/ dagi weekend logic bilan mos ishlasin"). It performs NO
session classification of its own.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from stream.stream_mode import is_weekend


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
