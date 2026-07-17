"""
AI Layer — Routing Rules (Phase 61.0: AI Infrastructure Foundation,
TASK 4).

A plain data table, `Capability -> ordered candidate provider names`
-- not a chain of `if capability == ...` branches. Per the brief:
"Hardcode YO'Q" -- adding or reordering a capability's candidates is a
one-line data edit here, never a change to `router.py`'s selection
logic. Provider names are plain strings matching
`ai/providers/provider_registry.py`'s `ProviderDescriptor.name` values
-- this module does not import `ai/providers/` itself, keeping the
rule table provider-registry-agnostic (a future provider can be added
to the registry without this file needing the class import).
"""

from typing import Dict, Tuple

from ai.capabilities.capability import Capability

# Ordering is a preference order, not an availability guarantee --
# router.py walks this list and skips any name the ProviderManager
# reports as unregistered or DISABLED.
ROUTING_RULES: Dict[Capability, Tuple[str, ...]] = {
    Capability.CHAT: ("gemini", "openai", "claude", "grok", "local_llm"),
    Capability.ANALYSIS: ("gemini", "claude", "openai"),
    Capability.EXPLANATION: ("gemini", "openai", "claude"),
    Capability.SUMMARY: ("openai", "gemini"),
    Capability.MEMORY: ("local_llm", "gemini"),
    Capability.EDUCATION: ("gemini", "openai"),
    Capability.TOOL_CALLING: ("openai", "claude"),
    Capability.VISION: ("openai", "gemini"),
    Capability.IMAGE: ("openai",),
    Capability.VIDEO: ("gemini",),
    Capability.VOICE: ("openai", "local_llm"),
    Capability.DOCUMENT: ("claude", "gemini"),
    # Phase 61.5 TASK 5 -- same candidate shape as ANALYSIS/EXPLANATION
    # (broad text-generation providers); still cleanly rejected by
    # ai/runtime/ai_service.py's _CAPABILITY_METHOD until a future
    # phase adds a runtime mapping, same as SUMMARY/EDUCATION today.
    Capability.AI_MARKET_REPORT: ("gemini", "claude", "openai"),
    Capability.AI_WEEKLY_OUTLOOK: ("gemini", "claude", "openai"),
    Capability.AI_NEWS_ANALYSIS: ("gemini", "claude", "openai"),
    Capability.AI_SCRIPT_GENERATION: ("openai", "gemini"),
    # Phase 63.0 TASK 8 -- same reasoning as the four Phase 61.5 AI_*
    # entries above: a data-only entry (this file's own "one-line data
    # edit" convention, never a router.py selection-logic change,
    # per Rule 9), required by tests/ai/router/test_router.py's own
    # "every Capability has a routing rule" invariant. Still cleanly
    # rejected by ai/runtime/ai_service.py's _CAPABILITY_METHOD until a
    # future phase adds a runtime mapping.
    Capability.AI_CONTENT: ("gemini", "claude", "openai"),
    Capability.AI_MEDIA: ("openai", "gemini"),
    Capability.AI_TRANSLATION: ("gemini", "openai"),
    Capability.AI_BROADCAST: ("gemini", "claude", "openai"),
}


def get_candidate_providers(capability: Capability) -> Tuple[str, ...]:
    """Returns the ordered candidate tuple for `capability`, or an empty tuple if the capability has no declared rule -- never raises, never falls back to a guessed default."""
    return ROUTING_RULES.get(capability, ())
