from typing import Optional
from enum import Enum
from dataclasses import dataclass


class SignalState(Enum):
    CREATED = "CREATED"
    SENT = "SENT"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    CLOSED = "CLOSED"


@dataclass(frozen=True)
class SignalLifecycleConfig:
    enabled: bool = True


@dataclass(frozen=True)
class LifecycleResult:
    transitioned: bool
    reason: str


class SignalLifecycle:
    """
    Execution Layer — signal state transition contract only.
    No execution_engine.py / ExecutionResult, no Telegram,
    no Database. Pure state machine interface.
    """

    def __init__(
        self,
        config: Optional[SignalLifecycleConfig] = None,
    ):
        self.config = config or SignalLifecycleConfig()

    def transition(
        self,
        current_state: SignalState,
        next_state: SignalState,
    ) -> LifecycleResult:
        """
        Entry point for state transition validation. Currently a
        placeholder — no actual state machine rules are enforced yet.
        """
        return LifecycleResult(
            transitioned=False,
            reason="Not implemented"
        )
