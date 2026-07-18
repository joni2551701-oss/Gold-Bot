"""Phase 61.5 TASK 5 — AI Content Types. No duplicate enum -- CONTENT_CAPABILITIES is a subset marker over the real ai.capabilities.capability.Capability enum."""

from ai.capabilities.capability import Capability
from ai.content.content_types import CONTENT_CAPABILITIES, ContentType, content_title, is_content_capability


def test_all_four_content_capabilities_are_marked():
    for capability in (
        Capability.AI_MARKET_REPORT, Capability.AI_WEEKLY_OUTLOOK,
        Capability.AI_NEWS_ANALYSIS, Capability.AI_SCRIPT_GENERATION,
    ):
        assert capability in CONTENT_CAPABILITIES
        assert is_content_capability(capability) is True


def test_non_content_capability_is_not_marked():
    assert is_content_capability(Capability.CHAT) is False
    assert is_content_capability(Capability.ANALYSIS) is False


def test_content_title_is_human_readable():
    assert content_title(Capability.AI_MARKET_REPORT) == "Market Report"
    assert content_title(Capability.AI_WEEKLY_OUTLOOK) == "Weekly Outlook"


def test_content_title_falls_back_to_value_for_a_non_content_capability():
    assert content_title(Capability.CHAT) == "CHAT"


# ---------------------------------------------------------------------------
# Phase 63.0 TASK 2 — ContentType vocabulary (foundation only, no generation)
# Phase 63.6 TASK 6 added TRADE_REPLAY (additive, Article 9) -- see
# docs/PHASE63_6_AUDIT.md for the naming-collision mapping of the
# brief's other five named types onto pre-existing members.
# ---------------------------------------------------------------------------

def test_content_type_has_all_eight_director_named_members():
    expected = {
        "WEEKLY_OUTLOOK", "DAILY_BRIEF", "NEWS_ANALYSIS", "MARKET_UPDATE",
        "PERFORMANCE_REVIEW", "EDUCATION", "EXPLANATION", "TRADE_REPLAY",
    }
    assert {member.value for member in ContentType} == expected
