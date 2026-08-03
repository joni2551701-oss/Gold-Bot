"""
AI Layer — Chart Intelligence Future Vision Provider Vocabulary (Phase
66.1: AI Chart Intelligence Foundation, TASK 8).

Pure vocabulary, metadata only -- no API client, no network call, no
provider wiring anywhere in this file (Rule 4: "LLM / Vision API ...
YO'Q. Bu faqat Foundation."). Additive to `ai/capabilities/capability.py`'s
already-existing `Capability.VISION`/`Capability.IMAGE` members
(Phase 61.0): that enum names *what* the AI layer can be asked to do;
this one names *which vendor* a future, separately-approved phase
might route a Chart Intelligence request to -- the same relationship
`ai/providers/provider_capabilities.py` already has to `Capability`
generally. No `ai/providers/` file references this enum; wiring it up
is itself a future phase's own scope.
"""

from enum import Enum


class ChartVisionProviderType(Enum):
    """A future live-wiring phase's own vendor choice -- this Foundation names the vocabulary only, calls none of them."""

    NONE = "NONE"
    OPENAI_VISION = "OPENAI_VISION"
    GEMINI_VISION = "GEMINI_VISION"
    CLAUDE_VISION = "CLAUDE_VISION"
    LOCAL_VISION = "LOCAL_VISION"
