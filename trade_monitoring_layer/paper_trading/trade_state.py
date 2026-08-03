"""
Lifecycle Layer — Trade State (Phase 59 Preparation, TASK 2: Paper
Trading Contract Foundation).

TradeState is the status vocabulary for a PaperTrade (paper_trade.py,
same package) -- a simulation-only trade record, never a real broker
order. Deliberately the exact four values named in this phase's brief,
no more: CREATED (built, not yet opened) -> OPEN (being monitored) ->
CLOSED (finished, a result recorded) or CANCELLED (abandoned before or
during monitoring, no result).
"""

from enum import Enum


class TradeState(Enum):
    CREATED = "CREATED"
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    CANCELLED = "CANCELLED"
