"""Phase 63.4 TASK 2 — ai/reasoning/models.py: ReasoningMode/ReasoningType/ReasoningPriority/ReasoningStep/ReasoningResult."""

from ai.reasoning.models import ReasoningMode, ReasoningPriority, ReasoningResult, ReasoningStep, ReasoningType


def test_reasoning_result_defaults_priority_to_normal_and_confidence_to_zero():
    result = ReasoningResult(key="k", mode=ReasoningMode.MARKET, reasoning_type=ReasoningType.SUMMARY, conclusion="c")
    assert result.priority is ReasoningPriority.NORMAL
    assert result.confidence == 0.0
    assert result.steps == ()


def test_reasoning_result_accepts_steps_and_explicit_confidence():
    step = ReasoningStep(label="CPI", value="bullish", source="memory:market.cpi_last")
    result = ReasoningResult(
        key="k", mode=ReasoningMode.MARKET, reasoning_type=ReasoningType.PROBABILITY_ESTIMATE,
        conclusion="c", steps=(step,), confidence=0.8, priority=ReasoningPriority.HIGH,
    )
    assert result.steps == (step,)
    assert result.confidence == 0.8
    assert result.priority is ReasoningPriority.HIGH


def test_reasoning_step_source_defaults_to_none():
    step = ReasoningStep(label="l", value="v")
    assert step.source is None


def test_reasoning_result_is_frozen():
    result = ReasoningResult(key="k", mode=ReasoningMode.GENERAL, reasoning_type=ReasoningType.SUMMARY, conclusion="c")
    try:
        result.conclusion = "mutated"
        assert False, "ReasoningResult should be frozen"
    except AttributeError:
        pass


def test_reasoning_step_is_frozen():
    step = ReasoningStep(label="l", value="v")
    try:
        step.value = "mutated"
        assert False, "ReasoningStep should be frozen"
    except AttributeError:
        pass


def test_reasoning_mode_has_the_three_brief_named_values():
    assert {m.value for m in ReasoningMode} == {"MARKET", "EDUCATION", "GENERAL"}


def test_reasoning_type_has_five_categories():
    assert {t.value for t in ReasoningType} == {
        "CORRELATION", "COMPARISON", "TREND_CONTINUITY", "PROBABILITY_ESTIMATE", "SUMMARY",
    }


def test_reasoning_priority_has_three_levels():
    assert {p.value for p in ReasoningPriority} == {"LOW", "NORMAL", "HIGH"}
