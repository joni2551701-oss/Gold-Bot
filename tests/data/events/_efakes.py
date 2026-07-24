"""Shared helpers for Event Bus tests (module 7)."""

import itertools
from datetime import datetime, timezone, timedelta

from data.events.event_model import Event, EventType, EventPriority

_seq = itertools.count(1)


def ts(i=0):
    return datetime(2026, 7, 24, tzinfo=timezone.utc) + timedelta(seconds=i)


def make_event(event_type=EventType.MARKET_CANDLE_CLOSED, payload="x",
               asset="XAUUSD", priority=EventPriority.NORMAL,
               when=None, correlation_id="c1"):
    return Event(
        type=event_type, payload=payload, asset=asset, priority=priority,
        event_id=f"e{next(_seq)}", timestamp=when or ts(0),
        source="test", correlation_id=correlation_id)
