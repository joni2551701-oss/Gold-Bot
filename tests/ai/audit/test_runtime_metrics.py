"""Phase 61.6 TASK 4 — AI Runtime Metrics. Extends the existing ai/audit/provider_stats.py -- no new metrics module."""

from datetime import datetime, timedelta, timezone

import pytest

from ai.audit.provider_stats import RuntimeMetricsCollector, compute_requests_per_minute
from ai.audit.request_log import AIRequestLogEntry
from ai.capabilities.capability import Capability
from ai.runtime.event_bus import EventBus, EventType, RuntimeEvent


def _request(created_at):
    return AIRequestLogEntry(request_id="r1", capability=Capability.CHAT, provider_name="gemini", telegram_id=None, created_at=created_at)


def test_compute_requests_per_minute_counts_only_the_last_60_seconds():
    now = datetime(2026, 1, 1, 0, 1, 0, tzinfo=timezone.utc)
    requests = [
        _request(now - timedelta(seconds=10)),
        _request(now - timedelta(seconds=59)),
        _request(now - timedelta(seconds=61)),
        _request(now - timedelta(minutes=5)),
    ]
    assert compute_requests_per_minute(requests, now=now) == 2.0


def test_compute_requests_per_minute_empty_list_is_zero():
    assert compute_requests_per_minute([]) == 0.0


def test_collector_counts_cache_hits_and_misses():
    bus = EventBus()
    collector = RuntimeMetricsCollector(bus)

    bus.publish(RuntimeEvent(event_type=EventType.CACHE_HIT))
    bus.publish(RuntimeEvent(event_type=EventType.CACHE_HIT))
    bus.publish(RuntimeEvent(event_type=EventType.CACHE_MISS))

    metrics = collector.snapshot()
    assert metrics.cache_hits == 2
    assert metrics.cache_misses == 1
    assert metrics.cache_hit_rate == pytest.approx(2 / 3)


def test_collector_cache_hit_rate_is_zero_with_no_data():
    bus = EventBus()
    collector = RuntimeMetricsCollector(bus)
    assert collector.snapshot().cache_hit_rate == 0.0


def test_collector_counts_validation_failures_retries_and_failover():
    bus = EventBus()
    collector = RuntimeMetricsCollector(bus)

    bus.publish(RuntimeEvent(event_type=EventType.VALIDATION_FAILED))
    bus.publish(RuntimeEvent(event_type=EventType.PROVIDER_FAILED))
    bus.publish(RuntimeEvent(event_type=EventType.PROVIDER_FAILED))
    bus.publish(RuntimeEvent(event_type=EventType.PROVIDER_CHANGED))

    metrics = collector.snapshot()
    assert metrics.validation_failures == 1
    assert metrics.retries == 2
    assert metrics.failover_count == 1


def test_collector_ignores_unrelated_events():
    bus = EventBus()
    collector = RuntimeMetricsCollector(bus)

    bus.publish(RuntimeEvent(event_type=EventType.RUNTIME_STARTED))
    bus.publish(RuntimeEvent(event_type=EventType.PROVIDER_RECOVERED))

    metrics = collector.snapshot()
    assert metrics.cache_hits == 0
    assert metrics.retries == 0
    assert metrics.failover_count == 0


def test_collector_snapshot_includes_requests_per_minute_when_given_a_request_log():
    bus = EventBus()
    collector = RuntimeMetricsCollector(bus)
    now = datetime(2026, 1, 1, 0, 1, 0, tzinfo=timezone.utc)
    requests = [_request(now - timedelta(seconds=5))]

    metrics = collector.snapshot(requests=requests, now=now)

    assert metrics.requests_per_minute == 1.0


def test_collector_snapshot_with_no_requests_reports_zero_never_fabricates():
    bus = EventBus()
    collector = RuntimeMetricsCollector(bus)
    assert collector.snapshot().requests_per_minute == 0.0
