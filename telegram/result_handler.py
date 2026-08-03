from typing import Optional
from dataclasses import dataclass

from database.signal_repository import SignalRepository
from core_layer.logger.logger import setup_logger

logger = setup_logger("ResultHandler")


@dataclass(frozen=True)
class ResultHandlerConfig:
    enabled: bool = True


@dataclass(frozen=True)
class ResultHandlerResult:
    handled: bool
    reason: str


class ResultHandler:
    """
    Telegram Layer — manual result update entry point.

    Bridges a human-reported trade outcome (WIN/LOSS/BE/CANCELLED)
    to the existing SignalRepository.update_signal_result(), which
    already validates the result, closes the signal (status=CLOSED,
    closed_at=now), and updates its result. This layer adds no new
    validation logic or schema knowledge -- it only forwards the call
    and converts every failure mode into a safe ResultHandlerResult
    instead of letting an exception escape.

    No aiogram, no Telegram Message/Update, no command parser, no
    raw user text -- command routing (Dispatcher) belongs to a
    future phase. Never analyzes signals, never recalculates risk,
    never makes a trading decision.
    """

    def __init__(
        self,
        config: Optional[ResultHandlerConfig] = None,
        signal_repository: Optional[SignalRepository] = None,
    ):
        self.config = config or ResultHandlerConfig()
        # Lazy: constructing SignalRepository() touches disk (schema
        # init). Bare ResultHandler() (e.g. main.py) must not do that
        # until an update is actually requested. May be injected for tests.
        self._signal_repository = signal_repository

    def _get_repository(self) -> SignalRepository:
        if self._signal_repository is None:
            self._signal_repository = SignalRepository()
        return self._signal_repository

    def handle(self) -> ResultHandlerResult:
        """
        Legacy placeholder entry point, retained for backward
        compatibility with existing callers (main.py). Use
        update_result() for the real signal -> database update.
        """
        return ResultHandlerResult(
            handled=False,
            reason="Not implemented"
        )

    def update_result(self, signal_id: str, result: str) -> ResultHandlerResult:
        """
        Updates a persisted signal's outcome. Delegates entirely to
        SignalRepository.update_signal_result() -- no re-implemented
        validation, no new schema, no new columns. Every failure mode
        (disabled config, invalid result, missing signal, database
        error) is caught and reported as handled=False; this method
        never raises.
        """
        if not self.config.enabled:
            return ResultHandlerResult(handled=False, reason="ResultHandler disabled")

        repository = self._get_repository()

        try:
            updated = repository.update_signal_result(signal_id, result)
        except ValueError as e:
            # Raised by update_signal_result() for a result outside
            # {WIN, LOSS, BE, CANCELLED} -- no SQL is executed in that case.
            return ResultHandlerResult(handled=False, reason=str(e))
        except Exception as e:
            logger.warning(f"Result update failed for signal {signal_id}: {e}")
            return ResultHandlerResult(handled=False, reason=f"Database error: {e}")

        if not updated:
            return ResultHandlerResult(handled=False, reason=f"Signal not found: {signal_id}")

        return ResultHandlerResult(handled=True, reason="")
