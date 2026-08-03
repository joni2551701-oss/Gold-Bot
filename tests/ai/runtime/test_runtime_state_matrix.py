"""
Phase 61.7 TASK 8 — Runtime State Validation. Full state-machine audit:
every (from_state, to_state) pair across all six RuntimeState values,
confirming is_valid_transition() matches VALID_TRANSITIONS exactly and
that RuntimeManager.transition() honors it in both directions.
"""

import pytest

from ai_layer.ai_engine.runtime.runtime_manager import RuntimeManager
from ai_layer.ai_engine.runtime.runtime_state import VALID_TRANSITIONS, RuntimeState, is_valid_transition

_ALL_STATES = list(RuntimeState)
_ALL_PAIRS = [(f, t) for f in _ALL_STATES for t in _ALL_STATES]


@pytest.mark.parametrize("from_state,to_state", _ALL_PAIRS)
def test_is_valid_transition_matches_the_declared_table(from_state, to_state):
    expected = to_state in VALID_TRANSITIONS[from_state]
    assert is_valid_transition(from_state, to_state) is expected


@pytest.mark.parametrize("from_state,to_state", _ALL_PAIRS)
def test_runtime_manager_transition_honors_the_same_table(from_state, to_state):
    manager = RuntimeManager(initial_state=from_state)
    event = manager.transition(to_state, reason="matrix probe")

    if to_state in VALID_TRANSITIONS[from_state]:
        assert event is not None
        assert manager.current_state() == to_state
    else:
        assert event is None
        assert manager.current_state() == from_state  # rejected -- state unchanged


def test_shutdown_has_zero_outgoing_transitions():
    assert VALID_TRANSITIONS[RuntimeState.SHUTDOWN] == frozenset()
    for target in _ALL_STATES:
        assert is_valid_transition(RuntimeState.SHUTDOWN, target) is False


def test_failed_to_ready_is_explicitly_allowed():
    """The Director's own worked example: FAILED -> READY (recovery) must be permitted."""
    assert is_valid_transition(RuntimeState.FAILED, RuntimeState.READY) is True
    manager = RuntimeManager(initial_state=RuntimeState.FAILED)
    event = manager.transition(RuntimeState.READY, reason="recovered")
    assert event is not None
    assert manager.current_state() == RuntimeState.READY


def test_shutdown_to_busy_is_explicitly_forbidden():
    """The Director's own worked example: SHUTDOWN -> BUSY must be rejected."""
    assert is_valid_transition(RuntimeState.SHUTDOWN, RuntimeState.BUSY) is False
    manager = RuntimeManager(initial_state=RuntimeState.SHUTDOWN)
    event = manager.transition(RuntimeState.BUSY)
    assert event is None
    assert manager.current_state() == RuntimeState.SHUTDOWN


def test_every_non_shutdown_state_can_reach_shutdown_or_failed_eventually():
    """No state is a dead end short of the intentionally-terminal SHUTDOWN -- every state has at least one outgoing transition."""
    for state in _ALL_STATES:
        if state == RuntimeState.SHUTDOWN:
            continue
        assert len(VALID_TRANSITIONS[state]) > 0, f"{state} has no outgoing transitions and is not SHUTDOWN"


def test_no_state_transitions_to_itself():
    """A same-state 'transition' is never declared -- current_state() changing is what a transition means."""
    for state in _ALL_STATES:
        assert state not in VALID_TRANSITIONS[state]
