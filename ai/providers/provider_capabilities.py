"""
AI Layer — Provider Capability Matrix (Phase 61.1: AI Provider
Reliability Foundation, TASK 3).

Declares which `Capability` each placeholder provider is meant to
answer for -- a second, provider-keyed view of the same information
`ai/router/routing_rules.py`'s `ROUTING_RULES` already encodes
capability-first. `supports()` lets `ai/router/router.py` (TASK 4)
reject a candidate the routing table names but the provider itself
never declared, before it ever reaches `ProviderHealthTracker`.

Every (capability, provider) pair below is derived directly from
`ROUTING_RULES`'s existing candidate lists (Phase 61.0) -- a provider
supports exactly the capabilities it was already listed as a
candidate for, so this matrix cannot silently narrow what Phase 61.0's
router already routed successfully.
"""

from typing import Dict, FrozenSet

from ai.capabilities.capability import Capability

PROVIDER_CAPABILITIES: Dict[str, FrozenSet[Capability]] = {
    "gemini": frozenset({
        Capability.CHAT, Capability.ANALYSIS, Capability.EXPLANATION,
        Capability.SUMMARY, Capability.MEMORY, Capability.EDUCATION,
        Capability.VISION, Capability.VIDEO, Capability.DOCUMENT,
        Capability.AI_MARKET_REPORT, Capability.AI_WEEKLY_OUTLOOK,
        Capability.AI_NEWS_ANALYSIS, Capability.AI_SCRIPT_GENERATION,
    }),
    "openai": frozenset({
        Capability.CHAT, Capability.ANALYSIS, Capability.EXPLANATION,
        Capability.SUMMARY, Capability.EDUCATION, Capability.TOOL_CALLING,
        Capability.VISION, Capability.IMAGE, Capability.VOICE,
        Capability.AI_MARKET_REPORT, Capability.AI_WEEKLY_OUTLOOK,
        Capability.AI_NEWS_ANALYSIS, Capability.AI_SCRIPT_GENERATION,
    }),
    "claude": frozenset({
        Capability.CHAT, Capability.ANALYSIS, Capability.EXPLANATION,
        Capability.TOOL_CALLING, Capability.DOCUMENT,
        Capability.AI_MARKET_REPORT, Capability.AI_WEEKLY_OUTLOOK,
        Capability.AI_NEWS_ANALYSIS,
    }),
    "grok": frozenset({
        Capability.CHAT,
    }),
    "local_llm": frozenset({
        Capability.CHAT, Capability.MEMORY, Capability.VOICE,
    }),
}


def supports(provider_name: str, capability: Capability) -> bool:
    """Never raises: an unregistered provider name supports nothing (fail-safe, same posture as ProviderHealthTracker.is_available())."""
    return capability in PROVIDER_CAPABILITIES.get(provider_name, frozenset())


def capabilities_of(provider_name: str) -> FrozenSet[Capability]:
    return PROVIDER_CAPABILITIES.get(provider_name, frozenset())
