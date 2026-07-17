"""Phase 61.5 TASK 3 — Telegram Owner AI Dashboard Integration. The first live wiring of telegram/owner/ai_commands.py into command_router/handlers."""

import asyncio

from telegram.command_router import route_command, PERMISSION_DENIED_TEXT, UNKNOWN_COMMAND_TEXT

OWNER_ID = "111"  # matches conftest's TELEGRAM_OWNER_ID
USER_ID = "333"


def _run(coro):
    return asyncio.run(coro)


def test_ai_status_is_owner_only_and_returns_real_status():
    owner = _run(route_command("/ai_status", telegram_id=OWNER_ID))
    user = _run(route_command("/ai_status", telegram_id=USER_ID))

    assert "AI CORE STATUS" in owner.text
    assert user.text == PERMISSION_DENIED_TEXT


def test_ai_provider_requires_a_capability_argument():
    missing_arg = _run(route_command("/ai_provider", telegram_id=OWNER_ID))
    assert missing_arg.text == "Usage: /ai_provider CAPABILITY"


def test_ai_provider_rejects_an_unknown_capability():
    result = _run(route_command("/ai_provider not_a_real_capability", telegram_id=OWNER_ID))
    assert "Unknown capability" in result.text


def test_ai_provider_with_a_known_capability_returns_a_real_answer():
    result = _run(route_command("/ai_provider analysis", telegram_id=OWNER_ID))
    assert "Current Provider" in result.text or "No available provider" in result.text


def test_ai_cost_reports_zero_with_no_live_audit_data_yet():
    result = _run(route_command("/ai_cost", telegram_id=OWNER_ID))
    assert "Today AI Cost" in result.text
    assert "$0.00" in result.text


def test_ai_usage_requires_a_telegram_id_argument():
    missing_arg = _run(route_command("/ai_usage", telegram_id=OWNER_ID))
    assert missing_arg.text == "Usage: /ai_usage TELEGRAM_ID"


def test_ai_usage_reports_no_usage_for_an_unknown_id():
    result = _run(route_command("/ai_usage 999999", telegram_id=OWNER_ID))
    assert "No AI usage" in result.text


def test_ai_health_is_owner_only_and_returns_a_ranking():
    owner = _run(route_command("/ai_health", telegram_id=OWNER_ID))
    user = _run(route_command("/ai_health", telegram_id=USER_ID))

    assert "AI Provider Health Ranking" in owner.text
    assert user.text == PERMISSION_DENIED_TEXT


def test_every_new_command_is_a_real_registered_command_not_unknown():
    for command in ("ai_status", "ai_provider analysis", "ai_cost", "ai_usage 1", "ai_health"):
        result = _run(route_command(f"/{command}", telegram_id=OWNER_ID))
        assert result.text != UNKNOWN_COMMAND_TEXT
