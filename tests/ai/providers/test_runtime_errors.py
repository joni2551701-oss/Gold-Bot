"""Phase 61.2 TASK 4 — Provider Runtime Error Handling. No real network call anywhere; API key never appears in any message."""

import requests

from ai.providers.provider_health import ProviderHealthTracker
from ai.providers.provider_status import HealthStatus
from ai.providers.runtime_errors import (
    ProviderInvalidResponseError,
    ProviderRateLimitError,
    ProviderRuntimeError,
    ProviderTimeoutError,
    ProviderUnavailableError,
    classify_provider_exception,
    record_provider_failure,
)


def test_provider_runtime_error_message_never_contains_a_passed_secret_by_accident():
    error = ProviderUnavailableError("gemini", "GEMINI_API_KEY not configured")
    assert "gemini" in str(error)
    assert "not configured" in str(error)


def test_classify_timeout_exception():
    classified = classify_provider_exception(requests.exceptions.Timeout(), "gemini")
    assert isinstance(classified, ProviderTimeoutError)
    assert classified.provider_name == "gemini"


def test_classify_generic_request_exception():
    classified = classify_provider_exception(requests.exceptions.ConnectionError(), "gemini")
    assert isinstance(classified, ProviderUnavailableError)


def test_classify_unrecognized_exception_falls_back_to_unavailable():
    classified = classify_provider_exception(ValueError("something else"), "gemini")
    assert isinstance(classified, ProviderUnavailableError)


def test_all_error_types_are_provider_runtime_errors():
    for cls in (ProviderTimeoutError, ProviderRateLimitError, ProviderInvalidResponseError, ProviderUnavailableError):
        assert issubclass(cls, ProviderRuntimeError)


def test_record_provider_failure_maps_timeout_to_offline():
    tracker = ProviderHealthTracker()
    error = ProviderTimeoutError("gemini", "request timed out")
    record_provider_failure(tracker, error)
    assert tracker.status_of("gemini") == HealthStatus.OFFLINE


def test_record_provider_failure_maps_rate_limit_to_rate_limited():
    tracker = ProviderHealthTracker()
    error = ProviderRateLimitError("gemini", "rate limited")
    record_provider_failure(tracker, error)
    assert tracker.status_of("gemini") == HealthStatus.RATE_LIMITED
    assert tracker.is_available("gemini") is False


def test_record_provider_failure_maps_invalid_response_to_degraded():
    tracker = ProviderHealthTracker()
    error = ProviderInvalidResponseError("gemini", "bad shape")
    record_provider_failure(tracker, error)
    assert tracker.status_of("gemini") == HealthStatus.DEGRADED
    assert tracker.is_available("gemini") is True  # DEGRADED is still usable


def test_record_provider_failure_maps_unavailable_to_offline():
    tracker = ProviderHealthTracker()
    error = ProviderUnavailableError("gemini", "no key")
    record_provider_failure(tracker, error)
    assert tracker.status_of("gemini") == HealthStatus.OFFLINE
