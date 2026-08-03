"""Phase 61.2 TASK 5 — Response Validator Foundation."""

from ai_layer.ai_engine.providers.base_provider import ProviderResult
from ai_layer.confidence_ai.response_validator import ValidationResult, validate_response
from ai_layer.confidence_ai.safety import check_safety
from ai_layer.confidence_ai.schemas import DEFAULT_SCHEMA, ResponseSchema


def test_valid_response_is_accepted():
    result = validate_response(ProviderResult(content="Gold is trending up."))
    assert result.accepted is True
    assert result.errors == []


def test_empty_content_is_rejected():
    result = validate_response(ProviderResult(content=""))
    assert result.accepted is False
    assert any("empty" in e for e in result.errors)


def test_whitespace_only_content_is_rejected():
    result = validate_response(ProviderResult(content="   "))
    assert result.accepted is False


def test_non_provider_result_is_rejected():
    result = validate_response("not a ProviderResult")
    assert result.accepted is False
    assert "not a ProviderResult instance" in result.errors[0]


def test_missing_required_metadata_key_is_rejected():
    schema = ResponseSchema(required_metadata_keys=("confidence",))
    result = validate_response(ProviderResult(content="ok"), schema=schema)
    assert result.accepted is False
    assert any("confidence" in e for e in result.errors)


def test_confidence_within_range_is_accepted():
    result = validate_response(ProviderResult(content="ok", metadata={"confidence": 0.75}))
    assert result.accepted is True


def test_confidence_above_range_is_rejected():
    result = validate_response(ProviderResult(content="ok", metadata={"confidence": 1.5}))
    assert result.accepted is False


def test_confidence_below_range_is_rejected():
    result = validate_response(ProviderResult(content="ok", metadata={"confidence": -0.1}))
    assert result.accepted is False


def test_non_numeric_confidence_is_rejected():
    result = validate_response(ProviderResult(content="ok", metadata={"confidence": "high"}))
    assert result.accepted is False


def test_trade_directive_content_is_rejected():
    result = validate_response(ProviderResult(content="You should BUY NOW at market price."))
    assert result.accepted is False
    assert any("trade-directive" in e for e in result.errors)


def test_leaked_api_key_pattern_is_rejected():
    fake_key = "AIza" + "x" * 35
    result = validate_response(ProviderResult(content=f"Here is your key: {fake_key}"))
    assert result.accepted is False
    assert any("leaked API key" in e for e in result.errors)


def test_check_safety_returns_empty_list_for_clean_content():
    assert check_safety("Gold is showing bullish momentum.") == []


def test_default_schema_min_content_length_is_one():
    assert DEFAULT_SCHEMA.min_content_length == 1


def test_validation_result_defaults_to_empty_errors():
    result = ValidationResult(accepted=True)
    assert result.errors == []
