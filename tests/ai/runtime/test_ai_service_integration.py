"""
Phase 61.7 — AI Platform Stabilization & Integration. End-to-end tests
driving a real AIService through RuntimeManager/CircuitBreaker/
RuntimeProfile/EventBus/RuntimeNotifier together -- not each piece in
isolation (already covered by tests/ai/runtime/test_runtime_lifecycle.py,
tests/ai/providers/test_provider_circuit_breaker.py,
tests/ai/runtime/test_runtime_profiles.py,
tests/telegram/owner/test_runtime_notifications.py). No real network
call anywhere -- every provider is faked.
"""

from ai.access.permissions import AIRole
from ai.capabilities.capability import Capability
from ai.providers.base_provider import ProviderResult
from ai.providers.circuit_breaker import CircuitBreakerConfig, CircuitState, ProviderCircuitBreaker
from ai.providers.provider_health import ProviderHealthTracker
from ai.providers.provider_manager import ProviderStatus
from ai.providers.runtime_errors import ProviderTimeoutError
from ai.runtime.ai_service import AIService
from ai.runtime.event_bus import EventBus, EventType
from ai.runtime.runtime_manager import RuntimeManager
from ai.runtime.runtime_profiles import DEVELOPMENT_PROFILE, PRODUCTION_PROFILE, TESTING_PROFILE
from ai.runtime.runtime_request import RuntimeRequest
from ai.runtime.runtime_state import RuntimeState
from ai.context.context_builder import build_ai_context
from ai.interfaces import MarketContext
from telegram.owner.runtime_notifications import RuntimeNotifier


class _FakeProvider:
    def __init__(self, name, behavior=None):
        self._name = name
        self._behavior = behavior or (lambda prompt: ProviderResult(content=f"[{name}] answer", metadata={}))

    @property
    def name(self):
        return self._name

    def chat(self, prompt):
        return self._behavior(prompt)

    def analyze(self, prompt):
        return self._behavior(prompt)

    def explain(self, prompt):
        return self._behavior(prompt)

    def vision(self, prompt, image_ref=None):
        return self._behavior(prompt)

    def image(self, prompt):
        return self._behavior(prompt)

    def voice(self, prompt):
        return self._behavior(prompt)


class _FakeProviderManager:
    def __init__(self, providers: dict):
        self._providers = providers

    def list_providers(self):
        return list(self._providers.keys())

    def get_provider(self, name):
        return self._providers.get(name)

    def status_of(self, name):
        return ProviderStatus.FALLBACK


def _context():
    return build_ai_context(market_context=MarketContext(symbol="XAUUSD", timeframe="M15", summary="uptrend"))


def _request(prompt="hi"):
    return RuntimeRequest(capability=Capability.CHAT, ai_context=_context(), role=AIRole.OWNER, prompt=prompt)


# ---------------------------------------------------------------------------
# TASK 2 — Runtime Manager gate
# ---------------------------------------------------------------------------

def test_unhealthy_runtime_rejects_before_touching_any_provider():
    provider_manager = _FakeProviderManager({"gemini": _FakeProvider("gemini")})
    runtime_manager = RuntimeManager(initial_state=RuntimeState.FAILED)
    service = AIService(provider_manager=provider_manager, runtime_manager=runtime_manager)

    response = service.ask(_request())

    assert response.accepted is False
    assert "runtime unavailable" in response.reason
    assert "FAILED" in response.reason


def test_degraded_runtime_still_serves_requests():
    provider_manager = _FakeProviderManager({"gemini": _FakeProvider("gemini")})
    runtime_manager = RuntimeManager(initial_state=RuntimeState.DEGRADED)
    service = AIService(provider_manager=provider_manager, runtime_manager=runtime_manager)

    response = service.ask(_request())

    assert response.accepted is True


# ---------------------------------------------------------------------------
# TASK 3 — Circuit Breaker integration (real, across multiple .ask() calls
# on the SAME AIService/breaker instance -- the only way the breaker's
# consecutive-failure count means anything).
# ---------------------------------------------------------------------------

def test_five_consecutive_failures_trip_the_circuit_and_it_stops_being_offered():
    def _fail(prompt):
        raise ProviderTimeoutError("gemini", "timed out")

    provider_manager = _FakeProviderManager({
        "gemini": _FakeProvider("gemini", behavior=_fail),
        "openai": _FakeProvider("openai"),
    })
    health_tracker = ProviderHealthTracker()
    breaker = ProviderCircuitBreaker(health_tracker=health_tracker, config=CircuitBreakerConfig(failure_threshold=5))
    service = AIService(provider_manager=provider_manager, health_tracker=health_tracker, circuit_breaker=breaker)

    for _ in range(5):
        response = service.ask(_request())
        assert response.accepted is True
        assert response.provider_name == "openai"  # gemini always fails over to openai

    assert breaker.state_of("gemini") == CircuitState.OPEN
    assert health_tracker.is_available("gemini") is False


