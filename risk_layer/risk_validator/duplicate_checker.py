"""
Risk Layer — Duplicate Trade Checker (Phase V1.0.1: Risk Management
Hardening Patch, TASK 6). Reuses the risk_decisions log this same
phase's TASK 8 already builds (database.risk_decision_repository.RiskDecisionRepository)
rather than inventing a second open-positions table -- GoldBot has no
persisted open-position store today (execution/ is simulator-only,
see docs/PHASE_V1_AUDIT.md's Execution Audit), so "was a similar
signal recently approved" is the closest available proxy for "is this
a duplicate."

Dormant unless a caller supplies `symbol` to RiskManager.evaluate() --
see risk_layer/risk_engine/account_state_tracker.py's module docstring for the same
"optional, additive, off by default" posture.
"""

from dataclasses import dataclass
from typing import Optional

from database.risk_decision_repository import RiskDecisionRepository

DEFAULT_DUPLICATE_WINDOW_SECONDS = 300.0


@dataclass(frozen=True)
class DuplicateCheckResult:
    duplicate: bool
    reason: str


class DuplicateTradeChecker:
    """Owns the recent-approvals lookup against RiskDecisionRepository -- risk_layer/risk_engine/risk_manager.py never queries the repository directly for this."""

    def __init__(self, repository: Optional[RiskDecisionRepository] = None):
        self.repository = repository or RiskDecisionRepository()

    def check(
        self,
        symbol: str,
        direction: str,
        strategy_name: Optional[str],
        within_seconds: float = DEFAULT_DUPLICATE_WINDOW_SECONDS,
    ) -> DuplicateCheckResult:
        """
        A duplicate is any prior APPROVE for the exact same
        (symbol, direction, strategy_name) within `within_seconds`.
        strategy_name=None widens the match to any strategy for this
        symbol/direction pair.
        """
        recent = self.repository.get_recent_approved(symbol, direction, strategy_name, within_seconds)
        if recent:
            return DuplicateCheckResult(
                duplicate=True,
                reason=(
                    f"Duplicate trade: {symbol} {direction} "
                    f"(strategy={strategy_name or 'any'}) already approved "
                    f"{len(recent)} time(s) within the last {within_seconds:.0f}s."
                ),
            )
        return DuplicateCheckResult(duplicate=False, reason="No recent duplicate found.")
