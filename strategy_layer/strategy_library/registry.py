"""
Strategies — setup-layer registry (TASK-CORE-007).

Registers every setup-detection strategy (the SetupStrategy instances
that return StrategyResult). This is DISTINCT from
strategies/lifecycle/strategy_registry.py, which stores StrategyDefinition
*metadata* about the live SignalCandidate strategies — this registry
holds the actual setup evaluators. build_setup_registry() returns a
fresh registry with all eleven strategies the Director listed.
"""

from typing import Dict, List, Optional

from strategy_layer.strategy_engine.base import SetupStrategy
from strategy_layer.strategy_library.amd_strategy import AMDSetupStrategy
from strategy_layer.strategy_library.liquidity_strategy import LiquiditySetupStrategy
from strategy_layer.strategy_library.fvg_strategy import FVGSetupStrategy
from strategy_layer.strategy_library.ob_strategy import OBStrategy
from strategy_layer.strategy_library.bos_strategy import BOSStrategy
from strategy_layer.strategy_library.trend_strategy import TrendStrategy
from strategy_layer.strategy_library.reversal_strategy import ReversalStrategy
from strategy_layer.strategy_library.breakout_strategy import BreakoutStrategy
from strategy_layer.strategy_library.session_strategy import SessionStrategy
from strategy_layer.strategy_library.snr_strategy import SNRStrategy
from strategy_layer.strategy_library.wyckoff_strategy import WyckoffStrategy


# The eleven setup strategies, in a stable default evaluation order.
DEFAULT_SETUP_STRATEGIES = (
    AMDSetupStrategy,
    LiquiditySetupStrategy,
    FVGSetupStrategy,
    OBStrategy,
    BOSStrategy,
    TrendStrategy,
    ReversalStrategy,
    BreakoutStrategy,
    SessionStrategy,
    SNRStrategy,
    WyckoffStrategy,
)


class DuplicateStrategyNameError(ValueError):
    """Raised when a strategy name() is already present in the registry."""


class SetupRegistry:
    """In-memory registry of SetupStrategy instances, keyed by name()."""

    def __init__(self) -> None:
        self._strategies: Dict[str, SetupStrategy] = {}

    def register(self, strategy: SetupStrategy) -> None:
        key = strategy.name()
        if key in self._strategies:
            raise DuplicateStrategyNameError(f"Strategy already registered: {key}")
        self._strategies[key] = strategy

    def get(self, name: str) -> Optional[SetupStrategy]:
        """None if never registered — never raises."""
        return self._strategies.get(name)

    def all(self) -> List[SetupStrategy]:
        return list(self._strategies.values())

    def names(self) -> List[str]:
        return list(self._strategies.keys())


def build_setup_registry() -> SetupRegistry:
    """A fresh SetupRegistry with all eleven default setup strategies registered."""
    registry = SetupRegistry()
    for strategy_cls in DEFAULT_SETUP_STRATEGIES:
        registry.register(strategy_cls())
    return registry
