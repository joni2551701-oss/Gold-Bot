"""
Strategy Lifecycle — data model (Phase A11).

StrategyDefinition is standard metadata about a strategy -- not the
strategy itself. It carries no trading logic, generates no signal, and
does not run anything -- see docs/STRATEGY_LIFECYCLE.md for the full
contract and strategy_registry.py for how the existing three
strategies (strategy_layer/strategy_library/liquidity_strategy.py, fvg_strategy.py,
amd_strategy.py) are registered.
"""

from dataclasses import dataclass
from typing import List, Optional

from strategy_layer.strategy_manager.lifecycle.strategy_status import StrategyStatus


@dataclass(frozen=True)
class StrategyDefinition:
    """
    id: matches the real strategies/*.py strategy's
        SignalCandidate.strategy_name exactly (e.g.
        "LIQUIDITY_SWEEP_STRATEGY") -- so a future consumer (Phase 59
        Validation, Analytics) can join a StrategyDefinition against
        actual SignalCandidate/SignalRecord rows without a separate
        mapping table.
    name: human-readable display name (e.g. "Liquidity Sweep").
    version: a plain string, e.g. "1.0" -- no versioning history exists
        yet; every currently-registered strategy starts at "1.0".
    status: StrategyStatus (TESTING/ACTIVE/DISABLED/DEPRECATED).
        Metadata only -- does not control whether StrategyManager
        actually runs the strategy.
    supported_assets: e.g. ["XAUUSD"] -- the real symbol constant this
        codebase runs today (see telegram/signal_service.py's
        DEFAULT_SYMBOL), not a placeholder.
    supported_styles: e.g. ["INTRADAY"] -- descriptive metadata, not a
        computed value.
    supported_timeframes: e.g. ["M15"] -- the real interval this
        codebase runs today (see main.py).
    performance: always None in this phase -- an explicit hook for a
        future, separately-approved phase (Phase 59 Validation,
        Analytics) to populate. Never a fabricated number.
    win_rate: always None in this phase -- same rationale as
        performance.
    last_validation: always None in this phase -- same rationale as
        performance; a future phase would populate this as an ISO
        timestamp string.
    """
    id: str
    name: str
    version: str
    status: StrategyStatus
    supported_assets: List[str]
    supported_styles: List[str]
    supported_timeframes: List[str]
    performance: Optional[float] = None
    win_rate: Optional[float] = None
    last_validation: Optional[str] = None
