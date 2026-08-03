"""
AI Layer — AI Strategy Intelligence Owner Mode Gate (Phase 66.6: AI
Strategy Intelligence Foundation, TASK 7).

Mirrors `ai.performance.access.is_performance_intelligence_enabled_for()`'s
own shape exactly: Owner-only, gated by a dedicated feature flag.
"""

from ai.access.permissions import AIRole
from goldbot.core_layer.configuration.feature_flags import DEFAULT_FLAGS, FeatureFlags


def is_strategy_intelligence_enabled_for(
    role: AIRole, flags: FeatureFlags = DEFAULT_FLAGS
) -> bool:
    """True only when both `flags.enable_strategy_intelligence` is set and `role` is `AIRole.OWNER`."""
    if not flags.enable_strategy_intelligence:
        return False
    return role == AIRole.OWNER
