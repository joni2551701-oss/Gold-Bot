"""Phase 61.5 TASK 2 — Provider Score. Recommendation/analytics only -- never imports or calls AIRouter.route()."""

from ai.audit.provider_stats import ProviderStats
from ai.providers.provider_health import ProviderHealthTracker
from ai.providers.provider_status import HealthStatus
from ai.router.provider_score import score_provider, score_providers


def _stats(success_rate=1.0, avg_latency_ms=100.0, total_cost=0.0, total_calls=10):
    success_count = round(success_rate * total_calls)
    return ProviderStats(
        provider_name="x", total_calls=total_calls, success_count=success_count,
        avg_latency_ms=avg_latency_ms, total_tokens=0, total_cost=total_cost,
    )


def test_online_healthy_cheap_fast_provider_scores_near_the_top():
    score = score_provider("gemini", _stats(success_rate=1.0, avg_latency_ms=50.0, total_cost=0.01), HealthStatus.ONLINE)
    assert score.score > 0.8


def test_offline_provider_scores_lower_than_an_online_one_with_identical_stats():
    stats = _stats(success_rate=1.0, avg_latency_ms=50.0, total_cost=0.01)
    online = score_provider("a", stats, HealthStatus.ONLINE)
    offline = score_provider("b", stats, HealthStatus.OFFLINE)
    assert offline.score < online.score


def test_rate_limited_scores_between_degraded_and_offline():
    stats = _stats()
    degraded = score_provider("a", stats, HealthStatus.DEGRADED)
    rate_limited = score_provider("b", stats, HealthStatus.RATE_LIMITED)
    offline = score_provider("c", stats, HealthStatus.OFFLINE)
    assert degraded.score > rate_limited.score > offline.score


def test_missing_stats_and_health_degrade_to_neutral_not_zero():
    score = score_provider("brand_new", stats=None, health_status=None)
    assert 0.0 < score.score < 1.0


def test_higher_success_rate_scores_higher_all_else_equal():
    low = score_provider("a", _stats(success_rate=0.5, avg_latency_ms=100.0, total_cost=1.0), HealthStatus.ONLINE)
    high = score_provider("b", _stats(success_rate=1.0, avg_latency_ms=100.0, total_cost=1.0), HealthStatus.ONLINE)
    assert high.score > low.score


def test_lower_latency_scores_higher_all_else_equal():
    slow = score_provider("a", _stats(avg_latency_ms=5000.0), HealthStatus.ONLINE)
    fast = score_provider("b", _stats(avg_latency_ms=10.0), HealthStatus.ONLINE)
    assert fast.score > slow.score


def test_lower_cost_scores_higher_all_else_equal():
    expensive = score_provider("a", _stats(total_cost=100.0), HealthStatus.ONLINE)
    cheap = score_provider("b", _stats(total_cost=0.0), HealthStatus.ONLINE)
    assert cheap.score > expensive.score


def test_score_providers_returns_best_first():
    stats = {
        "gemini": _stats(success_rate=1.0, avg_latency_ms=50.0, total_cost=0.01),
        "grok": _stats(success_rate=0.2, avg_latency_ms=5000.0, total_cost=10.0),
    }
    health_tracker = ProviderHealthTracker()
    health_tracker.record("gemini", HealthStatus.ONLINE)
    health_tracker.record("grok", HealthStatus.DEGRADED)

    ranked = score_providers(["grok", "gemini"], stats, health_tracker)

    assert [s.provider_name for s in ranked] == ["gemini", "grok"]


def test_score_providers_includes_a_provider_with_no_call_history():
    ranked = score_providers(["brand_new"], stats={}, health_tracker=None)
    assert len(ranked) == 1
    assert ranked[0].provider_name == "brand_new"


def test_score_providers_empty_list_returns_empty_list():
    assert score_providers([], {}, None) == []


def test_score_providers_never_calls_or_imports_router_route():
    import ai.router.provider_score as module
    import inspect
    source = inspect.getsource(module)
    assert "AIRouter" not in source
    assert ".route(" not in source
