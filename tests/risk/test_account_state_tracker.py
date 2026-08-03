"""
Phase V1.0.1 (Risk Management Hardening Patch) -- TASK 4 (Drawdown
Protection) and TASK 5 (Daily Loss Protection) tests, exercising
risk_layer/risk_engine/account_state_tracker.py directly against an isolated DB.
"""

from datetime import datetime, timezone, timedelta

from risk_layer.risk_engine.account_state_tracker import AccountStateTracker, NORMAL, TRADING_PAUSED
from database_layer.trade_repository.risk_state_repository import RiskStateRepository


def _tracker(isolated_db):
    return AccountStateTracker(repository=RiskStateRepository())


# ---------------------------------------------------------------------------
# TASK 4: Drawdown Protection
# ---------------------------------------------------------------------------

def test_first_observation_establishes_baseline_with_zero_drawdown(isolated_db):
    tracker = _tracker(isolated_db)
    result = tracker.check_drawdown("XAUUSD", current_equity=10000.0, max_drawdown=0.10)
    assert result.drawdown_percent == 0.0
    assert result.paused is False


def test_drawdown_below_limit_is_not_paused(isolated_db):
    tracker = _tracker(isolated_db)
    tracker.check_drawdown("XAUUSD", current_equity=10000.0, max_drawdown=0.10)
    result = tracker.check_drawdown("XAUUSD", current_equity=9500.0, max_drawdown=0.10)  # 5% down
    assert result.paused is False
    assert round(result.drawdown_percent, 4) == 0.05


def test_drawdown_exactly_at_limit_is_not_paused(isolated_db):
    """paused is strictly-greater-than, so exactly at the limit still passes."""
    tracker = _tracker(isolated_db)
    tracker.check_drawdown("XAUUSD", current_equity=10000.0, max_drawdown=0.10)
    result = tracker.check_drawdown("XAUUSD", current_equity=9000.0, max_drawdown=0.10)  # exactly 10%
    assert result.paused is False


def test_drawdown_exceeding_limit_is_paused(isolated_db):
    tracker = _tracker(isolated_db)
    tracker.check_drawdown("XAUUSD", current_equity=10000.0, max_drawdown=0.10)
    result = tracker.check_drawdown("XAUUSD", current_equity=8900.0, max_drawdown=0.10)  # 11% down
    assert result.paused is True
    assert "exceeds max" in result.reason


def test_drawdown_recovery_after_pause_is_not_paused_again(isolated_db):
    tracker = _tracker(isolated_db)
    tracker.check_drawdown("XAUUSD", current_equity=10000.0, max_drawdown=0.10)
    paused_result = tracker.check_drawdown("XAUUSD", current_equity=8000.0, max_drawdown=0.10)
    assert paused_result.paused is True
    recovered_result = tracker.check_drawdown("XAUUSD", current_equity=9900.0, max_drawdown=0.10)
    assert recovered_result.paused is False


def test_drawdown_persists_status_to_repository(isolated_db):
    tracker = _tracker(isolated_db)
    tracker.check_drawdown("XAUUSD", current_equity=10000.0, max_drawdown=0.10)
    tracker.check_drawdown("XAUUSD", current_equity=8000.0, max_drawdown=0.10)
    state = tracker.repository.get_state("XAUUSD")
    assert state.drawdown_status == TRADING_PAUSED


def test_drawdown_status_normal_when_within_limit(isolated_db):
    tracker = _tracker(isolated_db)
    tracker.check_drawdown("XAUUSD", current_equity=10000.0, max_drawdown=0.10)
    state = tracker.repository.get_state("XAUUSD")
    assert state.drawdown_status == NORMAL


def test_invalid_zero_equity_does_not_pause_or_crash(isolated_db):
    tracker = _tracker(isolated_db)
    result = tracker.check_drawdown("XAUUSD", current_equity=0.0, max_drawdown=0.10)
    assert result.paused is False
    assert result.drawdown_percent == 0.0


def test_invalid_negative_equity_does_not_pause_or_crash(isolated_db):
    tracker = _tracker(isolated_db)
    result = tracker.check_drawdown("XAUUSD", current_equity=-100.0, max_drawdown=0.10)
    assert result.paused is False


def test_drawdown_is_per_symbol_isolated(isolated_db):
    tracker = _tracker(isolated_db)
    tracker.check_drawdown("XAUUSD", current_equity=10000.0, max_drawdown=0.10)
    tracker.check_drawdown("XAUUSD", current_equity=8000.0, max_drawdown=0.10)  # XAUUSD paused

    eurusd_result = tracker.check_drawdown("EURUSD", current_equity=5000.0, max_drawdown=0.10)
    assert eurusd_result.paused is False  # fresh baseline for a different symbol


