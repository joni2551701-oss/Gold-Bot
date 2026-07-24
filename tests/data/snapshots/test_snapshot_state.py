"""Tests for the snapshot state machine (module 9, amendment 3)."""

import pytest

from data.snapshots.snapshot_state import (
    SnapshotState, VerifyState, SnapshotStateError,
    can_transition, assert_transition, CORE_VERSION,
)


def test_core_version_is_11():
    assert CORE_VERSION == "1.1.0"


def test_verify_states():
    assert {s.value for s in VerifyState} == {"unverified", "verified", "failed"}


def test_legal_transitions():
    assert can_transition(SnapshotState.CREATED, SnapshotState.VERIFIED)
    assert can_transition(SnapshotState.VERIFIED, SnapshotState.ARCHIVED)
    assert can_transition(SnapshotState.VERIFIED, SnapshotState.EXPORTED)
    assert can_transition(SnapshotState.ARCHIVED, SnapshotState.DELETED)
    assert can_transition(SnapshotState.IMPORTED, SnapshotState.VERIFIED)


def test_illegal_transitions():
    assert not can_transition(SnapshotState.CREATED, SnapshotState.EXPORTED)
    assert not can_transition(SnapshotState.DELETED, SnapshotState.VERIFIED)
    assert not can_transition(SnapshotState.CORRUPTED, SnapshotState.VERIFIED)


def test_assert_transition_raises_on_illegal():
    with pytest.raises(SnapshotStateError):
        assert_transition(SnapshotState.DELETED, SnapshotState.VERIFIED)


def test_assert_transition_ok_on_legal():
    assert_transition(SnapshotState.CREATED, SnapshotState.VERIFIED)  # no raise
