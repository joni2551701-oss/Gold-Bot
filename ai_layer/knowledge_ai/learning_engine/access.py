"""
AI Layer — AI Learning Intelligence Owner Mode Gate (Phase 66.3: AI
Learning Intelligence Foundation, TASK 6).

Mirrors `ai/trading_analyst/access.py`'s, `ai/chart_intelligence/access.py`'s,
and `ai/trade_journal/access.py`'s `is_*_enabled_for()` shape exactly
(Article 7 Reuse Principle -- reuse the pattern) rather than routing
through `ai/access/access_control.py`'s `AccessControl` matrix, which
grants `AIRole.OWNER` and `AIRole.ADMIN` the same
`frozenset(Capability)` -- TASK 6 requires Owner-only.
"""

from ai_layer.ai_service.access.permissions import AIRole
from core_layer.configuration.feature_flags import DEFAULT_FLAGS, FeatureFlags


def is_learning_intelligence_enabled_for(role: AIRole, flags: FeatureFlags = DEFAULT_FLAGS) -> bool:
    """
    True only when BOTH the global `enable_learning_intelligence` flag
    is on AND `role` is exactly `AIRole.OWNER`. Never raises: an
    unrecognized role value simply fails the equality check, no
    exception.
    """
    if not flags.enable_learning_intelligence:
        return False
    return role == AIRole.OWNER
