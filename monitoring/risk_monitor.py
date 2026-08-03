"""
Monitoring Layer — Risk Monitor (Phase V1.0.1: Risk Management
Hardening Patch, TASK 9). Read-only aggregator over the risk_decisions
log risk_layer/risk_engine/risk_manager.py's TASK 8 already writes
(database.risk_decision_repository.RiskDecisionRepository) -- this
module never computes a risk verdict, never mutates trading state,
and never writes to risk_decisions itself. Same "monitoring only
reads" posture as every prior monitoring phase in this codebase
(monitoring/decision_logger.py, monitoring/error_monitor.py).

Pause Events = EMERGENCY_PAUSED-category rejects + DRAWDOWN-category
rejects (both represent "trading is currently paused" from the
Owner's point of view); Drawdown Events is the DRAWDOWN-category
subset specifically -- see risk_layer/risk_engine/risk_manager.py's `reject_category`
values for the full taxonomy.
"""

from dataclasses import dataclass
from typing import Optional

from database.risk_decision_repository import RiskDecisionRepository


@dataclass(frozen=True)
class RiskCounts:
    total_checks: int
    approve_count: int
    reject_count: int
    risk_limit_events: int
    rr_reject_events: int
    drawdown_events: int
    daily_loss_events: int
    duplicate_events: int
    emergency_pause_events: int
    pause_events: int


class RiskMonitor:
    """Read-only -- every method here queries RiskDecisionRepository, never writes to it."""

    def __init__(self, repository: Optional[RiskDecisionRepository] = None):
        self.repository = repository or RiskDecisionRepository()

    def get_counts(self) -> RiskCounts:
        total = self.repository.count_all()
        approve = self.repository.count_by_decision("APPROVE")
        reject = self.repository.count_by_decision("REJECT")
        risk_limit = self.repository.count_by_reject_category("RISK_LIMIT")
        rr_reject = self.repository.count_by_reject_category("RR_BELOW_MIN")
        drawdown = self.repository.count_by_reject_category("DRAWDOWN")
        daily_loss = self.repository.count_by_reject_category("DAILY_LOSS")
        duplicate = self.repository.count_by_reject_category("DUPLICATE")
        emergency_pause = self.repository.count_by_reject_category("EMERGENCY_PAUSED")

        return RiskCounts(
            total_checks=total,
            approve_count=approve,
            reject_count=reject,
            risk_limit_events=risk_limit,
            rr_reject_events=rr_reject,
            drawdown_events=drawdown,
            daily_loss_events=daily_loss,
            duplicate_events=duplicate,
            emergency_pause_events=emergency_pause,
            pause_events=emergency_pause + drawdown,
        )


DEFAULT_RISK_MONITOR = RiskMonitor()


def get_risk_counts() -> RiskCounts:
    return DEFAULT_RISK_MONITOR.get_counts()
