"""Unit tests for data/events/event_bus.py sync dispatch (module 7)."""

import pytest

from data.events.event_bus import EventBus
from data.events.event_model import (
    EventType, EventPriority, EventValidationError, Event,
)
from data.events.event_bridge import EventBridge
from data.events.replay_log import RingBufferPolicy
from _efakes import make_event, ts


def test_typed_routing_and_unsubscribe():
    bus = EventBus()
    got = []
    h = bus.subscribe(EventType.MARKET_CANDLE_CLOSED, lambda e: got.append(e))
    bus.subscribe(EventType.MARKET_CANDLE_OPENED, lambda e: got.append("open"))
    bus.publish(make_event(EventType.MARKET_CANDLE_CLOSED))
    assert len(got) == 1
    bus.unsubscribe(h)
    bus.publish(make_event(EventType.MARKET_CANDLE_CLOSED))
    assert len(got) == 1        # no longer delivered


def test_namespace_wildcard_amendment6():
    bus = EventBus()
    seen = []
    bus.subscribe("MARKET", lambda e: seen.append(e.type))
    bus.publish(make_event(EventType.MARKET_CANDLE_OPENED))
    bus.publish(make_event(EventType.MARKET_CANDLE_CLOSED))
    bus.publish(make_event(EventType.BOOTSTRAP_STARTED))     # different ns
    assert seen == [EventType.MARKET_CANDLE_OPENED, EventType.MARKET_CANDLE_CLOSED]


def test_full_wildcard_amendment4():
    bus = EventBus()
    seen = []
    bus.subscribe("*", lambda e: seen.append(e.type))
    bus.publish(make_event(EventType.MARKET_CANDLE_OPENED))
    bus.publish(make_event(EventType.BOOTSTRAP_STARTED))
    assert len(seen) == 2


def test_priority_order():
    bus = EventBus()
    order = []
    bus.subscribe("*", lambda e: order.append("low"), priority=EventPriority.LOW)
    bus.subscribe("*", lambda e: order.append("high"), priority=EventPriority.HIGH)
    bus.subscribe("*", lambda e: order.append("normal"),
                  priority=EventPriority.NORMAL)
    bus.publish(make_event())
    assert order == ["high", "normal", "low"]


def test_handler_isolation():
    bus = EventBus()
    seen = []

    def boom(e):
        raise RuntimeError("boom")

    bus.subscribe("*", boom)
    bus.subscribe("*", lambda e: seen.append(e))
    bus.publish(make_event())           # must not raise
    assert len(seen) == 1
    assert bus.metrics().handler_errors == 1


def test_validation_rejects_bad_event():
    bus = EventBus()
    bad = Event(type=EventType.MARKET_CANDLE_CLOSED, event_id="", timestamp=ts(0))
    with pytest.raises(EventValidationError):
        bus.publish(bad)
    assert bus.metrics().rejected == 1


def test_metrics_counts():
    bus = EventBus()
    bus.subscribe("*", lambda e: None)
    bus.publish(make_event())
    bus.publish(make_event(EventType.BOOTSTRAP_STARTED))
    m = bus.metrics().as_dict()
    assert m["published"] == 2
    assert m["delivered"] == 2
    assert m["per_type"]["MARKET.CANDLE_CLOSED"] == 1


def test_bridge_receives_events():
    forwarded = []

    class _Bridge(EventBridge):
        def forward(self, event):
            forwarded.append(event.type)

    bus = EventBus()
    bus.attach_bridge(_Bridge())
    bus.publish(make_event(EventType.MARKET_CANDLE_OPENED))
    assert forwarded == [EventType.MARKET_CANDLE_OPENED]


def test_replay_log_records_and_replays():
    bus = EventBus()
    bus.enable_replay(RingBufferPolicy(capacity=10))
    bus.publish(make_event(EventType.MARKET_CANDLE_OPENED))
    bus.publish(make_event(EventType.MARKET_CANDLE_CLOSED))
    # late subscriber replays history
    late = []
    assert bus.replay_log.replay_to(lambda e: late.append(e.type)) == 2
    assert late == [EventType.MARKET_CANDLE_OPENED, EventType.MARKET_CANDLE_CLOSED]
