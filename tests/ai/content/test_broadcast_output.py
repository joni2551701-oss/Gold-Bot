"""Phase 61.5 TASK 6 — Broadcast Preparation Interface. Contract only -- no real send/schedule/media logic."""

from ai.content.broadcast_output import prepare_broadcast
from ai.content.content_schema import ContentResult


def _accepted_result(body="Gold is in an uptrend."):
    return ContentResult(
        accepted=True, content_type="AI_MARKET_REPORT", title="Market Report",
        body=body, reason="provider call succeeded", generated_at="2026-07-17T00:00:00+00:00",
        provider_name="gemini",
    )


def _rejected_result():
    return ContentResult(
        accepted=False, content_type="AI_MARKET_REPORT", title="Market Report",
        body=None, reason="no runtime method mapping yet", generated_at="2026-07-17T00:00:00+00:00",
    )


def test_prepare_broadcast_adapts_an_accepted_result():
    ready = prepare_broadcast(_accepted_result())

    assert ready is not None
    assert ready.content_type == "AI_MARKET_REPORT"
    assert ready.body == "Gold is in an uptrend."
    assert ready.provider_name == "gemini"


def test_prepare_broadcast_returns_none_for_a_rejected_result():
    assert prepare_broadcast(_rejected_result()) is None


def test_prepare_broadcast_returns_none_for_an_accepted_result_with_no_body():
    empty = _accepted_result(body=None)
    assert prepare_broadcast(empty) is None


def test_broadcast_ready_content_to_dict_is_json_serializable_shape():
    ready = prepare_broadcast(_accepted_result())
    data = ready.to_dict()

    assert data["content_type"] == "AI_MARKET_REPORT"
    assert data["body"] == "Gold is in an uptrend."
    assert data["prepared_at"] == "2026-07-17T00:00:00+00:00"
