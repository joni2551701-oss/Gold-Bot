"""Chart Service Foundation — chart events (FLOW-016).

Events are pure notifications: ChartRequested, ChartCreated,
ChartUpdated, ChartFailed. They carry a request hash and an optional
payload — they never call the Renderer, Cache, Market Memory or DB.
Canonical home: Chart_API is the Public API / Event API / Plugin API
gateway, so the Event API lives here. The recorder is an in-memory sink
the Service emits through; the Platform may subscribe later without
changing this contract.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ChartEvent:
    """A single chart-lifecycle event."""

    name: str
    request_hash: Optional[str] = None
    payload: dict = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


def chart_requested(request_hash: Optional[str] = None, **payload) -> ChartEvent:
    return ChartEvent(name="ChartRequested", request_hash=request_hash, payload=dict(payload))


def chart_created(request_hash: Optional[str] = None, **payload) -> ChartEvent:
    return ChartEvent(name="ChartCreated", request_hash=request_hash, payload=dict(payload))


def chart_updated(request_hash: Optional[str] = None, **payload) -> ChartEvent:
    return ChartEvent(name="ChartUpdated", request_hash=request_hash, payload=dict(payload))


def chart_failed(request_hash: Optional[str] = None, **payload) -> ChartEvent:
    return ChartEvent(name="ChartFailed", request_hash=request_hash, payload=dict(payload))


class ChartEventRecorder:
    """In-memory event sink. Emit-and-remember; no side effects."""

    def __init__(self) -> None:
        self._events: list = []

    def emit(self, event: ChartEvent) -> ChartEvent:
        self._events.append(event)
        return event

    @property
    def events(self) -> list:
        return list(self._events)

    def last(self) -> Optional[ChartEvent]:
        return self._events[-1] if self._events else None

    def clear(self) -> None:
        self._events.clear()

    def __len__(self) -> int:
        return len(self._events)
