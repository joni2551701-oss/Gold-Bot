"""Phase V1.0.1 -- database_layer/trade_repository/risk_decision_repository.py tests."""

from database_layer.trade_repository.risk_decision_repository import RiskDecisionRepository


def test_record_returns_entry(isolated_db):
    repo = RiskDecisionRepository()
    entry = repo.record(symbol="XAUUSD", decision="APPROVE", reason="ok")
    assert entry.symbol == "XAUUSD"
    assert entry.decision == "APPROVE"


def test_get_recent_returns_newest_first(isolated_db):
    repo = RiskDecisionRepository()
    repo.record(symbol="XAUUSD", decision="APPROVE", reason="first")
    repo.record(symbol="XAUUSD", decision="REJECT", reason="second")
    entries = repo.get_recent(limit=2)
    assert entries[0].reason == "second"
    assert entries[1].reason == "first"


def test_get_recent_respects_limit(isolated_db):
    repo = RiskDecisionRepository()
    for i in range(5):
        repo.record(symbol="XAUUSD", decision="APPROVE", reason=f"entry {i}")
    entries = repo.get_recent(limit=2)
    assert len(entries) == 2


def test_count_all(isolated_db):
    repo = RiskDecisionRepository()
    assert repo.count_all() == 0
    repo.record(symbol="XAUUSD", decision="APPROVE", reason="ok")
    assert repo.count_all() == 1


def test_count_by_decision(isolated_db):
    repo = RiskDecisionRepository()
    repo.record(symbol="XAUUSD", decision="APPROVE", reason="ok")
    repo.record(symbol="XAUUSD", decision="REJECT", reason="no")
    repo.record(symbol="XAUUSD", decision="REJECT", reason="no")
    assert repo.count_by_decision("APPROVE") == 1
    assert repo.count_by_decision("REJECT") == 2


def test_count_by_reject_category(isolated_db):
    repo = RiskDecisionRepository()
    repo.record(symbol="XAUUSD", decision="REJECT", reason="rr", reject_category="RR_BELOW_MIN")
    repo.record(symbol="XAUUSD", decision="REJECT", reason="dd", reject_category="DRAWDOWN")
    assert repo.count_by_reject_category("RR_BELOW_MIN") == 1
    assert repo.count_by_reject_category("DRAWDOWN") == 1
    assert repo.count_by_reject_category("DUPLICATE") == 0


def test_get_recent_approved_matches_symbol_direction_strategy(isolated_db):
    repo = RiskDecisionRepository()
    repo.record(symbol="XAUUSD", decision="APPROVE", reason="ok", direction="BUY", strategy_name="S1")
    matches = repo.get_recent_approved("XAUUSD", "BUY", "S1", within_seconds=300)
    assert len(matches) == 1


def test_get_recent_approved_excludes_rejects(isolated_db):
    repo = RiskDecisionRepository()
    repo.record(symbol="XAUUSD", decision="REJECT", reason="no", direction="BUY", strategy_name="S1")
    matches = repo.get_recent_approved("XAUUSD", "BUY", "S1", within_seconds=300)
    assert matches == []


def test_get_recent_approved_none_strategy_matches_any(isolated_db):
    repo = RiskDecisionRepository()
    repo.record(symbol="XAUUSD", decision="APPROVE", reason="ok", direction="BUY", strategy_name="S1")
    repo.record(symbol="XAUUSD", decision="APPROVE", reason="ok", direction="BUY", strategy_name="S2")
    matches = repo.get_recent_approved("XAUUSD", "BUY", None, within_seconds=300)
    assert len(matches) == 2


def test_repository_is_append_only_no_update_method(isolated_db):
    repo = RiskDecisionRepository()
    assert not hasattr(repo, "update")
    assert not hasattr(repo, "delete")
