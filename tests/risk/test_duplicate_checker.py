"""
Phase V1.0.1 (Risk Management Hardening Patch) -- TASK 6 (Duplicate
Trade Protection) tests, exercising risk/duplicate_checker.py against
an isolated DB.
"""

from risk.duplicate_checker import DuplicateTradeChecker
from database.risk_decision_repository import RiskDecisionRepository


def _checker(isolated_db):
    return DuplicateTradeChecker(repository=RiskDecisionRepository())


def test_no_prior_decisions_is_not_a_duplicate(isolated_db):
    checker = _checker(isolated_db)
    result = checker.check("XAUUSD", "BUY", "FIXTURE_STRATEGY")
    assert result.duplicate is False


def test_prior_approve_within_window_is_a_duplicate(isolated_db):
    repository = RiskDecisionRepository()
    repository.record(
        symbol="XAUUSD", decision="APPROVE", reason="ok",
        strategy_name="FIXTURE_STRATEGY", direction="BUY",
    )
    checker = DuplicateTradeChecker(repository=repository)
    result = checker.check("XAUUSD", "BUY", "FIXTURE_STRATEGY", within_seconds=300)
    assert result.duplicate is True
    assert "Duplicate trade" in result.reason


def test_prior_reject_is_not_a_duplicate(isolated_db):
    repository = RiskDecisionRepository()
    repository.record(
        symbol="XAUUSD", decision="REJECT", reason="RR below minimum",
        strategy_name="FIXTURE_STRATEGY", direction="BUY",
    )
    checker = DuplicateTradeChecker(repository=repository)
    result = checker.check("XAUUSD", "BUY", "FIXTURE_STRATEGY")
    assert result.duplicate is False


def test_different_symbol_is_not_a_duplicate(isolated_db):
    repository = RiskDecisionRepository()
    repository.record(symbol="EURUSD", decision="APPROVE", reason="ok", direction="BUY")
    checker = DuplicateTradeChecker(repository=repository)
    result = checker.check("XAUUSD", "BUY", None)
    assert result.duplicate is False


def test_different_direction_is_not_a_duplicate(isolated_db):
    repository = RiskDecisionRepository()
    repository.record(symbol="XAUUSD", decision="APPROVE", reason="ok", direction="BUY")
    checker = DuplicateTradeChecker(repository=repository)
    result = checker.check("XAUUSD", "SELL", None)
    assert result.duplicate is False


def test_different_strategy_is_not_a_duplicate_when_strategy_specified(isolated_db):
    repository = RiskDecisionRepository()
    repository.record(
        symbol="XAUUSD", decision="APPROVE", reason="ok",
        strategy_name="STRATEGY_A", direction="BUY",
    )
    checker = DuplicateTradeChecker(repository=repository)
    result = checker.check("XAUUSD", "BUY", "STRATEGY_B")
    assert result.duplicate is False


def test_any_strategy_matches_when_strategy_name_is_none(isolated_db):
    repository = RiskDecisionRepository()
    repository.record(
        symbol="XAUUSD", decision="APPROVE", reason="ok",
        strategy_name="STRATEGY_A", direction="BUY",
    )
    checker = DuplicateTradeChecker(repository=repository)
    result = checker.check("XAUUSD", "BUY", None)
    assert result.duplicate is True


def test_zero_second_window_never_finds_a_duplicate(isolated_db):
    repository = RiskDecisionRepository()
    repository.record(symbol="XAUUSD", decision="APPROVE", reason="ok", direction="BUY")
    checker = DuplicateTradeChecker(repository=repository)
    result = checker.check("XAUUSD", "BUY", None, within_seconds=0)
    assert result.duplicate is False


def test_default_duplicate_window_is_five_minutes():
    from risk.duplicate_checker import DEFAULT_DUPLICATE_WINDOW_SECONDS

    assert DEFAULT_DUPLICATE_WINDOW_SECONDS == 300.0


def test_multiple_approvals_all_counted_in_reason(isolated_db):
    repository = RiskDecisionRepository()
    repository.record(symbol="XAUUSD", decision="APPROVE", reason="ok", direction="BUY")
    repository.record(symbol="XAUUSD", decision="APPROVE", reason="ok", direction="BUY")
    checker = DuplicateTradeChecker(repository=repository)
    result = checker.check("XAUUSD", "BUY", None)
    assert result.duplicate is True
    assert "2 time(s)" in result.reason
