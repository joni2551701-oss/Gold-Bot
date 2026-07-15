"""
Phase 60.8 (Safe Integration Layer, TASK 2/3/5) --
core/guards/pipeline_guard.py tests. Uses lightweight stub managers
(never touches the real database) so every Emergency/Runtime
combination is deterministic and fast.
"""

from datetime import datetime, timezone

from configuration.runtime_state import FeatureRuntimeState
from core.emergency.emergency_state import EmergencyState, create_emergency_state_record
from core.guards.pipeline_guard import GuardDecision, PipelineGuard


class _StubRuntimeFeatureManager:
    def __init__(self, states=None):
        self._states = states or {}

    def status(self, name):
        return self._states.get(name)


class _StubEmergencyManager:
    def __init__(self, state=EmergencyState.NORMAL, reason=None):
        self._record = create_emergency_state_record(state, reason=reason)

    def get_status(self):
        return self._record


def _guard(emergency_state=EmergencyState.NORMAL, feature_states=None):
    return PipelineGuard(
        runtime_feature_manager=_StubRuntimeFeatureManager(feature_states),
        emergency_manager=_StubEmergencyManager(emergency_state),
    )


def _enabled(name, value):
    return {name: FeatureRuntimeState(name=name, enabled=value, last_changed=datetime.now(timezone.utc))}


# --- NORMAL -----------------------------------------------------------------

def test_normal_state_all_four_hooks_proceed_with_no_feature_states():
    guard = _guard(EmergencyState.NORMAL)

    for method in (guard.before_signal, guard.before_ai, guard.before_execution, guard.before_database):
        decision = method()
        assert isinstance(decision, GuardDecision)
        assert decision.proceed is True
        assert decision.abort is False


def test_enable_signals_off_skips_signal_stage():
    guard = _guard(EmergencyState.NORMAL, _enabled("ENABLE_SIGNALS", False))

    decision = guard.before_signal()

    assert decision.proceed is False
    assert decision.abort is False


def test_enable_ai_off_skips_ai_stage():
    guard = _guard(EmergencyState.NORMAL, _enabled("ENABLE_AI", False))

    decision = guard.before_ai()

    assert decision.proceed is False


def test_enable_database_off_skips_database_stage():
    guard = _guard(EmergencyState.NORMAL, _enabled("ENABLE_DATABASE", False))

    decision = guard.before_database()

    assert decision.proceed is False


def test_before_execution_ignores_runtime_feature_state():
    """
    Disclosed in pipeline_guard.py's own module docstring: before_execution()
    does not consult any runtime feature flag (ENABLE_EXECUTION stays
    declared-only, see configuration/feature_registry.py) -- only
    Emergency state gates this hook.
    """
    guard = _guard(EmergencyState.NORMAL, _enabled("ENABLE_EXECUTION", False))

    decision = guard.before_execution()

    assert decision.proceed is True


def test_missing_feature_state_defaults_to_proceed():
    """A feature name never seen by the runtime manager (status() -> None) fails open, not closed."""
    guard = _guard(EmergencyState.NORMAL, feature_states={})

    assert guard.before_signal().proceed is True
    assert guard.before_ai().proceed is True
    assert guard.before_database().proceed is True


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

def test_pipeline_guard_constructs_real_managers_by_default():
    """Never raises: default construction touches the (test-isolated) database but must not error."""
    guard = PipelineGuard()

    decision = guard.before_signal()

    assert isinstance(decision, GuardDecision)
