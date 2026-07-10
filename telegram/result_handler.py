from typing import Optional
from dataclasses import dataclass


@dataclass(frozen=True)
class ResultHandlerConfig:
    enabled: bool = True


@dataclass(frozen=True)
class ResultHandlerResult:
    handled: bool
    reason: str


class ResultHandler:
    """
    Telegram Layer — result handling contract only.
    No aiogram, no Telegram Message/Update, no command parser,
    no raw user text, no Database, no SignalRepository, no Notifier,
    no Bot, no Logger.

    Real command routing (Dispatcher) and database updates belong
    to future phases.
    """

    def __init__(
        self,
        config: Optional[ResultHandlerConfig] = None,
    ):
        self.config = config or ResultHandlerConfig()

    def handle(self) -> ResultHandlerResult:
        """
        Entry point for result handling. Currently a placeholder —
        takes no parameters. Signature will evolve once command
        routing and database integration are introduced.
        """
        return ResultHandlerResult(
            handled=False,
            reason="Not implemented"
        )
