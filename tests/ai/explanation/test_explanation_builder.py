"""Phase 63.1 TASK 2/4 — ExplanationBuilder. Deterministic, no AI call, uses the real (one) Persona."""

from ai_layer.explanation_ai.explanation_builder import ExplanationBuilder
from ai_layer.explanation_ai.explanation_input import ExplanationInput, ExplanationMode
from ai_layer.explanation_ai.explanation_output import ExplanationOutput
from ai_layer.personal_ai.persona_manager.persona_manager import PersonaManager


def test_build_trade_explanation_returns_explanation_output():
    builder = ExplanationBuilder()
    data = ExplanationInput(
        mode=ExplanationMode.TRADE, symbol="XAUUSD", market_bias="BULLISH",
        entry=2350.5, stop_loss=2342.0, take_profit=2368.0, confidence=82,
        risk_reward=2.1, technical_reason="Liquidity sweep + FVG support",
        risk_reason="Invalidation below liquidity zone",
        invalidation="if price closes below 2340",
    )
    output = builder.build(data)

    assert isinstance(output, ExplanationOutput)
    assert output.title == "XAUUSD Trade Explanation"
    assert output.confidence == 0.82
    assert output.technical_reasoning == "Liquidity sweep + FVG support"
    assert output.risk_reasoning == "Invalidation below liquidity zone"
    assert output.market_context == "BULLISH"
    assert "WHY" in output.body


def test_build_no_trade_explanation():
    builder = ExplanationBuilder()
    data = ExplanationInput(
        mode=ExplanationMode.NO_TRADE, symbol="XAUUSD",
        market_condition="Ranging", missing_confirmation="No sweep yet",
        waiting_condition="Wait for H1 close above 2360",
    )
    output = builder.build(data)
    assert "MARKET CONDITION" in output.body
    assert output.educational_note is None


def test_build_education_explanation():
    builder = ExplanationBuilder()
    data = ExplanationInput(
        mode=ExplanationMode.EDUCATION, symbol="XAUUSD",
        concept="Liquidity Sweep", example="Price wicks below a prior low.",
        lesson="Wait for confirmation.",
    )
    output = builder.build(data)
    assert output.educational_note == "Wait for confirmation."
    assert "CONCEPT" in output.body


def test_build_uses_the_active_persona_by_default():
    builder = ExplanationBuilder(persona_manager=PersonaManager())
    data = ExplanationInput(mode=ExplanationMode.TRADE, symbol="XAUUSD")
    output = builder.build(data)
    assert output.persona == "Senior Trading AI"
    assert "Educational content only" in output.risk_note


def test_build_confidence_missing_defaults_to_zero():
    builder = ExplanationBuilder()
    data = ExplanationInput(mode=ExplanationMode.TRADE, symbol="XAUUSD")
    output = builder.build(data)
    assert output.confidence == 0.0


def test_build_confidence_clamps_to_unit_scale():
    builder = ExplanationBuilder()
    data = ExplanationInput(mode=ExplanationMode.TRADE, symbol="XAUUSD", confidence=150)
    output = builder.build(data)
    assert output.confidence == 1.0
