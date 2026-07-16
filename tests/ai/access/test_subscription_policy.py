"""Phase 61.4 TASK 2 — Subscription Policy: pure SubscriptionRecord.plan string -> AIRole mapping."""

from ai.access.permissions import AIRole
from ai.access.subscription_policy import plan_to_ai_role


def test_vip_plan_maps_to_vip_role():
    assert plan_to_ai_role("VIP") == AIRole.VIP


def test_premium_plan_maps_to_premium_role():
    assert plan_to_ai_role("PREMIUM") == AIRole.PREMIUM


def test_free_plan_maps_to_free_role():
    assert plan_to_ai_role("FREE") == AIRole.FREE


def test_plan_matching_is_case_insensitive():
    assert plan_to_ai_role("premium") == AIRole.PREMIUM


def test_none_plan_fails_closed_to_free():
    assert plan_to_ai_role(None) == AIRole.FREE


def test_unrecognized_plan_fails_closed_to_free():
    assert plan_to_ai_role("SOME_FUTURE_PLAN") == AIRole.FREE
