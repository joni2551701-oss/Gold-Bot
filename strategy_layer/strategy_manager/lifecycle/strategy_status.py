"""
Strategy Lifecycle — status enum (Phase A11).

Four states only, per the roadmap's explicit scope -- no other status
is added. See docs/STRATEGY_LIFECYCLE.md for the full contract.
"""

from enum import Enum


class StrategyStatus(Enum):
    """
    TESTING: not yet run in production by StrategyManager.
    ACTIVE: currently run in production by StrategyManager
        (strategy_layer/strategy_manager/strategy_manager.py).
    DISABLED: temporarily excluded -- kept for future re-activation.
    DEPRECATED: permanently retired, kept only for historical/analytics
        reference.

    This enum only classifies metadata in the registry -- it does not
    control whether StrategyManager actually runs a strategy. See
    docs/STRATEGY_LIFECYCLE.md's "What this does NOT do" section.
    """
    TESTING = "TESTING"
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"
    DEPRECATED = "DEPRECATED"
