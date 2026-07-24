"""
AI Layer — AI Trading Analyst Owner Mode Gate (Phase 66.0: AI Trading
Analyst Foundation, TASK 9).

Mirrors `assistant/access.py`'s `is_personal_ai_enabled_for()` shape
exactly (Article 7 Reuse Principle — reuse the pattern) rather than
routing through `ai/access/access_control.py`'s `AccessControl`
matrix, which grants `AIRole.OWNER` and `AIRole.ADMIN` the same
`frozenset(Capability)` — TASK 9 requires Owner-only, matching every
other `65.x`/`66.x` Owner-gated feature this codebase has built.
"""

from ai.access.permissions import AIRole
from configuration.feature_flags import DEFAULT_FLAGS, FeatureFlags


def is_trading_analyst_enabled_for(role: AIRole, flags: FeatureFlags = DEFAULT_FLAGS) -> bool:
    """
    True only when BOTH the global `enable_trading_analyst` flag is on
    AND `role` is exactly `AIRole.OWNER`. Never raises: an unrecognized
    role value simply fails the equality check, no exception.
    """
    if not flags.enable_trading_analyst:
        return False
    return role == AIRole.OWNER
