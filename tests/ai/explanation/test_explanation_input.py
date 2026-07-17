"""Phase 63.1 TASK 2 — ExplanationInput contract. Primitive values only, never a decision/risk object."""

from ai.explanation.explanation_input import ExplanationInput, ExplanationMode


def test_explanation_input_trade_mode():
    data = ExplanationInput(
        mode=ExplanationMode.TRADE, symbol="XAUUSD", market_bias="BULLISH",
        entry=2350.50, stop_loss=2342.00, take_profit=2368.00,
        confidence=82, risk_reward=2.1,
        technical_reason="Liquidity sweep + FVG support",
        risk_reason="Invalidation below liquidity zone",
    )
    assert data.mode is ExplanationMode.TRADE
    assert data.symbol == "XAUUSD"
    assert data.entry == 2350.50
    assert data.language == "en"


def test_explanation_input_no_trade_mode_defaults():
    data = ExplanationInput(mode=ExplanationMode.NO_TRADE, symbol="XAUUSD")
    assert data.market_condition is None
    assert data.missing_confirmation is None
    assert data.waiting_condition is None


def test_explanation_input_education_mode():
    data = ExplanationInput(
        mode=ExplanationMode.EDUCATION, symbol="XAUUSD",
        concept="Liquidity Sweep", example="Price wicks below a prior low then reverses.",
        lesson="Wait for confirmation before entering.",
    )
    assert data.concept == "Liquidity Sweep"
    assert data.lesson == "Wait for confirmation before entering."


def test_explanation_input_never_carries_a_decision_or_risk_object():
    """The whole point of this contract (Phase 63.1 Director Decision): only primitives, never DecisionResult/RiskResult."""
    import dataclasses

    field_types = {f.name: f.type for f in dataclasses.fields(ExplanationInput)}
    for name, type_repr in field_types.items():
        assert "DecisionResult" not in str(type_repr), name
        assert "RiskResult" not in str(type_repr), name
        assert "TradeContext" not in str(type_repr), name
