"""
Execution Layer — Simulator Models (Phase 60.3: Execution Simulator
Foundation, TASK 2).

Reuse-audit finding (TASK 1): `execution/execution_engine.py`'s
`ExecutionEngine.dispatch()` and `execution/signal_lifecycle.py`'s
`SignalLifecycle.transition()` are both deliberately inert stubs
("Currently unimplemented"/"Currently a placeholder") -- neither has
any real behavior to reuse, and per `CLAUDE.md`'s Trading Safety rules
("wiring it up is itself a change requiring explicit approval, not a
routine addition"), this phase leaves both files completely untouched
rather than extending them. A new subpackage inside the existing
`execution/` top-level package (`execution/simulator/`, not a new
`simulation/` package) is the Module-Reuse-Principle-correct choice:
step 1 (does this exist?) is no, step 2 (extend an existing file
without breaking its contract?) is no for the reason above, so step 3
(new module) applies -- scoped as narrowly as possible, a subpackage
rather than a new top-level folder.

`execution_engine.py` already defines its own `ExecutionResult`
(`dispatched: bool, reason: str`) for the live-dispatch stub's own
tiny contract -- this module's richer simulation result is
deliberately named `ExecutionSimulationResult`, not `ExecutionResult`,
to avoid a same-package naming collision with a semantically
different, still-inert concept.

Never calls a broker, MT5, or the live `ExecutionEngine`/`SignalLifecycle`
stubs -- this package only computes what a fill *would* look like,
for `backtesting/`/analytics consumption, per the Director's own rule
that this phase never touches live execution.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class SimulatedOrder:
    """
    The request going into the simulator -- never mutates the
    `lifecycle.paper_trade.PaperTrade` it references; `requested_price`
    is that trade's own `entry`, copied here, never recomputed.
    """
    order_id: str
    trade_id: str
    symbol: str
    direction: str
    requested_price: float
    lot_size: float
    requested_at: datetime


@dataclass(frozen=True)
class SimulatedFill:
    """
    The outcome of applying spread + slippage to a `SimulatedOrder`.
    `fill_price` already has both spread and slippage baked in --
    see `simulator_engine.py`'s own docstring for the exact formula.
    """
    fill_price: float
    spread_points: float
    slippage_points: float
    latency_ms: int
    filled_at: datetime


@dataclass(frozen=True)
class ExecutionSimulationResult:
    """
    filled=False means `fill` is None and `rejection_reason` explains
    why (e.g. spread exceeded the configured maximum) -- never raises,
    same "structured result, never propagate" convention as
    `RiskResult`/`ExecutionResult` before it.
    """
    filled: bool
    order: SimulatedOrder
    fill: Optional[SimulatedFill] = None
    rejection_reason: Optional[str] = None
