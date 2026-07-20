"""
AI Layer — Coaching Access Control (Phase 66.4: AI Coaching
Intelligence Foundation, TASK 6).

Mirrors `ai.learning.access.is_learning_intelligence_enabled_for()`'s
own shape exactly: Owner-only, gated by a dedicated feature flag.
"""

from ai.access.permissions import AIRole
from configuration.feature_flags import DEFAULT_FLAGS, FeatureFlags


def is_coaching_intelligence_enabled_for(
    role: AIRole, flags: FeatureFlags = DEFAULT_FLAGS
) -> bool:
    """True only when both `flags.enable_coaching_intelligence` is set and `role` is `AIRole.OWNER`."""
    if not flags.enable_coaching_intelligence:
        return False
    return role == AIRole.OWNER
