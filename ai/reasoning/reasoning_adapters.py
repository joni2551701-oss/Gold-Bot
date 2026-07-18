"""
AI Layer — Reasoning Integration Adapters (Phase 63.4, TASK 4/5/6).

Three pure functions, each a one-way translation across a package
boundary the Intelligence Dependency Principle (Director Policy,
`docs/policies/DIRECTOR_POLICY.md`) allows or forbids:

- `step_from_knowledge_entry()` / `step_from_memory_entry()` --
  Knowledge and Memory are *upstream* of Reasoning in the Official
  Intelligence Pipeline, so reading their already-public dataclass
  fields (never `KnowledgeManager`/`MemoryRuntime`'s internal state)
  is allowed, same "reference a data shape from an earlier stage"
  pattern Constitution Article 3 already sanctions for
  `decision/` <- `AIAnalysisResult`.
- `reasoning_result_to_explanation_fields()` -- Explanation is
  *downstream* of Reasoning, so this function returns a plain `dict`
  of primitive values shaped like `ExplanationInput`'s own fields
  without importing `ai.explanation` at all. A future caller (not this
  module) would import both packages and bridge them.
"""

from typing import Dict, Union

from ai.memory.models import MemoryEntry
from ai.reasoning.models import ReasoningResult, ReasoningStep
from knowledge.models import KnowledgeEntry


def step_from_knowledge_entry(entry: KnowledgeEntry) -> ReasoningStep:
    return ReasoningStep(
        label=entry.title,
        value=entry.summary,
        source=f"knowledge:{entry.key}",
    )


def step_from_memory_entry(entry: MemoryEntry) -> ReasoningStep:
    return ReasoningStep(
        label=entry.scope.value,
        value=str(entry.value),
        source=f"memory:{entry.key}",
    )


def reasoning_result_to_explanation_fields(result: ReasoningResult) -> Dict[str, Union[str, float]]:
    """
    Returns a plain dict shaped like a subset of
    `ai.explanation.explanation_input.ExplanationInput`'s own fields --
    `technical_reason` (str) and `confidence` (0-100 scale, converted
    from this package's own 0.0-1.0 convention). `ai/explanation/` is
    never imported here; a future caller merges this dict's values into
    its own `ExplanationInput` construction.
    """
    return {
        "technical_reason": result.conclusion,
        "confidence": result.confidence * 100.0,
    }
