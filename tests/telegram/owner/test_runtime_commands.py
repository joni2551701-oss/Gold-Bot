"""Phase 61.6 TASK 6 — Owner Runtime Dashboard (/runtime, /runtime_events, /runtime_metrics). Extended Phase 61.7 TASK 7/8 — /runtime_status, /runtime_check."""

from ai.audit.provider_stats import RuntimeMetricsCollector
from ai.providers.circuit_breaker import CircuitBreakerConfig, ProviderCircuitBreaker
from ai.providers.provider_health import ProviderHealthTracker
from ai.runtime.event_bus import EventBus, EventType, RuntimeEvent
from ai.runtime.runtime_manager import RuntimeManager
from ai.runtime.runtime_profiles import PRODUCTION_PROFILE
from ai.runtime.runtime_state import RuntimeState
from ai.runtime.self_check import CheckStatus, RuntimeSelfCheckReport, SelfCheckResult
from telegram.owner.runtime_commands import runtime_check, runtime_events, runtime_full_status, runtime_metrics, runtime_status


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


class _FakeProviderManager:
    def __init__(self, names):
        self._names = names

    def list_providers(self):
        return list(self._names)


def test_runtime_full_status_with_no_injections_reports_defaults():
    result = runtime_full_status()

    assert result.success is True
    assert "State:" in result.message
    assert RuntimeState.READY.value in result.message
    assert "Profile:\nNone (default)" in result.message
    assert "Providers:" in result.message


def test_runtime_full_status_reflects_an_injected_profile():
    result = runtime_full_status(runtime_profile=PRODUCTION_PROFILE)
    assert "Profile:\nproduction" in result.message


def test_runtime_full_status_lists_provider_circuit_states():
    health_tracker = ProviderHealthTracker()
    breaker = ProviderCircuitBreaker(health_tracker=health_tracker, config=CircuitBreakerConfig(failure_threshold=2))
    for _ in range(2):
        breaker.record_failure("gemini")
    provider_manager = _FakeProviderManager(["gemini", "openai"])

    result = runtime_full_status(provider_manager=provider_manager, circuit_breaker=breaker, health_tracker=health_tracker)

    assert "Gemini" in result.message and "OPEN" in result.message
    assert "Openai" in result.message and "CLOSED" in result.message


def test_runtime_full_status_reflects_metrics_from_an_injected_collector():
    bus = EventBus()
    collector = RuntimeMetricsCollector(bus)
    bus.publish(RuntimeEvent(event_type=EventType.VALIDATION_FAILED))

    result = runtime_full_status(metrics_collector=collector, event_bus=bus)

    assert "Validation Failures:\n1" in result.message
    assert "Recent Events:\n1" in result.message


def test_runtime_check_with_no_injected_report_runs_a_real_self_check():
    result = runtime_check()

    assert result.success is True
    assert "Overall:" in result.message
    for name in ("Provider", "Runtime", "Validation", "Cache", "Audit", "EventBus", "CircuitBreaker"):
        assert name in result.message


def test_runtime_check_reflects_an_injected_report():
    report = RuntimeSelfCheckReport(results=[
        SelfCheckResult("Provider", CheckStatus.FAILED, "no providers registered"),
    ])

    result = runtime_check(report=report)

    assert "✗ Provider: FAILED" in result.message
    assert "Overall:\nFAILED" in result.message
