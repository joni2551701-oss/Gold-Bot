"""
strategies/ — setup-detection layer.

Two coexisting contracts:
  * Live SignalCandidate path (frozen): strategy_manager.StrategyManager
    runs LiquidityStrategy/FVGStrategy/AMDStrategy.analyze() into signals/.
  * Setup layer (TASK-CORE-007): SetupManager runs the eleven
    SetupStrategy classes, each returning a StrategyResult (setup yes/no,
    no signal). Not wired into core/pipeline.py.

Only the setup-layer public API is re-exported here; the live path is
imported directly by signals/signal_engine.py and is left untouched.
"""

from strategies.base import SetupStrategy
from strategies.result import StrategyResult, StrategyDirection, SetupStatus, compute_rr
from strategies.registry import SetupRegistry, build_setup_registry, DEFAULT_SETUP_STRATEGIES
from strategies.manager import SetupManager, SetupEvaluation

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
