"""
strategies/ — setup-detection layer.

Two coexisting contracts:
  * Live SignalCandidate path (frozen): strategy_manager.StrategyManager
    runs LiquidityStrategy/FVGStrategy/AMDStrategy.analyze() into signals/.
  * Setup layer (TASK-CORE-007): SetupManager runs the eleven
    SetupStrategy classes, each returning a StrategyResult (setup yes/no,
    no signal). Not wired into core/pipeline.py.

Only the setup-layer public API is re-exported here; the live path is
imported directly by signal_layer/signal_engine/signal_engine.py and is left untouched.
"""

from strategy_layer.strategy_engine.base import SetupStrategy
from strategy_layer.strategy_engine.result import StrategyResult, StrategyDirection, SetupStatus, compute_rr
from strategy_layer.strategy_library.registry import SetupRegistry, build_setup_registry, DEFAULT_SETUP_STRATEGIES
from strategy_layer.strategy_manager.manager import SetupManager, SetupEvaluation

__all__ = [
    "SetupStrategy",
    "StrategyResult",
    "StrategyDirection",
    "SetupStatus",
    "compute_rr",
    "SetupRegistry",
    "build_setup_registry",
    "DEFAULT_SETUP_STRATEGIES",
    "SetupManager",
    "SetupEvaluation",
]

# Canonical documentation: 05_Strategy_Layer/StrategyLibrary/README.md
