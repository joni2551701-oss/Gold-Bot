"""
Phase 52 — DecisionEngine unit tests. Phase A3 (Decision Engine v2):
extended for the weighted signal/HTF/risk/AI formula that replaced
the flat (signal + ai) / 2 average.

Covers the full APPROVE/REJECT/NO_TRADE branch matrix, the weighted-
confidence formula (DecisionWeights: signal=0.40, htf=0.25, risk=0.20,
ai=0.15), HTF Bias's contribution and quality-based dampening, and
backward compatibility (evaluate() without an htf_bias argument) --
against the real DecisionEngine/DecisionConfig/DecisionWeights, no
mocking.
"""

import pytest

from decision_layer.decision_engine.decision_engine import DecisionEngine, DecisionConfig, DecisionWeights
from decision_layer.decision_engine.models import DecisionAction
from context_layer.trend.htf_bias import HTFBias, HTFBiasResult


def _htf(bias, quality_score=1.0, confidence=100.0, timeframes=("Daily", "H4", "H1")):
    """Test-local HTFBiasResult builder -- isolates Decision Engine tests from context_layer/trend/htf_bias.py's own compute_htf_bias() logic."""
    return HTFBiasResult(bias=bias, confidence=confidence, timeframes=timeframes, quality_score=quality_score)


def test_approve_when_ai_approved_and_confidence_above_threshold(mock_signal_candidate, mock_ai_result):
    """
    signal=0.90, ai=0.90, no HTF (neutral 0.5), ai risk_score default
    0.1 (risk component 0.9): 0.40*0.90 + 0.25*0.5 + 0.20*0.9 + 0.15*0.90 = 0.80.
    """
    candidate = mock_signal_candidate(confidence=0.90)
    ai_result = mock_ai_result(approved=True, confidence=0.90)

    decision = DecisionEngine().evaluate(candidate, ai_result)

    assert decision.action == DecisionAction.APPROVE
    assert decision.confidence == pytest.approx(0.80)


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


def test_confidence_is_a_weighted_blend_of_all_four_components(mock_signal_candidate, mock_ai_result):
    """
    Phase A3: confidence is no longer a flat (signal + ai) / 2 average.
    signal=1.0, ai=0.60, ai risk_score=0.1 (risk component 0.9), no HTF (neutral 0.5):
    0.40*1.0 + 0.25*0.5 + 0.20*0.9 + 0.15*0.60 = 0.795 (below the 0.80
    approve threshold -- REJECT, unlike the pre-A3 flat-average result
    of 0.80/APPROVE for these same signal/ai inputs).
    """
    candidate = mock_signal_candidate(confidence=1.0)
    ai_result = mock_ai_result(approved=True, confidence=0.60)

    decision = DecisionEngine().evaluate(candidate, ai_result)

    assert decision.confidence == pytest.approx(0.795)
    assert decision.action == DecisionAction.REJECT


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


# ---------------------------------------------------------------------------
# Phase A3 -- Decision Engine v2 (HTF Integration)
# ---------------------------------------------------------------------------


def test_bullish_htf_increases_confidence_over_neutral(mock_signal_candidate, mock_ai_result):
    """signal=0.5, ai=0.5, ai risk_score=0.5 (risk component 0.5) held fixed; only HTF bias varies."""
    candidate = mock_signal_candidate(confidence=0.5)
    ai_result = mock_ai_result(approved=True, confidence=0.5, risk_score=0.5)

    neutral = DecisionEngine().evaluate(candidate, ai_result, _htf(HTFBias.NEUTRAL))
    bullish = DecisionEngine().evaluate(candidate, ai_result, _htf(HTFBias.BULLISH))

    assert neutral.confidence == pytest.approx(0.5)
    assert bullish.confidence == pytest.approx(0.625)
    assert bullish.confidence > neutral.confidence


def test_bearish_htf_decreases_confidence_below_neutral(mock_signal_candidate, mock_ai_result):
    candidate = mock_signal_candidate(confidence=0.5)
    ai_result = mock_ai_result(approved=True, confidence=0.5, risk_score=0.5)

    neutral = DecisionEngine().evaluate(candidate, ai_result, _htf(HTFBias.NEUTRAL))
    bearish = DecisionEngine().evaluate(candidate, ai_result, _htf(HTFBias.BEARISH))

    assert bearish.confidence == pytest.approx(0.375)
    assert bearish.confidence < neutral.confidence


