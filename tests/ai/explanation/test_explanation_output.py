"""Phase 63.0 TASK 3 — ExplanationOutput contract. Pure data, no generation logic, not read by ExplanationEngine yet."""

from ai_layer.ai_service.content.content_type_vocabulary import ContentType
from ai_layer.explanation_ai.explanation_output import ExplanationOutput


def test_explanation_output_is_pure_data():
    output = ExplanationOutput(
        title="Why gold rallied", summary="A short summary.", body="A longer body.",
        risk_note="Markets can move against any analysis.", invalidation="if price closes below 2300",
        confidence=0.75, language="en",
    )
    assert output.title == "Why gold rallied"
    assert output.confidence == 0.75
    assert output.content_type is None
    assert output.metadata == {}


def test_explanation_output_accepts_a_content_type():
    output = ExplanationOutput(
        title="t", summary="s", body="b", risk_note="r", invalidation="i",
        confidence=0.5, language="uz", content_type=ContentType.DAILY_BRIEF,
    )
    assert output.content_type == ContentType.DAILY_BRIEF


def test_explanation_output_accepts_metadata():
    output = ExplanationOutput(
        title="t", summary="s", body="b", risk_note="r", invalidation="i",
        confidence=0.5, language="en", metadata={"provider_name": "gemini"},
    )
    assert output.metadata == {"provider_name": "gemini"}


def test_explanation_output_phase_63_1_fields_default_to_none():
    """Phase 63.1 TASK 1 extension: six new optional fields, all default None -- additive, not breaking."""
    output = ExplanationOutput(
        title="t", summary="s", body="b", risk_note="r", invalidation="i",
        confidence=0.5, language="en",
    )
    assert output.market_context is None
    assert output.technical_reasoning is None
    assert output.fundamental_reasoning is None
    assert output.risk_reasoning is None
    assert output.educational_note is None
    assert output.persona is None


def test_explanation_output_accepts_phase_63_1_fields():
    output = ExplanationOutput(
        title="t", summary="s", body="b", risk_note="r", invalidation="i",
        confidence=0.5, language="en",
        market_context="Gold remains bullish on H1.",
        technical_reasoning="Liquidity sweep confirmed near demand zone.",
        fundamental_reasoning="US CPI beat expectations.",
        risk_reasoning="Invalidation below previous liquidity low.",
        educational_note="A liquidity sweep is a stop-hunt pattern.",
        persona="Senior Trading AI",
    )
    assert output.market_context == "Gold remains bullish on H1."
    assert output.risk_reasoning == "Invalidation below previous liquidity low."
    assert output.persona == "Senior Trading AI"
