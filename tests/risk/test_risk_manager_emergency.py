"""
Phase V1.0.1 (Risk Management Hardening Patch) -- TASK 7 (Emergency
State Correction) tests: PAUSED/KILLED/MAINTENANCE must now stop Risk
from approving a trade, not just suppress Telegram delivery (the gap
docs/V1_RISK_AUDIT.md's item 7 found). WARNING must NOT block (it is
advisory only, per core_layer.emergency.emergency_state.EmergencyState's
own docstring).
"""

from decision_layer.decision_engine.decision_engine import DecisionEngine


def _decision(candidate, ai_result):
    return DecisionEngine().evaluate(candidate, ai_result)


def _approved_decision(mock_signal_candidate, mock_ai_result):
    candidate = mock_signal_candidate(entry=4065.0, stop_loss=4060.0, take_profit=4080.0)
    return _decision(candidate, mock_ai_result(approved=True, confidence=0.95))


def test_normal_state_allows_approval(risk_manager, mock_signal_candidate, mock_ai_result):
    decision = _approved_decision(mock_signal_candidate, mock_ai_result)
    result = risk_manager.evaluate(decision)
    assert result.approved is True


def test_paused_state_blocks_new_approval(risk_manager, emergency_manager, mock_signal_candidate, mock_ai_result):
    emergency_manager.activate_pause(reason="owner requested", activated_by="owner")
    decision = _approved_decision(mock_signal_candidate, mock_ai_result)
    result = risk_manager.evaluate(decision)
    assert result.approved is False
    assert "PAUSED" in result.reason
    assert "no new trade approval" in result.reason.lower()


def test_killed_state_blocks_new_approval(risk_manager, emergency_manager, mock_signal_candidate, mock_ai_result):
    emergency_manager.activate_kill(reason="critical failure", activated_by="owner")
    decision = _approved_decision(mock_signal_candidate, mock_ai_result)
    result = risk_manager.evaluate(decision)
    assert result.approved is False
    assert "KILLED" in result.reason


def test_maintenance_state_blocks_new_approval(risk_manager, emergency_manager, mock_signal_candidate, mock_ai_result):
    emergency_manager.activate_maintenance(reason="scheduled window", activated_by="owner")
    decision = _approved_decision(mock_signal_candidate, mock_ai_result)
    result = risk_manager.evaluate(decision)
    assert result.approved is False
    assert "MAINTENANCE" in result.reason


def test_paused_then_resume_allows_approval_again(risk_manager, emergency_manager, mock_signal_candidate, mock_ai_result):
    emergency_manager.activate_pause(reason="owner requested")
    paused_decision = _approved_decision(mock_signal_candidate, mock_ai_result)
    paused_result = risk_manager.evaluate(paused_decision)
    assert paused_result.approved is False

    emergency_manager.restore_normal(reason="resolved")
    resumed_decision = _approved_decision(mock_signal_candidate, mock_ai_result)
    resumed_result = risk_manager.evaluate(resumed_decision)
    assert resumed_result.approved is True


def test_paused_reject_is_logged_with_emergency_category(risk_manager, emergency_manager, mock_signal_candidate, mock_ai_result):
    emergency_manager.activate_pause(reason="owner requested")
    decision = _approved_decision(mock_signal_candidate, mock_ai_result)
    risk_manager.evaluate(decision)
    entries = risk_manager.decision_repository.get_recent(limit=1)
    assert entries[0].reject_category == "EMERGENCY_PAUSED"


def test_warning_state_does_not_block_approval(risk_manager, emergency_manager, mock_signal_candidate, mock_ai_result):
    """WARNING is advisory only -- nothing paused or killed yet."""
    from database.emergency_repository import EmergencyRepository

    EmergencyRepository().record_transition("WARNING", reason="circuit breaker observation", source="system")
    decision = _approved_decision(mock_signal_candidate, mock_ai_result)
    result = risk_manager.evaluate(decision)
    assert result.approved is True


def test_paused_still_rejects_geometrically_invalid_signal_for_the_same_reason(
    risk_manager, emergency_manager, mock_signal_candidate, mock_ai_result,
):
    """Emergency check runs before geometry -- the reason should name PAUSED, not GEOMETRY."""
    emergency_manager.activate_pause(reason="owner requested")
    candidate = mock_signal_candidate(entry=4065.65, stop_loss=4060.00, take_profit=4065.54)  # invalid geometry
    decision = _decision(candidate, mock_ai_result(approved=True, confidence=0.95))
    result = risk_manager.evaluate(decision)
    assert result.approved is False
    assert "PAUSED" in result.reason


def test_default_emergency_manager_reads_real_repository_and_defaults_to_normal(isolated_db):
    from risk_layer.risk_engine.risk_manager import RiskManager

    manager = RiskManager()
    status = manager.emergency_manager.get_status()
    assert status.state.value == "NORMAL"


def test_injected_emergency_manager_is_used_over_default(risk_manager, emergency_manager, mock_signal_candidate, mock_ai_result):
    """Confirms RiskManager actually consults the injected EmergencyManager, not a second, unrelated instance."""
    assert risk_manager.emergency_manager is not None
    emergency_manager.activate_kill(reason="test")
    # risk_manager and emergency_manager share the same isolated DB (same isolated_db fixture upstream)
    decision = _approved_decision(mock_signal_candidate, mock_ai_result)
    result = risk_manager.evaluate(decision)
    assert result.approved is False
