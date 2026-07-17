"""Phase 63.0 TASK 3 — ExplanationOutput contract. Pure data, no generation logic, not read by ExplanationEngine yet."""

from ai.content.content_types import ContentType
from ai.explanation.explanation_output import ExplanationOutput


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
