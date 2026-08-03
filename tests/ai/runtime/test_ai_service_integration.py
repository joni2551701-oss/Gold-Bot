"""
Phase 61.7 — AI Platform Stabilization & Integration. End-to-end tests
driving a real AIService through RuntimeManager/CircuitBreaker/
RuntimeProfile/EventBus/RuntimeNotifier together -- not each piece in
isolation (already covered by tests/ai/runtime/test_runtime_lifecycle.py,
tests/ai/providers/test_provider_circuit_breaker.py,
tests/ai/runtime/test_runtime_profiles.py,
tests/platform_layer/telegram/owner/test_runtime_notifications.py). No real network
call anywhere -- every provider is faked.
"""

from ai_layer.ai_service.access.permissions import AIRole
from ai_layer.ai_engine.capabilities.capability import Capability
from ai_layer.ai_engine.providers.base_provider import ProviderResult
from ai_layer.ai_engine.providers.circuit_breaker import CircuitBreakerConfig, CircuitState, ProviderCircuitBreaker
from ai_layer.ai_engine.providers.provider_health import ProviderHealthTracker
from ai_layer.ai_engine.providers.provider_manager import ProviderStatus
from ai_layer.ai_engine.providers.runtime_errors import ProviderTimeoutError
from ai_layer.ai_engine.runtime.ai_service import AIService
from ai_layer.ai_service.event_bus import EventBus, EventType
from ai_layer.ai_engine.runtime.runtime_manager import RuntimeManager
from ai_layer.ai_engine.runtime.runtime_profiles import DEVELOPMENT_PROFILE, PRODUCTION_PROFILE, TESTING_PROFILE
from ai_layer.ai_engine.runtime.runtime_request import RuntimeRequest
from ai_layer.ai_engine.runtime.runtime_state import RuntimeState
from ai_layer.ai_engine.context.context_builder import build_ai_context
from ai_layer.ai_service.interfaces import MarketContext
from platform_layer.telegram.owner.runtime_notifications import RuntimeNotifier


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


def test_unhealthy_runtime_rejection_writes_an_audit_trail():
    """Phase 62.2 TASK 3: previously the one _execute() rejection path with zero audit trail -- every other rejection/success path already called request_log/response_log.record()."""
    from ai_layer.ai_service.audit.request_log import RequestLog
    from ai_layer.ai_service.audit.response_log import ResponseLog

    provider_manager = _FakeProviderManager({"gemini": _FakeProvider("gemini")})
    runtime_manager = RuntimeManager(initial_state=RuntimeState.FAILED)
    request_log = RequestLog()
    response_log = ResponseLog()
    service = AIService(
        provider_manager=provider_manager, runtime_manager=runtime_manager,
        request_log=request_log, response_log=response_log,
    )

    response = service.ask(_request())

    assert response.accepted is False
    assert response.request_id is not None
    logged_requests = request_log.all()
    assert len(logged_requests) == 1
    assert logged_requests[0].provider_name is None
    logged_responses = response_log.all()
    assert len(logged_responses) == 1
    assert logged_responses[0].status == "RUNTIME_UNAVAILABLE"
    assert logged_responses[0].request_id == response.request_id


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
    service = AIService(provider_manager=provider_manager, health_tracker=health_tracker, circuit_breaker=breaker, sleep_fn=lambda s: None)

    for _ in range(5):
        response = service.ask(_request())
        assert response.accepted is True
        assert response.provider_name == "openai"  # gemini always fails over to openai

    assert breaker.state_of("gemini") == CircuitState.OPEN
    assert health_tracker.is_available("gemini") is False


def test_circuit_recovers_to_half_open_and_closes_on_a_real_success(monkeypatch):
    import ai_layer.ai_engine.providers.circuit_breaker as circuit_breaker_module
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
    from ai_layer.ai_engine.runtime.runtime_profiles import RuntimeProfile
    from ai_layer.confidence_ai.schemas import DEFAULT_SCHEMA
    two_attempt_profile = RuntimeProfile(
        name="two-attempts", max_retries=2, timeout_seconds=5, cache_ttl_seconds=60, validation_schema=DEFAULT_SCHEMA,
    )
    service = AIService(provider_manager=provider_manager, runtime_profile=two_attempt_profile, sleep_fn=lambda s: None)

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
    service = AIService(provider_manager=provider_manager, event_bus=bus, sleep_fn=lambda s: None)

    response = service.ask(_request())

    assert response.accepted is True
    assert len(bus.history(EventType.RETRY_STARTED)) == 1
    completed = bus.history(EventType.RETRY_COMPLETED)
    assert len(completed) == 1
    assert completed[0].payload["success"] is True


