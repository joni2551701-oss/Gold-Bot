"""
Stream Layer — Stream Router (TASK-CORE-004).

StreamRouter decides which subscribers a StreamEvent reaches and
delivers it to them. Routing destinations are the consumers named in
the brief -- market, current price, database writer, future chart,
context consumer, Telegram live viewer -- each attached as a
StreamSubscriber.

The router may SPLIT/fan-out an event, but it performs NO business
logic (CLAUDE.md: "Router data'ni bo'lishi mumkin, lekin business
logic qilmaydi"). It does not compute signals, transform OHLC, or
decide trades -- it only dispatches.

Fault isolation: a subscriber that raises must not stop the others
from receiving the event. The router catches per-subscriber exceptions
and records the failing subscriber's name in the RouteResult, so one
broken consumer never takes the stream down.
"""

from dataclasses import dataclass, field
from typing import Dict, List

from data_layer.live_data.stream.stream_event import StreamEvent
from data_layer.live_data.stream.stream_subscriber import StreamSubscriber


@dataclass
class RouteResult:
    """Outcome of routing one event: which subscribers were delivered to, and which raised (by name)."""
    delivered: List[str] = field(default_factory=list)
    failed: List[str] = field(default_factory=list)


class StreamRouter:
    """Keeps a name-keyed set of subscribers; route() fan-outs one event to all of them with per-subscriber fault isolation. Never raises."""

    def __init__(self) -> None:
        self._subscribers: Dict[str, StreamSubscriber] = {}

    def subscribe(self, subscriber: StreamSubscriber) -> None:
        """Register a subscriber (keyed by its own .name -- re-subscribing the same name replaces it, last write wins)."""
        self._subscribers[subscriber.name] = subscriber

    def unsubscribe(self, name: str) -> None:
        """Remove a subscriber by name. No-op if absent -- never raises."""
        self._subscribers.pop(name, None)

    def subscribers(self) -> List[str]:
        """Names of all currently-registered subscribers."""
        return list(self._subscribers.keys())

    def route(self, event: StreamEvent) -> RouteResult:
        """
        Deliver `event` to every registered subscriber. Returns a
        RouteResult listing who received it and who raised. A raising
        subscriber is caught and recorded, never propagated -- the
        remaining subscribers still receive the event.
        """
        result = RouteResult()
        for name, subscriber in list(self._subscribers.items()):
            try:
                subscriber.on_event(event)
                result.delivered.append(name)
            except Exception:
                result.failed.append(name)
        return result
