"""
AI Layer — Conversation Integration Adapters (Phase 63.5, TASK 4/5/6/7).

Four pure functions, each a one-way translation across a package
boundary the Intelligence Dependency Principle (Director Policy,
`docs/policies/DIRECTOR_POLICY.md`) allows or forbids:

- `knowledge_key_from_entry()` / `memory_key_from_entry()` /
  `reasoning_key_from_result()` -- Knowledge, Memory, and Reasoning are
  all *upstream* of Conversation in the Official Intelligence Pipeline,
  so reading their already-public dataclass fields (never
  `KnowledgeManager`/`MemoryRuntime`/`ReasoningRuntime`'s internal
  state) is allowed, the same pattern
  `ai/reasoning/reasoning_adapters.py` already established in Phase
  63.4 for its own upstream reads.
- `conversation_context_to_explanation_fields()` -- Explanation is
  *downstream* of Conversation, so this function returns a plain
  `dict` of primitive values shaped like `ExplanationInput`'s own
  fields without importing `ai.explanation` at all.
"""

from typing import Dict

from ai.conversation.models import ConversationContext
from ai.memory.models import MemoryEntry
from ai.reasoning.models import ReasoningResult
from knowledge.models import KnowledgeEntry


def knowledge_key_from_entry(entry: KnowledgeEntry) -> str:
    """`category:key`, e.g. `"SMC:smc.bos"` -- uses the entry's own category metadata, never Knowledge storage/registry internals."""
    return f"{entry.category.value}:{entry.key}"


def memory_key_from_entry(entry: MemoryEntry) -> str:
    """`scope:key`, e.g. `"MARKET:market.cpi_last"` -- uses the entry's own scope metadata, never MemoryRuntime's internal storage."""
    return f"{entry.scope.value}:{entry.key}"


def reasoning_key_from_result(result: ReasoningResult) -> str:
    """`reasoning_type:key`, e.g. `"PROBABILITY_ESTIMATE:gold.cpi.prob"` -- uses the result's own reasoning_type metadata, never ReasoningRuntime's internal state."""
    return f"{result.reasoning_type.value}:{result.key}"


def conversation_context_to_explanation_fields(context: ConversationContext) -> Dict[str, str]:
    """
    Returns a plain dict shaped like a subset of
    `ai.explanation.explanation_input.ExplanationInput`'s own fields --
    `technical_reason` (a join of `context.recent_messages`).
    `ai/explanation/` is never imported here; a future caller merges
    this dict's values into its own `ExplanationInput` construction.
    """
    return {
        "technical_reason": "; ".join(f"{turn.role}: {turn.content}" for turn in context.recent_messages),
    }
