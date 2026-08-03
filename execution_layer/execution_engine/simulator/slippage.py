"""
Execution Layer — Slippage Engine (Phase 60.3: Execution Simulator
Foundation, TASK 3).

Requested Entry -> Market Price -> Slippage -> Actual Fill. Gold
(XAUUSD) trades in wide-enough price swings that slippage is a real,
non-negligible cost -- this module models it as a deterministic,
configurable price offset (not a random/stochastic draw): the same
`SlippageConfig` always produces the same `compute_slippage()` value
for a given signal, which keeps a backtest run reproducible and
directly comparable across repeated runs. A future phase could layer
a stochastic distribution on top of this deterministic base without
changing `apply_slippage()`'s own contract.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class SlippageConfig:
    """points are price units directly (XAUUSD is quoted in dollars, e.g. 0.15 = $0.15), matching the Director's own worked example (2350.00 requested -> 2350.15 filled)."""
    points: float = 0.10
    max_points: float = 0.50


def compute_slippage(config: SlippageConfig = None) -> float:
    """The deterministic slippage magnitude for one fill -- always config.points, clamped to max_points."""
    config = config or SlippageConfig()
    return min(config.points, config.max_points)


def apply_slippage(requested_price: float, direction: str, slippage_points: float) -> float:
    """
    Slippage always moves the fill against the trader: worse (higher)
    for a BUY, worse (lower) for a SELL -- matching the Director's own
    worked example exactly (BUY 2350.00 -> fill 2350.15).
    """
    if direction == "BUY":
        return requested_price + slippage_points
    if direction == "SELL":
        return requested_price - slippage_points
    raise ValueError(f"Unknown direction: {direction!r}")
