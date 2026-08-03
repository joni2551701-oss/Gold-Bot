"""
ReplayManager -- creates, tracks and ends replay sessions (v1.1 Phase 1,
module 8; amendment 5 SRP split). The manager owns session lifecycle; the
ReplayController owns the running session.

Validates before creating a session (amendment 4) -- a replay never
starts on invalid inputs. This module never imports from any layer above
data/.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from data_layer.market_memory.market_memory import MarketMemory
from backtesting_layer.replay_engine.replay_source import ReplayDataSource
from backtesting_layer.replay_engine.replay_session import ReplaySession
from backtesting_layer.replay_engine.replay_controller import ReplayController
from backtesting_layer.replay_engine.replay_clock import ReplayClock
from backtesting_layer.replay_engine.replay_validation import validate_replay, ReplayValidation
from data_layer.event_system.event_bus import EventBus


class ReplayCreationError(RuntimeError):
    """Raised when a replay session fails pre-start validation."""


class ReplayManager:
    def __init__(self, bus: Optional[EventBus] = None):
        self._bus = bus
        self._sessions: Dict[str, ReplayController] = {}

    def create_session(self, asset: str, source: ReplayDataSource,
                       memory: MarketMemory, speed: float = 1.0,
                       check_integrity: bool = True
                       ) -> Tuple[ReplaySession, ReplayController]:
        """Validate, then create an isolated session + controller."""
        validation = validate_replay(asset, source, memory,
                                     check_integrity=check_integrity)
        if not validation.ok:
            raise ReplayCreationError(
                f"replay validation failed: {validation.errors}")
        start, end = source.timeline(asset)
        session = ReplaySession(asset=asset, start=start, end=end, speed=speed)
        clock = ReplayClock(start, speed)
        controller = ReplayController(session, source, memory, clock=clock,
                                      bus=self._bus)
        self._sessions[session.session_id] = controller
        return session, controller

    def validate(self, asset: str, source: ReplayDataSource,
                 memory: MarketMemory) -> ReplayValidation:
        return validate_replay(asset, source, memory)

    def get(self, session_id: str) -> ReplayController:
        return self._sessions[session_id]

    def sessions(self) -> List[str]:
        return list(self._sessions.keys())

    def end_session(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)