def test_neutral_and_unknown_htf_contribute_identically(mock_signal_candidate, mock_ai_result):
    """UNKNOWN must never push the outcome either direction -- same as NEUTRAL, by design (HTF_BIAS.md)."""
    candidate = mock_signal_candidate(confidence=0.5)
    ai_result = mock_ai_result(approved=True, confidence=0.5, risk_score=0.5)

    neutral = DecisionEngine().evaluate(candidate, ai_result, _htf(HTFBias.NEUTRAL))
    unknown = DecisionEngine().evaluate(candidate, ai_result, _htf(HTFBias.UNKNOWN))

    assert unknown.confidence == pytest.approx(neutral.confidence)


def test_poor_quality_htf_is_dampened_not_rejected(mock_signal_candidate, mock_ai_result):
    """
    Step 5: quality 100% -> full weight, quality 0% -> neutral
    contribution, never an automatic rejection. Bullish bias at
    quality=0.0 must land exactly on the neutral value; quality=0.6
    must land strictly between neutral and full-bullish.
    """
    candidate = mock_signal_candidate(confidence=0.5)
    ai_result = mock_ai_result(approved=True, confidence=0.5, risk_score=0.5)

    zero_quality = DecisionEngine().evaluate(candidate, ai_result, _htf(HTFBias.BULLISH, quality_score=0.0))
    partial_quality = DecisionEngine().evaluate(candidate, ai_result, _htf(HTFBias.BULLISH, quality_score=0.6))
    full_quality = DecisionEngine().evaluate(candidate, ai_result, _htf(HTFBias.BULLISH, quality_score=1.0))

    assert zero_quality.confidence == pytest.approx(0.5)  # fully collapsed to neutral
    assert zero_quality.confidence < partial_quality.confidence < full_quality.confidence
    assert partial_quality.confidence == pytest.approx(0.575)


def test_htf_bias_can_flip_approve_reject_across_the_threshold(mock_signal_candidate, mock_ai_result):
    """
    Acceptance criterion: HTF Bias actively influences the Decision
    Engine. signal=0.75, ai=0.75, ai risk_score=0.1 (risk component
    0.9): neutral/no-HTF confidence 0.7175 -> REJECT (below 0.80).
    The identical signal+AI pair with a bullish HTF read reaches
    0.8425 -> APPROVE. Nothing about the signal or AI analysis changed
    -- only the HTF context did.
    """
    candidate = mock_signal_candidate(confidence=0.75)
    ai_result = mock_ai_result(approved=True, confidence=0.75, risk_score=0.1)

    no_htf = DecisionEngine().evaluate(candidate, ai_result)
    with_bullish_htf = DecisionEngine().evaluate(candidate, ai_result, _htf(HTFBias.BULLISH))

    assert no_htf.action == DecisionAction.REJECT
    assert with_bullish_htf.action == DecisionAction.APPROVE


def test_weighted_components_are_individually_correct(mock_signal_candidate, mock_ai_result):
    """
    signal=0.8, ai=0.6, ai risk_score=0.2 (risk component 0.8), HTF
    bullish quality=1.0 (htf_score=1.0):
    0.40*0.8 + 0.25*1.0 + 0.20*0.8 + 0.15*0.6 = 0.82. Verifies every
    exposed explainability field (Step 6), not just the final blend.
    """
    candidate = mock_signal_candidate(confidence=0.8)
    ai_result = mock_ai_result(approved=True, confidence=0.6, risk_score=0.2)

    decision = DecisionEngine().evaluate(candidate, ai_result, _htf(HTFBias.BULLISH, quality_score=1.0))

    assert decision.signal_score == pytest.approx(0.8)
    assert decision.htf_score == pytest.approx(1.0)
    assert decision.risk_score == pytest.approx(0.8)
    assert decision.ai_score == pytest.approx(0.6)
    assert decision.final_score == pytest.approx(0.82)
    assert decision.confidence == decision.final_score


