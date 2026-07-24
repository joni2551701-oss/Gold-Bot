"""
Execution Layer — Simulator Engine (Phase 60.3: Execution Simulator
Foundation, TASK 6).

    Decision APPROVE -> Risk Approved -> Execution Simulator -> Fill/Reject -> Trade Lifecycle

`ExecutionSimulator.simulate()` is the one entry point, taking an
already-OPEN `lifecycle.paper_trade.PaperTrade` (i.e. Decision already
APPROVEd and Risk already approved -- this module does not re-check
either) plus its `risk.risk_manager.RiskResult` (for `lot_size`), and
producing an `ExecutionSimulationResult` -- never mutating the
`PaperTrade` itself, never calling `execution/execution_engine.py`'s
still-inert `ExecutionEngine`, never touching `decision/`/`risk/`.

Fill price formula: `apply_slippage(requested_price, direction,
slippage_points + spread_points)` -- spread and slippage are both
adverse-to-the-trader costs, folded into one offset via the same
"worse for BUY, worse for SELL" direction `slippage.py`'s own
`apply_slippage()` already implements, rather than a second
near-duplicate function.
"""

import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from execution.simulator.latency import LatencyConfig, apply_latency, compute_latency
from execution.simulator.models import ExecutionSimulationResult, SimulatedFill, SimulatedOrder
from execution.simulator.slippage import SlippageConfig, apply_slippage, compute_slippage
from execution.simulator.spread import SpreadConfig, get_spread, is_spread_too_wide

if TYPE_CHECKING:
    from lifecycle.paper_trade import PaperTrade
    from risk.risk_manager import RiskResult


class ExecutionSimulator:
    def __init__(
        self,
        slippage_config: Optional[SlippageConfig] = None,
        spread_config: Optional[SpreadConfig] = None,
        latency_config: Optional[LatencyConfig] = None,
    ):
        self.slippage_config = slippage_config or SlippageConfig()
        self.spread_config = spread_config or SpreadConfig()
        self.latency_config = latency_config or LatencyConfig()

    def simulate(
        self,
        paper_trade: 'PaperTrade',
        risk_result: 'RiskResult',
        session: Optional[str] = None,
        signal_time: Optional[datetime] = None,
    ) -> ExecutionSimulationResult:
        order = SimulatedOrder(
            order_id=str(uuid.uuid4()),
            trade_id=paper_trade.trade_id,
            symbol=paper_trade.symbol,
            direction=paper_trade.direction,
            requested_price=paper_trade.entry,
            lot_size=risk_result.lot_size,
            requested_at=signal_time or datetime.now(timezone.utc),
        )

        spread_points = get_spread(session, self.spread_config)
        if is_spread_too_wide(spread_points, self.spread_config):
            return ExecutionSimulationResult(
                filled=False, order=order,
                rejection_reason=f"Spread {spread_points:.2f} too wide (max {self.spread_config.max_points:.2f})",
            )

        slippage_points = compute_slippage(self.slippage_config)
        fill_price = apply_slippage(order.requested_price, order.direction, slippage_points + spread_points)
        latency_ms = compute_latency(self.latency_config)

        fill = SimulatedFill(
            fill_price=fill_price,
            spread_points=spread_points,
            slippage_points=slippage_points,
            latency_ms=latency_ms,
            filled_at=apply_latency(order.requested_at, latency_ms),
        )
        return ExecutionSimulationResult(filled=True, order=order, fill=fill)
