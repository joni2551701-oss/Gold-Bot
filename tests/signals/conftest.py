"""Shared fixtures for the STEP-08 canonical signal layer tests (TASK-CORE-008)."""

from types import SimpleNamespace

import pytest


@pytest.fixture
def make_strategy_result():
    """
    Build a duck-typed StrategyResult (SimpleNamespace) the SignalManager can
    read, matching strategies.result.StrategyResult's shape without importing
    it. Override any field via keyword.
    """
    def _build(
        strategy_name="BOS_CHOCH_SETUP",
        direction="LONG",
        confidence=0.85,
        entry_zone=(100.0, 101.0),
        invalidation=98.0,
        rr=2.0,
        reasons=None,
        status="SETUP_FOUND",
    ):
        return SimpleNamespace(
            strategy_name=strategy_name,
            direction=SimpleNamespace(name=direction, value=direction.lower()),
            confidence=confidence,
            entry_zone=entry_zone,
            invalidation=invalidation,
            rr=rr,
            reasons=list(reasons) if reasons is not None else ["BOS up", "OB retest"],
            status=SimpleNamespace(name=status, value=status.lower()),
            has_setup=(status == "SETUP_FOUND"),
        )
    return _build
