"""
Phase 62.2 TASK 7 — real command_router/handlers dispatch for
/runtime_restart and /runtime_provider. This is exactly the layer a
misnamed handler (e.g. Phase 61.7's own caught mistake --
`runtime_status_handler` briefly named `runtime_status_full_handler`)
would silently fail at: `telegram.command_router.route_command()`
resolves `getattr(handlers, f"{command}_handler")` by name alone, so a
name mismatch is invisible to a unit test of the handler function in
isolation. Driving both commands through the real router is the only
way this class of bug gets caught before it reaches Telegram.
"""

import asyncio

from telegram.command_router import route_command, PERMISSION_DENIED_TEXT

OWNER_ID = "111"  # matches conftest's TELEGRAM_OWNER_ID
USER_ID = "333"


def _run(coro):
    return asyncio.run(coro)


def test_runtime_restart_dispatches_and_is_owner_only():
    owner = _run(route_command("/runtime_restart", telegram_id=OWNER_ID))
    user = _run(route_command("/runtime_restart", telegram_id=USER_ID))

    # A fresh RuntimeManager() defaults to READY (documented default,
    # same posture every other runtime_commands.py function uses) --
    # so the real dispatch path hits the "already READY" branch.
    assert "READY" in owner.text
    assert user.text == PERMISSION_DENIED_TEXT


def test_runtime_provider_dispatches_and_requires_an_argument():
    missing_arg = _run(route_command("/runtime_provider", telegram_id=OWNER_ID))
    assert missing_arg.text == "Usage: /runtime_provider PROVIDER"

    user = _run(route_command("/runtime_provider gemini", telegram_id=USER_ID))
    assert user.text == PERMISSION_DENIED_TEXT


def test_runtime_provider_with_a_known_provider_returns_a_real_panel():
    result = _run(route_command("/runtime_provider gemini", telegram_id=OWNER_ID))
    assert "AI PROVIDER STATUS" in result.text


def test_runtime_provider_rejects_an_unknown_provider():
    result = _run(route_command("/runtime_provider not-a-real-provider", telegram_id=OWNER_ID))
    assert "Unknown provider" in result.text
