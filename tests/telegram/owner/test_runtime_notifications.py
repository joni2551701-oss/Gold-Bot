"""Phase 61.6 TASK 7 — Runtime Notification Layer. Owner-only alerts for Provider DOWN/RECOVERED, Runtime FAILED, High Cost, Cache Disabled."""

from ai_layer.ai_service.audit.provider_stats import ProviderStats
from ai_layer.ai_service.event_bus import EventBus, EventType, RuntimeEvent
from platform_layer.telegram.owner.runtime_notifications import (
    RuntimeNotifier,
    deliver_alerts,
    evaluate_cache_disabled,
    evaluate_high_cost,
)


def _stats(provider_name: str, total_cost: float) -> ProviderStats:
    return ProviderStats(
        provider_name=provider_name, total_calls=10, success_count=10,
        avg_latency_ms=100.0, total_tokens=1000, total_cost=total_cost,
    )


class _StubNotifier:
    def __init__(self, succeed: bool = True):
        self.succeed = succeed
        self.sent = []

    def send_message(self, message, chat_id=None):
        self.sent.append((message, chat_id))
        return self.succeed


def test_provider_failed_with_circuit_state_open_queues_a_provider_down_alert():
    bus = EventBus()
    notifier = RuntimeNotifier(bus)

    bus.publish(RuntimeEvent(event_type=EventType.PROVIDER_FAILED, payload={"provider_name": "gemini", "circuit_state": "OPEN"}))

    alerts = notifier.drain()
    assert len(alerts) == 1
    assert "DOWN" in alerts[0].title
    assert "gemini" in alerts[0].message


def test_plain_provider_failed_without_circuit_state_is_not_alert_worthy():
    bus = EventBus()
    notifier = RuntimeNotifier(bus)

    bus.publish(RuntimeEvent(event_type=EventType.PROVIDER_FAILED, payload={"provider_name": "gemini"}))

    assert notifier.drain() == []


def test_provider_recovered_queues_an_alert():
    bus = EventBus()
    notifier = RuntimeNotifier(bus)

    bus.publish(RuntimeEvent(event_type=EventType.PROVIDER_RECOVERED, payload={"provider_name": "claude", "circuit_state": "CLOSED"}))

    alerts = notifier.drain()
    assert len(alerts) == 1
    assert "RECOVERED" in alerts[0].title
    assert "claude" in alerts[0].message


def test_runtime_failed_queues_an_alert_with_the_reason():
    bus = EventBus()
    notifier = RuntimeNotifier(bus)

    bus.publish(RuntimeEvent(event_type=EventType.RUNTIME_FAILED, payload={"reason": "every provider unavailable"}))

    alerts = notifier.drain()
    assert len(alerts) == 1
    assert "FAILED" in alerts[0].title
    assert "every provider unavailable" in alerts[0].message


def test_drain_clears_the_queue_and_never_redelivers():
    bus = EventBus()
    notifier = RuntimeNotifier(bus)
    bus.publish(RuntimeEvent(event_type=EventType.RUNTIME_FAILED, payload={"reason": "x"}))

    first = notifier.drain()
    second = notifier.drain()

    assert len(first) == 1
    assert second == []


def test_unrelated_events_never_queue_an_alert():
    bus = EventBus()
    notifier = RuntimeNotifier(bus)

    bus.publish(RuntimeEvent(event_type=EventType.CACHE_HIT))
    bus.publish(RuntimeEvent(event_type=EventType.RUNTIME_STARTED))

    assert notifier.drain() == []


def test_evaluate_high_cost_flags_only_providers_over_threshold():
    stats = {"gemini": _stats("gemini", 12.40), "openai": _stats("openai", 3.00)}

    alerts = evaluate_high_cost(stats, threshold=10.0)

    assert len(alerts) == 1
    assert "gemini" in alerts[0].message.lower()


def test_evaluate_high_cost_empty_stats_returns_no_alerts():
    assert evaluate_high_cost({}, threshold=10.0) == []


def test_evaluate_cache_disabled_returns_none_when_enabled():
    assert evaluate_cache_disabled(cache_enabled=True) is None


def test_evaluate_cache_disabled_returns_an_alert_when_disabled():
    alert = evaluate_cache_disabled(cache_enabled=False)
    assert alert is not None
    assert "Cache Disabled" in alert.title


def test_deliver_alerts_with_no_alerts_returns_zero_and_never_calls_notifier():
    stub = _StubNotifier()
    assert deliver_alerts([], notifier=stub) == 0
    assert stub.sent == []


def test_deliver_alerts_sends_each_alert_with_an_explicit_chat_id():
    stub = _StubNotifier(succeed=True)
    alert = evaluate_cache_disabled(cache_enabled=False)

    delivered = deliver_alerts([alert], notifier=stub, chat_id="12345")

    assert delivered == 1
    assert stub.sent[0][1] == "12345"


def test_deliver_alerts_counts_only_successful_sends():
    stub = _StubNotifier(succeed=False)
    alert = evaluate_cache_disabled(cache_enabled=False)

    delivered = deliver_alerts([alert], notifier=stub, chat_id="12345")

    assert delivered == 0


def test_deliver_alerts_with_no_chat_id_and_no_owner_configured_delivers_nothing(monkeypatch):
    monkeypatch.setenv("TELEGRAM_OWNER_ID", "")
    stub = _StubNotifier(succeed=True)
    alert = evaluate_cache_disabled(cache_enabled=False)

    delivered = deliver_alerts([alert], notifier=stub)

    assert delivered == 0
    assert stub.sent == []
