"""
AI Layer — AI Portfolio Intelligence Owner Mode Gate (Phase 66.7: AI
Portfolio Intelligence Foundation, TASK 7).

Mirrors `ai.strategy.access.is_strategy_intelligence_enabled_for()`'s
own shape exactly: Owner-only, gated by a dedicated feature flag.
"""

from ai.access.permissions import AIRole
from core_layer.configuration.feature_flags import DEFAULT_FLAGS, FeatureFlags


def is_portfolio_intelligence_enabled_for(
    role: AIRole, flags: FeatureFlags = DEFAULT_FLAGS
) -> bool:
    """True only when both `flags.enable_portfolio_intelligence` is set and `role` is `AIRole.OWNER`."""
    if not flags.enable_portfolio_intelligence:
        return False
    return role == AIRole.OWNER
