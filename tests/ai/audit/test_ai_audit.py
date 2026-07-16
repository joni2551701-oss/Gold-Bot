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
