from typing import Optional
from dataclasses import dataclass

from decision.models import TradeDecision, DecisionAction
from signals.models import SignalCandidate, SignalType
from core_layer.emergency.emergency_manager import EmergencyManager
from core_layer.emergency.emergency_state import EmergencyState
from core_layer.logger.logger import setup_logger
from database.risk_decision_repository import RiskDecisionRepository
from risk.account_state_tracker import AccountStateTracker
from risk.duplicate_checker import DuplicateTradeChecker, DEFAULT_DUPLICATE_WINDOW_SECONDS

logger = setup_logger("RiskManager")

_UNKNOWN_SYMBOL = "UNKNOWN"

# EmergencyStates that must block any new trade approval (TASK 7):
# PAUSED/KILLED/MAINTENANCE all mean "no new approval" for Risk
# specifically, even though KILLED/MAINTENANCE already abort/skip
# earlier pipeline stages via core_layer/pipeline/pipeline_guard.py in the
# real pipeline -- this is defense in depth for any direct caller
# (tests, backtesting) that reaches RiskManager.evaluate() without
# going through PipelineGuard. WARNING is advisory only (per
# core_layer.emergency.emergency_state.EmergencyState's own docstring) and
# does not block.
_BLOCKING_EMERGENCY_STATES = (EmergencyState.PAUSED, EmergencyState.KILLED, EmergencyState.MAINTENANCE)


@dataclass(frozen=True)
class RiskConfig:
    risk_per_trade: float = 0.01
    min_risk_per_trade: float = 0.001
    max_risk_per_trade: float = 0.02
    min_risk_reward_ratio: float = 2.0
    max_daily_loss: float = 0.05
    max_drawdown: float = 0.10
    max_open_trades: int = 1
    duplicate_window_seconds: float = DEFAULT_DUPLICATE_WINDOW_SECONDS


@dataclass(frozen=True)
class RiskResult:
    approved: bool
    lot_size: float
    risk_amount: float
    risk_reward: float
    reason: str
    risk_percent: float = 0.0
    drawdown_percent: Optional[float] = None


