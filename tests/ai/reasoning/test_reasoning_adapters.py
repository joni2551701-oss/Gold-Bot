"""Phase 63.4 TASK 4/5/6 — ai/reasoning/reasoning_adapters.py: Knowledge/Memory (upstream, type-only) and Explanation (downstream, dict-only) integration points."""

from ai.memory.models import MemoryEntry, MemoryScope, MemoryType
from ai.reasoning.models import ReasoningMode, ReasoningResult, ReasoningType
from ai.reasoning.reasoning_adapters import (
    reasoning_result_to_explanation_fields,
    step_from_knowledge_entry,
    step_from_memory_entry,
)
from knowledge.models import KnowledgeCategory, KnowledgeEntry


def test_step_from_knowledge_entry_maps_title_summary_and_key():
    entry = KnowledgeEntry(key="smc.bos", category=KnowledgeCategory.SMC, title="Break of Structure", summary="A structural break.")
    step = step_from_knowledge_entry(entry)

    assert step.label == "Break of Structure"
    assert step.value == "A structural break."
    assert step.source == "knowledge:smc.bos"


def test_step_from_memory_entry_maps_scope_value_and_key():
    entry = MemoryEntry(key="market.cpi_last", scope=MemoryScope.MARKET, memory_type=MemoryType.SHORT_TERM, value="bullish")
    step = step_from_memory_entry(entry)

    assert step.label == "MARKET"
    assert step.value == "bullish"
    assert step.source == "memory:market.cpi_last"


def test_reasoning_result_to_explanation_fields_scales_confidence_to_0_100():
    result = ReasoningResult(
        key="k", mode=ReasoningMode.MARKET, reasoning_type=ReasoningType.PROBABILITY_ESTIMATE,
        conclusion="Elevated bullish probability.", confidence=0.72,
    )
    fields = reasoning_result_to_explanation_fields(result)

    assert fields["technical_reason"] == "Elevated bullish probability."
    assert fields["confidence"] == 72.0


def test_reasoning_result_to_explanation_fields_returns_a_plain_dict():
    result = ReasoningResult(key="k", mode=ReasoningMode.GENERAL, reasoning_type=ReasoningType.SUMMARY, conclusion="c")
    fields = reasoning_result_to_explanation_fields(result)
    assert isinstance(fields, dict)
    assert set(fields.keys()) == {"technical_reason", "confidence"}


def test_reasoning_adapters_module_never_imports_ai_explanation():
    """The one file this phase's Intelligence Dependency Principle cares most about -- reasoning_result_to_explanation_fields() must return a plain dict, never import ai.explanation itself."""
    import ast
    import pathlib

    adapters_file = pathlib.Path(__file__).resolve().parents[3] / "ai" / "reasoning" / "reasoning_adapters.py"
    tree = ast.parse(adapters_file.read_text(), filename=str(adapters_file))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert not alias.name.startswith("ai.explanation"), alias.name
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                assert not node.module.startswith("ai.explanation"), node.module
