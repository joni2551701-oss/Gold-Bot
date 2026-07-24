"""
Pre-Phase 59 Architecture Readiness Review, AC-07 -- API error
classification tests (data/api_error_classifier.py). Extended by
Phase 59.1 TASK 5 (classify_empty_response(), API_003 heuristic).
"""

import requests

from data.api_error_classifier import classify_api_error, classify_empty_response
from core.errors.exceptions import ExternalAPIError
from core.errors import codes


def test_timeout_maps_to_api_001():
    result = classify_api_error(requests.exceptions.Timeout("timed out"))
    assert isinstance(result, ExternalAPIError)
    assert result.code == codes.API_001


def test_connection_error_maps_to_api_001():
    result = classify_api_error(ConnectionError("Failed to fetch data from Twelve Data after 3 attempts."))
    assert result.code == codes.API_001


def test_rate_limit_style_value_error_maps_to_api_002():
    result = classify_api_error(ValueError("Twelve Data API Error: rate limit exceeded"))
    assert result.code == codes.API_002


def test_unrecognized_exception_type_maps_to_api_002():
    result = classify_api_error(RuntimeError("something unexpected"))
    assert result.code == codes.API_002


def test_message_is_preserved():
    result = classify_api_error(ValueError("TWELVE_DATA_API_KEY not configured."))
    assert result.message == "TWELVE_DATA_API_KEY not configured."


def test_module_defaults_to_twelve_data_client():
    result = classify_api_error(ValueError("x"))
    assert result.module == "TwelveDataClient"


def test_module_can_be_overridden():
    result = classify_api_error(ValueError("x"), module="MarketDataNormalizer")
    assert result.module == "MarketDataNormalizer"


def test_details_records_the_exception_type():
    result = classify_api_error(requests.exceptions.Timeout("x"))
    assert result.details["exception_type"] == "Timeout"


def test_classify_api_error_never_raises():
    """Any exception type, even an unusual one, must produce a well-formed ExternalAPIError."""
    for exc in (Exception("generic"), KeyError("missing"), TypeError("bad type")):
        result = classify_api_error(exc)
        assert isinstance(result, ExternalAPIError)


def test_result_is_json_serializable():
    import json

    result = classify_api_error(ValueError("x"))
    json.dumps(result.to_dict())  # must not raise (GoldBotError has to_dict(), no to_json())


def test_invalid_symbol_style_value_error_maps_to_api_003():
    result = classify_api_error(ValueError("Twelve Data API Error: **symbol** parameter is missing or invalid"))
    assert result.code == codes.API_003


def test_symbol_heuristic_is_case_insensitive():
    result = classify_api_error(ValueError("Invalid SYMBOL requested"))
    assert result.code == codes.API_003


def test_rate_limit_message_without_symbol_still_maps_to_api_002():
    """Regression guard: the new symbol heuristic must not shadow the pre-existing API_002 fallback."""
    result = classify_api_error(ValueError("Twelve Data API Error: rate limit exceeded"))
    assert result.code == codes.API_002


def test_classify_empty_response_maps_to_api_004():
    result = classify_empty_response("XAUUSD", "M15")
    assert isinstance(result, ExternalAPIError)
    assert result.code == codes.API_004


def test_classify_empty_response_records_symbol_and_timeframe():
    result = classify_empty_response("EURUSD", "H1")
    assert result.details["symbol"] == "EURUSD"
    assert result.details["timeframe"] == "H1"
    assert "EURUSD" in result.message


def test_classify_empty_response_module_can_be_overridden():
    result = classify_empty_response("XAUUSD", "M15", module="CustomCaller")
    assert result.module == "CustomCaller"


def test_classify_empty_response_never_raises():
    classify_empty_response("", "")  # must not raise even on empty strings
