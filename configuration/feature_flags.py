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
    enable_personal_ai: reserved for the Personal AI Assistant
        (Phase 65.3, `assistant/`) -- always False by default; even
        when True, `assistant.access.is_personal_ai_enabled_for()`
        additionally requires `AIRole.OWNER` (Admin/VIP/Premium/Free
        all BLOCK regardless of this flag's value, per TASK 7).
    enable_trading_analyst: reserved for the AI Trading Analyst
        (Phase 66.0, `ai/trading_analyst/`) -- always False by
        default; even when True,
        `ai.trading_analyst.access.is_trading_analyst_enabled_for()`
        additionally requires `AIRole.OWNER` (TASK 9).
    enable_chart_intelligence: reserved for AI Chart Intelligence
        (Phase 66.1, `ai/chart_intelligence/`) -- always False by
        default; even when True,
        `ai.chart_intelligence.access.is_chart_intelligence_enabled_for()`
        additionally requires `AIRole.OWNER` (TASK 7).
    enable_trade_journal: reserved for AI Trade Journal Intelligence
        (Phase 66.2, `ai/trade_journal/`) -- always False by default;
        even when True,
        `ai.trade_journal.access.is_trade_journal_enabled_for()`
        additionally requires `AIRole.OWNER` (TASK 7). Distinct from
        `enable_ai_memory` (whose own docstring already references
        `ai/journal/trade_journal.py` but does not govern it) -- this
        is a dedicated flag for the new, unrelated `ai/trade_journal/`
        package.
    enable_learning_intelligence: reserved for AI Learning Intelligence
        (Phase 66.3, `ai/learning/`) -- always False by default; even
        when True,
        `ai.learning.access.is_learning_intelligence_enabled_for()`
        additionally requires `AIRole.OWNER` (TASK 6). Distinct from
        the pre-existing, unrelated `learning/` top-level package
        (Phase 60.6/60.7), which reads no feature flag at all.
    enable_coaching_intelligence: reserved for AI Coaching Intelligence
        (Phase 66.4, `ai/coaching/`) -- always False by default; even
        when True,
        `ai.coaching.access.is_coaching_intelligence_enabled_for()`
        additionally requires `AIRole.OWNER` (TASK 6).
    enable_performance_intelligence: reserved for AI Performance
        Intelligence (Phase 66.5, `ai/performance/`) -- always False
        by default; even when True,
        `ai.performance.access.is_performance_intelligence_enabled_for()`
        additionally requires `AIRole.OWNER` (TASK 8).
    enable_strategy_intelligence: reserved for AI Strategy Intelligence
        (Phase 66.6, `ai/strategy/`) -- always False by default; even
        when True,
        `ai.strategy.access.is_strategy_intelligence_enabled_for()`
        additionally requires `AIRole.OWNER` (TASK 7).
    """
    enable_ai: bool = False
    enable_crypto: bool = False
    enable_swing: bool = False
    enable_ai_memory: bool = False
    enable_replay: bool = False
    enable_personal_ai: bool = False
    enable_trading_analyst: bool = False
    enable_chart_intelligence: bool = False
    enable_trade_journal: bool = False
    enable_learning_intelligence: bool = False
    enable_coaching_intelligence: bool = False
    enable_performance_intelligence: bool = False
    enable_strategy_intelligence: bool = False


# The single safe-default instance -- every flag off. Not a singleton
# enforcement mechanism (a caller can still construct its own
# FeatureFlags), just a convenient, explicit "nothing enabled" value.
DEFAULT_FLAGS = FeatureFlags()
