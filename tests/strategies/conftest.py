"""
Shared fixtures for the strategies/ setup-layer tests (TASK-CORE-007).

Builds lightweight ContextSnapshot-shaped fakes (SimpleNamespace) so
each setup strategy can be exercised read-only without constructing a
full context pipeline. Real context enums are used for direction/type
fields so the strategies' identity comparisons behave exactly as in
production.
"""

from types import SimpleNamespace

import pytest

_CONTEXT_DEFAULTS = dict(
    candles=(),
    structure=(),
    bos_events=(),
    choch_events=(),
    liquidity_zones=(),
    liquidity_sweeps=(),
    order_blocks=(),
    fair_value_gaps=(),
    amd_events=(),
    wyckoff_events=(),
    session_events=(),
    market_regime=None,
)


@pytest.fixture
def make_ctx():
    """Return a builder: make_ctx(order_blocks=[...], candles=[...], …)."""
    def _build(**overrides):
        base = dict(_CONTEXT_DEFAULTS)
        base.update(overrides)
        return SimpleNamespace(**base)
    return _build


@pytest.fixture
def candle():
    """A minimal candle carrying just the close (all the setup layer reads)."""
    def _c(close):
        return SimpleNamespace(close=close)
    return _c
