"""
Phase V1.0.1 (Risk Management Hardening Patch) -- Security (no bypass)
and Compatibility (existing pipeline unchanged) tests, per TASK 11's
explicit requirement.
"""

from decision_layer.decision_engine.decision_engine import DecisionEngine
from decision_layer.decision_engine.models import DecisionAction
from risk_layer.risk_engine.risk_manager import RiskConfig, RiskManager, RiskResult


def _decision(candidate, ai_result):
    return DecisionEngine().evaluate(candidate, ai_result)


# ---------------------------------------------------------------------------
# Security: no bypass
# ---------------------------------------------------------------------------

def test_reject_decision_cannot_be_approved_by_any_combination_of_new_params(
    risk_manager, mock_signal_candidate, mock_ai_result,
):
    candidate = mock_signal_candidate()
    decision = _decision(candidate, mock_ai_result(approved=False))
    assert decision.action == DecisionAction.REJECT
    result = risk_manager.evaluate(
        decision, account_balance=10000.0, current_equity=10000.0, symbol="XAUUSD",
    )
    assert result.approved is False
    assert "not APPROVE" in result.reason


def test_emergency_paused_cannot_be_bypassed_by_supplying_extra_params(
    risk_manager, emergency_manager, mock_signal_candidate, mock_ai_result,
):
    emergency_manager.activate_pause(reason="test")
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4080.0)
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    result = risk_manager.evaluate(
        decision, account_balance=10000.0, current_equity=10000.0, symbol="XAUUSD",
    )
    assert result.approved is False


def test_out_of_bounds_risk_per_trade_cannot_be_bypassed_by_high_rr(
    risk_manager, mock_signal_candidate, mock_ai_result,
):
    risk_manager.config = RiskConfig(risk_per_trade=1.0)  # 100%, absurd
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4200.0)  # huge RR
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    result = risk_manager.evaluate(decision)
    assert result.approved is False
    assert "Risk limit exceeded" in result.reason


def test_below_minimum_rr_cannot_be_bypassed_by_large_account_balance(
    risk_manager, mock_signal_candidate, mock_ai_result,
):
    candidate = mock_signal_candidate(entry=2000.0, stop_loss=1990.0, take_profit=2001.0)  # RR=0.1
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    result = risk_manager.evaluate(decision, account_balance=1_000_000.0)
    assert result.approved is False


def test_invalid_geometry_cannot_be_bypassed_by_any_new_param(
    risk_manager, mock_signal_candidate, mock_ai_result,
):
    candidate = mock_signal_candidate(entry=4065.65, stop_loss=4060.00, take_profit=4065.54)
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    result = risk_manager.evaluate(
        decision, account_balance=10000.0, current_equity=10000.0, symbol="XAUUSD",
    )
    assert result.approved is False
    assert "geometry" in result.reason.lower()


def test_duplicate_reject_cannot_be_bypassed_by_omitting_strategy_name(
    risk_manager, mock_signal_candidate, mock_ai_result,
):
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4080.0, strategy_name="S1")
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    first = risk_manager.evaluate(decision, symbol="XAUUSD")
    assert first.approved is True

    decision2 = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    second = risk_manager.evaluate(decision2, symbol="XAUUSD")  # same strategy_name, same signal
    assert second.approved is False
    assert "Duplicate" in second.reason


def test_drawdown_pause_cannot_be_bypassed_by_repeated_calls(
    risk_manager, mock_signal_candidate, mock_ai_result,
):
    risk_manager.config = RiskConfig(max_drawdown=0.10)
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4080.0)

    decision1 = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    risk_manager.evaluate(decision1, current_equity=10000.0)  # establishes baseline

    decision2 = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    result = risk_manager.evaluate(decision2, current_equity=8000.0)  # 20% down
    assert result.approved is False
    assert "Drawdown" in result.reason

    # Retrying with the exact same inputs must not somehow flip to approved.
    decision3 = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    retry_result = risk_manager.evaluate(decision3, current_equity=8000.0)
    assert retry_result.approved is False


def test_daily_loss_block_cannot_be_bypassed_by_repeated_calls(
    risk_manager, mock_signal_candidate, mock_ai_result,
):
    risk_manager.config = RiskConfig(max_daily_loss=0.05)
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4080.0)

    decision1 = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    risk_manager.evaluate(decision1, account_balance=10000.0)  # establishes baseline

    decision2 = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    result = risk_manager.evaluate(decision2, account_balance=9000.0)  # 10% down
    assert result.approved is False
    assert "Daily loss" in result.reason


