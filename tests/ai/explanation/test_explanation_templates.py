"""Phase 63.1 TASK 3 — Explanation Templates. Pure, deterministic text assembly, no AI call."""

from ai_layer.explanation_ai.explanation_input import ExplanationInput, ExplanationMode
from ai_layer.explanation_ai.explanation_templates import (
    build_education_explanation,
    build_no_trade_explanation,
    build_trade_explanation,
)


def test_trade_template_has_all_five_sections():
    data = ExplanationInput(
        mode=ExplanationMode.TRADE, symbol="XAUUSD", market_bias="BULLISH",
        entry=2350.5, stop_loss=2342.0, take_profit=2368.0, risk_reward=2.1,
        technical_reason="Liquidity sweep + FVG support",
        risk_reason="Invalidation below liquidity zone",
        invalidation="if price closes below 2340",
    )
    body = build_trade_explanation(data)
    for section in ("WHY", "WHAT", "WHERE", "RISK", "INVALIDATION"):
        assert section in body
    assert "Liquidity sweep + FVG support" in body
    assert "if price closes below 2340" in body


def test_trade_template_missing_fields_render_as_not_specified():
    data = ExplanationInput(mode=ExplanationMode.TRADE, symbol="XAUUSD")
    body = build_trade_explanation(data)
    assert "not specified" in body


def test_no_trade_template_has_all_four_sections():
    data = ExplanationInput(
        mode=ExplanationMode.NO_TRADE, symbol="XAUUSD",
        market_condition="Ranging, no clear structure",
        missing_confirmation="No liquidity sweep yet",
        risk_reason="Unclear invalidation level",
        waiting_condition="Wait for H1 close above 2360",
    )
    body = build_no_trade_explanation(data)
    for section in ("MARKET CONDITION", "MISSING CONFIRMATION", "RISK REASON", "WAITING CONDITION"):
        assert section in body
    assert "Wait for H1 close above 2360" in body


def test_education_template_has_all_three_sections():
    data = ExplanationInput(
        mode=ExplanationMode.EDUCATION, symbol="XAUUSD",
        concept="Liquidity Sweep", example="Price wicks below a prior low then reverses.",
        lesson="Wait for confirmation before entering.",
    )
    body = build_education_explanation(data)
    for section in ("CONCEPT", "EXAMPLE", "LESSON"):
        assert section in body
