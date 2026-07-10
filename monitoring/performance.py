from typing import Optional
from dataclasses import dataclass


@dataclass(frozen=True)
class PerformanceConfig:
    enabled: bool = True


@dataclass(frozen=True)
class PerformanceResult:
    calculated: bool
    reason: str


class PerformanceTracker:
    """
    Monitoring Layer — performance statistics contract only.
    No SignalMonitor import, no database.*, no signal history access,
    no win-rate/RR/profit calculation logic.

    Actual analytics computation belongs to a future phase, once
    signal outcome data becomes available through a defined contract.
    """

    def __init__(
        self,
        config: Optional[PerformanceConfig] = None,
    ):
        self.config = config or PerformanceConfig()

    def calculate(self) -> PerformanceResult:
        """
        Entry point for performance calculation. Currently a
        placeholder — no statistics are computed yet.
        """
        return PerformanceResult(
            calculated=False,
            reason="Not implemented"
        )
