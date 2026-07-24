"""
Risk Layer — Account State Tracker (Phase V1.0.1: Risk Management
Hardening Patch, TASK 4/5). Pure calculation, backed by a single
per-symbol persisted row (database.risk_state_repository.RiskStateRepository)
that serves both the drawdown baseline (starting_equity/current_equity)
and the daily-loss baseline (daily_start_balance/daily_date) -- see
docs/PHASE_V1_0_1_RISK_AUDIT.md's TASK 4/10 section for why one table
serves both.

Dormant unless a caller supplies current_equity/account_balance to
RiskManager.evaluate() -- the existing core/pipeline.py and
backtesting/backtest_engine.py call sites, both untouched this phase,
never supply either, so this tracker has zero effect on today's live
pipeline until a future, separately-approved phase wires a real
equity/balance source in (same "additive, off by default" posture as
risk/duplicate_checker.py).
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from database.risk_state_repository import RiskStateRepository

TRADING_PAUSED = "TRADING_PAUSED"
NORMAL = "NORMAL"


@dataclass(frozen=True)
class DrawdownCheckResult:
    drawdown_percent: float
    paused: bool
    reason: str


@dataclass(frozen=True)
class DailyLossCheckResult:
    loss_percent: float
    blocked: bool
    reason: str


class AccountStateTracker:
    """Owns the read-modify-write cycle against RiskStateRepository -- risk/risk_manager.py never touches the repository directly."""

    def __init__(self, repository: Optional[RiskStateRepository] = None):
        self.repository = repository or RiskStateRepository()

    def check_drawdown(self, symbol: str, current_equity: float, max_drawdown: float) -> DrawdownCheckResult:
        """
        On the first-ever observation for `symbol`, current_equity
        becomes the starting_equity baseline (drawdown_percent=0.0,
        never paused on that first call). Every subsequent call
        compares current_equity against the stored starting_equity.
        `max_drawdown` is a fraction (0.10 = 10%), same convention as
        RiskConfig.max_drawdown.
        """
        if current_equity <= 0:
            return DrawdownCheckResult(drawdown_percent=0.0, paused=False, reason="Invalid current_equity.")

        state = self.repository.get_state(symbol)
        starting_equity = state.starting_equity if state and state.starting_equity else current_equity
        if starting_equity <= 0:
            starting_equity = current_equity

        drawdown_percent = max(0.0, (starting_equity - current_equity) / starting_equity)
        paused = drawdown_percent > max_drawdown
        status = TRADING_PAUSED if paused else NORMAL

        self.repository.upsert_state(
            symbol=symbol,
            starting_equity=starting_equity,
            current_equity=current_equity,
            drawdown_status=status,
            daily_start_balance=state.daily_start_balance if state else None,
            daily_date=state.daily_date if state else None,
        )

        reason = (
            f"Drawdown {drawdown_percent:.2%} exceeds max {max_drawdown:.2%}."
            if paused else f"Drawdown {drawdown_percent:.2%} within limit {max_drawdown:.2%}."
        )
        return DrawdownCheckResult(drawdown_percent=drawdown_percent, paused=paused, reason=reason)

    def check_daily_loss(self, symbol: str, current_balance: float, max_daily_loss: float) -> DailyLossCheckResult:
        """
        Resets the daily baseline whenever the stored `daily_date`
        (UTC calendar date, ISO string) differs from today -- including
        the very first observation for `symbol`. `max_daily_loss` is a
        fraction (0.05 = 5%), same convention as RiskConfig.max_daily_loss.
        """
        if current_balance <= 0:
            return DailyLossCheckResult(loss_percent=0.0, blocked=False, reason="Invalid current_balance.")

        today = datetime.now(timezone.utc).date().isoformat()
        state = self.repository.get_state(symbol)

        if state is None or state.daily_date != today or state.daily_start_balance is None:
            daily_start_balance = current_balance
        else:
            daily_start_balance = state.daily_start_balance
        if daily_start_balance <= 0:
            daily_start_balance = current_balance

        loss_percent = max(0.0, (daily_start_balance - current_balance) / daily_start_balance)
        blocked = loss_percent > max_daily_loss

        self.repository.upsert_state(
            symbol=symbol,
            starting_equity=state.starting_equity if state else None,
            current_equity=state.current_equity if state else None,
            drawdown_status=state.drawdown_status if state else NORMAL,
            daily_start_balance=daily_start_balance,
            daily_date=today,
        )

        reason = (
            f"Daily loss {loss_percent:.2%} exceeds max {max_daily_loss:.2%}."
            if blocked else f"Daily loss {loss_percent:.2%} within limit {max_daily_loss:.2%}."
        )
        return DailyLossCheckResult(loss_percent=loss_percent, blocked=blocked, reason=reason)