class RiskManager:
    """
    Risk Layer — validates a decision that already exists and suggests
    a lot size. Risk never originates a trade idea, never changes
    BUY/SELL/entry/TP/SL, never selects a strategy -- it only returns
    ALLOW (approved=True) or REJECT (approved=False).

    Phase V1.0.1 (Risk Management Hardening Patch) extends this
    module's original "no MT5, no SymbolInfo, no Database, no
    Telegram, no Logger" contract with three new, deliberate,
    documented dependencies -- each read-only or append-only, none
    of them able to originate a trade or override a BUY/SELL/entry/
    TP/SL decision:

    - core_layer.emergency.emergency_manager.EmergencyManager (read-only
      get_status() only) -- so Emergency PAUSED/KILLED/MAINTENANCE
      actually stops Risk from approving, not just Telegram delivery
      (see docs/PHASE_V1_0_1_RISK_AUDIT.md section 7 and
      docs/trading/RISK_SYSTEM.md).
    - database.risk_decision_repository.RiskDecisionRepository
      (append-only `record()` calls only) -- every evaluate() call is
      logged (TASK 8), the same "core/ -> database/" one-directional
      foundation-service exception core_layer/emergency/emergency_manager.py
      already established.
    - risk.account_state_tracker.AccountStateTracker /
      risk.duplicate_checker.DuplicateTradeChecker -- both dormant
      unless a caller supplies the new optional evaluate() parameters
      (current_equity, symbol); see their own module docstrings.

    lot_size is a sizing suggestion for manual execution, never an
    order instruction. No knowledge of broker specifications (contract
    size, tick value, lot step, min/max lot, stop level).
    """

    def __init__(
        self,
        config: Optional[RiskConfig] = None,
        emergency_manager: Optional[EmergencyManager] = None,
        decision_repository: Optional[RiskDecisionRepository] = None,
        account_state_tracker: Optional[AccountStateTracker] = None,
        duplicate_checker: Optional[DuplicateTradeChecker] = None,
    ):
        self.config = config or RiskConfig()
        self.emergency_manager = emergency_manager or EmergencyManager()
        self.decision_repository = decision_repository or RiskDecisionRepository()
        self.account_state_tracker = account_state_tracker or AccountStateTracker()
        self.duplicate_checker = duplicate_checker or DuplicateTradeChecker()

    def evaluate(
        self,
        trade_decision: TradeDecision,
        account_balance: Optional[float] = None,
        current_equity: Optional[float] = None,
        symbol: Optional[str] = None,
    ) -> RiskResult:
        """
        Entry point for Risk Layer. Rejects anything the Decision
        Engine did not APPROVE, anything Emergency state currently
        blocks, invalid geometry, an out-of-bounds configured risk %,
        a below-minimum risk/reward ratio, invalid balance/equity
        input, a detected duplicate, an exceeded drawdown, or an
        exceeded daily loss -- in that order, first match wins. For a
        surviving APPROVE, validates the stop-loss distance and
        computes risk/reward from the underlying SignalCandidate.

        account_balance/current_equity/symbol are all optional and
        additive (Phase V1.0.1) -- `core/pipeline.py` and
        `backtesting/backtest_engine.py` (both untouched this phase,
        both Trading Core / locked) call this with only
        `trade_decision`, so every check gated behind one of these
        three parameters is dormant in the live pipeline today,
        exactly like account_balance already was before this phase.
        GoldBot is semi-automated (no MT5/broker connection), so it
        has no built-in source of any of the three.
        """
        strategy_name = trade_decision.signal.strategy_name
        direction = trade_decision.signal.signal_type.value
        symbol_for_log = symbol or _UNKNOWN_SYMBOL

        if trade_decision.action != DecisionAction.APPROVE:
            return self._reject(
                symbol_for_log, strategy_name, direction,
                f"Decision Engine action was {trade_decision.action.value}, not APPROVE.",
                "DECISION_NOT_APPROVE",
            )

        emergency_status = self.emergency_manager.get_status()
        if emergency_status.state in _BLOCKING_EMERGENCY_STATES:
            return self._reject(
                symbol_for_log, strategy_name, direction,
                f"Trading is {emergency_status.state.value}: no new trade approval "
                f"(reason={emergency_status.reason or 'n/a'}).",
                "EMERGENCY_PAUSED",
            )

        signal = trade_decision.signal

        if not self.validate_geometry(signal):
            return self._reject(
                symbol_for_log, strategy_name, direction,
                f"Invalid {signal.signal_type.value} geometry: "
                f"entry={signal.entry}, stop_loss={signal.stop_loss}, "
                f"take_profit={signal.take_profit}.",
                "GEOMETRY",
            )

        stop_loss_distance = abs(signal.entry - signal.stop_loss)

        if not self.validate_stop_loss_distance(stop_loss_distance):
            return self._reject(
                symbol_for_log, strategy_name, direction,
                f"Invalid stop-loss distance: {stop_loss_distance}.", "INVALID_INPUT",
            )

        if not (self.config.min_risk_per_trade <= self.config.risk_per_trade <= self.config.max_risk_per_trade):
            return self._reject(
                symbol_for_log, strategy_name, direction,
                f"Risk limit exceeded: configured risk_per_trade={self.config.risk_per_trade:.4f} "
                f"outside [{self.config.min_risk_per_trade:.4f}, {self.config.max_risk_per_trade:.4f}].",
                "RISK_LIMIT",
            )

        risk_reward = self.calculate_risk_reward(signal.entry, signal.stop_loss, signal.take_profit)

        if risk_reward < self.config.min_risk_reward_ratio:
            return self._reject(
                symbol_for_log, strategy_name, direction,
                f"Risk Reward ratio below minimum: {risk_reward:.2f} < "
                f"{self.config.min_risk_reward_ratio:.2f}.",
                "RR_BELOW_MIN", risk_reward=risk_reward,
            )

        if account_balance is not None and account_balance <= 0:
            return self._reject(
                symbol_for_log, strategy_name, direction,
                f"Invalid account balance: {account_balance}.", "INVALID_INPUT", risk_reward=risk_reward,
            )

        if current_equity is not None and current_equity <= 0:
            return self._reject(
                symbol_for_log, strategy_name, direction,
                f"Invalid current equity: {current_equity}.", "INVALID_INPUT", risk_reward=risk_reward,
            )

        if symbol is not None:
            duplicate = self.duplicate_checker.check(
                symbol, direction, strategy_name, within_seconds=self.config.duplicate_window_seconds,
            )
            if duplicate.duplicate:
                return self._reject(
                    symbol_for_log, strategy_name, direction,
                    duplicate.reason, "DUPLICATE", risk_reward=risk_reward,
                )

        drawdown_percent = None
        if current_equity is not None:
            drawdown_result = self.account_state_tracker.check_drawdown(
                symbol_for_log, current_equity, self.config.max_drawdown,
            )
            drawdown_percent = drawdown_result.drawdown_percent
            if drawdown_result.paused:
                return self._reject(
                    symbol_for_log, strategy_name, direction,
                    drawdown_result.reason, "DRAWDOWN",
                    risk_reward=risk_reward, drawdown_percent=drawdown_percent,
                )

        if account_balance is not None:
            daily_loss_result = self.account_state_tracker.check_daily_loss(
                symbol_for_log, account_balance, self.config.max_daily_loss,
            )
            if daily_loss_result.blocked:
                return self._reject(
                    symbol_for_log, strategy_name, direction,
                    daily_loss_result.reason, "DAILY_LOSS",
                    risk_reward=risk_reward, drawdown_percent=drawdown_percent,
                )

        if account_balance is None:
            result = RiskResult(
                approved=True, lot_size=0.0, risk_amount=0.0, risk_reward=risk_reward,
                reason="Approved. Position sizing not computed: no account_balance supplied.",
                risk_percent=self.config.risk_per_trade, drawdown_percent=drawdown_percent,
            )
            self._log(symbol_for_log, strategy_name, direction, result, None)
            return result

        risk_amount = self.calculate_risk_amount(account_balance, self.config.risk_per_trade)
        lot_size = self.calculate_position_size(risk_amount, stop_loss_distance)

        result = RiskResult(
            approved=True, lot_size=lot_size, risk_amount=risk_amount, risk_reward=risk_reward,
            reason=f"Approved. risk_reward={risk_reward:.2f}, risk_amount={risk_amount:.2f}.",
            risk_percent=self.config.risk_per_trade, drawdown_percent=drawdown_percent,
        )
        self._log(symbol_for_log, strategy_name, direction, result, None)
        return result

    def _reject(
        self,
        symbol: str,
        strategy_name: str,
        direction: str,
        reason: str,
        reject_category: str,
        risk_reward: float = 0.0,
        drawdown_percent: Optional[float] = None,
    ) -> RiskResult:
        result = RiskResult(
            approved=False, lot_size=0.0, risk_amount=0.0, risk_reward=risk_reward,
            reason=reason, drawdown_percent=drawdown_percent,
        )
        self._log(symbol, strategy_name, direction, result, reject_category)
        return result

    def _log(
        self,
        symbol: str,
        strategy_name: str,
        direction: str,
        result: "RiskResult",
        reject_category: Optional[str],
    ) -> None:
        """
        Persists one risk_decisions row for every evaluate() call
        (TASK 8) -- never raises: a logging failure must never turn an
        otherwise-valid Risk verdict into an exception, same "capture,
        never break the caller" posture as
        monitoring.error_monitor.ErrorMonitor.capture().
        """
        try:
            self.decision_repository.record(
                symbol=symbol,
                decision="APPROVE" if result.approved else "REJECT",
                reason=result.reason,
                strategy_name=strategy_name,
                direction=direction,
                risk_percent=result.risk_percent or None,
                risk_reward=result.risk_reward,
                drawdown_percent=result.drawdown_percent,
                reject_category=reject_category,
            )
        except Exception as e:
            logger.warning(f"risk_decision_log_failed: {e}")

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

    def validate_geometry(
        self,
        signal: SignalCandidate,
    ) -> bool:
        """
        A BUY must risk downward and target upward
        (stop_loss < entry < take_profit); a SELL is the mirror
        (take_profit < entry < stop_loss). Any other arrangement is
        not executable and must never reach a trader.
        """
        if signal.signal_type == SignalType.BUY:
            return signal.stop_loss < signal.entry < signal.take_profit
        if signal.signal_type == SignalType.SELL:
            return signal.take_profit < signal.entry < signal.stop_loss
        return False
