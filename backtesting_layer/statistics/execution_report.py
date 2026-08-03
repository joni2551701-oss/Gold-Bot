"""
Analytics Layer — Execution Report (Phase 60.3: Execution Simulator
Foundation, TASK 8).

Packages an `execution_layer.execution_engine.simulator.models.ExecutionSimulationResult`
into the persistence/reporting shape every other Phase 59.x/60.x
report module already uses (`backtesting_layer/statistics/dataset_report.py`,
`backtesting_layer/statistics/strategy_report.py`, etc.) — requested price, fill price,
slippage, latency, rejection reason, kept explicitly "for later
comparison against real MT5" per the Director's own brief. No new
execution logic here; this module only reads an already-computed
`ExecutionSimulationResult`.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from execution_layer.execution_engine.simulator.models import ExecutionSimulationResult


@dataclass(frozen=True)
class ExecutionAnalyticsRecord:
    order_id: str
    trade_id: str
    symbol: str
    direction: str
    requested_price: float
    filled: bool
    fill_price: Optional[float] = None
    slippage_points: Optional[float] = None
    spread_points: Optional[float] = None
    latency_ms: Optional[int] = None
    rejection_reason: Optional[str] = None
    created_at: Optional[datetime] = None


@dataclass(frozen=True)
class ExecutionAnalyticsSummary:
    """Aggregated across many records -- the future `/execution_report` command's own comparison-ready view."""
    total_orders: int
    filled_count: int
    rejected_count: int
    average_slippage_points: Optional[float] = None
    average_latency_ms: Optional[float] = None

    @property
    def fill_rate(self) -> float:
        return self.filled_count / self.total_orders if self.total_orders else 0.0


def build_execution_record(result: 'ExecutionSimulationResult') -> ExecutionAnalyticsRecord:
    """Never raises: a rejected result simply produces None for every fill-only field."""
    fill = result.fill
    return ExecutionAnalyticsRecord(
        order_id=result.order.order_id,
        trade_id=result.order.trade_id,
        symbol=result.order.symbol,
        direction=result.order.direction,
        requested_price=result.order.requested_price,
        filled=result.filled,
        fill_price=fill.fill_price if fill else None,
        slippage_points=fill.slippage_points if fill else None,
        spread_points=fill.spread_points if fill else None,
        latency_ms=fill.latency_ms if fill else None,
        rejection_reason=result.rejection_reason,
        created_at=datetime.now(timezone.utc),
    )


def summarize_execution_records(records: List[ExecutionAnalyticsRecord]) -> ExecutionAnalyticsSummary:
    """Never raises: an empty list produces an all-zero summary, not an error (same convention as build_strategy_report())."""
    filled = [r for r in records if r.filled]
    rejected = [r for r in records if not r.filled]
    slippages = [r.slippage_points for r in filled if r.slippage_points is not None]
    latencies = [r.latency_ms for r in filled if r.latency_ms is not None]
    return ExecutionAnalyticsSummary(
        total_orders=len(records),
        filled_count=len(filled),
        rejected_count=len(rejected),
        average_slippage_points=sum(slippages) / len(slippages) if slippages else None,
        average_latency_ms=sum(latencies) / len(latencies) if latencies else None,
    )


def format_execution_record(record: ExecutionAnalyticsRecord) -> str:
    """The future `/execution_status` per-order detail line."""
    if not record.filled:
        return f"{record.symbol} {record.direction} @ {record.requested_price} -- REJECTED ({record.rejection_reason})"
    return (
        f"{record.symbol} {record.direction} requested={record.requested_price} "
        f"fill={record.fill_price} slippage={record.slippage_points} "
        f"spread={record.spread_points} latency={record.latency_ms}ms"
    )
