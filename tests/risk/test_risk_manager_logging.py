"""
Phase V1.0.1 (Risk Management Hardening Patch) -- TASK 8 (Risk
Logging) tests: every RiskManager.evaluate() call must persist one
risk_decisions row (timestamp, symbol, risk%, rr, drawdown, decision,
reason).
"""

from decision_layer.decision_engine.decision_engine import DecisionEngine


def _decision(candidate, ai_result):
    return DecisionEngine().evaluate(candidate, ai_result)


def test_approve_is_logged(risk_manager, mock_signal_candidate, mock_ai_result):
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4080.0)
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    risk_manager.evaluate(decision)
    entries = risk_manager.decision_repository.get_recent(limit=1)
    assert len(entries) == 1
    assert entries[0].decision == "APPROVE"


def test_reject_is_logged(risk_manager, mock_signal_candidate, mock_ai_result):
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4065.0, take_profit=4080.0)  # zero SL distance
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    risk_manager.evaluate(decision)
    entries = risk_manager.decision_repository.get_recent(limit=1)
    assert entries[0].decision == "REJECT"


def test_logged_entry_has_timestamp(risk_manager, mock_signal_candidate, mock_ai_result):
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4080.0)
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    risk_manager.evaluate(decision)
    entries = risk_manager.decision_repository.get_recent(limit=1)
    assert entries[0].created_at is not None


def test_logged_entry_has_symbol(risk_manager, mock_signal_candidate, mock_ai_result):
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4080.0)
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    risk_manager.evaluate(decision, symbol="XAUUSD")
    entries = risk_manager.decision_repository.get_recent(limit=1)
    assert entries[0].symbol == "XAUUSD"


def test_logged_entry_defaults_symbol_to_unknown_when_not_supplied(risk_manager, mock_signal_candidate, mock_ai_result):
    """The existing core/pipeline.py and backtesting_layer/backtest_engine/backtest_engine.py call sites never supply symbol."""
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4080.0)
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    risk_manager.evaluate(decision)
    entries = risk_manager.decision_repository.get_recent(limit=1)
    assert entries[0].symbol == "UNKNOWN"


def test_logged_entry_has_risk_reward(risk_manager, mock_signal_candidate, mock_ai_result):
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4080.0)
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    risk_manager.evaluate(decision)
    entries = risk_manager.decision_repository.get_recent(limit=1)
    assert entries[0].risk_reward == 3.0


def test_logged_entry_has_risk_percent_when_approved(risk_manager, mock_signal_candidate, mock_ai_result):
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4080.0)
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    risk_manager.evaluate(decision)
    entries = risk_manager.decision_repository.get_recent(limit=1)
    assert entries[0].risk_percent == risk_manager.config.risk_per_trade


def test_logged_entry_has_drawdown_percent_when_current_equity_supplied(risk_manager, mock_signal_candidate, mock_ai_result):
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4080.0)
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    risk_manager.evaluate(decision, current_equity=10000.0)
    entries = risk_manager.decision_repository.get_recent(limit=1)
    assert entries[0].drawdown_percent == 0.0


def test_logged_entry_has_reason(risk_manager, mock_signal_candidate, mock_ai_result):
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4065.0, take_profit=4080.0)
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    risk_manager.evaluate(decision)
    entries = risk_manager.decision_repository.get_recent(limit=1)
    assert entries[0].reason != ""


def test_logged_entry_has_strategy_name(risk_manager, mock_signal_candidate, mock_ai_result):
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4080.0, strategy_name="MY_STRATEGY")
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    risk_manager.evaluate(decision)
    entries = risk_manager.decision_repository.get_recent(limit=1)
    assert entries[0].strategy_name == "MY_STRATEGY"


def test_logged_entry_has_direction(risk_manager, mock_signal_candidate, mock_ai_result):
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4080.0)
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    risk_manager.evaluate(decision)
    entries = risk_manager.decision_repository.get_recent(limit=1)
    assert entries[0].direction == "BUY"


def test_multiple_evaluations_each_produce_their_own_log_row(risk_manager, mock_signal_candidate, mock_ai_result):
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4080.0)
    for _ in range(3):
        decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
        risk_manager.evaluate(decision)
    entries = risk_manager.decision_repository.get_recent(limit=10)
    assert len(entries) == 3


def test_logging_failure_does_not_break_evaluate(risk_manager, mock_signal_candidate, mock_ai_result):
    """Never raises: a logging failure must never turn an otherwise-valid Risk verdict into an exception."""
    class _BrokenRepository:
        def record(self, **kwargs):
            raise RuntimeError("simulated DB failure")

    risk_manager.decision_repository = _BrokenRepository()
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4080.0)
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    result = risk_manager.evaluate(decision)
    assert result.approved is True


def test_json_shaped_decision_and_reason_example_from_brief(risk_manager, mock_signal_candidate, mock_ai_result):
    """The exact {"decision": "REJECT", "reason": "RR below minimum"}-shaped example from the Worker Brief."""
    candidate = mock_signal_candidate(entry=2000.0, stop_loss=1990.0, take_profit=2001.0)  # RR=0.1
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    result = risk_manager.evaluate(decision)
    entries = risk_manager.decision_repository.get_recent(limit=1)
    payload = {"decision": entries[0].decision, "reason": entries[0].reason}
    assert payload["decision"] == "REJECT"
    assert "RR" in payload["reason"] or "Risk Reward" in payload["reason"]
    assert result.approved is False
