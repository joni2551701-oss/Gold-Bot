"""
Phase 63.1 TASK 7 — real command_router/handlers dispatch for
/ai_explanation_status. Same discipline `test_runtime_owner_dispatch.py`
established (Phase 62.2): a unit test of the handler function alone
cannot catch a `getattr(handlers, f"{command}_handler")` name mismatch
(the Phase 61.7 bug this repository has already been bitten by once).
"""

import asyncio

from telegram.command_router import route_command, PERMISSION_DENIED_TEXT

OWNER_ID = "111"  # matches conftest's TELEGRAM_OWNER_ID
USER_ID = "333"


def _run(coro):
    return asyncio.run(coro)


def test_ai_explanation_status_dispatches_and_is_owner_only():
    owner = _run(route_command("/ai_explanation_status", telegram_id=OWNER_ID))
    user = _run(route_command("/ai_explanation_status", telegram_id=USER_ID))

    assert "AI EXPLANATION STATUS" in owner.text
    assert "Templates:\n3" in owner.text
    assert user.text == PERMISSION_DENIED_TEXT
