"""Phase 61.4 TASK 2 — AI Permission Service: real telegram_id -> AIRole resolver, over already-resolved identity facts."""

from ai.access.permissions import AIRole
from ai.access.permission_service import resolve_ai_role


def test_owner_flag_wins_regardless_of_plan():
    assert resolve_ai_role(is_owner=True, is_admin=False, plan="FREE") == AIRole.OWNER


def test_admin_flag_wins_over_plan_when_not_owner():
    assert resolve_ai_role(is_owner=False, is_admin=True, plan="FREE") == AIRole.ADMIN


def test_owner_takes_priority_over_admin():
    assert resolve_ai_role(is_owner=True, is_admin=True, plan="FREE") == AIRole.OWNER


def test_neither_owner_nor_admin_falls_back_to_plan():
    assert resolve_ai_role(is_owner=False, is_admin=False, plan="VIP") == AIRole.VIP
    assert resolve_ai_role(is_owner=False, is_admin=False, plan="PREMIUM") == AIRole.PREMIUM


def test_no_plan_and_no_admin_or_owner_defaults_to_free():
    assert resolve_ai_role(is_owner=False, is_admin=False, plan=None) == AIRole.FREE


def test_neither_flag_with_unrecognized_plan_fails_closed_to_free():
    assert resolve_ai_role(is_owner=False, is_admin=False, plan="NOT_A_REAL_PLAN") == AIRole.FREE
