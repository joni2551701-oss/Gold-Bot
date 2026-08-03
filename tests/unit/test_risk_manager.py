"""
Phase 52 — RiskManager unit tests.

Previously ZERO dedicated tests existed for risk_layer/risk_engine/risk_manager.py (the
geometry-validation fix from the earlier critical-bug-fix phase was
only ever verified with ad-hoc scripts in chat, never captured as a
permanent regression test). This file closes that gap: geometry
validation, stop-loss distance validation, and the APPROVE-only gate,
using the real RiskManager/DecisionEngine, no mocking.
"""

from decision_layer.decision_engine.decision_engine import DecisionEngine
from decision_layer.decision_engine.models import DecisionAction
from risk_layer.risk_engine.risk_manager import RiskManager


def _decision(candidate, ai_result):
    return DecisionEngine().evaluate(candidate, ai_result)


def test_valid_buy_geometry_passes(mock_signal_candidate, mock_ai_result):
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4080.0)
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    assert decision.action == DecisionAction.APPROVE

    result = RiskManager().evaluate(decision)
    assert result.approved is True
    assert "PASSED" not in result.reason  # sanity: no hardcoded literal leak
    assert result.risk_reward > 0


def test_valid_sell_geometry_passes(mock_signal_candidate, mock_ai_result):
    from signal_layer.signal_builder.models import SignalType

    candidate = mock_signal_candidate(
        signal_type=SignalType.SELL, entry=4111.40, stop_loss=4116.00, take_profit=4090.00,
    )
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    assert decision.action == DecisionAction.APPROVE

    result = RiskManager().evaluate(decision)
    assert result.approved is True


def test_invalid_buy_geometry_blocked(mock_signal_candidate, mock_ai_result):
    """BUY requires stop_loss < entry < take_profit. TP below entry must block."""
    candidate = mock_signal_candidate(entry=4065.65, stop_loss=4060.00, take_profit=4065.54)
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    assert decision.action == DecisionAction.APPROVE  # Decision layer doesn't check geometry

    result = RiskManager().evaluate(decision)
    assert result.approved is False
    assert "geometry" in result.reason.lower()


def test_invalid_sell_geometry_blocked(mock_signal_candidate, mock_ai_result):
    """SELL requires take_profit < entry < stop_loss. SL below entry must block."""
    from signal_layer.signal_builder.models import SignalType

    candidate = mock_signal_candidate(
        signal_type=SignalType.SELL, entry=4111.40, stop_loss=4111.33, take_profit=4090.00,
    )
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    assert decision.action == DecisionAction.APPROVE

    result = RiskManager().evaluate(decision)
    assert result.approved is False
    assert "geometry" in result.reason.lower()


def test_zero_stop_loss_distance_blocked(mock_signal_candidate, mock_ai_result):
    """entry == stop_loss is also invalid geometry (stop_loss is not < entry)."""
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4065.0, take_profit=4075.0)
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))

    result = RiskManager().evaluate(decision)
    assert result.approved is False


def test_risk_blocked_when_decision_is_reject(mock_signal_candidate, mock_ai_result):
    """RiskManager never evaluates geometry for a non-APPROVE decision -- short-circuits first."""
    candidate = mock_signal_candidate()
    decision = _decision(candidate, mock_ai_result(approved=False))
    assert decision.action == DecisionAction.REJECT

    result = RiskManager().evaluate(decision)
    assert result.approved is False
    assert "not APPROVE" in result.reason


def test_risk_reward_calculation():
    manager = RiskManager()
    rr = manager.calculate_risk_reward(entry=4065.0, stop_loss=4060.0, take_profit=4080.0)
    assert rr == 3.0  # (4080-4065)/(4065-4060) = 15/5


def test_position_size_zero_when_stop_loss_distance_zero():
    manager = RiskManager()
    assert manager.calculate_position_size(risk_amount=100.0, stop_loss_distance=0.0) == 0.0