def test_circuit_recovers_to_half_open_and_closes_on_a_real_success(monkeypatch):
    import ai.providers.circuit_breaker as circuit_breaker_module
    from datetime import datetime, timedelta, timezone

    calls = {"count": 0}

    def _fail_then_succeed(prompt):
        calls["count"] += 1
        if calls["count"] <= 5:
            raise ProviderTimeoutError("gemini", "timed out")
        return ProviderResult(content="[gemini] recovered", metadata={})

    provider_manager = _FakeProviderManager({"gemini": _FakeProvider("gemini", behavior=_fail_then_succeed)})
    health_tracker = ProviderHealthTracker()
    breaker = ProviderCircuitBreaker(health_tracker=health_tracker, config=CircuitBreakerConfig(failure_threshold=5, recovery_timeout_seconds=30))
    service = AIService(provider_manager=provider_manager, health_tracker=health_tracker, circuit_breaker=breaker)

    for _ in range(5):
        service.ask(_request())
    assert breaker.state_of("gemini") == CircuitState.OPEN

    future = datetime.now(timezone.utc) + timedelta(seconds=31)

    class _FixedDatetime(datetime):
        @classmethod
        def now(cls, tz=None):
            return future

    monkeypatch.setattr(circuit_breaker_module, "datetime", _FixedDatetime)

    response = service.ask(_request())

    assert response.accepted is True
    assert breaker.state_of("gemini") == CircuitState.CLOSED


# ---------------------------------------------------------------------------
# TASK 4 — Runtime Profile integration
# ---------------------------------------------------------------------------

def test_production_profile_rejects_a_response_missing_confidence_metadata():
    provider_manager = _FakeProviderManager({"gemini": _FakeProvider("gemini")})  # no "confidence" in metadata
    service = AIService(provider_manager=provider_manager, runtime_profile=PRODUCTION_PROFILE)

    response = service.ask(_request())

    assert response.accepted is False
    assert "validation" in response.reason


def test_no_profile_accepts_the_same_response_production_would_reject():
    provider_manager = _FakeProviderManager({"gemini": _FakeProvider("gemini")})
    service = AIService(provider_manager=provider_manager)

    response = service.ask(_request())

    assert response.accepted is True


def test_testing_profile_disables_caching_across_two_identical_calls():
    call_count = {"n": 0}

    def _counting(prompt):
        call_count["n"] += 1
        return ProviderResult(content="answer", metadata={})

    provider_manager = _FakeProviderManager({"gemini": _FakeProvider("gemini", behavior=_counting)})
    service = AIService(provider_manager=provider_manager, runtime_profile=TESTING_PROFILE)

    service.ask(_request())
    service.ask(_request())

    assert call_count["n"] == 2  # a cache hit would have kept this at 1


def test_production_profile_max_retries_limits_attempts_even_with_more_providers_registered():
    def _fail(prompt):
        raise ProviderTimeoutError("gemini", "timed out")

    provider_manager = _FakeProviderManager({
        "gemini": _FakeProvider("gemini", behavior=_fail),
        "openai": _FakeProvider("openai", behavior=_fail),
        "claude": _FakeProvider("claude", behavior=_fail),
        "grok": _FakeProvider("grok"),
    })
    from ai.runtime.runtime_profiles import RuntimeProfile
    from ai.validation.schemas import DEFAULT_SCHEMA
    two_attempt_profile = RuntimeProfile(
        name="two-attempts", max_retries=2, timeout_seconds=5, cache_ttl_seconds=60, validation_schema=DEFAULT_SCHEMA,
    )
    service = AIService(provider_manager=provider_manager, runtime_profile=two_attempt_profile)

    response = service.ask(_request())

    assert response.accepted is False  # only 2 providers attempted (both fail), grok never reached
    assert "every available provider failed" in response.reason


# ---------------------------------------------------------------------------
# TASK 5 — Event Bus: real request-lifecycle events fire from a real ask()
# ---------------------------------------------------------------------------

def test_successful_request_publishes_started_and_completed_not_failed():
    provider_manager = _FakeProviderManager({"gemini": _FakeProvider("gemini")})
    bus = EventBus()
    service = AIService(provider_manager=provider_manager, event_bus=bus)

    service.ask(_request())

    assert len(bus.history(EventType.REQUEST_STARTED)) == 1
    assert len(bus.history(EventType.REQUEST_COMPLETED)) == 1
    assert len(bus.history(EventType.REQUEST_FAILED)) == 0


