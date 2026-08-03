"""
Backtesting Layer — Replay Controller (Phase 60.1: Historical Replay
Engine Foundation, TASK 6).

The public-facing session-management API -- start()/pause()/resume()/
stop()/restart()/step()/get_status(), each keyed by a `session_id`.
One process-local `ReplayController` owns a `{session_id: (ReplaySession,
ReplayEngine)}` map, the same "in-memory holder" convention as
`configuration.runtime_state.RuntimeStateCache`. This is the layer
`telegram/owner/replay_commands.py` (TASK 8) wraps -- no new session/
engine logic belongs there, only formatting.
"""

from typing import Dict, Optional, Tuple

from backtesting.replay_engine import ReplayEngine
from backtesting.replay_models import ReplayConfig, ReplayResult, ReplayState
from backtesting.replay_session import ReplaySession
from data_layer.providers.twelve_data_client import Candle
from core_layer.logger.logger import setup_logger

logger = setup_logger("ReplayController")


class ReplayController:
    def __init__(self):
        self._entries: Dict[str, Tuple[ReplaySession, ReplayEngine]] = {}

    def _get(self, session_id: str) -> Tuple[Optional[ReplaySession], Optional[ReplayEngine]]:
        entry = self._entries.get(session_id)
        return entry if entry else (None, None)

    def _sync_progress(self, session: ReplaySession, engine: ReplayEngine) -> None:
        session.record_progress(engine.candles_replayed)
        if engine.is_finished and session.state not in (ReplayState.FINISHED, ReplayState.STOPPED):
            session.mark_finished()

    def start(self, config: ReplayConfig) -> ReplaySession:
        """Loads the configured candle window (via ReplayEngine's own construction) and starts running immediately."""
        engine = ReplayEngine(config)
        session = ReplaySession(config, candles_total=engine.candles_total)
        session.mark_running()
        engine.clock.play()
        self._entries[session.session_id] = (session, engine)
        logger.info(f"Replay started: session={session.session_id} {config.symbol} {config.timeframe} candles={engine.candles_total}")
        return session

    def pause(self, session_id: str) -> Optional[ReplaySession]:
        session, engine = self._get(session_id)
        if session is None:
            return None
        engine.clock.pause()
        session.mark_paused()
        return session

    def resume(self, session_id: str) -> Optional[ReplaySession]:
        session, engine = self._get(session_id)
        if session is None:
            return None
        engine.clock.resume()
        session.mark_running()
        return session

    def stop(self, session_id: str) -> Optional[ReplaySession]:
        session, engine = self._get(session_id)
        if session is None:
            return None
        engine.clock.stop()
        session.mark_stopped()
        return session

    def restart(self, session_id: str) -> Optional[ReplaySession]:
        """Re-runs the same session_id's own config from the beginning -- a fresh ReplayEngine, same identity."""
        session, _ = self._get(session_id)
        if session is None:
            return None
        new_engine = ReplayEngine(session.config)
        new_session = ReplaySession(session.config, candles_total=new_engine.candles_total)
        new_session.session_id = session_id
        new_session.mark_running()
        new_engine.clock.play()
        self._entries[session_id] = (new_session, new_engine)
        return new_session

    def step(self, session_id: str) -> Optional[Candle]:
        """Advances one replay step (per ReplayConfig.speed) and returns the new current candle -- None for an unknown session_id."""
        session, engine = self._get(session_id)
        if session is None:
            return None
        candle = engine.step()
        self._sync_progress(session, engine)
        return candle

    def get_status(self, session_id: str) -> Optional[ReplayResult]:
        session, engine = self._get(session_id)
        if session is None:
            return None
        self._sync_progress(session, engine)
        return session.to_result()
