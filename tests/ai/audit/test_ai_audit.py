"""Phase 61.0 TASK 9 — AI Audit System: in-memory request/response log + provider stats."""

from ai.audit.provider_stats import compute_provider_stats
from ai.audit.request_log import RequestLog
from ai.audit.response_log import ResponseLog
from ai.capabilities.capability import Capability


def test_request_log_records_and_lists_entries():
    log = RequestLog()
    entry = log.record(Capability.CHAT, "gemini", telegram_id="123")
    assert entry in log.all()
    assert entry.capability == Capability.CHAT
    assert entry.provider_name == "gemini"


def test_response_log_records_full_shape():
    log = ResponseLog()
    entry = log.record(
        request_id="r1", capability=Capability.CHAT, provider_name="gemini",
        latency_ms=120.5, tokens=42, cost=0.001, status="SUCCESS",
    )
    assert entry in log.all()
    assert entry.status == "SUCCESS"


def test_provider_stats_aggregates_per_provider():
    log = ResponseLog()
    log.record(request_id="r1", capability=Capability.CHAT, provider_name="gemini", latency_ms=100.0, tokens=10, cost=0.01, status="SUCCESS")
    log.record(request_id="r2", capability=Capability.CHAT, provider_name="gemini", latency_ms=200.0, tokens=20, cost=0.02, status="FAILED")
    log.record(request_id="r3", capability=Capability.ANALYSIS, provider_name="openai", latency_ms=50.0, tokens=5, cost=0.005, status="SUCCESS")

    stats = compute_provider_stats(log.all())

    assert stats["gemini"].total_calls == 2
    assert stats["gemini"].success_count == 1
    assert stats["gemini"].success_rate == 0.5
    assert stats["gemini"].avg_latency_ms == 150.0
    assert stats["gemini"].total_tokens == 30
    assert stats["openai"].total_calls == 1
    assert stats["openai"].success_rate == 1.0


def test_provider_stats_excludes_entries_with_no_provider():
    log = ResponseLog()
    log.record(request_id="r1", capability=Capability.CHAT, provider_name=None, latency_ms=0.0, tokens=0, cost=0.0, status="FAILED")
    stats = compute_provider_stats(log.all())
    assert stats == {}


def test_provider_stats_on_empty_log_returns_empty_dict():
    assert compute_provider_stats([]) == {}


def test_success_rate_is_zero_when_no_calls():
    from ai.audit.provider_stats import ProviderStats
    stats = ProviderStats(provider_name="x", total_calls=0, success_count=0, avg_latency_ms=0.0, total_tokens=0, total_cost=0.0)
    assert stats.success_rate == 0.0


def test_rank_providers_orders_by_success_rate_first():
    from ai.audit.provider_stats import ProviderStats, rank_providers

    stats = {
        "slow_reliable": ProviderStats(provider_name="slow_reliable", total_calls=10, success_count=10, avg_latency_ms=500.0, total_tokens=0, total_cost=0.0),
        "fast_unreliable": ProviderStats(provider_name="fast_unreliable", total_calls=10, success_count=2, avg_latency_ms=50.0, total_tokens=0, total_cost=0.0),
    }
    ranked = rank_providers(stats)
    assert [s.provider_name for s in ranked] == ["slow_reliable", "fast_unreliable"]


def test_rank_providers_breaks_success_rate_ties_by_latency():
    from ai.audit.provider_stats import ProviderStats, rank_providers

    stats = {
        "slower": ProviderStats(provider_name="slower", total_calls=10, success_count=10, avg_latency_ms=300.0, total_tokens=0, total_cost=0.0),
        "faster": ProviderStats(provider_name="faster", total_calls=10, success_count=10, avg_latency_ms=100.0, total_tokens=0, total_cost=0.0),
    }
    ranked = rank_providers(stats)
    assert [s.provider_name for s in ranked] == ["faster", "slower"]


