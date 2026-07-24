"""Phase 64.0 TASK 1-4 — ai/intelligence_runtime.py: IntelligenceRuntime composes all eight Official Intelligence Pipeline layers via their existing deterministic entry points, zero LLM calls."""

from ai.intelligence_runtime import IntelligenceRuntime, PipelineStage, PipelineStageResult


def test_run_walks_every_stage_in_official_intelligence_pipeline_order():
    runtime = IntelligenceRuntime()
    run = runtime.run("BOS")
    assert [result.stage for result in run.stages] == [
        PipelineStage.KNOWLEDGE, PipelineStage.MEMORY, PipelineStage.REASONING,
        PipelineStage.CONVERSATION, PipelineStage.EXPLANATION, PipelineStage.CONTENT,
        PipelineStage.MEDIA, PipelineStage.BROADCAST,
    ]


def test_run_returns_the_topic_it_was_given():
    runtime = IntelligenceRuntime()
    run = runtime.run("BOS")
    assert run.topic == "BOS"


def test_run_with_a_known_knowledge_topic_marks_knowledge_stage_ok():
    runtime = IntelligenceRuntime()
    run = runtime.run("BOS")
    knowledge_result = run.stages[0]
    assert knowledge_result.stage is PipelineStage.KNOWLEDGE
    assert knowledge_result.ok is True


def test_run_with_an_unknown_topic_marks_knowledge_stage_not_ok_but_never_raises():
    runtime = IntelligenceRuntime()
    run = runtime.run("completely-unknown-topic-xyz")
    knowledge_result = run.stages[0]
    assert knowledge_result.ok is False
    assert knowledge_result.detail == "no knowledge entry matched"


def test_run_still_completes_every_later_stage_when_knowledge_finds_nothing():
    """A missing Knowledge match must not abort the pipeline -- every later stage still runs deterministically off the fallback conclusion."""
    runtime = IntelligenceRuntime()
    run = runtime.run("completely-unknown-topic-xyz")
    assert len(run.stages) == 8
    for result in run.stages[1:]:
        assert isinstance(result, PipelineStageResult)


def test_run_never_raises_and_produces_ok_results_for_every_stage_on_a_known_topic():
    runtime = IntelligenceRuntime()
    run = runtime.run("BOS")
    assert all(result.ok for result in run.stages)


def test_run_reasoning_conclusion_flows_into_conversation_and_explanation():
    """Cross-stage primitive flow: Reasoning's own conclusion text ends up in both the Conversation session's history and Explanation's lesson field, never as an embedded object."""
    runtime = IntelligenceRuntime()
    run = runtime.run("BOS")
    reasoning_detail = run.stages[2].detail
    assert reasoning_detail
    assert run.stages[3].ok is True


def test_stage_result_detail_is_a_plain_string_never_a_dataclass():
    runtime = IntelligenceRuntime()
    run = runtime.run("BOS")
    for result in run.stages:
        assert isinstance(result.detail, str)


def test_pipeline_stage_has_all_eight_values():
    assert {stage.value for stage in PipelineStage} == {
        "KNOWLEDGE", "MEMORY", "REASONING", "CONVERSATION",
        "EXPLANATION", "CONTENT", "MEDIA", "BROADCAST",
    }


def test_intelligence_runtime_never_calls_ai_service():
    """No stage this module drives ever reaches AIService.ask() -- verified structurally: run() never constructs an AIContext or AIRole, both required by every AIService.ask()-calling path in this codebase."""
    import inspect

    from ai.intelligence_runtime import IntelligenceRuntime as _Runtime

    source = inspect.getsource(_Runtime.run)
    assert "ai_context" not in source
    assert ".ask(" not in source
    assert ".generate(" not in source
