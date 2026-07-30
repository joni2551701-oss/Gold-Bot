"""
Stream Layer — Stream State (TASK-CORE-004).

StreamState holds the LAST-seen runtime state of the stream -- a
volatile snapshot, not history. It answers "where did the stream leave
off?" so a restart or a status check has a single place to read from.

Held (exactly TASK-CORE-004's list):
    last_price, last_event (the last candle), last_timestamp,
    last_provider, last_mode.

Explicitly NOT a history store (that is data/'s responsibility) and
NOT a signal/decision computer. No secret is read or logged.
"""

from datetime import datetime
from typing import Optional

from stream.stream_event import StreamEvent
from stream.stream_mode import StreamMode


class StreamState:
    """Single-slot runtime state. update() overwrites; the getters read the latest. Never raises."""

    def __init__(self) -> None:
        self._last_event: Optional[StreamEvent] = None
        self._last_price: Optional[float] = None
        self._last_timestamp: Optional[datetime] = None
        self._last_provider: Optional[str] = None
        self._last_mode: StreamMode = StreamMode.ACTIVE

    def update(self, event: Optional[StreamEvent] = None, mode: Optional[StreamMode] = None) -> None:
        """
        Record the latest event and/or mode. Both are optional so a
        mode change with no new data (e.g. entering WEEKEND_WAIT) still
        updates state. Overwrites -- no history.
        """
        if event is not None:
            self._last_event = event
            self._last_price = event.close
            self._last_timestamp = event.timestamp
            self._last_provider = event.provider
        if mode is not None:
            self._last_mode = mode

    @property
    def last_event(self) -> Optional[StreamEvent]:
        return self._last_event

    @property
    def last_price(self) -> Optional[float]:
        return self._last_price

    @property
    def last_timestamp(self) -> Optional[datetime]:
        return self._last_timestamp

    @property
    def last_provider(self) -> Optional[str]:
        return self._last_provider

    @property
    def last_mode(self) -> StreamMode:
        return self._last_mode

    def to_dict(self) -> dict:
        """A serializable snapshot of the current runtime state (for a status view/monitoring). No secret present."""
        return {
            "last_price": self._last_price,
            "last_timestamp": self._last_timestamp.isoformat() if self._last_timestamp else None,
            "last_provider": self._last_provider,
            "last_mode": self._last_mode.value,
            "has_event": self._last_event is not None,
        }
