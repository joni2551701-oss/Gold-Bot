from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING
from decision.decision_engine import DecisionType  # Runtime import for strict Enum comparison

if TYPE_CHECKING:
    from decision.decision_engine import DecisionResult

@dataclass(frozen=True)
class RiskConfig:
    """
    Immutable configuration for risk management parameters.
    Default values provided for strict initialization.
    """
    risk_per_trade: float = 0.01
    max_daily_loss: float = 0.05
    max_drawdown: float = 0.10
    max_open_trades: int = 1

@dataclass(frozen=True)
class RiskResult:
    """
    Immutable data contract representing the final risk assessment
    and position sizing passed to the Execution Engine.
    """
    approved: bool
    lot_size: float
    risk_amount: float
    reason: str

class RiskManager:
    """
    Stateless component responsible for evaluating trading decisions 
    against risk parameters and outputting safe execution instructions.
    """

    def __init__(self, config: Optional[RiskConfig] = None):
        """
        Initializes the Risk Manager with provided config or defaults.
        """
        self.config = config or RiskConfig()

    def evaluate(self, decision_result: 'DecisionResult') -> RiskResult:
        """
        Validates the upstream decision. Acts as a strict type-safe gate before 
        applying any position sizing or risk formulas.
        """
        
        # Phase 8.0.1A Gate: Strict Enum comparison to block unapproved signals
        if decision_result.decision != DecisionType.APPROVED:
            return RiskResult(
                approved=False,
                lot_size=0.0,
                risk_amount=0.0,
                reason="Upstream decision rejected."
            )

        # Placeholder for successfully gated decisions (formulas deferred)
        return RiskResult(
            approved=False,
            lot_size=0.0,
            risk_amount=0.0,
            reason="Risk evaluation not implemented."
        )
