"""Tests for the service lifecycle state machine (module 10, amendment 1)."""

import pytest

from core.gateway.service_state import (
    ServiceState, ServiceStateError, can_transition, assert_transition,
)


def test_states_present():
    names = {s.name for s in ServiceState}
    assert names == {"REGISTERED", "STARTING", "READY", "DEGRADED",
                     "STOPPING", "STOPPED", "FAILED"}


def test_legal_transitions():
    assert can_transition(ServiceState.REGISTERED, ServiceState.STARTING)
    assert can_transition(ServiceState.STARTING, ServiceState.READY)
    assert can_transition(ServiceState.READY, ServiceState.DEGRADED)
    assert can_transition(ServiceState.DEGRADED, ServiceState.READY)
    assert can_transition(ServiceState.STOPPING, ServiceState.STOPPED)
    assert can_transition(ServiceState.STOPPED, ServiceState.STARTING)


def test_illegal_transitions():
    assert not can_transition(ServiceState.REGISTERED, ServiceState.READY)
    assert not can_transition(ServiceState.STOPPED, ServiceState.READY)
    assert not can_transition(ServiceState.READY, ServiceState.REGISTERED)


def test_assert_raises_on_illegal():
    with pytest.raises(ServiceStateError):
        assert_transition(ServiceState.REGISTERED, ServiceState.READY)


def test_assert_ok_on_legal():
    assert_transition(ServiceState.STARTING, ServiceState.READY)  # no raise