def test_retry_waits_via_the_injectable_sleep_fn_with_exponential_backoff():
    """Phase 62.2 TASK 5: 2 ** attempt formula, same one data_layer/providers/twelve_data_client.py already uses -- reused, not reinvented."""
    def _fail(prompt):
        raise ProviderTimeoutError("gemini", "timed out")

    provider_manager = _FakeProviderManager({
        "gemini": _FakeProvider("gemini", behavior=_fail),
        "openai": _FakeProvider("openai", behavior=_fail),
        "claude": _FakeProvider("claude"),
    })
    sleeps = []
    service = AIService(provider_manager=provider_manager, sleep_fn=sleeps.append)

    response = service.ask(_request())

    assert response.accepted is True
    assert sleeps == [1, 2]  # 2**0 before the 2nd attempt, 2**1 before the 3rd


def test_single_provider_success_never_sleeps():
    provider_manager = _FakeProviderManager({"gemini": _FakeProvider("gemini")})
    sleeps = []
    service = AIService(provider_manager=provider_manager, sleep_fn=sleeps.append)

    service.ask(_request())

    assert sleeps == []


def test_provider_failed_event_carries_a_structured_error_type():
    """Phase 62.2 TASK 6: PROVIDER_TIMEOUT resolved the same way ProviderDown already was -- payload key, not a new EventType."""
    def _fail(prompt):
        raise ProviderTimeoutError("gemini", "timed out")

    provider_manager = _FakeProviderManager({
        "gemini": _FakeProvider("gemini", behavior=_fail),
        "openai": _FakeProvider("openai"),
    })
    bus = EventBus()
    service = AIService(provider_manager=provider_manager, event_bus=bus, sleep_fn=lambda s: None)

    service.ask(_request())

    failed_events = bus.history(EventType.PROVIDER_FAILED)
    assert len(failed_events) == 1
    assert failed_events[0].payload["error_type"] == "TIMEOUT"


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
    service = AIService(provider_manager=provider_manager, health_tracker=health_tracker, circuit_breaker=breaker, event_bus=bus, sleep_fn=lambda s: None)

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
    service = AIService(provider_manager=provider_manager, event_bus=bus, sleep_fn=lambda s: None)

    service.ask(_request())  # gemini fails once, falls over to openai -- circuit never trips

    assert notifier.drain() == []


# ---------------------------------------------------------------------------
# Phase 62.2 TASK 8 — AI Cost Protection
# ---------------------------------------------------------------------------

def test_no_configured_limits_never_degrades_the_runtime():
    provider_manager = _FakeProviderManager({"gemini": _FakeProvider("gemini")})
    runtime_manager = RuntimeManager()
    service = AIService(provider_manager=provider_manager, runtime_manager=runtime_manager)

    service.ask(_request())

    assert runtime_manager.current_state() == RuntimeState.READY


def test_a_breached_cost_limit_degrades_the_runtime():
    """Real response_log entries always log cost=0.0 today (no provider reports usage yet -- see ai_service.py's own docstring), so this pre-seeds the log with a breaching entry the same way a future real-cost-reporting phase would."""
    from ai_layer.ai_service.audit.response_log import ResponseLog

    provider_manager = _FakeProviderManager({"gemini": _FakeProvider("gemini")})
    runtime_manager = RuntimeManager()
    response_log = ResponseLog()
    response_log.record(request_id="pre-existing", capability=Capability.CHAT, provider_name="gemini", latency_ms=0.0, tokens=0, cost=999.0, status="SUCCESS")
    service = AIService(
        provider_manager=provider_manager, runtime_manager=runtime_manager,
        response_log=response_log, daily_cost_limit=10.0,
    )

    response = service.ask(_request())

    assert response.accepted is True  # the request itself still succeeds
    assert runtime_manager.current_state() == RuntimeState.DEGRADED
    assert "cost protection" in runtime_manager.history()[-1].reason


def test_a_breached_token_limit_degrades_the_runtime():
    from ai_layer.ai_service.audit.response_log import ResponseLog

    provider_manager = _FakeProviderManager({"gemini": _FakeProvider("gemini")})
    runtime_manager = RuntimeManager()
    response_log = ResponseLog()
    response_log.record(request_id="pre-existing", capability=Capability.CHAT, provider_name="gemini", latency_ms=0.0, tokens=999999, cost=0.0, status="SUCCESS")
    service = AIService(
        provider_manager=provider_manager, runtime_manager=runtime_manager,
        response_log=response_log, daily_token_limit=1000,
    )

    service.ask(_request())

    assert runtime_manager.current_state() == RuntimeState.DEGRADED


