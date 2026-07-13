"""
Telegram Layer — signal service (Phase 38).

Bridges Telegram /signal and /history commands to
database.signal_repository.SignalRepository. No Telegram/aiogram
objects here, no formatting -- only READ access to already-persisted
signals, with exception handling so a database failure never
propagates up to a command handler. This service never creates,
updates, or deletes a signal -- that remains
core.pipeline.TradingPipeline / telegram.result_handler's job.

    Telegram Handler -> SignalService -> SignalRepository -> Database
"""

from typing import Optional, List, Dict
from dataclasses import dataclass, field

from database.signal_repository import SignalRepository
from core.logger import setup_logger

logger = setup_logger("SignalService")

# GoldBot trades a single symbol end to end (TradingPipeline is always
# constructed with symbol="XAUUSD" in main.py); accepted here for a
# future multi-symbol schema, not filtered on today.
DEFAULT_SYMBOL = "XAUUSD"


@dataclass(frozen=True)
class SignalServiceResult:
    success: bool
    reason: str
    signal: Optional[Dict] = None
    signals: List[Dict] = field(default_factory=list)


class SignalService:
    """Telegram -> Repository bridge for read-only signal retrieval."""

    def __init__(self, signal_repository: Optional[SignalRepository] = None):
        # Lazy, same pattern as UserService/AdminService: constructing
        # SignalRepository() touches disk (schema init). A bare
        # SignalService() must not do that until a method is actually
        # called. May be injected for tests.
        self._signal_repository = signal_repository

    def _get_repository(self) -> SignalRepository:
        if self._signal_repository is None:
            self._signal_repository = SignalRepository()
        return self._signal_repository

    def get_latest_signal(self, symbol: str = DEFAULT_SYMBOL) -> SignalServiceResult:
        """Most recently persisted signal. Never raises."""
        try:
            repository = self._get_repository()
            row = repository.get_latest_signal()
            if row is None:
                return SignalServiceResult(success=False, reason="No active signal available.")
            return SignalServiceResult(success=True, reason="", signal=row)
        except Exception as e:
            logger.warning(f"get_latest_signal failed: {e}")
            return SignalServiceResult(success=False, reason=f"Database error: {e}")

    def get_signal_history(self, limit: int = 5) -> SignalServiceResult:
        """Most recent `limit` signals, newest first. Never raises."""
        try:
            repository = self._get_repository()
            rows = repository.get_recent_signals(limit=limit)
            if not rows:
                return SignalServiceResult(success=False, reason="No signal history available.")
            return SignalServiceResult(success=True, reason="", signals=rows)
        except Exception as e:
            logger.warning(f"get_signal_history failed: {e}")
            return SignalServiceResult(success=False, reason=f"Database error: {e}")

    def get_signal_status(self) -> SignalServiceResult:
        """Whether at least one signal has ever been persisted. Never raises."""
        try:
            repository = self._get_repository()
            row = repository.get_latest_signal()
            exists = row is not None
            return SignalServiceResult(
                success=exists,
                reason="" if exists else "No signals recorded yet.",
            )
        except Exception as e:
            logger.warning(f"get_signal_status failed: {e}")
            return SignalServiceResult(success=False, reason=f"Database error: {e}")