def test_rejected_request_publishes_completed_and_failed():
    provider_manager = _FakeProviderManager({})
    bus = EventBus()
    runtime_manager = RuntimeManager(initial_state=RuntimeState.FAILED, event_bus=bus)
    service = AIService(provider_manager=provider_manager, event_bus=bus, runtime_manager=runtime_manager)

    service.ask(_request())

    assert len(bus.history(EventType.REQUEST_COMPLETED)) == 1
    assert len(bus.history(EventType.REQUEST_FAILED)) == 1


def test_failover_publishes_retry_started_and_retry_completed():
    def _fail(prompt):
        raise ProviderTimeoutError("gemini", "timed out")

    provider_manager = _FakeProviderManager({
        "gemini": _FakeProvider("gemini", behavior=_fail),
        "openai": _FakeProvider("openai"),
    })
    bus = EventBus()
    service = AIService(provider_manager=provider_manager, event_bus=bus)

    response = service.ask(_request())

    assert response.accepted is True
    assert len(bus.history(EventType.RETRY_STARTED)) == 1
    completed = bus.history(EventType.RETRY_COMPLETED)
    assert len(completed) == 1
    assert completed[0].payload["success"] is True


def test_single_provider_success_never_publishes_a_retry_event():
    provider_manager = _FakeProviderManager({"gemini": _FakeProvider("gemini")})
    bus = EventBus()
    service = AIService(provider_manager=provider_manager, event_bus=bus)

    service.ask(_request())

    assert bus.history(EventType.RETRY_STARTED) == []
    assert bus.history(EventType.RETRY_COMPLETED) == []


# ---------------------------------------------------------------------------
# TASK 6 — Runtime Notification Integration: RuntimeNotifier attached to
# the SAME bus as a real AIService's circuit breaker receives a real
# Provider DOWN alert once the circuit actually trips.
# ---------------------------------------------------------------------------

def test_runtime_notifier_receives_a_real_provider_down_alert_from_a_tripped_circuit():
    def _fail(prompt):
        raise ProviderTimeoutError("gemini", "timed out")

    provider_manager = _FakeProviderManager({
        "gemini": _FakeProvider("gemini", behavior=_fail),
        "openai": _FakeProvider("openai"),
    })
    bus = EventBus()
    notifier = RuntimeNotifier(bus)
    health_tracker = ProviderHealthTracker()
    breaker = ProviderCircuitBreaker(health_tracker=health_tracker, event_bus=bus, config=CircuitBreakerConfig(failure_threshold=5))
    service = AIService(provider_manager=provider_manager, health_tracker=health_tracker, circuit_breaker=breaker, event_bus=bus)

    for _ in range(5):
        service.ask(_request())

    alerts = notifier.drain()
    assert any("DOWN" in alert.title and "gemini" in alert.message for alert in alerts)


# ---------------------------------------------------------------------------
# Final Audit #5 — proof that all three named RuntimeProfiles are actually
# used by AIService, not just constructible.
# ---------------------------------------------------------------------------

def test_development_profile_is_actually_used_its_cache_ttl_reaches_the_response_cache():
    service = AIService(provider_manager=_FakeProviderManager({"gemini": _FakeProvider("gemini")}), runtime_profile=DEVELOPMENT_PROFILE)
    assert service._response_cache._policy.default_ttl_seconds == DEVELOPMENT_PROFILE.cache_ttl_seconds


def test_testing_profile_is_actually_used_it_disables_caching_end_to_end():
    call_count = {"n": 0}

    def _counting(prompt):
        call_count["n"] += 1
        return ProviderResult(content="answer", metadata={})

    provider_manager = _FakeProviderManager({"gemini": _FakeProvider("gemini", behavior=_counting)})
    service = AIService(provider_manager=provider_manager, runtime_profile=TESTING_PROFILE)

    service.ask(_request())
    service.ask(_request())

    assert call_count["n"] == 2


def test_production_profile_is_actually_used_it_enforces_strict_validation_end_to_end():
    provider_manager = _FakeProviderManager({"gemini": _FakeProvider("gemini")})  # no confidence metadata
    service = AIService(provider_manager=provider_manager, runtime_profile=PRODUCTION_PROFILE)

    response = service.ask(_request())

    assert response.accepted is False
    assert "confidence" in " ".join(response.errors).lower()


def test_runtime_notifier_never_alerts_on_a_single_ai_service_level_failure():
    """A plain ai_service.py PROVIDER_FAILED (below the breaker's own threshold) must not spam the Owner."""
    def _fail(prompt):
        raise ProviderTimeoutError("gemini", "timed out")

    provider_manager = _FakeProviderManager({
        "gemini": _FakeProvider("gemini", behavior=_fail),
        "openai": _FakeProvider("openai"),
    })
    bus = EventBus()
    notifier = RuntimeNotifier(bus)
    service = AIService(provider_manager=provider_manager, event_bus=bus)

    service.ask(_request())  # gemini fails once, falls over to openai -- circuit never trips

    assert notifier.drain() == []
