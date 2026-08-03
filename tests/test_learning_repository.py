"""
Phase 60.6, TASK 5 -- database_layer/journal_repository/learning_repository.py and
learning_models.py tests. Real SQLite (tests/conftest.py's autouse
fresh_database fixture), no mocks.
"""

from datetime import datetime

from database_layer.journal_repository.learning_models import create_learning_record_row
from database_layer.journal_repository.learning_repository import LearningRepository


def test_record_persists_and_returns_the_row():
    repo = LearningRepository()

    row = repo.record(
        "rec-1", "trade-1", "signal-1", strategy_name="Liquidity Sweep",
        market_phase="DISTRIBUTION", session="London", result="SL", r_multiple=-1.0,
        failure_type="No HTF confirmation",
    )

    assert row.record_id == "rec-1"
    assert row.trade_id == "trade-1"
    assert row.strategy_name == "Liquidity Sweep"
    assert row.failure_type == "No HTF confirmation"


def test_get_recent_returns_newest_first():
    repo = LearningRepository()
    repo.record("rec-1", "t1", "s1")
    repo.record("rec-2", "t2", "s2")
    repo.record("rec-3", "t3", "s3")

    recent = repo.get_recent()

    assert [r.record_id for r in recent] == ["rec-3", "rec-2", "rec-1"]


def test_get_recent_respects_limit():
    repo = LearningRepository()
    for i in range(5):
        repo.record(f"rec-{i}", f"t{i}", f"s{i}")

    recent = repo.get_recent(limit=2)

    assert len(recent) == 2


def test_get_recent_rows_carry_a_real_database_id():
    repo = LearningRepository()
    repo.record("rec-1", "t1", "s1")

    recent = repo.get_recent()

    assert recent[0].id is not None


def test_get_by_strategy_filters_correctly():
    repo = LearningRepository()
    repo.record("rec-1", "t1", "s1", strategy_name="Liquidity Sweep")
    repo.record("rec-2", "t2", "s2", strategy_name="FVG Strategy")

    sweep_records = repo.get_by_strategy("Liquidity Sweep")

    assert len(sweep_records) == 1
    assert sweep_records[0].record_id == "rec-1"


def test_count_reflects_total_records():
    repo = LearningRepository()
    assert repo.count() == 0
    repo.record("rec-1", "t1", "s1")
    repo.record("rec-2", "t2", "s2")
    assert repo.count() == 2


def test_no_records_returns_empty_list_not_none():
    repo = LearningRepository()
    assert repo.get_recent() == []
    assert repo.get_by_strategy("nobody") == []


def test_repository_has_no_update_or_delete_method():
    """Append-only by design, per the Director's own brief -- structural guard."""
    assert not hasattr(LearningRepository, "update")
    assert not hasattr(LearningRepository, "delete")


def test_create_learning_record_row_stamps_created_at():
    row = create_learning_record_row("rec-1", "t1", "s1")
    assert isinstance(row.created_at, datetime)
    assert row.created_at.tzinfo is not None


def test_learning_record_row_is_frozen():
    row = create_learning_record_row("rec-1", "t1", "s1")
    try:
        row.result = "TP"
        assert False, "LearningRecordRow must be immutable"
    except AttributeError:
        pass


def test_learning_record_row_to_dict_is_json_safe():
    import json

    row = create_learning_record_row("rec-1", "t1", "s1", r_multiple=1.5)
    data = row.to_dict()

    json.dumps(data)  # must not raise
    assert data["r_multiple"] == 1.5


# --- Phase 60.7 TASK 3: Enhanced Learning Schema (additive) ---

def test_record_persists_and_returns_the_new_phase_607_fields():
    repo = LearningRepository()

    row = repo.record(
        "rec-1", "trade-1", "signal-1", htf_bias="BULLISH", volatility_state="LOW_VOLATILITY",
        fundamental_bias="BULLISH GOLD", confidence_score=0.78, engine_version="60.7", sample_size=42,
    )

    assert row.htf_bias == "BULLISH"
    assert row.volatility_state == "LOW_VOLATILITY"
    assert row.fundamental_bias == "BULLISH GOLD"
    assert row.confidence_score == 0.78
    assert row.engine_version == "60.7"
    assert row.sample_size == 42


def test_new_phase_607_fields_default_to_none():
    repo = LearningRepository()

    row = repo.record("rec-1", "t1", "s1")

    assert row.htf_bias is None
    assert row.volatility_state is None
    assert row.fundamental_bias is None
    assert row.confidence_score is None
    assert row.engine_version is None
    assert row.sample_size is None


def test_get_recent_round_trips_the_new_phase_607_fields():
    repo = LearningRepository()
    repo.record("rec-1", "t1", "s1", htf_bias="BEARISH", confidence_score=0.5, sample_size=10)

    recent = repo.get_recent()

    assert recent[0].htf_bias == "BEARISH"
    assert recent[0].confidence_score == 0.5
    assert recent[0].sample_size == 10


def test_phase_606_calls_are_unaffected_by_the_extension():
    """A Phase 60.6-shaped call (no new kwargs) must still work identically."""
    repo = LearningRepository()

    row = repo.record(
        "rec-1", "trade-1", "signal-1", strategy_name="Liquidity Sweep",
        market_phase="DISTRIBUTION", session="London", result="SL", r_multiple=-1.0,
        failure_type="No HTF confirmation",
    )

    assert row.record_id == "rec-1"
    assert row.failure_type == "No HTF confirmation"
    assert repo.count() == 1
