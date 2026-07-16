"""Phase 61.4 TASK 6 — AI Usage Accounting: per-telegram_id cost aggregation, generalizing trace.py's request_id -> telegram_id join."""

from ai.audit.request_log import RequestLog
from ai.audit.response_log import ResponseLog
from ai.audit.usage_accounting import compute_user_usage
from ai.capabilities.capability import Capability


def test_aggregates_calls_tokens_and_cost_for_one_user():
    request_log = RequestLog()
    response_log = ResponseLog()

    entry = request_log.record(Capability.CHAT, "gemini", telegram_id="111")
    response_log.record(request_id=entry.request_id, capability=Capability.CHAT, provider_name="gemini", latency_ms=100.0, tokens=50, cost=0.05, status="SUCCESS")

    stats = compute_user_usage(request_log.all(), response_log.all())

    assert stats["111"].total_calls == 1
    assert stats["111"].total_tokens == 50
    assert stats["111"].total_cost == 0.05
    assert stats["111"].cost_by_provider == {"gemini": 0.05}


def test_aggregates_across_multiple_requests_and_providers_for_one_user():
    request_log = RequestLog()
    response_log = ResponseLog()

    e1 = request_log.record(Capability.CHAT, "gemini", telegram_id="111")
    e2 = request_log.record(Capability.ANALYSIS, "openai", telegram_id="111")
    response_log.record(request_id=e1.request_id, capability=Capability.CHAT, provider_name="gemini", latency_ms=100.0, tokens=10, cost=0.01, status="SUCCESS")
    response_log.record(request_id=e2.request_id, capability=Capability.ANALYSIS, provider_name="openai", latency_ms=200.0, tokens=20, cost=0.02, status="SUCCESS")

    stats = compute_user_usage(request_log.all(), response_log.all())

    assert stats["111"].total_calls == 2
    assert stats["111"].total_tokens == 30
    assert round(stats["111"].total_cost, 2) == 0.03
    assert stats["111"].cost_by_provider == {"gemini": 0.01, "openai": 0.02}


def test_keeps_two_users_usage_independent():
    request_log = RequestLog()
    response_log = ResponseLog()

    e1 = request_log.record(Capability.CHAT, "gemini", telegram_id="111")
    e2 = request_log.record(Capability.CHAT, "gemini", telegram_id="222")
    response_log.record(request_id=e1.request_id, capability=Capability.CHAT, provider_name="gemini", latency_ms=100.0, tokens=10, cost=0.01, status="SUCCESS")
    response_log.record(request_id=e2.request_id, capability=Capability.CHAT, provider_name="gemini", latency_ms=100.0, tokens=99, cost=0.99, status="SUCCESS")

    stats = compute_user_usage(request_log.all(), response_log.all())

    assert stats["111"].total_tokens == 10
    assert stats["222"].total_tokens == 99


def test_requests_with_no_telegram_id_are_excluded():
    request_log = RequestLog()
    response_log = ResponseLog()

    entry = request_log.record(Capability.CHAT, "gemini", telegram_id=None)
    response_log.record(request_id=entry.request_id, capability=Capability.CHAT, provider_name="gemini", latency_ms=100.0, tokens=10, cost=0.01, status="SUCCESS")

    stats = compute_user_usage(request_log.all(), response_log.all())

    assert stats == {}


def test_response_with_unmatched_request_id_is_excluded():
    response_log = ResponseLog()
    response_log.record(request_id="no-matching-request", capability=Capability.CHAT, provider_name="gemini", latency_ms=100.0, tokens=10, cost=0.01, status="SUCCESS")

    stats = compute_user_usage([], response_log.all())

    assert stats == {}


def test_empty_logs_return_empty_dict():
    assert compute_user_usage([], []) == {}
