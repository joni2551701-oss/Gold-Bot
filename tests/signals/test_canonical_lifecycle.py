"""STEP-08: canonical signal build/publish lifecycle (TASK-CORE-008)."""

from signals.lifecycle.state import (
    CanonicalSignalStatus as St,
    transition,
    is_terminal,
)
from signals.lifecycle import CanonicalSignalStatus as StFromPkg


def test_package_reexport():
    assert StFromPkg is St


def test_happy_path_transitions():
    chain = [St.CREATED, St.VALIDATED, St.ENRICHED, St.READY, St.PUBLISHED]
    for cur, nxt in zip(chain, chain[1:]):
        assert transition(cur, nxt).success


def test_cancel_from_any_prepublish():
    for s in (St.CREATED, St.VALIDATED, St.ENRICHED, St.READY):
        assert transition(s, St.CANCELLED).success


def test_invalid_transition_reported_not_raised():
    res = transition(St.CREATED, St.PUBLISHED)
    assert not res.success
    assert "not an allowed transition" in res.reason


def test_expire_and_terminal():
    assert transition(St.READY, St.EXPIRED).success
    assert transition(St.PUBLISHED, St.EXPIRED).success
    assert is_terminal(St.EXPIRED)
    assert is_terminal(St.CANCELLED)
    assert not is_terminal(St.READY)
