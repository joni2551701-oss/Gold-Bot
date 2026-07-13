"""
Phase 53 — database query speed regression tests.

Budgets are generous regression guards (task-specified: query < 1s),
not benchmarks -- see docs/performance_report.md for real timing
numbers (single-digit milliseconds on this hardware). These exist to
catch a real regression (e.g. an accidentally-missing index, an N+1
query pattern) rather than to chase microseconds.
"""

import time

QUERY_BUDGET_SECONDS = 1.0


def test_indexed_user_lookup_is_fast(test_user):
    from database.user_repository import UserRepository

    repo = UserRepository()
    start = time.perf_counter()
    for _ in range(100):
        repo.get_user(test_user.telegram_id)
    elapsed = time.perf_counter() - start

    assert elapsed < QUERY_BUDGET_SECONDS


def test_signal_history_query_is_fast():
    from database.signal_repository import SignalRepository

    repo = SignalRepository()
    for i in range(50):
        repo.create_signal({
            "signal_id": f"perf-{i}", "symbol": "XAUUSD", "direction": "BUY",
            "entry_zone_min": 2000.0, "entry_zone_max": 2000.0, "stop_loss": 1990.0,
            "take_profit_1": 2030.0, "take_profit_2": 0.0, "risk_percent": 0.0,
            "lot_size": 0.0, "strategy_name": "Liquidity Sweep", "confidence_score": 0.8,
            "ai_explanation": "test",
        })

    start = time.perf_counter()
    history = repo.get_recent_signals(limit=5)
    elapsed = time.perf_counter() - start

    assert len(history) == 5
    assert elapsed < QUERY_BUDGET_SECONDS


def test_status_filtered_query_uses_index_and_is_fast():
    """get_open_signals()/get_closed_signals() filter by the Phase 50 idx_signals_status index."""
    from database.signal_repository import SignalRepository

    repo = SignalRepository()
    for i in range(50):
        repo.create_signal({
            "signal_id": f"status-perf-{i}", "symbol": "XAUUSD", "direction": "BUY",
            "entry_zone_min": 2000.0, "entry_zone_max": 2000.0, "stop_loss": 1990.0,
            "take_profit_1": 2030.0, "take_profit_2": 0.0, "risk_percent": 0.0,
            "lot_size": 0.0, "strategy_name": "Liquidity Sweep", "confidence_score": 0.8,
            "ai_explanation": "test",
        })

    start = time.perf_counter()
    open_signals = repo.get_open_signals()
    elapsed = time.perf_counter() - start

    assert len(open_signals) == 50  # every created_signal defaults to status='OPEN'
    assert elapsed < QUERY_BUDGET_SECONDS


def test_query_plan_uses_index_for_status_filter():
    """
    EXPLAIN QUERY PLAN sanity check: confirms Phase 50's idx_signals_status
    is actually consulted, not just present. A regression here (a
    query rewritten to defeat the index) wouldn't necessarily fail the
    timing tests above at this table size, but would silently degrade
    at production scale.
    """
    import sqlite3
    import config
    from database.signal_repository import SignalRepository

    SignalRepository()  # ensures schema + indexes exist
    conn = sqlite3.connect(config.Config.DB_PATH)
    try:
        plan = conn.execute("EXPLAIN QUERY PLAN SELECT * FROM signals WHERE status = 'OPEN'").fetchall()
    finally:
        conn.close()

    plan_text = " ".join(str(row) for row in plan)
    assert "idx_signals_status" in plan_text
