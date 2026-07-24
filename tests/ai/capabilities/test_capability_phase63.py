"""Phase 63.0 TASK 8 — four new Capability members (AI_CONTENT/AI_MEDIA/AI_TRANSLATION/AI_BROADCAST). Purely additive -- no runtime dispatch mapping, no router.py selection-logic change."""

from ai.access.access_control import AccessControl
from ai.access.permissions import AIRole
from ai.capabilities.capability import Capability
from ai.router.routing_rules import ROUTING_RULES, get_candidate_providers


def test_four_new_capabilities_exist():
    for name in ("AI_CONTENT", "AI_MEDIA", "AI_TRANSLATION", "AI_BROADCAST"):
        assert hasattr(Capability, name)


def test_owner_and_admin_gain_the_new_capabilities_automatically():
    access = AccessControl()
    for capability in (Capability.AI_CONTENT, Capability.AI_MEDIA, Capability.AI_TRANSLATION, Capability.AI_BROADCAST):
        assert access.is_allowed(AIRole.OWNER, capability) is True
        assert access.is_allowed(AIRole.ADMIN, capability) is True


def test_free_tier_does_not_gain_the_new_capabilities_by_default():
    access = AccessControl()
    for capability in (Capability.AI_CONTENT, Capability.AI_MEDIA, Capability.AI_TRANSLATION, Capability.AI_BROADCAST):
        assert access.is_allowed(AIRole.FREE, capability) is False


def test_each_new_capability_has_a_routing_rule():
    for capability in (Capability.AI_CONTENT, Capability.AI_MEDIA, Capability.AI_TRANSLATION, Capability.AI_BROADCAST):
        assert capability in ROUTING_RULES
        assert len(get_candidate_providers(capability)) > 0
