"""
Phase 52 — DecisionEngine unit tests.

Previously ZERO dedicated tests existed for decision/decision_engine.py
(0% coverage before this phase). Covers the full APPROVE/REJECT/
NO_TRADE branch matrix and the confidence-blending threshold logic,
against the real DecisionEngine/DecisionConfig, no mocking.
"""

from decision.decision_engine import DecisionEngine, DecisionConfig
from decision.models import DecisionAction


def test_approve_when_ai_approved_and_confidence_above_threshold(mock_signal_candidate, mock_ai_result):
    candidate = mock_signal_candidate(confidence=0.90)
    ai_result = mock_ai_result(approved=True, confidence=0.90)

    decision = DecisionEngine().evaluate(candidate, ai_result)

    assert decision.action == DecisionAction.APPROVE
    assert decision.confidence == 0.90


def test_reject_when_ai_not_approved(mock_signal_candidate, mock_ai_result):
    """AI rejection overrides everything else, even a high blended confidence."""
    candidate = mock_signal_candidate(confidence=0.95)
    ai_result = mock_ai_result(approved=False, confidence=0.95)

    decision = DecisionEngine().evaluate(candidate, ai_result)

    assert decision.action == DecisionAction.REJECT
    assert "did not approve" in decision.reason.lower()


def test_reject_when_confidence_below_approve_threshold(mock_signal_candidate, mock_ai_result):
    """AI approves, but blended confidence (0.60) is below the 0.80 approve_confidence default."""
    candidate = mock_signal_candidate(confidence=0.60)
    ai_result = mock_ai_result(approved=True, confidence=0.60)

    decision = DecisionEngine().evaluate(candidate, ai_result)

    assert decision.action == DecisionAction.REJECT
    assert "approval threshold" in decision.reason.lower()


def test_no_trade_when_confidence_below_min_threshold(mock_signal_candidate, mock_ai_result):
    """Blended confidence (0.30) is below the 0.50 min_confidence default -- NO_TRADE, not REJECT."""
    candidate = mock_signal_candidate(confidence=0.30)
    ai_result = mock_ai_result(approved=True, confidence=0.30)

    decision = DecisionEngine().evaluate(candidate, ai_result)

    assert decision.action == DecisionAction.NO_TRADE
    assert "minimum threshold" in decision.reason.lower()


def test_confidence_is_averaged_from_signal_and_ai(mock_signal_candidate, mock_ai_result):
    candidate = mock_signal_candidate(confidence=1.0)
    ai_result = mock_ai_result(approved=True, confidence=0.60)

    decision = DecisionEngine().evaluate(candidate, ai_result)

    assert decision.confidence == 0.80  # (1.0 + 0.60) / 2


def test_custom_thresholds_are_respected(mock_signal_candidate, mock_ai_result):
    """A stricter approve_confidence must reject a signal the default config would approve."""
    strict_config = DecisionConfig(min_confidence=0.50, approve_confidence=0.95)
    engine = DecisionEngine(config=strict_config)

    candidate = mock_signal_candidate(confidence=0.85)
    ai_result = mock_ai_result(approved=True, confidence=0.85)

    decision = engine.evaluate(candidate, ai_result)

    assert decision.action == DecisionAction.REJECT


def test_decision_carries_original_signal_and_ai_analysis(mock_signal_candidate, mock_ai_result):
    candidate = mock_signal_candidate()
    ai_result = mock_ai_result(approved=True, confidence=0.90)

    decision = DecisionEngine().evaluate(candidate, ai_result)

    assert decision.signal is candidate
    assert decision.ai_analysis is ai_result
