"""Phase V1.0.1 -- database/risk_state_repository.py tests."""

from database.risk_state_repository import RiskStateRepository


def test_get_state_returns_none_when_absent(isolated_db):
    repo = RiskStateRepository()
    assert repo.get_state("XAUUSD") is None


def test_upsert_state_creates_new_row(isolated_db):
    repo = RiskStateRepository()
    entry = repo.upsert_state("XAUUSD", starting_equity=10000.0, current_equity=10000.0)
    assert entry.symbol == "XAUUSD"
    assert entry.starting_equity == 10000.0


def test_upsert_state_updates_existing_row(isolated_db):
    repo = RiskStateRepository()
    repo.upsert_state("XAUUSD", starting_equity=10000.0, current_equity=10000.0)
    updated = repo.upsert_state("XAUUSD", starting_equity=10000.0, current_equity=9500.0)
    assert updated.current_equity == 9500.0


def test_upsert_state_preserves_created_at_across_updates(isolated_db):
    repo = RiskStateRepository()
    first = repo.upsert_state("XAUUSD", starting_equity=10000.0, current_equity=10000.0)
    second = repo.upsert_state("XAUUSD", starting_equity=10000.0, current_equity=9500.0)
    assert first.created_at == second.created_at


def test_upsert_state_updates_updated_at(isolated_db):
    repo = RiskStateRepository()
    first = repo.upsert_state("XAUUSD", starting_equity=10000.0, current_equity=10000.0)
    second = repo.upsert_state("XAUUSD", starting_equity=10000.0, current_equity=9500.0)
    assert second.updated_at >= first.updated_at


def test_state_is_isolated_per_symbol(isolated_db):
    repo = RiskStateRepository()
    repo.upsert_state("XAUUSD", starting_equity=10000.0)
    repo.upsert_state("EURUSD", starting_equity=5000.0)
    assert repo.get_state("XAUUSD").starting_equity == 10000.0
    assert repo.get_state("EURUSD").starting_equity == 5000.0


def test_drawdown_status_defaults_to_normal(isolated_db):
    repo = RiskStateRepository()
    entry = repo.upsert_state("XAUUSD", starting_equity=10000.0)
    assert entry.drawdown_status == "NORMAL"


def test_daily_fields_round_trip(isolated_db):
    repo = RiskStateRepository()
    entry = repo.upsert_state("XAUUSD", daily_start_balance=10000.0, daily_date="2026-01-01")
    assert entry.daily_start_balance == 10000.0
    assert entry.daily_date == "2026-01-01"