def test_custom_weights_are_respected(mock_signal_candidate, mock_ai_result):
    """DecisionWeights are injectable, matching DecisionConfig's existing pattern -- never hardcoded inline."""
    htf_only_weights = DecisionWeights(signal_weight=0.0, htf_weight=1.0, risk_weight=0.0, ai_weight=0.0)
    engine = DecisionEngine(weights=htf_only_weights)

    candidate = mock_signal_candidate(confidence=0.1)
    ai_result = mock_ai_result(approved=True, confidence=0.1, risk_score=0.9)

    decision = engine.evaluate(candidate, ai_result, _htf(HTFBias.BULLISH))

    assert decision.confidence == pytest.approx(1.0)  # 100% weight on a fully-bullish HTF read


def test_evaluate_without_htf_bias_argument_still_works(mock_signal_candidate, mock_ai_result):
    """
    Backward compatibility: htf_bias is optional and defaults to None
    -- any pre-Phase-A2/A3 call site keeps working unchanged, and gets
    the same neutral HTF contribution as an explicit UNKNOWN/quality=0
    result.
    """
    candidate = mock_signal_candidate(confidence=0.5)
    ai_result = mock_ai_result(approved=True, confidence=0.5, risk_score=0.5)

    without_arg = DecisionEngine().evaluate(candidate, ai_result)
    explicit_none = DecisionEngine().evaluate(candidate, ai_result, None)

    assert without_arg.confidence == pytest.approx(0.5)
    assert without_arg.confidence == explicit_none.confidence
    assert without_arg.action in (DecisionAction.APPROVE, DecisionAction.REJECT, DecisionAction.NO_TRADE)


def test_decision_still_carries_signal_and_ai_analysis_with_htf(mock_signal_candidate, mock_ai_result):
    """The pre-existing signal/ai_analysis contract is unaffected by adding HTF/explainability fields."""
    candidate = mock_signal_candidate()
    ai_result = mock_ai_result(approved=True, confidence=0.90)

    decision = DecisionEngine().evaluate(candidate, ai_result, _htf(HTFBias.BULLISH))

    assert decision.signal is candidate
    assert decision.ai_analysis is ai_result


def test_all_component_scores_and_final_confidence_stay_within_0_and_1(mock_signal_candidate, mock_ai_result):
    """Confidence-bounds invariant across extreme inputs and every HTF bias/quality combination."""
    extremes = [
        (0.0, 0.0, 0.0),
        (1.0, 1.0, 1.0),
        (0.0, 1.0, 1.0),
        (1.0, 0.0, 0.0),
    ]
    htf_scenarios = [
        None,
        _htf(HTFBias.BULLISH, quality_score=0.0),
        _htf(HTFBias.BULLISH, quality_score=1.0),
        _htf(HTFBias.BEARISH, quality_score=0.3),
        _htf(HTFBias.NEUTRAL, quality_score=1.0),
        _htf(HTFBias.UNKNOWN, quality_score=1.0),
    ]

    for signal_conf, ai_conf, ai_risk in extremes:
        for htf in htf_scenarios:
            candidate = mock_signal_candidate(confidence=signal_conf)
            ai_result = mock_ai_result(approved=True, confidence=ai_conf, risk_score=ai_risk)

            decision = DecisionEngine().evaluate(candidate, ai_result, htf)

            for value in (
                decision.signal_score, decision.htf_score, decision.risk_score,
                decision.ai_score, decision.final_score, decision.confidence,
            ):
                assert 0.0 <= value <= 1.0


def test_threshold_actions_still_map_correctly_under_the_new_formula(mock_signal_candidate, mock_ai_result):
    """Same three-branch (APPROVE/REJECT/NO_TRADE) threshold logic, now driven by the weighted final_confidence."""
    low = mock_signal_candidate(confidence=0.0)
    low_ai = mock_ai_result(approved=True, confidence=0.0, risk_score=1.0)
    no_trade = DecisionEngine().evaluate(low, low_ai, _htf(HTFBias.NEUTRAL))
    assert no_trade.action == DecisionAction.NO_TRADE

    high = mock_signal_candidate(confidence=1.0)
    high_ai = mock_ai_result(approved=True, confidence=1.0, risk_score=0.0)
    approve = DecisionEngine().evaluate(high, high_ai, _htf(HTFBias.BULLISH))
    assert approve.action == DecisionAction.APPROVE
    assert approve.confidence == pytest.approx(1.0)

