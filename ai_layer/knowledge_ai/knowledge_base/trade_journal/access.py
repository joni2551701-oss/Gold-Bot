"""
AI Layer — AI Trade Journal Owner Mode Gate (Phase 66.2: AI Trade
Journal Intelligence Foundation, TASK 7).

Mirrors `ai/trading_analyst/access.py`'s and `ai/chart_intelligence/access.py`'s
`is_*_enabled_for()` shape exactly (Article 7 Reuse Principle -- reuse
the pattern) rather than routing through `ai/access/access_control.py`'s
`AccessControl` matrix, which grants `AIRole.OWNER` and `AIRole.ADMIN`
the same `frozenset(Capability)` -- TASK 7 requires Owner-only.
"""

from ai_layer.ai_service.access.permissions import AIRole
from core_layer.configuration.feature_flags import DEFAULT_FLAGS, FeatureFlags


def is_trade_journal_enabled_for(role: AIRole, flags: FeatureFlags = DEFAULT_FLAGS) -> bool:
    """
    True only when BOTH the global `enable_trade_journal` flag is on
    AND `role` is exactly `AIRole.OWNER`. Never raises: an
    unrecognized role value simply fails the equality check, no
    exception.
    """
    if not flags.enable_trade_journal:
        return False
    return role == AIRole.OWNER
