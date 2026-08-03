"""Phase 61.6 TASK 3 — Provider Circuit Breaker. No duplicate provider state -- every transition writes into the existing ProviderHealthTracker (Rule 4)."""

from datetime import datetime, timedelta, timezone

from ai_layer.ai_engine.providers.circuit_breaker import CircuitBreakerConfig, CircuitState, ProviderCircuitBreaker
from ai_layer.ai_engine.providers.provider_health import ProviderHealthTracker
from ai_layer.ai_engine.providers.provider_status import HealthStatus
from ai_layer.ai_service.event_bus import EventBus, EventType


def test_fresh_provider_starts_closed():
    breaker = ProviderCircuitBreaker()
    assert breaker.state_of("gemini") == CircuitState.CLOSED
    assert breaker.allow_request("gemini") is True


def test_closed_stays_closed_below_the_failure_threshold():
    breaker = ProviderCircuitBreaker(config=CircuitBreakerConfig(failure_threshold=5))
    for _ in range(4):
        breaker.record_failure("gemini")
    assert breaker.state_of("gemini") == CircuitState.CLOSED


def test_reaching_the_failure_threshold_opens_the_circuit():
    breaker = ProviderCircuitBreaker(config=CircuitBreakerConfig(failure_threshold=5))
    for _ in range(5):
        breaker.record_failure("gemini")
    assert breaker.state_of("gemini") == CircuitState.OPEN
    assert breaker.allow_request("gemini") is False


def test_opening_the_circuit_writes_offline_into_the_shared_health_tracker():
    health_tracker = ProviderHealthTracker()
    breaker = ProviderCircuitBreaker(health_tracker=health_tracker, config=CircuitBreakerConfig(failure_threshold=5))

    for _ in range(5):
        breaker.record_failure("gemini")

    assert health_tracker.status_of("gemini") == HealthStatus.OFFLINE
    assert health_tracker.is_available("gemini") is False


def test_open_circuit_transitions_to_half_open_after_the_recovery_timeout():
    health_tracker = ProviderHealthTracker()
    breaker = ProviderCircuitBreaker(
        health_tracker=health_tracker,
        config=CircuitBreakerConfig(failure_threshold=5, recovery_timeout_seconds=30),
    )
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    for _ in range(5):
        breaker.record_failure("gemini", now=start)

    allowed = breaker.allow_request("gemini", now=start + timedelta(seconds=31))

    assert allowed is True
    assert breaker.state_of("gemini") == CircuitState.HALF_OPEN
    assert health_tracker.status_of("gemini") == HealthStatus.DEGRADED
    assert health_tracker.is_available("gemini") is True  # DEGRADED is in AVAILABLE_STATUSES -- the one probe request


def test_open_circuit_still_denies_before_the_recovery_timeout():
    breaker = ProviderCircuitBreaker(config=CircuitBreakerConfig(failure_threshold=5, recovery_timeout_seconds=30))
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    for _ in range(5):
        breaker.record_failure("gemini", now=start)

    assert breaker.allow_request("gemini", now=start + timedelta(seconds=10)) is False
    assert breaker.state_of("gemini") == CircuitState.OPEN


def test_half_open_probe_success_closes_the_circuit_and_reports_online():
    health_tracker = ProviderHealthTracker()
    breaker = ProviderCircuitBreaker(
        health_tracker=health_tracker,
        config=CircuitBreakerConfig(failure_threshold=5, recovery_timeout_seconds=30),
    )
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    for _ in range(5):
        breaker.record_failure("gemini", now=start)
    breaker.allow_request("gemini", now=start + timedelta(seconds=31))

    breaker.record_success("gemini")

    assert breaker.state_of("gemini") == CircuitState.CLOSED
    assert health_tracker.status_of("gemini") == HealthStatus.ONLINE
    assert breaker.allow_request("gemini") is True


