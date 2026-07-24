"""
ReplaySession -- an isolated, bookmarkable replay session (module 8;
amendment 3 bookmarks). Each session has its own id, timeline, position
and state. This module never imports from any layer above data/.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional

from data.replay.replay_state import ReplayState


@dataclass
class ReplaySession:
    asset: str
    start: datetime
    end: datetime
    session_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    state: ReplayState = ReplayState.IDLE
    position: Optional[datetime] = None      # current virtual time
    speed: float = 1.0
    frame_index: int = 0
    _bookmarks: Dict[str, datetime] = field(default_factory=dict)

    def bookmark(self, name: str) -> datetime:
        """Save the current position under `name` (amendment 3)."""
        if self.position is None:
            raise ValueError("cannot bookmark before the session has a position")
        self._bookmarks[name] = self.position
        return self.position

    def restore(self, name: str) -> datetime:
        """Return the bookmarked position for `name` (raises if unknown)."""
        try:
            return self._bookmarks[name]
        except KeyError:
            raise KeyError(f"no bookmark named {name!r}")

    def bookmarks(self) -> Dict[str, datetime]:
        return dict(self._bookmarks)
