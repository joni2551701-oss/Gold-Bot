"""
AI Layer — Reasoning Type Registry (Phase 63.4, TASK 1/3).

Static catalog of every `ReasoningType` this codebase knows the
identity of -- same "descriptor + build function" pattern
`ai/persona/persona_registry.py` and `ai/memory/memory_registry.py`
already established. Metadata only, zero AI reasoning, zero LLM/network
call -- a fixed, hand-authored tuple decided at commit time.
"""

from dataclasses import dataclass
from typing import Optional, Sequence

from ai_layer.ai_engine.reasoning.models import ReasoningType


@dataclass(frozen=True)
class ReasoningTypeDescriptor:
    reasoning_type: ReasoningType
    label: str
    description: str


_REGISTRY: Sequence[ReasoningTypeDescriptor] = (
    ReasoningTypeDescriptor(
        reasoning_type=ReasoningType.CORRELATION,
        label="Correlation",
        description="Relates a current market observation to a known Knowledge fact.",
    ),
    ReasoningTypeDescriptor(
        reasoning_type=ReasoningType.COMPARISON,
        label="Comparison",
        description="Compares a current situation with a Memory-recalled past occurrence.",
    ),
    ReasoningTypeDescriptor(
        reasoning_type=ReasoningType.TREND_CONTINUITY,
        label="Trend Continuity",
        description="Assesses whether an already-observed pattern is likely to continue, from already-supplied steps only.",
    ),
    ReasoningTypeDescriptor(
        reasoning_type=ReasoningType.PROBABILITY_ESTIMATE,
        label="Probability Estimate",
        description="Synthesizes multiple reasoning steps into one confidence-scored conclusion, supplied by the caller.",
    ),
    ReasoningTypeDescriptor(
        reasoning_type=ReasoningType.SUMMARY,
        label="Summary",
        description="Condenses multiple reasoning steps into one short statement.",
    ),
)


def build_reasoning_type_registry() -> Sequence[ReasoningTypeDescriptor]:
    """Never raises. Five entries this phase -- a future phase may register more without changing this function's shape."""
    return _REGISTRY


def describe(reasoning_type: ReasoningType) -> Optional[ReasoningTypeDescriptor]:
    """Never raises: an unknown type returns None rather than a fabricated descriptor."""
    return next((descriptor for descriptor in _REGISTRY if descriptor.reasoning_type == reasoning_type), None)
