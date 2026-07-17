"""Phase 61.6 TASK 6 — Owner Runtime Dashboard (/runtime, /runtime_events, /runtime_metrics)."""

from ai.audit.provider_stats import RuntimeMetricsCollector
from ai.runtime.event_bus import EventBus, EventType, RuntimeEvent
from ai.runtime.runtime_manager import RuntimeManager
from ai.runtime.runtime_state import RuntimeState
from telegram.owner.runtime_commands import runtime_events, runtime_metrics, runtime_status


def test_runtime_status_with_no_injected_manager_reports_the_documented_default():
    result = runtime_status()

    assert result.success is True
    assert "State:" in result.message
    assert RuntimeState.READY.value in result.message
    assert "Healthy:" in result.message
    assert "🟢 Yes" in result.message


def test_runtime_status_reflects_an_injected_manager():
    manager = RuntimeManager(initial_state=RuntimeState.DEGRADED)

    result = runtime_status(runtime_manager=manager)

    assert RuntimeState.DEGRADED.value in result.message


def test_runtime_status_reflects_unhealthy_state():
    manager = RuntimeManager(initial_state=RuntimeState.FAILED)

    result = runtime_status(runtime_manager=manager)

    assert "🔴 No" in result.message


def test_runtime_status_counts_recorded_transitions():
    manager = RuntimeManager()
    manager.transition(RuntimeState.BUSY, reason="processing")
    manager.transition(RuntimeState.READY, reason="done")

    result = runtime_status(runtime_manager=manager)

    assert "Transitions Recorded:\n3" in result.message  # constructed + 2 transitions


def test_runtime_events_with_no_injected_bus_reports_no_events():
    result = runtime_events()

    assert result.success is True
    assert "No events recorded." in result.message


def test_runtime_events_lists_published_events_newest_first():
    bus = EventBus()
    bus.publish(RuntimeEvent(event_type=EventType.CACHE_HIT, payload={"provider_name": "gemini"}))
    bus.publish(RuntimeEvent(event_type=EventType.CACHE_MISS, payload={"provider_name": "claude"}))

    result = runtime_events(event_bus=bus)

    hit_index = result.message.index("CacheHit")
    miss_index = result.message.index("CacheMiss")
    assert miss_index < hit_index  # newest (CacheMiss) first


def test_runtime_events_respects_limit():
    bus = EventBus()
    for _ in range(5):
        bus.publish(RuntimeEvent(event_type=EventType.RUNTIME_STARTED))

    result = runtime_events(event_bus=bus, limit=2)

    assert result.message.count("RuntimeStarted") == 2


def test_runtime_metrics_with_no_injected_collector_reports_zero_counts():
    result = runtime_metrics()

    assert result.success is True
    assert "Cache Hits:\n0" in result.message
    assert "Cache Misses:\n0" in result.message
    assert "Retries:\n0" in result.message
    assert "Failover Count:\n0" in result.message


def test_runtime_metrics_reflects_an_injected_collector_with_accumulated_counts():
    bus = EventBus()
    collector = RuntimeMetricsCollector(bus)
    bus.publish(RuntimeEvent(event_type=EventType.CACHE_HIT))
    bus.publish(RuntimeEvent(event_type=EventType.CACHE_HIT))
    bus.publish(RuntimeEvent(event_type=EventType.CACHE_MISS))
    bus.publish(RuntimeEvent(event_type=EventType.PROVIDER_CHANGED))

    result = runtime_metrics(collector=collector)

    assert "Cache Hits:\n2" in result.message
    assert "Cache Misses:\n1" in result.message
    assert "Failover Count:\n1" in result.message
    assert "Cache Hit Rate:\n67%" in result.message


def test_runtime_metrics_attaches_a_fresh_collector_to_an_injected_event_bus():
    bus = EventBus()
    collector = RuntimeMetricsCollector(bus)  # pre-subscribed, simulating a live wiring
    bus.publish(RuntimeEvent(event_type=EventType.VALIDATION_FAILED))

    result = runtime_metrics(collector=collector)

    assert "Validation Failures:\n1" in result.message
