"""
Phase 52 — database integration tests: indexes, migration-repeat
safety, and a basic query-execution smoke check.

Schema-shape and duplicate-prevention coverage already exists in
tests/test_database.py (Phase 47) -- this file adds what that one
doesn't: verifying the Phase 50 indexes actually exist, and a basic
performance/execution sanity check (not a benchmark).
"""

import sqlite3
import time

import config


def _indexes(table: str) -> set:
    conn = sqlite3.connect(config.Config.DB_PATH)
    try:
        rows = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='index' AND tbl_name = ?", (table,)
        ).fetchall()
        return {row[0] for row in rows}
    finally:
        conn.close()


def test_users_indexes_exist():
    from database_layer.user_repository.user_repository import UserRepository

    UserRepository()
    indexes = _indexes("users")
    assert "idx_users_status" in indexes
    assert "idx_users_created_at" in indexes


def test_signals_indexes_exist():
    from database_layer.trade_repository.signal_repository import SignalRepository

    SignalRepository()
    indexes = _indexes("signals")
    assert "idx_signals_status" in indexes
    assert "idx_signals_created_at" in indexes


def test_feedback_indexes_exist():
    from database_layer.user_repository.feedback_repository import FeedbackRepository

    FeedbackRepository()
    indexes = _indexes("feedback")
    assert "idx_feedback_status" in indexes
    assert "idx_feedback_created_at" in indexes


def test_no_duplicate_index_on_unique_columns():
    """
    telegram_id columns are already covered by each table's UNIQUE
    constraint -- Phase 50 deliberately did not add a second explicit
    index on top of it. Regression guard against that decision being
    silently reversed.
    """
    from database_layer.user_repository.user_repository import UserRepository
    from database_layer.user_repository.subscription_repository import SubscriptionRepository
    from database_layer.user_repository.admin_repository import AdminRepository

    UserRepository()
    SubscriptionRepository()
    AdminRepository()

    for table in ("users", "subscriptions", "admins"):
        explicit_telegram_id_indexes = {
            name for name in _indexes(table) if "telegram_id" in name and not name.startswith("sqlite_autoindex")
        }
        assert explicit_telegram_id_indexes == set(), (
            f"{table} should rely on its UNIQUE constraint's implicit index, "
            f"not a duplicate explicit one: {explicit_telegram_id_indexes}"
        )


def test_repository_construction_is_idempotent_across_repeated_calls():
    """Constructing every repository twice must never raise (schema/migration/index all idempotent)."""
    from database_layer.user_repository.user_repository import UserRepository
    from database_layer.trade_repository.signal_repository import SignalRepository
    from database_layer.user_repository.feedback_repository import FeedbackRepository
    from database_layer.user_repository.subscription_repository import SubscriptionRepository
    from database_layer.user_repository.admin_repository import AdminRepository

    for _ in range(2):
        UserRepository()
        SignalRepository()
        FeedbackRepository()
        SubscriptionRepository()
        AdminRepository()
    # No exception raised -- idempotency confirmed.


def test_basic_query_execution_is_fast(test_user):
    """
    Not a benchmark -- a sanity floor. An indexed telegram_id lookup
    against a near-empty table must complete in well under a second;
    a regression here (e.g. an accidental full scan or N+1 pattern)
    would blow past this by orders of magnitude.
    """
    from database_layer.user_repository.user_repository import UserRepository

    repo = UserRepository()
    start = time.monotonic()
    for _ in range(50):
        repo.get_user(test_user.telegram_id)
    elapsed = time.monotonic() - start

    assert elapsed < 1.0
