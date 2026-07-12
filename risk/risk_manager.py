from typing import Optional
from dataclasses import dataclass
from decision.models import TradeDecision, DecisionAction


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
    risk_reward: float
    reason: str


class RiskManager:
    """
    Risk Layer — pure calculation contracts only.
    No MT5, no SymbolInfo, no Database, no Telegram, no Logger.
    No knowledge of broker specifications (contract size, tick value,
    lot step, min/max lot, stop level). lot_size is a sizing
    suggestion for manual execution, never an order instruction.
    """

    def __init__(
        self,
        config: Optional[RiskConfig] = None,
    ):
        self.config = config or RiskConfig()

    def evaluate(
        self,
        trade_decision: TradeDecision,
        account_balance: Optional[float] = None,
    ) -> RiskResult:
        """
        Entry point for Risk Layer. Rejects anything the Decision
        Engine did not APPROVE. For an APPROVE decision, validates
        the stop-loss distance and computes risk/reward from the
        underlying SignalCandidate.

        GoldBot is semi-automated (no MT5/broker connection), so it
        has no built-in source of account balance. Dollar risk_amount
        and a suggested lot_size are only computed when a caller
        supplies account_balance explicitly; otherwise those fields
        stay 0.0 and the reason explains why.
        """
        if trade_decision.action != DecisionAction.APPROVE:
            return RiskResult(
                approved=False,
                lot_size=0.0,
                risk_amount=0.0,
                risk_reward=0.0,
                reason=f"Decision Engine action was {trade_decision.action.value}, not APPROVE.",
            )

        signal = trade_decision.signal
        stop_loss_distance = abs(signal.entry - signal.stop_loss)

        if not self.validate_stop_loss_distance(stop_loss_distance):
            return RiskResult(
                approved=False,
                lot_size=0.0,
                risk_amount=0.0,
                risk_reward=0.0,
                reason=f"Invalid stop-loss distance: {stop_loss_distance}.",
            )

        risk_reward = self.calculate_risk_reward(signal.entry, signal.stop_loss, signal.take_profit)

        if account_balance is None:
            return RiskResult(
                approved=True,
                lot_size=0.0,
                risk_amount=0.0,
                risk_reward=risk_reward,
                reason="Approved. Position sizing not computed: no account_balance supplied.",
            )

        risk_amount = self.calculate_risk_amount(account_balance, self.config.risk_per_trade)
        lot_size = self.calculate_position_size(risk_amount, stop_loss_distance)

        return RiskResult(
            approved=True,
            lot_size=lot_size,
            risk_amount=risk_amount,
            risk_reward=risk_reward,
            reason=f"Approved. risk_reward={risk_reward:.2f}, risk_amount={risk_amount:.2f}.",
        )

    def calculate_risk_amount(
        self,
        account_balance: float,
        risk_percent: float,
    ) -> float:
        """
        Dollar amount at risk for one trade: account_balance * risk_percent.
        """
        if account_balance <= 0 or risk_percent <= 0:
            return 0.0
        return account_balance * risk_percent

    def calculate_position_size(
        self,
        risk_amount: float,
        stop_loss_distance: float,
    ) -> float:
        """
        Suggested position size: risk_amount / stop_loss_distance.
        Does not accept contract size, tick value, tick size,
        point value, or lot step — these belong to a future
        Symbol Specification layer. Not an MT5 lot value.
        """
        if stop_loss_distance <= 0:
            return 0.0
        return risk_amount / stop_loss_distance

    def calculate_risk_reward(
        self,
        entry: float,
        stop_loss: float,
        take_profit: float,
    ) -> float:
        """
        Reward-to-risk ratio: distance to take_profit / distance to stop_loss.
        """
        risk = abs(entry - stop_loss)
        reward = abs(take_profit - entry)
        if risk <= 0:
            return 0.0
        return reward / risk

    def validate_stop_loss_distance(
        self,
        stop_loss_distance: float,
    ) -> bool:
        """
        A stop-loss distance must be strictly positive to be usable.
        """
        return stop_loss_distance > 0
