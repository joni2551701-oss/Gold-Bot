"""
AI Layer — AI Chart Intelligence Owner Mode Gate (Phase 66.1: AI Chart
Intelligence Foundation, TASK 7).

Mirrors `ai/trading_analyst/access.py`'s `is_trading_analyst_enabled_for()`
shape exactly (Article 7 Reuse Principle -- reuse the pattern) rather
than routing through `ai/access/access_control.py`'s `AccessControl`
matrix, which grants `AIRole.OWNER` and `AIRole.ADMIN` the same
`frozenset(Capability)` -- TASK 7 requires Owner-only, matching every
other `65.x`/`66.x` Owner-gated feature this codebase has built.
"""

from ai_layer.ai_service.access.permissions import AIRole
from core_layer.configuration.feature_flags import DEFAULT_FLAGS, FeatureFlags


def is_chart_intelligence_enabled_for(role: AIRole, flags: FeatureFlags = DEFAULT_FLAGS) -> bool:
    """
    True only when BOTH the global `enable_chart_intelligence` flag is
    on AND `role` is exactly `AIRole.OWNER`. Never raises: an
    unrecognized role value simply fails the equality check, no
    exception.
    """
    if not flags.enable_chart_intelligence:
        return False
    return role == AIRole.OWNER
