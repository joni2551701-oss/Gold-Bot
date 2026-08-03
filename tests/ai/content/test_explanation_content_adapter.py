"""Phase 63.1 TASK 6 — Explanation-to-Content adapter. Reuses BroadcastReadyContent (Phase 61.5), never a new parallel model."""

from ai_layer.ai_service.content.broadcast_output import BroadcastReadyContent
from ai_layer.ai_service.content.explanation_content_adapter import explanation_to_broadcast_ready
from ai_layer.explanation_ai.explanation_output import ExplanationOutput


def test_explanation_to_broadcast_ready_reuses_existing_contract():
    explanation = ExplanationOutput(
        title="XAUUSD Trade Explanation", summary="s", body="Full explanation body.",
        risk_note="r", invalidation="i", confidence=0.8, language="en",
    )
    ready = explanation_to_broadcast_ready(explanation)

    assert isinstance(ready, BroadcastReadyContent)
    assert ready.title == "XAUUSD Trade Explanation"
    assert ready.body == "Full explanation body."
    assert ready.content_type == "EXPLANATION"
    assert ready.provider_name is None


def test_explanation_to_broadcast_ready_never_returns_none():
    """Unlike ai.content.broadcast_output.prepare_broadcast(), this never rejects -- every ExplanationOutput has a real title/body by construction."""
    explanation = ExplanationOutput(
        title="t", summary="s", body="b", risk_note="r", invalidation="i",
        confidence=0.0, language="en",
    )
    assert explanation_to_broadcast_ready(explanation) is not None
