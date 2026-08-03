"""
Phase V1.0.1 (Risk Management Hardening Patch) -- shared fixtures for
tests/risk/. Every RiskManager()/AccountStateTracker()/
DuplicateTradeChecker()/RiskDecisionRepository()/EmergencyManager()
default-constructs against `config.Config.DB_PATH` read fresh at
Database() construction time -- monkeypatching it once before
constructing anything isolates the *entire* dependency graph to one
temp sqlite file, same convention as
tests/monitoring/test_monitoring_repository_phase_b0.py's own
`repository` fixture.
"""

import os

import pytest

from config import Config


@pytest.fixture
def isolated_db(tmp_path, monkeypatch):
    """Points Config.DB_PATH at a fresh temp file for the duration of one test -- returns the path for tests that want to construct their own repository directly."""
    db_path = os.path.join(str(tmp_path), "phase_v1_0_1_risk_test.db")
    monkeypatch.setattr(Config, "DB_PATH", db_path)
    return db_path


@pytest.fixture
def risk_manager(isolated_db):
    """A bare, fully-isolated RiskManager() -- every internal dependency (EmergencyManager, RiskDecisionRepository, AccountStateTracker, DuplicateTradeChecker) points at the same isolated_db."""
    from risk.risk_manager import RiskManager

    return RiskManager()


@pytest.fixture
def emergency_manager(isolated_db):
    from core_layer.emergency.emergency_manager import EmergencyManager

    return EmergencyManager()
