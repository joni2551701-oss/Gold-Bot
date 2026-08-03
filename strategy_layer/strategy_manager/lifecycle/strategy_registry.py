"""
Strategy Lifecycle — registry (Phase A11).

StrategyRegistry stores StrategyDefinition metadata only -- it does
not run a strategy, does not generate a signal, and does not write to
the database. See docs/STRATEGY_LIFECYCLE.md for the full contract.

build_default_registry() registers the three strategies that already
exist and already run in production via
strategy_layer/strategy_manager/strategy_manager.py's StrategyManager -- no new strategy is
introduced. Each StrategyDefinition.id matches the real
SignalCandidate.strategy_name string each strategy already produces
(strategy_layer/strategy_library/liquidity_strategy.py, fvg_strategy.py, amd_strategy.py),
so a future consumer can join registry metadata against actual
signals without a separate mapping table.
"""

from typing import Dict, List, Optional, Tuple

from strategy_layer.strategy_manager.lifecycle.strategy_model import StrategyDefinition
from strategy_layer.strategy_manager.lifecycle.strategy_status import StrategyStatus

# The real symbol/interval this codebase runs today (main.py,
# telegram/signal_service.py's DEFAULT_SYMBOL) -- not a placeholder.
_SUPPORTED_ASSETS = ["XAUUSD"]
_SUPPORTED_TIMEFRAMES = ["M15"]
_SUPPORTED_STYLES = ["INTRADAY"]

# The three strategies strategy_layer/strategy_manager/strategy_manager.py's StrategyManager
# already runs in production today -- all ACTIVE, since none is
# currently disabled/deprecated/testing-only. version="1.0" for all
# three: no versioning history exists yet.
DEFAULT_STRATEGIES: Tuple[StrategyDefinition, ...] = (
    StrategyDefinition(
        id="LIQUIDITY_SWEEP_STRATEGY",
        name="Liquidity Sweep",
        version="1.0",
        status=StrategyStatus.ACTIVE,
        supported_assets=list(_SUPPORTED_ASSETS),
        supported_styles=list(_SUPPORTED_STYLES),
        supported_timeframes=list(_SUPPORTED_TIMEFRAMES),
    ),
    StrategyDefinition(
        id="FVG_STRATEGY",
        name="Fair Value Gap",
        version="1.0",
        status=StrategyStatus.ACTIVE,
        supported_assets=list(_SUPPORTED_ASSETS),
        supported_styles=list(_SUPPORTED_STYLES),
        supported_timeframes=list(_SUPPORTED_TIMEFRAMES),
    ),
    StrategyDefinition(
        id="AMD_STRATEGY",
        name="AMD (Accumulation-Manipulation-Distribution)",
        version="1.0",
        status=StrategyStatus.ACTIVE,
        supported_assets=list(_SUPPORTED_ASSETS),
        supported_styles=list(_SUPPORTED_STYLES),
        supported_timeframes=list(_SUPPORTED_TIMEFRAMES),
    ),
)


class DuplicateStrategyIdError(ValueError):
    """Raised by register() when the id is already present in the registry."""


class StrategyRegistry:
    """
    An in-memory metadata store, keyed by StrategyDefinition.id.
    Never imports strategy_layer/strategy_manager/strategy_manager.py or any strategies/*.py
    strategy class -- it stores metadata about them, it does not
    instantiate or run them.
    """

    def __init__(self) -> None:
        self._definitions: Dict[str, StrategyDefinition] = {}

    def register(self, definition: StrategyDefinition) -> None:
        """Raises DuplicateStrategyIdError if definition.id is already registered."""
        if definition.id in self._definitions:
            raise DuplicateStrategyIdError(
                f"Strategy id already registered: {definition.id}"
            )
        self._definitions[definition.id] = definition

    def get(self, strategy_id: str) -> Optional[StrategyDefinition]:
        """Returns None if strategy_id was never registered -- never raises."""
        return self._definitions.get(strategy_id)

    def list(self) -> List[StrategyDefinition]:
        """Every registered StrategyDefinition, regardless of status."""
        return list(self._definitions.values())

    def active(self) -> List[StrategyDefinition]:
        """Only StrategyDefinitions with status == StrategyStatus.ACTIVE."""
        return [d for d in self._definitions.values() if d.status == StrategyStatus.ACTIVE]


def build_default_registry() -> StrategyRegistry:
    """
    Returns a fresh StrategyRegistry with the three existing, real
    strategies registered (DEFAULT_STRATEGIES) -- not a shared
    singleton, so tests/future callers each get an independent
    registry unaffected by another caller's register() calls.
    """
    registry = StrategyRegistry()
    for definition in DEFAULT_STRATEGIES:
        registry.register(definition)
    return registry