def test_rank_providers_breaks_remaining_ties_by_cost():
    from ai.audit.provider_stats import ProviderStats, rank_providers

    stats = {
        "expensive": ProviderStats(provider_name="expensive", total_calls=10, success_count=10, avg_latency_ms=100.0, total_tokens=0, total_cost=1.0),
        "cheap": ProviderStats(provider_name="cheap", total_calls=10, success_count=10, avg_latency_ms=100.0, total_tokens=0, total_cost=0.1),
    }
    ranked = rank_providers(stats)
    assert [s.provider_name for s in ranked] == ["cheap", "expensive"]


def test_rank_providers_on_empty_stats_returns_empty_list():
    from ai.audit.provider_stats import rank_providers
    assert rank_providers({}) == []


def test_rank_providers_end_to_end_from_response_log():
    from ai.audit.provider_stats import compute_provider_stats, rank_providers

    log = ResponseLog()
    log.record(request_id="r1", capability=Capability.CHAT, provider_name="gemini", latency_ms=100.0, tokens=10, cost=0.01, status="SUCCESS")
    log.record(request_id="r2", capability=Capability.CHAT, provider_name="openai", latency_ms=50.0, tokens=5, cost=0.005, status="FAILED")

    ranked = rank_providers(compute_provider_stats(log.all()))
    assert ranked[0].provider_name == "gemini"


# ---------------------------------------------------------------------------
# Phase 62.2 TASK 8 — AI Cost Protection: compute_daily_usage / evaluate_cost_protection
# ---------------------------------------------------------------------------

def test_compute_daily_usage_sums_cost_and_tokens_across_providers():
    from datetime import datetime, timezone
    from ai.audit.provider_stats import compute_daily_usage

    log = ResponseLog()
    log.record(request_id="r1", capability=Capability.CHAT, provider_name="gemini", latency_ms=100.0, tokens=100, cost=1.50, status="SUCCESS")
    log.record(request_id="r2", capability=Capability.CHAT, provider_name="openai", latency_ms=50.0, tokens=50, cost=0.75, status="SUCCESS")

    usage = compute_daily_usage(log.all(), now=datetime.now(timezone.utc))

    assert usage.total_cost == 2.25
    assert usage.total_tokens == 150


def test_compute_daily_usage_excludes_entries_older_than_24h():
    from datetime import datetime, timedelta, timezone
    from ai.audit.provider_stats import compute_daily_usage

    log = ResponseLog()
    log.record(request_id="r1", capability=Capability.CHAT, provider_name="gemini", latency_ms=100.0, tokens=100, cost=5.00, status="SUCCESS")

    now = datetime.now(timezone.utc) + timedelta(hours=25)  # the recorded entry is now >24h in the past
    usage = compute_daily_usage(log.all(), now=now)

    assert usage.total_cost == 0.0
    assert usage.total_tokens == 0


def test_evaluate_cost_protection_no_limits_configured_never_breaches():
    from ai.audit.provider_stats import DailyUsage, evaluate_cost_protection

    assert evaluate_cost_protection(DailyUsage(total_cost=1000.0, total_tokens=999999), None, None) is None


def test_evaluate_cost_protection_reports_a_cost_breach():
    from ai.audit.provider_stats import DailyUsage, evaluate_cost_protection

    reason = evaluate_cost_protection(DailyUsage(total_cost=15.0, total_tokens=0), cost_limit=10.0, token_limit=None)

    assert reason is not None
    assert "daily cost" in reason


def test_evaluate_cost_protection_reports_a_token_breach():
    from ai.audit.provider_stats import DailyUsage, evaluate_cost_protection

    reason = evaluate_cost_protection(DailyUsage(total_cost=0.0, total_tokens=50000), cost_limit=None, token_limit=10000)

    assert reason is not None
    assert "daily tokens" in reason


def test_evaluate_cost_protection_under_both_limits_is_none():
    from ai.audit.provider_stats import DailyUsage, evaluate_cost_protection

    assert evaluate_cost_protection(DailyUsage(total_cost=1.0, total_tokens=100), cost_limit=10.0, token_limit=10000) is None