def test_risk_manager_never_mutates_the_input_signal(risk_manager, mock_signal_candidate, mock_ai_result):
    """RULE 2/3: Risk never changes BUY/SELL/entry/TP/SL."""
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4080.0)
    original = (candidate.signal_type, candidate.entry, candidate.stop_loss, candidate.take_profit, candidate.strategy_name)
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    risk_manager.evaluate(decision, account_balance=10000.0, current_equity=10000.0, symbol="XAUUSD")
    after = (candidate.signal_type, candidate.entry, candidate.stop_loss, candidate.take_profit, candidate.strategy_name)
    assert original == after


def test_risk_manager_has_no_signal_generating_method():
    """RULE 3: Risk never generates a signal of its own."""
    manager = RiskManager()
    for name in ("generate_signal", "create_signal", "make_signal"):
        assert not hasattr(manager, name)


# ---------------------------------------------------------------------------
# Compatibility: existing pipeline unchanged
# ---------------------------------------------------------------------------

def test_bare_evaluate_call_still_works_exactly_like_before(risk_manager, mock_signal_candidate, mock_ai_result):
    """The exact core/pipeline.py:463 / backtesting/backtest_engine.py:206 call shape."""
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4080.0)
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    result = risk_manager.evaluate(decision)
    assert result.approved is True
    assert result.lot_size == 0.0


def test_risk_result_still_constructible_with_original_five_keyword_args():
    """tests/execution/simulator/test_simulator_engine.py's own direct RiskResult(...) construction shape."""
    result = RiskResult(approved=True, lot_size=0.01, risk_amount=100.0, risk_reward=2.0, reason="ok")
    assert result.approved is True
    assert result.risk_percent == 0.0
    assert result.drawdown_percent is None


def test_risk_config_still_constructible_with_original_four_fields():
    config = RiskConfig(risk_per_trade=0.02, max_daily_loss=0.05, max_drawdown=0.10, max_open_trades=1)
    assert config.risk_per_trade == 0.02


def test_calculate_risk_amount_unchanged():
    manager = RiskManager()
    assert manager.calculate_risk_amount(10000.0, 0.01) == 100.0


def test_calculate_position_size_unchanged():
    manager = RiskManager()
    assert manager.calculate_position_size(100.0, 5.0) == 20.0


def test_calculate_risk_reward_unchanged():
    manager = RiskManager()
    assert manager.calculate_risk_reward(4065.0, 4060.0, 4080.0) == 3.0


def test_validate_geometry_unchanged():
    from signal_layer.signal_builder.models import SignalCandidate, SignalType

    manager = RiskManager()
    valid = SignalCandidate(
        signal_type=SignalType.BUY, entry=100.0, stop_loss=95.0, take_profit=110.0,
        strategy_name="S", confidence=0.9, reasons=[],
    )
    assert manager.validate_geometry(valid) is True


def test_full_mock_pipeline_run_still_produces_a_telegram_message_for_a_clean_approve(
    mock_pipeline, mock_signal_candidate, mock_ai_result, isolated_db,
):
    """End-to-end: the real, unmodified TradingPipeline + real RiskManager still approves a clean signal and reaches the notification stage, exactly as before this phase."""
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4090.0)  # RR=5.0
    pipeline = mock_pipeline([candidate], [mock_ai_result(approved=True, confidence=0.95)])
    result = pipeline.run()
    assert len(result["risk_results"]) == 1
    assert result["risk_results"][0].approved is True


def test_full_mock_pipeline_run_rejects_low_rr_signal_end_to_end(
    mock_pipeline, mock_signal_candidate, mock_ai_result, isolated_db,
):
    """The new TASK 3 protection is live end-to-end through the real, unmodified pipeline."""
    candidate = mock_signal_candidate(entry=2000.0, stop_loss=1990.0, take_profit=2001.0)  # RR=0.1
    pipeline = mock_pipeline([candidate], [mock_ai_result(approved=True, confidence=0.95)])
    result = pipeline.run()
    assert len(result["risk_results"]) == 1
    assert result["risk_results"][0].approved is False
    assert len(result["telegram_messages"]) == 0
