"""Phase 61.1 TASK 4/8 — Router Safety (capability matrix + health) and read-only Metrics Integration."""

from ai.capabilities.capability import Capability
from ai.providers.provider_health import ProviderHealthTracker
from ai.providers.provider_manager import ProviderManager
from ai.providers.provider_status import HealthStatus
from ai.router.router import AIRouter
from ai.audit.response_log import ResponseLog


def test_router_without_health_tracker_behaves_exactly_like_phase_61_0():
    router = AIRouter(ProviderManager())
    result = router.route(Capability.EXPLANATION)
    assert result.provider_name == "gemini"


def test_router_skips_unhealthy_candidate_and_falls_back():
    tracker = ProviderHealthTracker()
    tracker.record("gemini", HealthStatus.OFFLINE)
    router = AIRouter(ProviderManager(), health_tracker=tracker)
    result = router.route(Capability.EXPLANATION)
    assert result.provider_name == "openai"


def test_router_treats_degraded_provider_as_still_available():
    tracker = ProviderHealthTracker()
    tracker.record("gemini", HealthStatus.DEGRADED)
    router = AIRouter(ProviderManager(), health_tracker=tracker)
    result = router.route(Capability.EXPLANATION)
    assert result.provider_name == "gemini"


def test_router_returns_none_when_every_candidate_unhealthy():
    tracker = ProviderHealthTracker()
    for name in ("gemini", "openai", "claude"):
        tracker.record(name, HealthStatus.OFFLINE)
    router = AIRouter(ProviderManager(), health_tracker=tracker)
    result = router.route(Capability.EXPLANATION)
    assert result.provider_name is None


def test_router_never_selects_a_provider_the_capability_matrix_does_not_support():
    router = AIRouter(ProviderManager())
    result = router.route(Capability.IMAGE)
    assert result.provider_name == "openai"


def test_provider_metrics_is_empty_without_a_response_log():
    router = AIRouter(ProviderManager())
    assert router.provider_metrics() == {}


def test_provider_metrics_reuses_provider_stats_from_response_log():
    log = ResponseLog()
    log.record(request_id="r1", capability=Capability.CHAT, provider_name="gemini", latency_ms=100.0, tokens=10, cost=0.01, status="SUCCESS")
    router = AIRouter(ProviderManager(), response_log=log)
    metrics = router.provider_metrics()
    assert metrics["gemini"].total_calls == 1
    assert metrics["gemini"].success_rate == 1.0


def test_provider_metrics_never_influences_route_selection():
    log = ResponseLog()
    log.record(request_id="r1", capability=Capability.CHAT, provider_name="gemini", latency_ms=9999.0, tokens=1, cost=99.0, status="FAILED")
    router = AIRouter(ProviderManager(), response_log=log)
    result = router.route(Capability.EXPLANATION)
    assert result.provider_name == "gemini"
