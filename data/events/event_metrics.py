"""
EventMetrics -- counters for the Event Bus (v1.1 Phase 1, module 7).
Monitoring-friendly. This module never imports from any layer above data/.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Dict

from data.events.event_model import EventType


class EventMetrics:
    def __init__(self):
        self.published = 0
        self.delivered = 0
        self.dropped = 0
        self.handler_errors = 0
        self.rejected = 0
        self.queue_depth = 0
        self._per_type: Dict[str, int] = defaultdict(int)

    def record_published(self, event_type: EventType) -> None:
        self.published += 1
        self._per_type[event_type.value] += 1

    def as_dict(self) -> dict:
        return {
            "published": self.published,
            "delivered": self.delivered,
            "dropped": self.dropped,
            "handler_errors": self.handler_errors,
            "rejected": self.rejected,
            "queue_depth": self.queue_depth,
            "per_type": dict(self._per_type),
        }