def test_cost_protection_notifies_the_owner():
    from ai_layer.ai_service.audit.response_log import ResponseLog

    provider_manager = _FakeProviderManager({"gemini": _FakeProvider("gemini")})
    bus = EventBus()
    runtime_manager = RuntimeManager(event_bus=bus)
    notifier = RuntimeNotifier(bus)
    response_log = ResponseLog()
    response_log.record(request_id="pre-existing", capability=Capability.CHAT, provider_name="gemini", latency_ms=0.0, tokens=0, cost=999.0, status="SUCCESS")
    service = AIService(
        provider_manager=provider_manager, runtime_manager=runtime_manager,
        response_log=response_log, event_bus=bus, daily_cost_limit=10.0,
    )

    service.ask(_request())

    alerts = notifier.drain()
    assert any("Cost Protection" in a.title for a in alerts)


def test_cost_protection_does_not_re_trigger_once_already_degraded():
    from ai_layer.ai_service.audit.response_log import ResponseLog

    provider_manager = _FakeProviderManager({"gemini": _FakeProvider("gemini")})
    runtime_manager = RuntimeManager()
    response_log = ResponseLog()
    response_log.record(request_id="pre-existing", capability=Capability.CHAT, provider_name="gemini", latency_ms=0.0, tokens=0, cost=999.0, status="SUCCESS")
    service = AIService(
        provider_manager=provider_manager, runtime_manager=runtime_manager,
        response_log=response_log, daily_cost_limit=10.0,
    )

    service.ask(_request())
    transitions_after_first = len(runtime_manager.history())
    service.ask(_request())  # runtime is already DEGRADED -- is_healthy() still True, but _check_cost_protection() should not spam a redundant transition

    assert len(runtime_manager.history()) == transitions_after_first


def test_cost_protection_under_the_limit_never_degrades():
    provider_manager = _FakeProviderManager({"gemini": _FakeProvider("gemini")})
    runtime_manager = RuntimeManager()
    service = AIService(provider_manager=provider_manager, runtime_manager=runtime_manager, daily_cost_limit=1000.0, daily_token_limit=1000000)

    service.ask(_request())

    assert runtime_manager.current_state() == RuntimeState.READY


# ---------------------------------------------------------------------------
# Phase 62.2 TASK 9 — Full Integration Test Matrix (Director's own 4 scenarios)
# ---------------------------------------------------------------------------

def test_scenario_1_full_provider_failure_flow_timeout_retry_breaker_fallback_audit_event():
    """AI Request -> Provider Timeout -> Retry -> Circuit Breaker -> Fallback -> Audit -> Owner Event, in one real end-to-end call sequence."""
    from ai_layer.ai_service.audit.request_log import RequestLog
    from ai_layer.ai_service.audit.response_log import ResponseLog

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
    request_log = RequestLog()
    response_log = ResponseLog()
    service = AIService(
        provider_manager=provider_manager, health_tracker=health_tracker, circuit_breaker=breaker,
        event_bus=bus, request_log=request_log, response_log=response_log, sleep_fn=lambda s: None,
    )

    # 5 real calls with distinct prompts (avoids a cache hit masking a real
    # attempt -- the response cache is keyed per-provider, so an identical
    # repeated prompt would let the earlier openai success serve later
    # calls from cache instead of exercising a fresh fallback each time).
    for i in range(5):
        response = service.ask(_request(prompt=f"question {i}"))
        assert response.accepted is True  # no crash, always recovers via fallback
        assert response.provider_name == "openai"

    # Circuit Breaker: 5 consecutive gemini failures trip it.
    assert breaker.state_of("gemini") == CircuitState.OPEN
    assert health_tracker.is_available("gemini") is False

    # Audit: every attempt (both the failed gemini attempt and the successful openai attempt) is logged.
    assert len(request_log.all()) == 10  # 2 attempts per call x 5 calls
    statuses = [e.status for e in response_log.all()]
    assert statuses.count("FAILED") == 5
    assert statuses.count("SUCCESS") == 5

    # Owner Event: the tripped circuit produced a real "Provider DOWN" alert.
    alerts = notifier.drain()
    assert any("DOWN" in a.title and "gemini" in a.message for a in alerts)


