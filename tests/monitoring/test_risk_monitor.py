"""
Phase V1.0.1 (Risk Management Hardening Patch) -- TASK 9 (Monitoring
Integration) tests: monitoring/risk_monitor.py is a read-only
aggregator over database.risk_decision_repository.RiskDecisionRepository
-- it never writes to risk_decisions itself.
"""

import os

import pytest

from config import Config
from database.risk_decision_repository import RiskDecisionRepository
from monitoring.risk_monitor import RiskMonitor


@pytest.fixture
def isolated_db(tmp_path, monkeypatch):
    db_path = os.path.join(str(tmp_path), "phase_v1_0_1_risk_monitor_test.db")
    monkeypatch.setattr(Config, "DB_PATH", db_path)
    return db_path


def test_zero_checks_when_nothing_recorded(isolated_db):
    monitor = RiskMonitor(repository=RiskDecisionRepository())
    counts = monitor.get_counts()
    assert counts.total_checks == 0
    assert counts.approve_count == 0
    assert counts.reject_count == 0


def test_total_checks_counts_all_decisions(isolated_db):
    repo = RiskDecisionRepository()
    repo.record(symbol="XAUUSD", decision="APPROVE", reason="ok")
    repo.record(symbol="XAUUSD", decision="REJECT", reason="no")
    monitor = RiskMonitor(repository=repo)
    assert monitor.get_counts().total_checks == 2


def test_approve_and_reject_counts_split_correctly(isolated_db):
    repo = RiskDecisionRepository()
    repo.record(symbol="XAUUSD", decision="APPROVE", reason="ok")
    repo.record(symbol="XAUUSD", decision="APPROVE", reason="ok")
    repo.record(symbol="XAUUSD", decision="REJECT", reason="no")
    monitor = RiskMonitor(repository=repo)
    counts = monitor.get_counts()
    assert counts.approve_count == 2
    assert counts.reject_count == 1


def test_risk_limit_events_counted(isolated_db):
    repo = RiskDecisionRepository()
    repo.record(symbol="XAUUSD", decision="REJECT", reason="limit", reject_category="RISK_LIMIT")
    monitor = RiskMonitor(repository=repo)
    assert monitor.get_counts().risk_limit_events == 1


def test_rr_reject_events_counted(isolated_db):
    repo = RiskDecisionRepository()
    repo.record(symbol="XAUUSD", decision="REJECT", reason="rr", reject_category="RR_BELOW_MIN")
    monitor = RiskMonitor(repository=repo)
    assert monitor.get_counts().rr_reject_events == 1


def test_drawdown_events_counted(isolated_db):
    repo = RiskDecisionRepository()
    repo.record(symbol="XAUUSD", decision="REJECT", reason="dd", reject_category="DRAWDOWN")
    monitor = RiskMonitor(repository=repo)
    assert monitor.get_counts().drawdown_events == 1


def test_daily_loss_events_counted(isolated_db):
    repo = RiskDecisionRepository()
    repo.record(symbol="XAUUSD", decision="REJECT", reason="loss", reject_category="DAILY_LOSS")
    monitor = RiskMonitor(repository=repo)
    assert monitor.get_counts().daily_loss_events == 1


def test_duplicate_events_counted(isolated_db):
    repo = RiskDecisionRepository()
    repo.record(symbol="XAUUSD", decision="REJECT", reason="dup", reject_category="DUPLICATE")
    monitor = RiskMonitor(repository=repo)
    assert monitor.get_counts().duplicate_events == 1


def test_emergency_pause_events_counted(isolated_db):
    repo = RiskDecisionRepository()
    repo.record(symbol="XAUUSD", decision="REJECT", reason="paused", reject_category="EMERGENCY_PAUSED")
    monitor = RiskMonitor(repository=repo)
    assert monitor.get_counts().emergency_pause_events == 1


def test_pause_events_combines_emergency_and_drawdown(isolated_db):
    repo = RiskDecisionRepository()
    repo.record(symbol="XAUUSD", decision="REJECT", reason="paused", reject_category="EMERGENCY_PAUSED")
    repo.record(symbol="XAUUSD", decision="REJECT", reason="dd", reject_category="DRAWDOWN")
    monitor = RiskMonitor(repository=repo)
    assert monitor.get_counts().pause_events == 2


def test_risk_monitor_never_writes(isolated_db):
    """Read-only contract: RiskMonitor has no record()/write-shaped method of its own."""
    monitor = RiskMonitor(repository=RiskDecisionRepository())
    assert not hasattr(monitor, "record")
    assert not hasattr(monitor, "write")


def test_default_risk_monitor_module_function_works(isolated_db):
    from monitoring.risk_monitor import get_risk_counts, DEFAULT_RISK_MONITOR

    DEFAULT_RISK_MONITOR.repository = RiskDecisionRepository()
    counts = get_risk_counts()
    assert counts.total_checks >= 0
