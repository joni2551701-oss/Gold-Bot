"""
AI Layer — AI Research Intelligence Owner Mode Gate (Phase 66.8: AI
Research Intelligence Foundation, TASK 8).

Mirrors `ai.portfolio.access.is_portfolio_intelligence_enabled_for()`'s
own shape exactly: Owner-only, gated by a dedicated feature flag.
"""

from ai.access.permissions import AIRole
from core_layer.configuration.feature_flags import DEFAULT_FLAGS, FeatureFlags


def is_research_intelligence_enabled_for(
    role: AIRole, flags: FeatureFlags = DEFAULT_FLAGS
) -> bool:
    """True only when both `flags.enable_research_intelligence` is set and `role` is `AIRole.OWNER`."""
    if not flags.enable_research_intelligence:
        return False
    return role == AIRole.OWNER
