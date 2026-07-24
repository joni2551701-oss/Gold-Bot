"""
Replay state machine (v1.1 Phase 1, module 8; amendment 1).

An explicit transition table -- illegal transitions are rejected, so a
replay session can never enter an inconsistent state.

    IDLE -> LOADED -> PLAYING <-> PAUSED -> FINISHED -> LIVE

This module never imports from any layer above data/.
"""

from __future__ import annotations

from enum import Enum
from typing import Dict, Set


class ReplayState(Enum):
    IDLE = "idle"
    LOADED = "loaded"
    PLAYING = "playing"
    PAUSED = "paused"
    FINISHED = "finished"
    LIVE = "live"


# Legal transitions (self-transitions allow step/seek/speed to keep state).
_TRANSITIONS: Dict[ReplayState, Set[ReplayState]] = {
    ReplayState.IDLE: {ReplayState.LOADED},
    ReplayState.LOADED: {ReplayState.PLAYING, ReplayState.FINISHED,
                         ReplayState.LOADED},
    ReplayState.PLAYING: {ReplayState.PAUSED, ReplayState.FINISHED,
                          ReplayState.PLAYING},
    ReplayState.PAUSED: {ReplayState.PLAYING, ReplayState.FINISHED,
                         ReplayState.PAUSED},
    ReplayState.FINISHED: {ReplayState.LIVE},
    ReplayState.LIVE: set(),   # terminal (handed off to live)
}


class ReplayStateError(RuntimeError):
    """Raised on an illegal replay state transition."""


def can_transition(src: ReplayState, dst: ReplayState) -> bool:
    return dst in _TRANSITIONS.get(src, set())


def assert_transition(src: ReplayState, dst: ReplayState) -> None:
    if not can_transition(src, dst):
        raise ReplayStateError(f"illegal replay transition {src.value} -> {dst.value}")
