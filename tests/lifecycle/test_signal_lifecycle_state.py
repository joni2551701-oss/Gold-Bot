"""
Phase 59 Preparation, TASK 4 -- trade_monitoring_layer/paper_trading/signal_state.py tests.
"""

from datetime import datetime, timezone

from trade_monitoring_layer.paper_trading.paper_trade import create_paper_trade, open_paper_trade, close_paper_trade
from trade_monitoring_layer.paper_trading.signal_state import (
    SignalLifecycleState,
    derive_signal_lifecycle_state,
    transition_signal_state,
)
from signal_layer.signal_builder.schema import SignalSchema


def _signal(**overrides) -> SignalSchema:
    base = dict(
        signal_id="sig-1",
        created_at=datetime.now(timezone.utc),
        symbol="XAUUSD",
        timeframe="M15",
        direction="BUY",
        entry_price=2000.0,
        stop_loss=1990.0,
        take_profit=2020.0,
    )
    base.update(overrides)
    return SignalSchema(**base)


# --- transition_signal_state ---

def test_full_happy_path_is_allowed_step_by_step():
    path = [
        SignalLifecycleState.CREATED,
        SignalLifecycleState.QUALITY_CHECKED,
        SignalLifecycleState.EXPLAINED,
        SignalLifecycleState.APPROVED,
        SignalLifecycleState.PAPER_OPEN,
        SignalLifecycleState.CLOSED,
    ]
    for current, next_state in zip(path, path[1:]):
        result = transition_signal_state(current, next_state)
        assert result.success is True, f"{current} -> {next_state} should be allowed"


def test_explained_can_also_go_to_rejected():
    result = transition_signal_state(SignalLifecycleState.EXPLAINED, SignalLifecycleState.REJECTED)
    assert result.success is True


def test_rejected_is_terminal():
    for next_state in SignalLifecycleState:
        result = transition_signal_state(SignalLifecycleState.REJECTED, next_state)
        assert result.success is False


def test_closed_is_terminal():
    for next_state in SignalLifecycleState:
        result = transition_signal_state(SignalLifecycleState.CLOSED, next_state)
        assert result.success is False


def test_skipping_a_stage_is_rejected():
    result = transition_signal_state(SignalLifecycleState.CREATED, SignalLifecycleState.APPROVED)
    assert result.success is False
    assert "CREATED" in result.reason and "APPROVED" in result.reason


def test_rejected_cannot_go_to_paper_open():
    result = transition_signal_state(SignalLifecycleState.REJECTED, SignalLifecycleState.PAPER_OPEN)
    assert result.success is False


def test_never_raises_on_any_state_pair():
    for current in SignalLifecycleState:
        for next_state in SignalLifecycleState:
            transition_signal_state(current, next_state)  # must not raise


# --- derive_signal_lifecycle_state ---

def test_derive_pending_with_no_quality_grade_is_created():
    signal = _signal(decision="PENDING")
    assert derive_signal_lifecycle_state(signal) == SignalLifecycleState.CREATED


def test_derive_pending_with_quality_grade_is_quality_checked():
    signal = _signal(decision="PENDING", quality_grade="A")
    assert derive_signal_lifecycle_state(signal) == SignalLifecycleState.QUALITY_CHECKED


def test_derive_approved_decision():
    signal = _signal(decision="APPROVED", quality_grade="A+")
    assert derive_signal_lifecycle_state(signal) == SignalLifecycleState.APPROVED


def test_derive_rejected_decision():
    signal = _signal(decision="REJECTED", quality_grade="C")
    assert derive_signal_lifecycle_state(signal) == SignalLifecycleState.REJECTED


def test_derive_with_open_paper_trade_overrides_approved():
    signal = _signal(decision="APPROVED")
    trade = create_paper_trade(signal)
    opened = open_paper_trade(trade).trade

    assert derive_signal_lifecycle_state(signal, paper_trade=opened) == SignalLifecycleState.PAPER_OPEN


def test_derive_with_closed_paper_trade_is_closed():
    signal = _signal(decision="APPROVED")
    trade = create_paper_trade(signal)
    opened = open_paper_trade(trade).trade
    closed = close_paper_trade(opened, "TP").trade

    assert derive_signal_lifecycle_state(signal, paper_trade=closed) == SignalLifecycleState.CLOSED


def test_derive_with_created_paper_trade_does_not_override_approved():
    """A CREATED (not yet OPEN) paper trade doesn't change the derived state -- only OPEN/CLOSED do."""
    signal = _signal(decision="APPROVED")
    trade = create_paper_trade(signal)  # still CREATED

    assert derive_signal_lifecycle_state(signal, paper_trade=trade) == SignalLifecycleState.APPROVED


def test_derive_never_raises_on_minimal_signal():
    signal = _signal(direction="NONE", entry_price=None, stop_loss=None, take_profit=None, decision="PENDING")
    derive_signal_lifecycle_state(signal)  # must not raise
