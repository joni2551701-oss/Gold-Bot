"""data_layer/snapshots/snapshot_state -- canonical module package (GoldBot Engineering Law GEL-001, Strict).

Implementation in `snapshot_state.py`; this `__init__` re-exports the public surface
so every established import path stays stable. Generated 2026-08-04. No behaviour
changed; the module code was moved intact from the former flat `snapshot_state.py`.
"""
from data_layer.snapshots.snapshot_state.snapshot_state import (
    annotations,
    Enum,
    Dict,
    Set,
    CORE_VERSION,
    VerifyState,
    SnapshotState,
    SnapshotStateError,
    can_transition,
    assert_transition,
)

__all__ = [
    "annotations",
    "Enum",
    "Dict",
    "Set",
    "CORE_VERSION",
    "VerifyState",
    "SnapshotState",
    "SnapshotStateError",
    "can_transition",
    "assert_transition",
]
