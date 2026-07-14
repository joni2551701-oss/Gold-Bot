"""
Configuration Layer — feature flags foundation (Phase A13).

FeatureFlags is a foundation for future feature gating -- it is not
business logic, and its existence does not mean any of these features
are implemented. See docs/CONFIGURATION_MANAGEMENT.md for the full
contract.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class FeatureFlags:
    """
    Every flag defaults to False -- a safe default is required for
    every new flag (see docs/CONFIGURATION_MANAGEMENT.md's Design
    Rules). A flag existing here does not mean the feature exists:
    ai/, strategies/, decision/, risk/, and core/pipeline.py are all
    unmodified by this phase and read none of these flags. Frozen,
    like every other Phase A model in this codebase -- "toggling" a
    flag means constructing a new FeatureFlags (e.g. via
    dataclasses.replace()), not mutating one in place.

    enable_ai: reserved for a future real AI provider decision (see
        docs/AI_ARCHITECTURE.md) -- ai/ai_analyzer.py stays a
        heuristic stub regardless of this flag's value in this phase.
    enable_crypto: reserved for a future Crypto AssetType profile
        (assets/, Phase A12) -- no Crypto data provider exists.
    enable_swing: reserved for a future swing-timeframe strategy or
        supported_styles entry (strategies/lifecycle/, Phase A11) --
        no such strategy exists.
    enable_ai_memory: reserved for a future AI Assistant memory/
        journal feature (see ai/journal/trade_journal.py, which exists
        independently of this flag and is unaffected by it).
    enable_replay: reserved for a future backtest/replay harness
        (named in docs/FEATURE_ENGINEERING.md's and
        docs/STRATEGY_LIFECYCLE.md's own "Future" sections) -- no
        replay harness exists.
    """
    enable_ai: bool = False
    enable_crypto: bool = False
    enable_swing: bool = False
    enable_ai_memory: bool = False
    enable_replay: bool = False


# The single safe-default instance -- every flag off. Not a singleton
# enforcement mechanism (a caller can still construct its own
# FeatureFlags), just a convenient, explicit "nothing enabled" value.
DEFAULT_FLAGS = FeatureFlags()
