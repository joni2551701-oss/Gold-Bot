"""
data.replay -- GoldBot v1.1 Market Data Foundation: Replay Engine
(Phase 1 module 8). The Core time-control layer: LIVE/REPLAY modes, a
virtual clock, timeline control (play/pause/resume/step/seek/speed),
seamless Replay->LIVE handoff, isolated bookmarkable sessions, replay
events on the bus, and pluggable data sources (snapshot / historical /
future simulation).

Controls time and data flow into MarketMemory only -- no Strategy/Chart/
Decision logic; not wired into core/pipeline.py (Trading Safety). Never
imports from telegram/, ai/, decision/, risk/, strategies/, signals/,
context/, or database/.
"""

from data.replay.replay_state import (
    ReplayState, ReplayStateError, can_transition, assert_transition,
)
from data.replay.replay_clock import ReplayClock
from data.replay.replay_source import (
    Frame, ReplayDataSource, SnapshotReplaySource, HistoricalReplaySource,
    SimulationSource,
)
from data.replay.replay_session import ReplaySession
from data.replay.replay_validation import validate_replay, ReplayValidation
from data.replay.replay_metrics import ReplayMetrics
from data.replay.replay_controller import ReplayController, MemoryReplaySink
from data.replay.replay_manager import ReplayManager, ReplayCreationError

__all__ = [
    "ReplayState", "ReplayStateError", "can_transition", "assert_transition",
    "ReplayClock",
    "Frame", "ReplayDataSource", "SnapshotReplaySource",
    "HistoricalReplaySource", "SimulationSource",
    "ReplaySession",
    "validate_replay", "ReplayValidation",
    "ReplayMetrics",
    "ReplayController", "MemoryReplaySink",
    "ReplayManager", "ReplayCreationError",
]
