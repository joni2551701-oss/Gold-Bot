"""
Phase V1.0.1 (Risk Management Hardening Patch) -- TASK 1 (Risk Per
Trade Protection), TASK 2 (Risk Calculation Validation), TASK 3
(Minimum Risk Reward Protection) tests.
"""

from decision_layer.decision_engine.decision_engine import DecisionEngine
from risk_layer.risk_engine.risk_manager import RiskConfig


def _decision(candidate, ai_result):
    return DecisionEngine().evaluate(candidate, ai_result)


# ---------------------------------------------------------------------------
# TASK 1: Risk Per Trade Protection
# ---------------------------------------------------------------------------

def test_default_risk_per_trade_is_within_default_bounds():
    config = RiskConfig()
    assert config.min_risk_per_trade <= config.risk_per_trade <= config.max_risk_per_trade


def test_risk_per_trade_at_exact_minimum_is_allowed(risk_manager, mock_signal_candidate, mock_ai_result):
    risk_manager.config = RiskConfig(risk_per_trade=0.001, min_risk_per_trade=0.001, max_risk_per_trade=0.02)
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4080.0)
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    result = risk_manager.evaluate(decision)
    assert result.approved is True


def test_risk_per_trade_at_exact_maximum_is_allowed(risk_manager, mock_signal_candidate, mock_ai_result):
    risk_manager.config = RiskConfig(risk_per_trade=0.02, min_risk_per_trade=0.001, max_risk_per_trade=0.02)
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4080.0)
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    result = risk_manager.evaluate(decision)
    assert result.approved is True


def test_risk_per_trade_below_minimum_is_rejected(risk_manager, mock_signal_candidate, mock_ai_result):
    risk_manager.config = RiskConfig(risk_per_trade=0.0001, min_risk_per_trade=0.001, max_risk_per_trade=0.02)
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4080.0)
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    result = risk_manager.evaluate(decision)
    assert result.approved is False
    assert "Risk limit exceeded" in result.reason


def test_risk_per_trade_above_maximum_is_rejected(risk_manager, mock_signal_candidate, mock_ai_result):
    risk_manager.config = RiskConfig(risk_per_trade=0.05, min_risk_per_trade=0.001, max_risk_per_trade=0.02)
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4080.0)
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    result = risk_manager.evaluate(decision)
    assert result.approved is False
    assert "Risk limit exceeded" in result.reason


def test_risk_per_trade_way_above_maximum_is_rejected(risk_manager, mock_signal_candidate, mock_ai_result):
    """The pre-hardening bug: risk_per_trade=2.0 (200%) used to silently flow through unclamped."""
    risk_manager.config = RiskConfig(risk_per_trade=2.0, min_risk_per_trade=0.001, max_risk_per_trade=0.02)
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4080.0)
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    result = risk_manager.evaluate(decision)
    assert result.approved is False
    assert "Risk limit exceeded" in result.reason


def test_risk_limit_rejection_is_logged_with_risk_limit_category(risk_manager, mock_signal_candidate, mock_ai_result):
    risk_manager.config = RiskConfig(risk_per_trade=5.0)
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4080.0)
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    risk_manager.evaluate(decision)
    entries = risk_manager.decision_repository.get_recent(limit=1)
    assert entries[0].reject_category == "RISK_LIMIT"


# ---------------------------------------------------------------------------
# TASK 2: Risk Calculation Validation
# ---------------------------------------------------------------------------

def test_zero_account_balance_is_rejected(risk_manager, mock_signal_candidate, mock_ai_result):
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4080.0)
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    result = risk_manager.evaluate(decision, account_balance=0.0)
    assert result.approved is False
    assert "Invalid account balance" in result.reason


def test_negative_account_balance_is_rejected(risk_manager, mock_signal_candidate, mock_ai_result):
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4080.0)
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    result = risk_manager.evaluate(decision, account_balance=-500.0)
    assert result.approved is False
    assert "Invalid account balance" in result.reason


def test_positive_account_balance_is_accepted(risk_manager, mock_signal_candidate, mock_ai_result):
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4080.0)
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    result = risk_manager.evaluate(decision, account_balance=10000.0)
    assert result.approved is True
    assert result.lot_size > 0


def test_zero_current_equity_is_rejected(risk_manager, mock_signal_candidate, mock_ai_result):
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4080.0)
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    result = risk_manager.evaluate(decision, current_equity=0.0)
    assert result.approved is False
    assert "Invalid current equity" in result.reason


