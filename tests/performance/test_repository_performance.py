"""
Phase 53 — repository construction/CRUD performance regression tests.

Real numbers (docs/PERFORMANCE.md): SignalRepository()
construction (schema + Phase 50 index creation) ~15ms one-time per
pipeline run; a single insert ~3ms. Budgets here are generous
regression guards, not tight benchmarks.
"""

import time

REPO_CONSTRUCTION_BUDGET_SECONDS = 1.0
BATCH_INSERT_BUDGET_SECONDS = 2.0


def test_repository_construction_is_fast():
    """Schema init + migration checks + Phase 50 index creation, combined, for every repository."""
    from database.user_repository import UserRepository
    from database.signal_repository import SignalRepository
    from database.feedback_repository import FeedbackRepository
    from database.subscription_repository import SubscriptionRepository
    from database.admin_repository import AdminRepository

    start = time.perf_counter()
    UserRepository()
    SignalRepository()
    FeedbackRepository()
    SubscriptionRepository()
    AdminRepository()
    elapsed = time.perf_counter() - start

    assert elapsed < REPO_CONSTRUCTION_BUDGET_SECONDS


def test_repeated_repository_construction_does_not_degrade():
    """
    Idempotent CREATE TABLE/INDEX IF NOT EXISTS checks must stay cheap
    on repeat construction (as happens every pipeline run/every
    Telegram command handler call) -- not re-run expensive migration
    work once already applied.
    """
    from database.user_repository import UserRepository

    UserRepository()  # first construction: full schema + migration + index path
    start = time.perf_counter()
    for _ in range(20):
        UserRepository()
    elapsed = time.perf_counter() - start

    assert elapsed < REPO_CONSTRUCTION_BUDGET_SECONDS


def test_batch_signal_insert_performance():
    from database.signal_repository import SignalRepository

    repo = SignalRepository()
    start = time.perf_counter()
    for i in range(100):
        repo.create_signal({
            "signal_id": f"batch-{i}", "symbol": "XAUUSD", "direction": "BUY",
            "entry_zone_min": 2000.0, "entry_zone_max": 2000.0, "stop_loss": 1990.0,
            "take_profit_1": 2030.0, "take_profit_2": 0.0, "risk_percent": 0.0,
            "lot_size": 0.0, "strategy_name": "Liquidity Sweep", "confidence_score": 0.8,
            "ai_explanation": "test",
        })
    elapsed = time.perf_counter() - start

    assert elapsed < BATCH_INSERT_BUDGET_SECONDS


def test_user_settings_update_performance(test_user):
    from database.user_repository import UserRepository

    repo = UserRepository()
    start = time.perf_counter()
    for i in range(50):
        repo.update_user(test_user.telegram_id, risk_percent=float(i % 5 + 1))
    elapsed = time.perf_counter() - start

    assert elapsed < REPO_CONSTRUCTION_BUDGET_SECONDS
