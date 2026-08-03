"""
TASK-CORE-003 -- tests for the market-data provider error contract
(data_layer/providers/provider_errors.py).
"""

import pytest

from data_layer.providers.provider_errors import (
    ProviderAuthError,
    ProviderError,
    ProviderRateLimitError,
    ProviderResponseError,
    ProviderTimeoutError,
    ProviderUnavailableError,
    provider_error_for_status,
)


def test_hierarchy_all_subclass_provider_error():
    for cls in (
        ProviderAuthError,
        ProviderTimeoutError,
        ProviderRateLimitError,
        ProviderResponseError,
        ProviderUnavailableError,
    ):
        assert issubclass(cls, ProviderError)


def test_error_carries_provider_and_message():
    err = ProviderAuthError("twelvedata", "bad key")
    assert err.provider == "twelvedata"
    assert err.message == "bad key"
    assert "twelvedata" in str(err)
    assert "bad key" in str(err)


def test_error_str_without_message_is_just_provider():
    err = ProviderError("bitget")
    assert str(err) == "bitget"


def test_error_can_be_raised_and_caught_as_base():
    with pytest.raises(ProviderError):
        raise ProviderTimeoutError("keynorq", "timed out")


@pytest.mark.parametrize("status,expected", [
    (401, ProviderAuthError),
    (403, ProviderAuthError),
    (404, ProviderResponseError),
    (429, ProviderRateLimitError),
    (500, ProviderUnavailableError),
    (503, ProviderUnavailableError),
    (400, ProviderResponseError),
    (418, ProviderResponseError),
])
def test_provider_error_for_status_maps_codes(status, expected):
    err = provider_error_for_status("binance", status)
    assert isinstance(err, expected)
    assert err.provider == "binance"


def test_provider_error_for_status_unknown_code_is_base():
    err = provider_error_for_status("binance", 302)
    assert type(err) is ProviderError


def test_provider_error_for_status_chains_cause():
    cause = ValueError("boom")
    err = provider_error_for_status("twelvedata", 500, "server error", cause=cause)
    assert err.__cause__ is cause


def test_error_message_never_contains_a_secret_the_caller_did_not_add():
    # The contract: the error only holds what the caller passes. A
    # caller passing a safe reason yields a safe repr.
    err = provider_error_for_status("bitget", 401, "auth rejected")
    assert "auth rejected" in str(err)
    assert "api_key" not in repr(err).lower()
