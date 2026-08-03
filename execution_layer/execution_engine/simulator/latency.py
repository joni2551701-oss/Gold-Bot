"""
Execution Layer — Execution Delay (Phase 60.3: Execution Simulator
Foundation, TASK 5).

Models the real-world gap between a signal existing and an order
reaching the market -- the Director's own worked example (signal at
10:00:00, order at 10:00:02) is a 2000ms latency. Deterministic, same
reproducibility reasoning as slippage.py.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class LatencyConfig:
    execution_latency_ms: int = 2000


def compute_latency(config: LatencyConfig = None) -> int:
    config = config or LatencyConfig()
    return config.execution_latency_ms


def apply_latency(signal_time: datetime, latency_ms: int) -> datetime:
    """The timestamp an order would actually reach the market, given when the signal itself fired."""
    return signal_time + timedelta(milliseconds=latency_ms)
