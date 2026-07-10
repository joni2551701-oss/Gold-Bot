from typing import Optional
from dataclasses import dataclass


@dataclass(frozen=True)
class MonitorConfig:
    enabled: bool = True


@dataclass(frozen=True)
class MonitorResult:
    monitored: bool
    reason: str


class SignalMonitor:
    """
    Monitoring Layer — signal observation contract only.
    No SignalState / execution.signal_lifecycle import, no
    execution.*, no database.*, no telegram.*, no logger, no MT5.

    Monitoring will connect to signal state via a future event
    contract, not a direct import of the Execution Layer's state
    model.
    """

    def __init__(
        self,
        config: Optional[MonitorConfig] = None,
    ):
        self.config = config or MonitorConfig()

    def monitor(self) -> MonitorResult:
        """
        Entry point for signal monitoring. Currently a placeholder —
        takes no parameters. Signal ID, state, and timestamp will
        arrive via a future event contract.
        """
        return MonitorResult(
            monitored=False,
            reason="Not implemented"
        )
