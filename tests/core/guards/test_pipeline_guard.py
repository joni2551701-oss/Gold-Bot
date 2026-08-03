"""
Phase 60.8 (Safe Integration Layer, TASK 2/3/5) --
core_layer/pipeline/pipeline_guard.py tests. Simplified in Phase 60.9 (Runtime
Registry Separation, TASK 4): PipelineGuard no longer reads
RuntimeFeatureManager at all -- every hook is Emergency-only. Uses a
lightweight stub EmergencyManager (never touches the real database) so
every Emergency combination is deterministic and fast.
"""

from core_layer.emergency.emergency_state import EmergencyState, create_emergency_state_record
from core_layer.pipeline.pipeline_guard import GuardDecision, PipelineGuard


class _StubEmergencyManager:
    def __init__(self, state=EmergencyState.NORMAL, reason=None):
        self._record = create_emergency_state_record(state, reason=reason)

    def get_status(self):
        return self._record


def _guard(emergency_state=EmergencyState.NORMAL):
    return PipelineGuard(emergency_manager=_StubEmergencyManager(emergency_state))


# --- NORMAL -----------------------------------------------------------------

def test_normal_state_all_four_hooks_proceed():
    guard = _guard(EmergencyState.NORMAL)

    for method in (guard.before_signal, guard.before_ai, guard.before_execution, guard.before_database):
        decision = method()
        assert isinstance(decision, GuardDecision)
        assert decision.proceed is True
        assert decision.abort is False


# --- WARNING ------------------------------------------------------------

def test_warning_state_all_hooks_still_proceed():
    guard = _guard(EmergencyState.WARNING)

    for method in (guard.before_signal, guard.before_ai, guard.before_execution, guard.before_database):
        decision = method()
        assert decision.proceed is True
        assert decision.abort is False


def test_warning_state_logs_a_warning(caplog):
    import logging

    guard = _guard(EmergencyState.WARNING)

    with caplog.at_level(logging.WARNING, logger="PipelineGuard"):
        guard.before_signal()

    assert any("emergency_state=WARNING" in message for message in caplog.messages)


# --- PAUSED ---------------------------------------------------------------

def test_paused_state_skips_execution_only():
    guard = _guard(EmergencyState.PAUSED)

    assert guard.before_signal().proceed is True
    assert guard.before_ai().proceed is True
    assert guard.before_execution().proceed is False
    assert guard.before_database().proceed is True


def test_paused_execution_skip_is_not_an_abort():
    guard = _guard(EmergencyState.PAUSED)

    decision = guard.before_execution()

    assert decision.proceed is False
    assert decision.abort is False


# --- MAINTENANCE ------------------------------------------------------------

def test_maintenance_state_skips_all_four_hooks():
    guard = _guard(EmergencyState.MAINTENANCE)

    for method in (guard.before_signal, guard.before_ai, guard.before_execution, guard.before_database):
        decision = method()
        assert decision.proceed is False
        assert decision.abort is False


# --- KILLED -----------------------------------------------------------------

def test_killed_state_aborts_on_every_hook():
    guard = _guard(EmergencyState.KILLED)

    for method in (guard.before_signal, guard.before_ai, guard.before_execution, guard.before_database):
        decision = method()
        assert decision.proceed is False
        assert decision.abort is True


def test_killed_state_reason_names_the_stage():
    guard = _guard(EmergencyState.KILLED)

    decision = guard.before_ai()

    assert "KILLED" in decision.reason
    assert "ai" in decision.reason


# --- Real manager construction (no stubs) -----------------------------------

def test_pipeline_guard_constructs_real_manager_by_default():
    """Never raises: default construction touches the (test-isolated) database but must not error."""
    guard = PipelineGuard()

    decision = guard.before_signal()

    assert isinstance(decision, GuardDecision)