def test_half_open_probe_failure_reopens_the_circuit():
    health_tracker = ProviderHealthTracker()
    breaker = ProviderCircuitBreaker(
        health_tracker=health_tracker,
        config=CircuitBreakerConfig(failure_threshold=5, recovery_timeout_seconds=30),
    )
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    for _ in range(5):
        breaker.record_failure("gemini", now=start)
    breaker.allow_request("gemini", now=start + timedelta(seconds=31))

    breaker.record_failure("gemini", now=start + timedelta(seconds=31))

    assert breaker.state_of("gemini") == CircuitState.OPEN
    assert health_tracker.status_of("gemini") == HealthStatus.OFFLINE


def test_success_while_closed_resets_the_failure_count_never_raises():
    breaker = ProviderCircuitBreaker(config=CircuitBreakerConfig(failure_threshold=5))
    breaker.record_failure("gemini")
    breaker.record_failure("gemini")
    breaker.record_success("gemini")
    for _ in range(4):
        breaker.record_failure("gemini")
    assert breaker.state_of("gemini") == CircuitState.CLOSED  # only 4 since the reset


def test_breaker_tracks_multiple_providers_independently():
    breaker = ProviderCircuitBreaker(config=CircuitBreakerConfig(failure_threshold=2))
    breaker.record_failure("gemini")
    breaker.record_failure("gemini")
    assert breaker.state_of("gemini") == CircuitState.OPEN
    assert breaker.state_of("claude") == CircuitState.CLOSED


def test_opening_the_circuit_publishes_provider_failed_with_circuit_state_open():
    bus = EventBus()
    breaker = ProviderCircuitBreaker(event_bus=bus, config=CircuitBreakerConfig(failure_threshold=5))

    for _ in range(5):
        breaker.record_failure("gemini")

    failed = bus.history(EventType.PROVIDER_FAILED)
    assert len(failed) == 1
    assert failed[0].payload["provider_name"] == "gemini"
    assert failed[0].payload["circuit_state"] == "OPEN"


def test_recovering_from_half_open_publishes_provider_recovered():
    bus = EventBus()
    breaker = ProviderCircuitBreaker(event_bus=bus, config=CircuitBreakerConfig(failure_threshold=5, recovery_timeout_seconds=30))
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    for _ in range(5):
        breaker.record_failure("gemini", now=start)
    breaker.allow_request("gemini", now=start + timedelta(seconds=31))

    breaker.record_success("gemini")

    recovered = bus.history(EventType.PROVIDER_RECOVERED)
    assert len(recovered) == 1
    assert recovered[0].payload["provider_name"] == "gemini"
    assert recovered[0].payload["circuit_state"] == "CLOSED"


def test_success_while_closed_never_publishes_provider_recovered():
    bus = EventBus()
    breaker = ProviderCircuitBreaker(event_bus=bus)

    breaker.record_success("gemini")

    assert bus.history(EventType.PROVIDER_RECOVERED) == []


def test_no_injected_event_bus_never_raises_on_open_or_recover():
    breaker = ProviderCircuitBreaker(config=CircuitBreakerConfig(failure_threshold=2, recovery_timeout_seconds=1))
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    breaker.record_failure("gemini", now=start)
    breaker.record_failure("gemini", now=start)
    breaker.allow_request("gemini", now=start + timedelta(seconds=2))
    breaker.record_success("gemini")


def test_router_only_uses_healthy_providers_because_breaker_writes_into_the_same_tracker():
    """No change to ai/router/router.py is needed -- confirmed here directly against the real AIRouter/ProviderManager, not a fake."""
    from ai_layer.ai_engine.capabilities.capability import Capability
    from ai_layer.ai_engine.providers.provider_manager import ProviderManager
    from ai_layer.ai_coordinator.router import AIRouter

    health_tracker = ProviderHealthTracker()
    breaker = ProviderCircuitBreaker(health_tracker=health_tracker, config=CircuitBreakerConfig(failure_threshold=2))
    provider_manager = ProviderManager()
    router = AIRouter(provider_manager, health_tracker=health_tracker)

    for _ in range(2):
        breaker.record_failure("gemini")

    result = router.route(Capability.EXPLANATION)

    assert result.provider_name != "gemini"
