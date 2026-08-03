"""
backtesting_layer.replay_engine -- GoldBot v1.1 Market Data Foundation: Replay Engine
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

from backtesting_layer.replay_engine.replay_state import (
    ReplayState, ReplayStateError, can_transition, assert_transition,
)
from backtesting_layer.replay_engine.replay_clock import ReplayClock
from backtesting_layer.replay_engine.replay_source import (
    Frame, ReplayDataSource, SnapshotReplaySource, HistoricalReplaySource,
    SimulationSource,
)
from backtesting_layer.replay_engine.replay_session import ReplaySession
from backtesting_layer.replay_engine.replay_validation import validate_replay, ReplayValidation
from backtesting_layer.replay_engine.replay_metrics import ReplayMetrics
from backtesting_layer.replay_engine.replay_controller import ReplayController, MemoryReplaySink
from backtesting_layer.replay_engine.replay_manager import ReplayManager, ReplayCreationError

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

# Canonical documentation: 17_Backtesting_Layer/ReplayEngine/README.md