def test_scenario_2_runtime_failed_rejects_with_audit_and_event():
    from ai_layer.ai_service.audit.request_log import RequestLog
    from ai_layer.ai_service.audit.response_log import ResponseLog

    provider_manager = _FakeProviderManager({"gemini": _FakeProvider("gemini")})
    bus = EventBus()
    runtime_manager = RuntimeManager(initial_state=RuntimeState.FAILED, event_bus=bus)
    request_log = RequestLog()
    response_log = ResponseLog()
    service = AIService(
        provider_manager=provider_manager, runtime_manager=runtime_manager, event_bus=bus,
        request_log=request_log, response_log=response_log,
    )

    response = service.ask(_request())

    # Rejected.
    assert response.accepted is False
    assert "FAILED" in response.reason

    # Audit.
    assert len(request_log.all()) == 1
    assert response_log.all()[0].status == "RUNTIME_UNAVAILABLE"

    # Event.
    assert len(bus.history(EventType.REQUEST_FAILED)) == 1


def test_scenario_3_cost_limit_breach_degrades_notifies_without_false_metrics():
    from ai_layer.ai_service.audit.response_log import ResponseLog

    provider_manager = _FakeProviderManager({"gemini": _FakeProvider("gemini")})
    bus = EventBus()
    runtime_manager = RuntimeManager(event_bus=bus)
    notifier = RuntimeNotifier(bus)
    response_log = ResponseLog()
    response_log.record(request_id="pre-existing", capability=Capability.CHAT, provider_name="gemini", latency_ms=0.0, tokens=0, cost=999.0, status="SUCCESS")
    service = AIService(
        provider_manager=provider_manager, runtime_manager=runtime_manager, event_bus=bus,
        response_log=response_log, daily_cost_limit=10.0,
    )

    service.ask(_request())

    # Runtime DEGRADED.
    assert runtime_manager.current_state() == RuntimeState.DEGRADED
    # Owner notification.
    assert any("Cost Protection" in a.title for a in notifier.drain())
    # No false metrics: the breach reason reflects the real, injected total, not a fabricated number.
    from ai_layer.ai_service.audit.provider_stats import compute_daily_usage
    usage = compute_daily_usage(response_log.all())
    assert usage.total_cost == 999.0  # the real pre-seeded cost, not made up


def test_scenario_4_cache_behavior_hit_miss_stale_and_prompt_collision():
    from ai_layer.ai_engine.runtime.runtime_profiles import RuntimeProfile
    from ai_layer.confidence_ai.schemas import DEFAULT_SCHEMA

    call_count = {"n": 0}

    def _counting(prompt):
        call_count["n"] += 1
        return ProviderResult(content=f"answer-{call_count['n']}", metadata={})

    provider_manager = _FakeProviderManager({"gemini": _FakeProvider("gemini", behavior=_counting)})
    bus = EventBus()

    # (a) cache miss then (b) cache hit on an identical repeated call.
    service = AIService(provider_manager=provider_manager, event_bus=bus)
    first = service.ask(_request(prompt="what is the trend?"))
    second = service.ask(_request(prompt="what is the trend?"))

    assert first.from_cache is False
    assert second.from_cache is True
    assert second.content == first.content
    assert len(bus.history(EventType.CACHE_MISS)) == 1
    assert len(bus.history(EventType.CACHE_HIT)) == 1

    # (c) stale snapshot: a 0-second TTL profile means the cached entry is
    # already expired by the time the very next call checks it.
    zero_ttl_profile = RuntimeProfile(name="zero-ttl", max_retries=1, timeout_seconds=5, cache_ttl_seconds=0, validation_schema=DEFAULT_SCHEMA)
    stale_service = AIService(provider_manager=provider_manager, runtime_profile=zero_ttl_profile)
    stale_first = stale_service.ask(_request(prompt="stale test"))
    stale_second = stale_service.ask(_request(prompt="stale test"))
    assert stale_first.from_cache is False
    assert stale_second.from_cache is False  # expired, not served from a stale entry

    # (d) different prompt, same market context -> no collision (Phase 61.3's own cache-key fix).
    collision_service = AIService(provider_manager=provider_manager, event_bus=EventBus())
    answer_a = collision_service.ask(_request(prompt="question A"))
    answer_b = collision_service.ask(_request(prompt="question B"))
    assert answer_a.from_cache is False
    assert answer_b.from_cache is False  # a different prompt must never be served question A's cached answer
    assert answer_a.content != answer_b.content
