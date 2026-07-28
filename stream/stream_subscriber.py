"""
Stream Layer — Stream Subscriber (TASK-CORE-004).

StreamSubscriber is the single contract every stream consumer
implements to receive events. Chart, market, database, context, and
Telegram consumers all connect through THIS interface -- the stream
layer never knows their concrete types, only that each exposes
`name` and `on_event()`.

A subscriber MUST NOT put trading logic here that belongs to another
layer -- on_event() is a delivery hook. What a subscriber does with an
event (render a chart, write a row, forward to Telegram) is that
consumer's own concern in its own layer; the stream layer only calls
the hook. `CallbackSubscriber` is a tiny built-in adapter so a plain
function can subscribe without a class.
"""

from abc import ABC, abstractmethod
from typing import Callable

from stream.stream_event import StreamEvent


class StreamSubscriber(ABC):
    """
    The consumer contract. `name` is a short, stable identifier (for
    the router's registry and status views); `on_event()` receives one
    validated StreamEvent. Implementations should not raise -- the
    router isolates failures, but a well-behaved subscriber handles its
    own errors.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """A short, stable identifier, e.g. "chart", "market", "telegram"."""
        raise NotImplementedError

    @abstractmethod
    def on_event(self, event: StreamEvent) -> None:
        """Handle one validated StreamEvent. Delivery hook only -- no cross-layer business logic."""
        raise NotImplementedError


class CallbackSubscriber(StreamSubscriber):
    """Adapter: wrap a plain `callable(event)` as a StreamSubscriber, so a consumer can subscribe without defining a class."""

    def __init__(self, name: str, callback: Callable[[StreamEvent], None]) -> None:
        self._name = name
        self._callback = callback

    @property
    def name(self) -> str:
        return self._name

    def on_event(self, event: StreamEvent) -> None:
        self._callback(event)
