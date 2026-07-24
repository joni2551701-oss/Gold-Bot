"""
Event model for the GoldBot Event Bus (v1.1 Phase 1, module 7).

Typed, immutable, namespaced events with version (DD amendment 1),
correlation id (amendment 2) and minimal validation (amendment 3).

Namespaces (amendment 6): MARKET / BOOTSTRAP / SYSTEM / STREAM / MEMORY /
PLATFORM. Event values are "NAMESPACE.NAME" so 100+ event types stay
manageable and namespace-wildcard subscription is possible.

This module never imports from any layer above data/.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional

EVENT_SCHEMA_VERSION = 1


class EventPriority(Enum):
    HIGH = 0
    NORMAL = 1
    LOW = 2


class EventType(Enum):
    """Namespaced event types (amendment 6)."""
    # MARKET.*  (candle lifecycle, DD-028)
    MARKET_CANDLE_OPENED = "MARKET.CANDLE_OPENED"
    MARKET_CANDLE_UPDATED = "MARKET.CANDLE_UPDATED"
    MARKET_CANDLE_CLOSED = "MARKET.CANDLE_CLOSED"
    # BOOTSTRAP.*  (DD-066)
    BOOTSTRAP_STARTED = "BOOTSTRAP.STARTED"
    BOOTSTRAP_TIMEFRAME_COMPLETED = "BOOTSTRAP.TIMEFRAME_COMPLETED"
    BOOTSTRAP_PROGRESS_UPDATED = "BOOTSTRAP.PROGRESS_UPDATED"
    BOOTSTRAP_COMPLETED = "BOOTSTRAP.COMPLETED"
    BOOTSTRAP_FAILED = "BOOTSTRAP.FAILED"
    BOOTSTRAP_CANCELLED = "BOOTSTRAP.CANCELLED"
    # SYSTEM.*
    SYSTEM_READINESS_CHANGED = "SYSTEM.READINESS_CHANGED"
    # STREAM.*
    STREAM_CONNECTED = "STREAM.CONNECTED"
    STREAM_DISCONNECTED = "STREAM.DISCONNECTED"
    STREAM_STATE_CHANGED = "STREAM.STATE_CHANGED"
    # REPLAY.*  (module 8, DD amendment 2)
    REPLAY_STARTED = "REPLAY.STARTED"
    REPLAY_PAUSED = "REPLAY.PAUSED"
    REPLAY_RESUMED = "REPLAY.RESUMED"
    REPLAY_SEEKED = "REPLAY.SEEKED"
    REPLAY_SPEED_CHANGED = "REPLAY.SPEED_CHANGED"
    REPLAY_FINISHED = "REPLAY.FINISHED"
    REPLAY_LIVE_TRANSITION = "REPLAY.LIVE_TRANSITION"
    # SNAPSHOT.*  (module 9, amendment 6)
    SNAPSHOT_CREATED = "SNAPSHOT.CREATED"
    SNAPSHOT_VERIFIED = "SNAPSHOT.VERIFIED"
    SNAPSHOT_ARCHIVED = "SNAPSHOT.ARCHIVED"
    SNAPSHOT_DELETED = "SNAPSHOT.DELETED"
    SNAPSHOT_IMPORTED = "SNAPSHOT.IMPORTED"
    SNAPSHOT_EXPORTED = "SNAPSHOT.EXPORTED"
    SNAPSHOT_CLEANUP = "SNAPSHOT.CLEANUP"
    SNAPSHOT_CORRUPTED = "SNAPSHOT.CORRUPTED"

    @property
    def namespace(self) -> str:
        return self.value.split(".", 1)[0]


class EventValidationError(ValueError):
    """Raised when an event fails pre-publish validation (amendment 3)."""


@dataclass(frozen=True)
class Event:
    """An immutable, typed bus event."""
    type: EventType
    payload: Any = None
    asset: Optional[str] = None
    priority: EventPriority = EventPriority.NORMAL
    event_id: str = ""
    timestamp: Optional[datetime] = None
    source: str = ""
    correlation_id: Optional[str] = None          # amendment 2
    event_version: int = EVENT_SCHEMA_VERSION      # amendment 1
    metadata: dict = field(default_factory=dict)

    @property
    def namespace(self) -> str:
        return self.type.namespace


def validate_event(event: Event, require_payload: bool = False) -> None:
    """
    Minimal pre-publish validation (amendment 3): a malformed event never
    enters the bus. `require_payload` optionally rejects a None payload
    (some system/signal events legitimately carry no payload).
    """
    if not isinstance(event, Event):
        raise EventValidationError(f"not an Event: {event!r}")
    if not isinstance(event.type, EventType):
        raise EventValidationError("event.type must be an EventType")
    if not event.event_id:
        raise EventValidationError("event.event_id is required")
    if not isinstance(event.timestamp, datetime):
        raise EventValidationError("event.timestamp (datetime) is required")
    if event.timestamp.tzinfo is None:
        raise EventValidationError("event.timestamp must be timezone-aware (UTC)")
    if require_payload and event.payload is None:
        raise EventValidationError("event.payload must not be None")
    if not isinstance(event.event_version, int) or event.event_version < 1:
        raise EventValidationError("event.event_version must be a positive int")
