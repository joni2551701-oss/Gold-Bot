from typing import Optional
from dataclasses import dataclass
from decision.decision_engine import DecisionResult


@dataclass(frozen=True)
class RiskConfig:
    risk_per_trade: float = 0.01
    max_daily_loss: float = 0.05
    max_drawdown: float = 0.10
    max_open_trades: int = 1


@dataclass(frozen=True)
class RiskResult:
    approved: bool
    lot_size: float
    risk_amount: float
    reason: str


class RiskManager:
    """
    Risk Layer — pure calculation contracts only.
    No MT5, no SymbolInfo, no Database, no Telegram, no Logger.
    No knowledge of broker specifications (contract size, tick value,
    lot step, min/max lot, stop level).
    """

    def __init__(
        self,
        config: Optional[RiskConfig] = None,
    ):
        self.config = config or RiskConfig()

    def evaluate(
        self,
        decision_result: DecisionResult,
    ) -> RiskResult:
        """
        Entry point for Risk Layer. Currently unimplemented —
        orchestration will be wired in a future phase once
        Symbol Specification integration is available.
        """
        return RiskResult(
            approved=False,
            lot_size=0.0,
            risk_amount=0.0,
            reason="Not implemented"
        )

    def calculate_risk_amount(
        self,
        account_balance: float,
        risk_percent: float,
    ) -> float:
        """
        Interface only. No formula yet.
        """
        return 0.0

    def calculate_position_size(
        self,
        risk_amount: float,
        stop_loss_distance: float,
    ) -> float:
        """
        Interface only. No formula yet.
        Does not accept contract size, tick value, tick size,
        point value, or lot step — these belong to a future
        Symbol Specification layer.
        """
        return 0.0

    def validate_stop_loss_distance(
        self,
        stop_loss_distance: float,
    ) -> bool:
        """
        Interface only. No formula yet.
        """
        return False
