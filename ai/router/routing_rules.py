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
}


def get_candidate_providers(capability: Capability) -> Tuple[str, ...]:
    """Returns the ordered candidate tuple for `capability`, or an empty tuple if the capability has no declared rule -- never raises, never falls back to a guessed default."""
    return ROUTING_RULES.get(capability, ())