def test_negative_current_equity_is_rejected(risk_manager, mock_signal_candidate, mock_ai_result):
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4080.0)
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    result = risk_manager.evaluate(decision, current_equity=-1.0)
    assert result.approved is False
    assert "Invalid current equity" in result.reason


def test_invalid_geometry_still_rejected_before_new_checks_run(risk_manager, mock_signal_candidate, mock_ai_result):
    """Pre-existing geometry validation still short-circuits before any Phase V1.0.1 check."""
    candidate = mock_signal_candidate(entry=4065.65, stop_loss=4060.00, take_profit=4065.54)
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    result = risk_manager.evaluate(decision, account_balance=10000.0)
    assert result.approved is False
    assert "geometry" in result.reason.lower()


def test_invalid_stop_loss_distance_still_rejected(risk_manager, mock_signal_candidate, mock_ai_result):
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4065.0, take_profit=4075.0)
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    result = risk_manager.evaluate(decision)
    assert result.approved is False


def test_no_account_balance_still_approves_with_zero_lot_size(risk_manager, mock_signal_candidate, mock_ai_result):
    """Backward compatibility: omitting account_balance entirely keeps the pre-hardening behavior (approved, sizing not computed)."""
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4080.0)
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    result = risk_manager.evaluate(decision)
    assert result.approved is True
    assert result.lot_size == 0.0
    assert "no account_balance supplied" in result.reason


# ---------------------------------------------------------------------------
# TASK 3: Minimum Risk Reward Protection
# ---------------------------------------------------------------------------

def test_rr_exactly_at_minimum_is_approved(risk_manager, mock_signal_candidate, mock_ai_result):
    """entry=100, stop_loss=95 (risk=5), take_profit=110 (reward=10) -> RR=2.0 exactly."""
    candidate = mock_signal_candidate(entry=100.0, stop_loss=95.0, take_profit=110.0)
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    result = risk_manager.evaluate(decision)
    assert result.approved is True
    assert result.risk_reward == 2.0


def test_rr_just_below_minimum_is_rejected(risk_manager, mock_signal_candidate, mock_ai_result):
    """entry=100, stop_loss=95 (risk=5), take_profit=109 (reward=9) -> RR=1.8 < 2.0."""
    candidate = mock_signal_candidate(entry=100.0, stop_loss=95.0, take_profit=109.0)
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    result = risk_manager.evaluate(decision)
    assert result.approved is False
    assert "Risk Reward ratio below minimum" in result.reason


def test_rr_of_point_one_is_rejected(risk_manager, mock_signal_candidate, mock_ai_result):
    """entry=2000, stop_loss=1990 (risk=10), take_profit=2001 (reward=1) -> RR=0.1 -- the exact scenario from docs/V1_RISK_AUDIT.md's FAIL finding."""
    candidate = mock_signal_candidate(entry=2000.0, stop_loss=1990.0, take_profit=2001.0)
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    result = risk_manager.evaluate(decision)
    assert result.approved is False
    assert "Risk Reward ratio below minimum" in result.reason
    assert result.risk_reward == 0.1


def test_high_rr_is_approved(risk_manager, mock_signal_candidate, mock_ai_result):
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4090.0)
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    result = risk_manager.evaluate(decision)
    assert result.approved is True
    assert result.risk_reward == 5.0


def test_rr_below_minimum_sell_side_is_rejected(risk_manager, mock_signal_candidate, mock_ai_result):
    from signal_layer.signal_builder.models import SignalType

    candidate = mock_signal_candidate(
        signal_type=SignalType.SELL, entry=100.0, stop_loss=105.0, take_profit=99.0,
    )
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    result = risk_manager.evaluate(decision)
    assert result.approved is False
    assert "Risk Reward ratio below minimum" in result.reason


def test_custom_min_rr_config_is_respected(risk_manager, mock_signal_candidate, mock_ai_result):
    risk_manager.config = RiskConfig(min_risk_reward_ratio=1.0)
    candidate = mock_signal_candidate(entry=100.0, stop_loss=95.0, take_profit=104.0)  # RR=0.8
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    result = risk_manager.evaluate(decision)
    assert result.approved is False


def test_rr_reject_is_logged_with_rr_below_min_category(risk_manager, mock_signal_candidate, mock_ai_result):
    candidate = mock_signal_candidate(entry=2000.0, stop_loss=1990.0, take_profit=2001.0)
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    risk_manager.evaluate(decision)
    entries = risk_manager.decision_repository.get_recent(limit=1)
    assert entries[0].reject_category == "RR_BELOW_MIN"


def test_default_min_risk_reward_ratio_is_two():
    assert RiskConfig().min_risk_reward_ratio == 2.0
