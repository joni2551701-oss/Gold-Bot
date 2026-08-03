from typing import Dict, List, Optional
from dataclasses import dataclass, field

from database_layer.trade_repository.signal_repository import SignalRepository
from core_layer.logger.logger import setup_logger

logger = setup_logger("PerformanceTracker")


@dataclass(frozen=True)
class PerformanceConfig:
    enabled: bool = True
    # "High confidence" bucket threshold, on the same 0.0-1.0 scale as
    # confidence_score (matches SignalCandidate/TradeDecision confidence
    # convention used across the rest of the codebase).
    high_confidence_threshold: float = 0.80


@dataclass(frozen=True)
class StrategyStats:
    total_signals: int = 0
    win_count: int = 0
    loss_count: int = 0
    win_rate: float = 0.0


@dataclass(frozen=True)
class ConfidenceBucketStats:
    total_signals: int = 0
    win_count: int = 0
    loss_count: int = 0


@dataclass(frozen=True)
class PerformanceResult:
    calculated: bool
    reason: str
    total_signals: int = 0
    closed_signals: int = 0
    win_count: int = 0
    loss_count: int = 0
    breakeven_count: int = 0
    # Fraction (0.0-1.0), not a percentage -- same convention as
    # SignalCandidate.confidence / TradeDecision.confidence elsewhere
    # in the codebase. WIN / (WIN + LOSS); BE is ignored for v0.1.
    win_rate: float = 0.0
    strategy_breakdown: Dict[str, StrategyStats] = field(default_factory=dict)
    high_confidence_stats: ConfidenceBucketStats = field(default_factory=ConfidenceBucketStats)


class PerformanceTracker:
    """
    Monitoring Layer — historical performance statistics.

    Reads closed/open signals via SignalRepository and computes basic,
    deterministic counts and rates. No ML, no AI learning, no
    optimization, no dashboard -- pure arithmetic over data that is
    already persisted by the Signal Persistence / Manual Result Update
    layers (Phase 27.1 / 27.2).

    Called independently (e.g. on demand from a future Telegram
    command), not from the trading pipeline -- historical analysis is
    not part of signal generation.
    """

    def __init__(
        self,
        config: Optional[PerformanceConfig] = None,
        signal_repository: Optional[SignalRepository] = None,
    ):
        self.config = config or PerformanceConfig()
        # Lazy, same pattern as ResultHandler: constructing
        # SignalRepository() touches disk (schema init). Bare
        # PerformanceTracker() (e.g. main.py) must not do that until
        # calculate() is actually invoked. May be injected for tests.
        self._signal_repository = signal_repository

    def _get_repository(self) -> SignalRepository:
        if self._signal_repository is None:
            self._signal_repository = SignalRepository()
        return self._signal_repository

    def calculate(self) -> PerformanceResult:
        """
        Computes basic statistics from the signals table. Never
        raises: a disabled config or a database error is reported as
        calculated=False with a reason, never an exception.
        """
        if not self.config.enabled:
            return PerformanceResult(calculated=False, reason="PerformanceTracker disabled")

        try:
            repository = self._get_repository()
            open_signals = repository.get_open_signals()
            closed_signals = repository.get_closed_signals()
        except Exception as e:
            logger.warning(f"Performance calculation failed: {e}")
            return PerformanceResult(calculated=False, reason=f"Database error: {e}")

        win_count = sum(1 for row in closed_signals if row.get("result") == "WIN")
        loss_count = sum(1 for row in closed_signals if row.get("result") == "LOSS")
        breakeven_count = sum(1 for row in closed_signals if row.get("result") == "BE")

        win_rate = self._win_rate(win_count, loss_count)
        strategy_breakdown = self._build_strategy_breakdown(closed_signals)
        high_confidence_stats = self._build_confidence_bucket(
            closed_signals, self.config.high_confidence_threshold
        )

        return PerformanceResult(
            calculated=True,
            reason="",
            total_signals=len(open_signals) + len(closed_signals),
            closed_signals=len(closed_signals),
            win_count=win_count,
            loss_count=loss_count,
            breakeven_count=breakeven_count,
            win_rate=win_rate,
            strategy_breakdown=strategy_breakdown,
            high_confidence_stats=high_confidence_stats,
        )

    @staticmethod
    def _win_rate(win_count: int, loss_count: int) -> float:
        """WIN / (WIN + LOSS). BE is excluded from both sides for v0.1."""
        decided = win_count + loss_count
        if decided == 0:
            return 0.0
        return win_count / decided

    @classmethod
    def _build_strategy_breakdown(cls, closed_signals: List[Dict]) -> Dict[str, StrategyStats]:
        """Groups closed signals by strategy_name and computes per-strategy win rate."""
        grouped: Dict[str, Dict[str, int]] = {}
        for row in closed_signals:
            name = row.get("strategy_name") or "UNKNOWN"
            bucket = grouped.setdefault(name, {"total": 0, "win": 0, "loss": 0})
            bucket["total"] += 1
            result = row.get("result")
            if result == "WIN":
                bucket["win"] += 1
            elif result == "LOSS":
                bucket["loss"] += 1

        return {
            name: StrategyStats(
                total_signals=counts["total"],
                win_count=counts["win"],
                loss_count=counts["loss"],
                win_rate=cls._win_rate(counts["win"], counts["loss"]),
            )
            for name, counts in grouped.items()
        }

    @staticmethod
    def _build_confidence_bucket(closed_signals: List[Dict], threshold: float) -> ConfidenceBucketStats:
        """Simple confidence-accuracy check: signals at/above threshold, and their outcomes."""
        total = win = loss = 0
        for row in closed_signals:
            score = row.get("confidence_score")
            if not isinstance(score, (int, float)) or score < threshold:
                continue
            total += 1
            result = row.get("result")
            if result == "WIN":
                win += 1
            elif result == "LOSS":
                loss += 1
        return ConfidenceBucketStats(total_signals=total, win_count=win, loss_count=loss)
