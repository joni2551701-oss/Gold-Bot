"""
Snapshot state machine (v1.1 Phase 1, module 9; amendment 3).

A general SnapshotState (lifecycle) alongside VerifyState (verification
result). Explicit transitions keep the lifecycle consistent. This module
never imports from any layer above data/.
"""

from __future__ import annotations

from enum import Enum
from typing import Dict, Set

CORE_VERSION = "1.1.0"


class VerifyState(Enum):
    UNVERIFIED = "unverified"
    VERIFIED = "verified"
    FAILED = "failed"


class SnapshotState(Enum):
    CREATED = "created"
    VERIFIED = "verified"
    ARCHIVED = "archived"
    IMPORTED = "imported"
    EXPORTED = "exported"
    DELETED = "deleted"
    CORRUPTED = "corrupted"
    LOCKED = "locked"


# Legal lifecycle transitions (EXPORTED/LOCKED are transient overlays handled
# via locks, not terminal states here).
_TRANSITIONS: Dict[SnapshotState, Set[SnapshotState]] = {
    SnapshotState.CREATED: {SnapshotState.VERIFIED, SnapshotState.CORRUPTED,
                            SnapshotState.ARCHIVED, SnapshotState.DELETED},
    SnapshotState.IMPORTED: {SnapshotState.VERIFIED, SnapshotState.CORRUPTED,
                             SnapshotState.DELETED},
    SnapshotState.VERIFIED: {SnapshotState.ARCHIVED, SnapshotState.DELETED,
                             SnapshotState.CORRUPTED, SnapshotState.EXPORTED,
                             SnapshotState.VERIFIED},
    SnapshotState.ARCHIVED: {SnapshotState.DELETED, SnapshotState.VERIFIED},
    SnapshotState.EXPORTED: {SnapshotState.VERIFIED, SnapshotState.ARCHIVED,
                             SnapshotState.DELETED},
    SnapshotState.CORRUPTED: {SnapshotState.DELETED},
    SnapshotState.DELETED: set(),
    SnapshotState.LOCKED: set(),
}


class SnapshotStateError(RuntimeError):
    """Raised on an illegal snapshot lifecycle transition."""


def can_transition(src: SnapshotState, dst: SnapshotState) -> bool:
    return dst in _TRANSITIONS.get(src, set())


def assert_transition(src: SnapshotState, dst: SnapshotState) -> None:
    if not can_transition(src, dst):
        raise SnapshotStateError(
            f"illegal snapshot transition {src.value} -> {dst.value}")
