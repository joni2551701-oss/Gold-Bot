from typing import Optional
from dataclasses import dataclass
from risk_layer.risk_engine.risk_manager import RiskResult


@dataclass(frozen=True)
class ExecutionConfig:
    enabled: bool = True


@dataclass(frozen=True)
class ExecutionResult:
    dispatched: bool
    reason: str


class ExecutionEngine:
    """
    Execution Layer — signal dispatch contract only.
    No MT5, no Telegram, no HTTP, no Database, no Logger,
    no async/threading/queue. No knowledge of message formatting
    or delivery mechanics.
    """

    def __init__(
        self,
        config: Optional[ExecutionConfig] = None,
    ):
        self.config = config or ExecutionConfig()

    def dispatch(
        self,
        risk_result: RiskResult,
    ) -> ExecutionResult:
        """
        Entry point for Execution Layer. Currently unimplemented —
        orchestration and delivery mechanics will be wired in a
        future phase.
        """
        return ExecutionResult(
            dispatched=False,
            reason="Not implemented"
        )
