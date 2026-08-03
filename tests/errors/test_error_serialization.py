"""
Phase A18 -- Error Classification tests: serialization
(GoldBotError.to_dict()).
"""

import json

from core_layer.errors import codes
from core_layer.errors.exceptions import DataError, PermissionError


def test_to_dict_matches_required_shape():
    error = DataError(code=codes.DATA_001, message="Invalid candle", module="MarketData")
    data = error.to_dict()

    assert data["type"] == "DataError"
    assert data["code"] == "DATA_001"
    assert data["message"] == "Invalid candle"
    assert data["module"] == "MarketData"
    assert "timestamp" in data
    assert "details" in data


def test_to_dict_type_reflects_the_actual_subclass():
    error = PermissionError(code=codes.PERMISSION_001, message="Not authorized", module="TelegramHandlers")
    assert error.to_dict()["type"] == "PermissionError"


def test_to_dict_timestamp_is_iso8601_string():
    error = DataError(code=codes.DATA_001, message="x", module="M")
    data = error.to_dict()

    assert isinstance(data["timestamp"], str)
    # must be parseable back -- the whole point of ISO-8601
    from datetime import datetime
    datetime.fromisoformat(data["timestamp"])


def test_to_dict_is_json_safe():
    error = DataError(
        code=codes.DATA_001, message="Invalid candle", module="MarketData",
        details={"symbol": "XAUUSD", "candle_index": 42},
    )
    data = error.to_dict()

    serialized = json.dumps(data)  # raises TypeError if anything isn't JSON-native
    restored = json.loads(serialized)
    assert restored["details"]["symbol"] == "XAUUSD"


def test_to_dict_details_defaults_to_empty_dict():
    error = DataError(code=codes.DATA_001, message="x", module="M")
    assert error.to_dict()["details"] == {}


def test_logger_error_accepts_to_dict_output_directly():
    """docs/ERROR_HANDLING.md's own rule: logger.error(error.to_dict()) must not raise."""
    import logging

    logger = logging.getLogger("test_error_serialization")
    error = DataError(code=codes.DATA_001, message="Invalid candle", module="MarketData")

    logger.error(error.to_dict())  # must not raise


def test_to_dict_matches_brief_example_shape():
    """{"type":"DataError","code":"DATA_001","message":"Invalid candle","module":"MarketData"} -- every one of these keys must be present with these exact values."""
    error = DataError(code="DATA_001", message="Invalid candle", module="MarketData")
    data = error.to_dict()

    expected_subset = {
        "type": "DataError",
        "code": "DATA_001",
        "message": "Invalid candle",
        "module": "MarketData",
    }
    for key, value in expected_subset.items():
        assert data[key] == value
