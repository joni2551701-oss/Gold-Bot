"""
Phase 54 — database / SQL injection security tests.

Every query in database/*.py already uses parameterized ('?')
placeholders (confirmed by static audit in the Phase 48 full-system
audit and re-confirmed this phase -- see docs/SECURITY.md).
These tests prove it dynamically: classic SQL-injection payloads are
fed through as telegram_id/message/username values and must be stored
and read back literally, never alter query structure, corrupt data,
or raise a database error.
"""

import sqlite3

import config

SQLI_PAYLOADS = [
    "1' OR '1'='1",
    "'; DROP TABLE users; --",
    "1; DELETE FROM users WHERE 1=1; --",
    "' UNION SELECT * FROM admins --",
    "\" OR \"\"=\"",
    "Robert'); DROP TABLE students;--",
]


def _table_exists(table: str) -> bool:
    conn = sqlite3.connect(config.Config.DB_PATH)
    try:
        row = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name = ?", (table,)
        ).fetchone()
        return row is not None
    finally:
        conn.close()


def test_sql_injection_payload_as_telegram_id_is_stored_literally():
    from database_layer.user_repository.user_repository import UserRepository

    repo = UserRepository()
    for payload in SQLI_PAYLOADS:
        created = repo.create_user(telegram_id=payload, username="attacker")
        assert created is not None, f"payload should insert as a normal row: {payload}"
        assert created.telegram_id == payload

        fetched = repo.get_user(payload)
        assert fetched is not None
        assert fetched.telegram_id == payload

    # Every table this suite depends on must still exist -- a real
    # injection would have dropped or corrupted one.
    assert _table_exists("users")


def test_sql_injection_payload_as_username_does_not_corrupt_query():
    from database_layer.user_repository.user_repository import UserRepository

    repo = UserRepository()
    for i, payload in enumerate(SQLI_PAYLOADS):
        created = repo.create_user(telegram_id=f"sqli-user-{i}", username=payload)
        assert created is not None
        assert created.username == payload

    assert repo.count_users() == len(SQLI_PAYLOADS)


def test_sql_injection_payload_as_feedback_message_is_stored_literally():
    from platform_layer.telegram.feedback_service import FeedbackService

    service = FeedbackService()
    for i, payload in enumerate(SQLI_PAYLOADS):
        result = service.send_feedback(f"sqli-feedback-{i}", payload)
        assert result.success is True
        assert result.feedback.message == payload

    assert _table_exists("feedback")


def test_sql_injection_payload_via_command_router_does_not_crash():
    """End-to-end: a malicious /feedback body through the real command chain."""
    import asyncio
    from platform_layer.telegram.command_router import route_command

    async def scenario():
        return await route_command(
            "/feedback '; DROP TABLE signals; --", telegram_id="sqli-router-1"
        )

    result = asyncio.run(scenario())
    assert result.text.startswith("✅ Fikr-mulohaza qabul qilindi.")
    assert _table_exists("feedback")


def test_dynamic_update_column_allowlist_rejects_unknown_fields():
    """
    UserRepository.update_user()/SubscriptionRepository._update() build
    their SET clause from an f-string, but only for column names
    filtered against a fixed allowlist first -- an unrecognized/attacker
    -supplied field name must be silently dropped, never reach SQL.
    """
    from database_layer.user_repository.user_repository import UserRepository

    repo = UserRepository()
    repo.create_user(telegram_id="allowlist-1", username="victim")

    updated = repo.update_user(
        "allowlist-1",
        risk_percent=3.0,
        **{"telegram_id = '1'; DROP TABLE users; --": "malicious"},
    )
    assert updated is True  # risk_percent alone is a valid update
    assert repo.get_user("allowlist-1").risk_percent == 3.0
    assert _table_exists("users")


def test_admins_table_survives_injection_attempt_via_admin_id():
    from database_layer.user_repository.admin_repository import AdminRepository
    from database_layer.user_repository.user_repository import UserRepository

    UserRepository()  # a sibling table -- must be unaffected by admins-table injection attempts
    repo = AdminRepository()
    for payload in SQLI_PAYLOADS:
        added = repo.add_admin(payload)
        assert added is not None
    assert _table_exists("admins")
    assert _table_exists("users")
