"""
Database Layer — Risk Account State persistence model (Phase V1.0.1:
Risk Management Hardening Patch, TASK 4/5/10). One row per symbol,
upserted -- same one-row-per-name convention as
database.runtime_feature_models.RuntimeFeatureRecord. Holds the
drawdown baseline and the daily-loss baseline together, since both
are small, related, per-symbol account-state facts read/written by
risk.account_state_tracker.AccountStateTracker.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass(frozen=True)
class RiskAccountStateEntry:
    """
    Mirrors the 'risk_account_state' table row shape.

    starting_equity/current_equity: the drawdown baseline (TASK 4).
        starting_equity is set once, on the first-ever observation for
        this symbol, and never changes afterward except via an
        explicit reset (no reset mechanism exists yet -- out of scope
        for this phase).
    drawdown_status: "NORMAL" or "TRADING_PAUSED" -- the last computed
        drawdown check's outcome, exposed for monitoring to read.
    daily_start_balance/daily_date: the daily-loss baseline (TASK 5).
        daily_date is an ISO date string ("YYYY-MM-DD", UTC); when a
        new observation's date differs from the stored one, the
        tracker resets daily_start_balance to that observation's
        balance (see risk.account_state_tracker's own docstring).
    """
    symbol: str
    starting_equity: Optional[float] = None
    current_equity: Optional[float] = None
    drawdown_status: str = "NORMAL"
    daily_start_balance: Optional[float] = None
    daily_date: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


def create_risk_account_state_entry(
    symbol: str,
    starting_equity: Optional[float] = None,
    current_equity: Optional[float] = None,
    drawdown_status: str = "NORMAL",
    daily_start_balance: Optional[float] = None,
    daily_date: Optional[str] = None,
    created_at: Optional[datetime] = None,
) -> RiskAccountStateEntry:
    """Pure, deterministic factory. `created_at` is preserved across an upsert (only `updated_at` changes on every write) -- see database_layer/trade_repository/risk_state_repository.py."""
    now = datetime.now(timezone.utc)
    return RiskAccountStateEntry(
        symbol=symbol,
        starting_equity=starting_equity,
        current_equity=current_equity,
        drawdown_status=drawdown_status,
        daily_start_balance=daily_start_balance,
        daily_date=daily_date,
        created_at=created_at or now,
        updated_at=now,
    )
