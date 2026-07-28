"""Phase 61.6 TASK 5 — Runtime Event Bus. In-memory pub/sub, no module calls another directly."""

from ai.event_bus import EventBus, EventType, RuntimeEvent


def test_publish_calls_the_subscribed_handler():
    bus = EventBus()
    received = []
    bus.subscribe(EventType.CACHE_HIT, lambda e: received.append(e))

    bus.publish(RuntimeEvent(event_type=EventType.CACHE_HIT, payload={"provider_name": "gemini"}))

    assert len(received) == 1
    assert received[0].payload["provider_name"] == "gemini"


def test_publish_never_calls_a_handler_subscribed_to_a_different_event_type():
    bus = EventBus()
    received = []
    bus.subscribe(EventType.CACHE_HIT, lambda e: received.append(e))

    bus.publish(RuntimeEvent(event_type=EventType.CACHE_MISS))

    assert received == []


def test_publish_with_no_subscribers_never_raises():
    bus = EventBus()
    bus.publish(RuntimeEvent(event_type=EventType.RUNTIME_STARTED))


def test_a_failing_subscriber_never_breaks_publish_or_other_subscribers():
    bus = EventBus()
    received = []

    def _bad_handler(event):
        raise RuntimeError("boom")

    bus.subscribe(EventType.PROVIDER_FAILED, _bad_handler)
    bus.subscribe(EventType.PROVIDER_FAILED, lambda e: received.append(e))

    bus.publish(RuntimeEvent(event_type=EventType.PROVIDER_FAILED))

    assert len(received) == 1


def test_multiple_subscribers_to_the_same_event_type_all_receive_it():
    bus = EventBus()
    received_a, received_b = [], []
    bus.subscribe(EventType.VALIDATION_FAILED, lambda e: received_a.append(e))
    bus.subscribe(EventType.VALIDATION_FAILED, lambda e: received_b.append(e))

    bus.publish(RuntimeEvent(event_type=EventType.VALIDATION_FAILED))

    assert len(received_a) == 1
    assert len(received_b) == 1


def test_history_returns_every_published_event_oldest_first():
    bus = EventBus()
    bus.publish(RuntimeEvent(event_type=EventType.RUNTIME_STARTED))
    bus.publish(RuntimeEvent(event_type=EventType.RUNTIME_STOPPED))

    history = bus.history()

    assert [e.event_type for e in history] == [EventType.RUNTIME_STARTED, EventType.RUNTIME_STOPPED]


def test_history_can_filter_by_event_type():
    bus = EventBus()
    bus.publish(RuntimeEvent(event_type=EventType.PROVIDER_CHANGED))
    bus.publish(RuntimeEvent(event_type=EventType.PROVIDER_RECOVERED))
    bus.publish(RuntimeEvent(event_type=EventType.PROVIDER_CHANGED))

    filtered = bus.history(EventType.PROVIDER_CHANGED)

    assert len(filtered) == 2
    assert all(e.event_type == EventType.PROVIDER_CHANGED for e in filtered)


def test_every_director_named_event_type_exists():
    expected = {
        "ProviderChanged", "ProviderFailed", "ProviderRecovered",
        "CacheHit", "CacheMiss", "ValidationFailed",
        "RuntimeStarted", "RuntimeStopped",
        "RuntimeFailed",  # Phase 61.6 TASK 7 addition -- see event_bus.py's own docstring
        "RequestStarted", "RequestCompleted",  # Phase 61.7 TASK 5 addition -- see event_bus.py's own docstring
        "RequestFailed", "RuntimeStateChanged", "RetryStarted", "RetryCompleted",  # Phase 61.7 TASK 7 (continuation) addition -- see event_bus.py's own docstring
    }
    actual = {member.value for member in EventType}
    assert actual == expected
