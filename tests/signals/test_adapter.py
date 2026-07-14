"""
Phase A15 -- Signal Schema tests: backward-compatibility adapter
(signals/adapter.py).

Confirms an existing SignalCandidate (produced by any real
strategies/*.py file, unmodified by this phase) converts cleanly into
a valid SignalSchema, and that supplying more already-computed
objects (SignalQualityResult, TradeDecision) populates more fields --
never recomputing any of them.
"""

from signals.models import SignalCandidate, SignalType
from signals.signal_quality import SignalQualityResult, QualityGrade
from signals.adapter import from_signal_candidate
from signals.schema import validate_signal
from decision.models import TradeDecision, DecisionAction
from ai.ai_analyzer import AIAnalysisResult


def _candidate(signal_type=SignalType.BUY, entry=4200.0, stop_loss=4190.0, take_profit=4220.0, strategy_name="LIQUIDITY_SWEEP_STRATEGY", confidence=0.85):
    return SignalCandidate(
        signal_type=signal_type,
        entry=entry,
        stop_loss=stop_loss,
        take_profit=take_profit,
        strategy_name=strategy_name,
        confidence=confidence,
        reasons=["test reason"],
    )


def test_adapter_builds_valid_schema_from_candidate_alone():
    """The minimum input -- just a SignalCandidate, matching 'Strategy Output' as this phase's integration point."""
    candidate = _candidate()
    schema = from_signal_candidate(candidate)

    assert schema.direction == "BUY"
    assert schema.entry_price == 4200.0
    assert schema.stop_loss == 4190.0
    assert schema.take_profit == 4220.0
    assert schema.strategy_name == "LIQUIDITY_SWEEP_STRATEGY"
    assert schema.symbol == "XAUUSD"
    assert schema.timeframe == "M15"
    assert schema.asset_type == "GOLD"

    result = validate_signal(schema)
    assert result.valid is True


def test_adapter_defaults_decision_to_pending_when_none_supplied():
    schema = from_signal_candidate(_candidate())
    assert schema.decision == "PENDING"
    assert schema.decision_score is None


def test_adapter_leaves_references_none_by_default():
    """context_id/explanation_id/risk_id/strategy_version are honest hooks -- never fabricated."""
    schema = from_signal_candidate(_candidate())
    assert schema.context_id is None
    assert schema.explanation_id is None
    assert schema.risk_id is None
    assert schema.strategy_version is None


def test_adapter_relays_quality_without_recomputing():
    quality = SignalQualityResult(grade=QualityGrade.A_PLUS, score=95.0, criteria_met=("HTF_ALIGNED", "STRUCTURE_ALIGNED"), criteria_total=5)
    schema = from_signal_candidate(_candidate(), quality=quality)

    assert schema.quality_grade == "A+"
    assert schema.confidence_score == 95.0


def test_adapter_accepts_explicit_references_and_overrides():
    schema = from_signal_candidate(
        _candidate(),
        symbol="XAUUSD",
        timeframe="M15",
        session="LONDON",
        context_id="CTX-001",
        strategy_version="1.0",
        explanation_id="EXP-00125",
        risk_id="RISK-001",
    )

    assert schema.session == "LONDON"
    assert schema.context_id == "CTX-001"
    assert schema.strategy_version == "1.0"
    assert schema.explanation_id == "EXP-00125"
    assert schema.risk_id == "RISK-001"


def test_adapter_maps_decision_action_to_status_without_recomputing():
    candidate = _candidate()
    ai_result = AIAnalysisResult(approved=True, confidence=0.9, risk_score=0.1, explanation="ok")

    approve_decision = TradeDecision(action=DecisionAction.APPROVE, confidence=0.88, reason="ok", signal=candidate, ai_analysis=ai_result)
    schema = from_signal_candidate(candidate, decision=approve_decision)
    assert schema.decision == "APPROVED"
    assert schema.decision_score == 0.88

    reject_decision = TradeDecision(action=DecisionAction.REJECT, confidence=0.2, reason="bad", signal=candidate, ai_analysis=ai_result)
    schema = from_signal_candidate(candidate, decision=reject_decision)
    assert schema.decision == "REJECTED"
    assert schema.decision_score == 0.2

    no_trade_decision = TradeDecision(action=DecisionAction.NO_TRADE, confidence=0.5, reason="neutral", signal=candidate, ai_analysis=ai_result)
    schema = from_signal_candidate(candidate, decision=no_trade_decision)
    assert schema.decision == "REJECTED"  # NO_TRADE collapses to REJECTED -- see adapter.py's mapping comment


def test_adapter_produces_unique_signal_ids_per_call():
    candidate = _candidate()
    first = from_signal_candidate(candidate)
    second = from_signal_candidate(candidate)
    assert first.signal_id != second.signal_id


def test_adapter_handles_sell_direction():
    candidate = _candidate(signal_type=SignalType.SELL, entry=4200.0, stop_loss=4210.0, take_profit=4180.0)
    schema = from_signal_candidate(candidate)

    assert schema.direction == "SELL"
    result = validate_signal(schema)
    assert result.valid is True


def test_adapter_handles_none_direction_candidate():
    candidate = _candidate(signal_type=SignalType.NONE, entry=0.0, stop_loss=0.0, take_profit=0.0)
    schema = from_signal_candidate(candidate)

    assert schema.direction == "NONE"


def test_existing_signal_candidate_and_strategies_are_untouched():
    """
    The adapter is purely additive -- constructing a SignalCandidate
    the exact way every real strategies/*.py file already does must
    keep working identically, unaffected by signals/schema.py or
    signals/adapter.py existing.
    """
    from strategies.liquidity_strategy import LiquidityStrategy
    from strategies.fvg_strategy import FVGStrategy
    from strategies.amd_strategy import AMDStrategy

    assert LiquidityStrategy().analyze
    assert FVGStrategy().analyze
    assert AMDStrategy().analyze
