"""
AI Layer — Memory Scope Registry (Phase 63.3, TASK 3).

Static catalog of every `MemoryScope` this codebase knows the identity
of -- same "descriptor + build function" pattern
`ai/persona/persona_registry.py` and `ai/providers/provider_registry.py`
already established. Registering a scope here does not select it for
use anywhere; it is metadata only, read by nothing but
`MemoryRuntime`'s own future callers. No AI reasoning, no LLM call, no
storage of its own -- a fixed, hand-authored tuple decided at commit
time, the same posture `ai_layer/knowledge_ai/knowledge_base/registry.py` and
`ai/persona/persona_registry.py` both already use.
"""

from dataclasses import dataclass
from typing import Optional, Sequence

from ai_layer.knowledge_ai.memory_manager.models import MemoryScope, MemoryType


@dataclass(frozen=True)
class MemoryScopeDescriptor:
    scope: MemoryScope
    label: str
    description: str
    default_memory_type: MemoryType


_REGISTRY: Sequence[MemoryScopeDescriptor] = (
    MemoryScopeDescriptor(
        scope=MemoryScope.CONVERSATION,
        label="Conversation Memory",
        description="Short-term continuity within a single multi-turn AI conversation.",
        default_memory_type=MemoryType.SHORT_TERM,
    ),
    MemoryScopeDescriptor(
        scope=MemoryScope.MARKET,
        label="Market Memory",
        description="Short-term market context an AI surface referenced recently.",
        default_memory_type=MemoryType.SHORT_TERM,
    ),
    MemoryScopeDescriptor(
        scope=MemoryScope.EDUCATION,
        label="Education Memory",
        description="Long-term record of education topics already covered with a user.",
        default_memory_type=MemoryType.LONG_TERM,
    ),
    MemoryScopeDescriptor(
        scope=MemoryScope.USER_PREFERENCE,
        label="User Preference",
        description="Long-term, user-scoped preference (e.g. language, tone) an AI surface can read back.",
        default_memory_type=MemoryType.LONG_TERM,
    ),
    MemoryScopeDescriptor(
        scope=MemoryScope.EXPLANATION_HISTORY,
        label="Explanation History",
        description="Long-term record of past ExplanationOutput content, for future reference -- not a live trading record.",
        default_memory_type=MemoryType.LONG_TERM,
    ),
    MemoryScopeDescriptor(
        scope=MemoryScope.KNOWLEDGE_REFERENCE,
        label="Knowledge Reference",
        description="Long-term pointer to a knowledge/ entry key a caller resolved once and wants to recall without a fresh lookup.",
        default_memory_type=MemoryType.LONG_TERM,
    ),
)


def build_memory_scope_registry() -> Sequence[MemoryScopeDescriptor]:
    """Never raises. Six entries this phase -- a future phase may register more without changing this function's shape."""
    return _REGISTRY


def describe(scope: MemoryScope) -> Optional[MemoryScopeDescriptor]:
    """Never raises: an unknown scope returns None rather than a fabricated descriptor."""
    return next((descriptor for descriptor in _REGISTRY if descriptor.scope == scope), None)
