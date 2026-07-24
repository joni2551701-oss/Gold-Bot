"""
AI Layer — Reasoning Model (Phase 63.4, TASK 2).

The structured shape `ai/reasoning/reasoning_runtime.py`'s
`ReasoningRuntime` stores and queries. Every field on `ReasoningStep`
and `ReasoningResult` is a primitive or an enum defined in this same
file -- no `DecisionResult`, `RiskResult`, `Trade`, `Position`,
`Order`, `MT5` object, or `Execution` type is a valid field type here,
and `ai/reasoning/` itself never imports any of those (verified by the
AST regression test this phase adds, same pattern
`ai/explanation/explanation_input.py`'s and `ai/memory/models.py`'s
own regression guards already established in Phase 63.1/63.3).
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Sequence


class ReasoningMode(Enum):
    MARKET = "MARKET"
    EDUCATION = "EDUCATION"
    GENERAL = "GENERAL"


class ReasoningType(Enum):
    CORRELATION = "CORRELATION"
    COMPARISON = "COMPARISON"
    TREND_CONTINUITY = "TREND_CONTINUITY"
    PROBABILITY_ESTIMATE = "PROBABILITY_ESTIMATE"
    SUMMARY = "SUMMARY"


class ReasoningPriority(Enum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"


@dataclass(frozen=True)
class ReasoningStep:
    """
    `source` is a free-text pointer (e.g. `"knowledge:smc.bos"`,
    `"memory:market.cpi_last"`) rather than an embedded
    `KnowledgeEntry`/`MemoryEntry` object -- `ReasoningStep` never
    carries another package's object graph. `reasoning_adapters.py`
    reads a `KnowledgeEntry`/`MemoryEntry`'s own fields to *produce* a
    `ReasoningStep`; it never stores the source object itself.
    """
    label: str
    value: str
    source: Optional[str] = None


@dataclass(frozen=True)
class ReasoningResult:
    """
    `confidence` is a 0.0-1.0 scale, matching `ExplanationOutput`'s own
    convention (Phase 63.0) -- `reasoning_adapters.py`'s
    `reasoning_result_to_explanation_fields()` converts to
    `ExplanationInput`'s 0-100 scale at the boundary, never here.
    """
    key: str
    mode: ReasoningMode
    reasoning_type: ReasoningType
    conclusion: str
    steps: Sequence[ReasoningStep] = field(default_factory=tuple)
    confidence: float = 0.0
    priority: ReasoningPriority = ReasoningPriority.NORMAL
