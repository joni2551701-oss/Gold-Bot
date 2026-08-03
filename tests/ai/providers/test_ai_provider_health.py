"""Phase 61.1 TASK 2 — Provider Health/Status/Failover. No real API call anywhere."""

from ai_layer.ai_engine.providers.provider_failover import select_available
from ai_layer.ai_engine.providers.provider_health import ProviderHealthTracker
from ai_layer.ai_engine.providers.provider_status import AVAILABLE_STATUSES, HealthStatus


def test_every_registered_provider_starts_online():
    tracker = ProviderHealthTracker()
    for name in ("openai", "gemini", "claude", "grok", "local_llm"):
        assert tracker.status_of(name) == HealthStatus.ONLINE
        assert tracker.is_available(name) is True


def test_degraded_is_still_available():
    tracker = ProviderHealthTracker()
    tracker.record("gemini", HealthStatus.DEGRADED, reason="elevated latency")
    assert tracker.is_available("gemini") is True


def test_offline_is_not_available():
    tracker = ProviderHealthTracker()
    tracker.record("gemini", HealthStatus.OFFLINE, reason="timeout")
    assert tracker.is_available("gemini") is False


def test_rate_limited_is_not_available():
    tracker = ProviderHealthTracker()
    tracker.record("gemini", HealthStatus.RATE_LIMITED, reason="429")
    assert tracker.is_available("gemini") is False


def test_disabled_is_not_available():
    tracker = ProviderHealthTracker()
    tracker.record("gemini", HealthStatus.DISABLED)
    assert tracker.is_available("gemini") is False


def test_mark_recovered_returns_provider_to_online():
    tracker = ProviderHealthTracker()
    tracker.record("gemini", HealthStatus.OFFLINE)
    tracker.mark_recovered("gemini")
    assert tracker.status_of("gemini") == HealthStatus.ONLINE
    assert tracker.is_available("gemini") is True


def test_unknown_provider_is_not_available():
    tracker = ProviderHealthTracker()
    assert tracker.status_of("unknown") is None
    assert tracker.is_available("unknown") is False


def test_all_records_returns_every_tracked_provider():
    tracker = ProviderHealthTracker()
    records = tracker.all_records()
    assert set(records.keys()) == {"openai", "gemini", "claude", "grok", "local_llm"}


def test_available_statuses_are_online_and_degraded_only():
    assert AVAILABLE_STATUSES == frozenset({HealthStatus.ONLINE, HealthStatus.DEGRADED})


def test_select_available_returns_first_healthy_candidate():
    tracker = ProviderHealthTracker()
    tracker.record("gemini", HealthStatus.OFFLINE)
    result = select_available(["gemini", "openai", "claude"], tracker)
    assert result == "openai"


def test_select_available_returns_none_when_nothing_healthy():
    tracker = ProviderHealthTracker()
    for name in ("gemini", "openai"):
        tracker.record(name, HealthStatus.OFFLINE)
    assert select_available(["gemini", "openai"], tracker) is None


def test_select_available_on_empty_candidates_returns_none():
    tracker = ProviderHealthTracker()
    assert select_available([], tracker) is None
