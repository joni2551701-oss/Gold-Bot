"""Async dispatch tests for the Event Bus (module 7)."""

import threading

from data.events.event_bus import EventBus
from data.events.event_model import EventType
from _efakes import make_event


def test_async_delivery():
    bus = EventBus()
    delivered = []
    done = threading.Event()

    def handler(e):
        delivered.append(e.type)
        if len(delivered) == 3:
            done.set()

    bus.subscribe("*", handler)
    bus.start()
    try:
        for _ in range(3):
            bus.publish_async(make_event(EventType.MARKET_CANDLE_UPDATED))
        bus.flush()
        done.wait(timeout=2.0)
    finally:
        bus.stop()
    assert len(delivered) == 3
    assert bus.metrics().published == 3


def test_async_falls_back_to_sync_without_worker():
    bus = EventBus()
    got = []
    bus.subscribe("*", lambda e: got.append(e))
    bus.publish_async(make_event())     # no worker started -> sync
    assert len(got) == 1
