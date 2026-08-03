from typing import Optional
from dataclasses import dataclass

from core_layer.logger.logger import setup_logger
from database_layer.trade_repository.signal_repository import SignalRepository
from core_layer.health_monitor.models import SignalHealth

logger = setup_logger("SignalMonitor")


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


def get_signal_health(signal_repository: Optional[SignalRepository] = None) -> SignalHealth:
    """
    GoldBot Core Owner Monitoring Alpha (TASK 4) — today's signal
    activity counts, aggregated from `database_layer.trade_repository.signal_repository.SignalRepository.get_signals_today()`
    (a new, additive read method -- see
    `docs/PHASE_CORE_MONITORING_AUDIT.md`'s own "database/" section).
    Read-only: never writes, never grades, never computes a verdict.

    Never raises: a database error returns an all-zero `SignalHealth`
    rather than propagating an exception.
    """
    try:
        rows = (signal_repository or SignalRepository()).get_signals_today()
    except Exception as e:
        logger.warning(f"get_signal_health: SignalRepository failed: {e}")
        return SignalHealth(total_signals=0, buy_count=0, sell_count=0, none_count=0, average_confidence=0.0)

    buy_count = sum(1 for row in rows if row.get("direction") == "BUY")
    sell_count = sum(1 for row in rows if row.get("direction") == "SELL")
    none_count = len(rows) - buy_count - sell_count

    confidences = [row.get("confidence_score") for row in rows if isinstance(row.get("confidence_score"), (int, float))]
    average_confidence = (sum(confidences) / len(confidences)) if confidences else 0.0

    return SignalHealth(
        total_signals=len(rows),
        buy_count=buy_count,
        sell_count=sell_count,
        none_count=none_count,
        average_confidence=average_confidence,
    )