def test_drawdown_never_negative_when_equity_increases(isolated_db):
    tracker = _tracker(isolated_db)
    tracker.check_drawdown("XAUUSD", current_equity=10000.0, max_drawdown=0.10)
    result = tracker.check_drawdown("XAUUSD", current_equity=11000.0, max_drawdown=0.10)  # equity grew
    assert result.drawdown_percent == 0.0
    assert result.paused is False


# ---------------------------------------------------------------------------
# TASK 5: Daily Loss Protection
# ---------------------------------------------------------------------------

def test_first_observation_establishes_daily_baseline(isolated_db):
    tracker = _tracker(isolated_db)
    result = tracker.check_daily_loss("XAUUSD", current_balance=10000.0, max_daily_loss=0.05)
    assert result.loss_percent == 0.0
    assert result.blocked is False


def test_daily_loss_below_limit_is_not_blocked(isolated_db):
    tracker = _tracker(isolated_db)
    tracker.check_daily_loss("XAUUSD", current_balance=10000.0, max_daily_loss=0.05)
    result = tracker.check_daily_loss("XAUUSD", current_balance=9700.0, max_daily_loss=0.05)  # 3% loss
    assert result.blocked is False


def test_daily_loss_exceeding_limit_is_blocked(isolated_db):
    tracker = _tracker(isolated_db)
    tracker.check_daily_loss("XAUUSD", current_balance=10000.0, max_daily_loss=0.05)
    result = tracker.check_daily_loss("XAUUSD", current_balance=9400.0, max_daily_loss=0.05)  # 6% loss
    assert result.blocked is True
    assert "exceeds max" in result.reason


def test_daily_loss_exactly_at_limit_is_not_blocked(isolated_db):
    tracker = _tracker(isolated_db)
    tracker.check_daily_loss("XAUUSD", current_balance=10000.0, max_daily_loss=0.05)
    result = tracker.check_daily_loss("XAUUSD", current_balance=9500.0, max_daily_loss=0.05)  # exactly 5%
    assert result.blocked is False


def test_daily_loss_resets_on_new_day(isolated_db):
    tracker = _tracker(isolated_db)
    tracker.check_daily_loss("XAUUSD", current_balance=10000.0, max_daily_loss=0.05)
    blocked_result = tracker.check_daily_loss("XAUUSD", current_balance=9000.0, max_daily_loss=0.05)
    assert blocked_result.blocked is True

    # Simulate a new day by directly rewriting the stored daily_date to yesterday.
    yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).date().isoformat()
    state = tracker.repository.get_state("XAUUSD")
    tracker.repository.upsert_state(
        symbol="XAUUSD", starting_equity=state.starting_equity, current_equity=state.current_equity,
        drawdown_status=state.drawdown_status, daily_start_balance=9000.0, daily_date=yesterday,
    )
    fresh_result = tracker.check_daily_loss("XAUUSD", current_balance=9000.0, max_daily_loss=0.05)
    assert fresh_result.loss_percent == 0.0
    assert fresh_result.blocked is False


def test_daily_loss_invalid_zero_balance_does_not_block_or_crash(isolated_db):
    tracker = _tracker(isolated_db)
    result = tracker.check_daily_loss("XAUUSD", current_balance=0.0, max_daily_loss=0.05)
    assert result.blocked is False


def test_daily_loss_invalid_negative_balance_does_not_block_or_crash(isolated_db):
    tracker = _tracker(isolated_db)
    result = tracker.check_daily_loss("XAUUSD", current_balance=-50.0, max_daily_loss=0.05)
    assert result.blocked is False


def test_daily_loss_is_per_symbol_isolated(isolated_db):
    tracker = _tracker(isolated_db)
    tracker.check_daily_loss("XAUUSD", current_balance=10000.0, max_daily_loss=0.05)
    tracker.check_daily_loss("XAUUSD", current_balance=9000.0, max_daily_loss=0.05)  # XAUUSD blocked

    eurusd_result = tracker.check_daily_loss("EURUSD", current_balance=5000.0, max_daily_loss=0.05)
    assert eurusd_result.blocked is False


def test_daily_loss_persists_baseline_to_repository(isolated_db):
    tracker = _tracker(isolated_db)
    tracker.check_daily_loss("XAUUSD", current_balance=10000.0, max_daily_loss=0.05)
    state = tracker.repository.get_state("XAUUSD")
    assert state.daily_start_balance == 10000.0
    assert state.daily_date == datetime.now(timezone.utc).date().isoformat()


def test_drawdown_and_daily_loss_share_state_without_clobbering_each_other(isolated_db):
    """Both trackers write to the same risk_account_state row -- neither should erase the other's fields."""
    tracker = _tracker(isolated_db)
    tracker.check_drawdown("XAUUSD", current_equity=10000.0, max_drawdown=0.10)
    tracker.check_daily_loss("XAUUSD", current_balance=10000.0, max_daily_loss=0.05)

    state = tracker.repository.get_state("XAUUSD")
    assert state.starting_equity == 10000.0
    assert state.daily_start_balance == 10000.0
