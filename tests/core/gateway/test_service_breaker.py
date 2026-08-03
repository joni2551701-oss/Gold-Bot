"""Tests for the service circuit breaker (module 10, amendment 5)."""

from datetime import timedelta

from core_layer.gateway.service_breaker import ServiceCircuitBreaker, BreakerState

from _gfakes import at


def test_starts_closed():
    cb = ServiceCircuitBreaker()
    assert cb.state is BreakerState.CLOSED
    assert cb.allow(at(0)) is True


def test_trips_open_after_threshold():
    cb = ServiceCircuitBreaker(failure_threshold=3)
    cb.record_failure(at(0))
    cb.record_failure(at(1))
    assert cb.state is BreakerState.CLOSED   # under threshold
    cb.record_failure(at(2))
    assert cb.state is BreakerState.OPEN
    assert cb.allow(at(2)) is False          # rejected while open


def test_half_open_after_recovery_then_close_on_success():
    cb = ServiceCircuitBreaker(failure_threshold=1,
                               recovery_timeout=timedelta(seconds=10))
    cb.record_failure(at(0))
    assert cb.state is BreakerState.OPEN
    assert cb.allow(at(5)) is False       # 5s < 10s cooldown
    assert cb.allow(at(10)) is True       # cooldown elapsed
    assert cb.state is BreakerState.HALF_OPEN
    cb.record_success()
    assert cb.state is BreakerState.CLOSED


def test_half_open_failure_reopens():
    cb = ServiceCircuitBreaker(failure_threshold=1,
                               recovery_timeout=timedelta(seconds=10))
    cb.record_failure(at(0))
    cb.allow(at(10))               # -> HALF_OPEN
    assert cb.state is BreakerState.HALF_OPEN
    cb.record_failure(at(11))      # trial fails
    assert cb.state is BreakerState.OPEN


def test_success_resets_failure_count():
    cb = ServiceCircuitBreaker(failure_threshold=3)
    cb.record_failure(at(0))
    cb.record_failure(at(1))
    cb.record_success()
    assert cb.failure_count == 0
    assert cb.state is BreakerState.CLOSED
