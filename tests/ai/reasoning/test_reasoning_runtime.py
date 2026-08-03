"""Phase 63.4 TASK 3 — ai/reasoning/reasoning_runtime.py: ReasoningRuntime (reason/explain/summarize/evaluate/compare/chain/history), all deterministic."""

from ai_layer.ai_engine.reasoning.models import ReasoningMode, ReasoningResult, ReasoningStep, ReasoningType
from ai_layer.ai_engine.reasoning.reasoning_runtime import ReasoningRuntime


def _result(key="k1", conclusion="c1", confidence=0.5, steps=()):
    return ReasoningResult(
        key=key, mode=ReasoningMode.MARKET, reasoning_type=ReasoningType.CORRELATION,
        conclusion=conclusion, steps=steps, confidence=confidence,
    )


def test_reason_stores_and_returns_the_result_unchanged():
    runtime = ReasoningRuntime()
    result = _result()
    assert runtime.reason(result) is result


def test_reason_overwrites_an_existing_key():
    runtime = ReasoningRuntime()
    runtime.reason(_result(confidence=0.1))
    runtime.reason(_result(confidence=0.9))
    assert runtime.evaluate("k1") == 0.9


def test_explain_returns_conclusion():
    runtime = ReasoningRuntime()
    runtime.reason(_result(conclusion="bullish bias"))
    assert runtime.explain("k1") == "bullish bias"


def test_explain_missing_key_returns_none():
    runtime = ReasoningRuntime()
    assert runtime.explain("does-not-exist") is None


def test_summarize_joins_step_labels_and_values():
    steps = (ReasoningStep(label="CPI", value="bullish"), ReasoningStep(label="Structure", value="uptrend"))
    runtime = ReasoningRuntime()
    runtime.reason(_result(steps=steps))
    summary = runtime.summarize("k1")
    assert "CPI: bullish" in summary
    assert "Structure: uptrend" in summary


def test_summarize_missing_key_returns_none():
    runtime = ReasoningRuntime()
    assert runtime.summarize("does-not-exist") is None


def test_evaluate_returns_confidence():
    runtime = ReasoningRuntime()
    runtime.reason(_result(confidence=0.42))
    assert runtime.evaluate("k1") == 0.42


def test_evaluate_missing_key_returns_none():
    runtime = ReasoningRuntime()
    assert runtime.evaluate("does-not-exist") is None


def test_compare_returns_confidence_delta():
    runtime = ReasoningRuntime()
    runtime.reason(_result(key="a", confidence=0.8))
    runtime.reason(_result(key="b", confidence=0.3))
    assert runtime.compare("a", "b") == 0.5


def test_compare_missing_either_key_returns_none():
    runtime = ReasoningRuntime()
    runtime.reason(_result(key="a"))
    assert runtime.compare("a", "does-not-exist") is None
    assert runtime.compare("does-not-exist", "a") is None


def test_chain_returns_results_in_the_given_key_order():
    runtime = ReasoningRuntime()
    runtime.reason(_result(key="a"))
    runtime.reason(_result(key="b"))
    chained = runtime.chain(["b", "a"])
    assert [r.key for r in chained] == ["b", "a"]


def test_chain_skips_unknown_keys():
    runtime = ReasoningRuntime()
    runtime.reason(_result(key="a"))
    chained = runtime.chain(["a", "does-not-exist"])
    assert [r.key for r in chained] == ["a"]


def test_history_returns_every_result_in_first_stored_order():
    runtime = ReasoningRuntime()
    runtime.reason(_result(key="a"))
    runtime.reason(_result(key="b"))
    runtime.reason(_result(key="a", confidence=0.99))  # re-store, should not move position
    assert [r.key for r in runtime.history()] == ["a", "b"]


def test_reasoning_runtime_never_imports_trading_or_downstream_intelligence_layers():
    """ai_layer/ai_engine/reasoning/ never imports decision/risk/execution/strategies/database/telegram (Constitution Article 3), and never imports ai.explanation/ai.content/ai.conversation/broadcast/media/translation (Intelligence Dependency Principle -- all downstream of Reasoning)."""
    import ast
    import pathlib

    reasoning_dir = pathlib.Path(__file__).resolve().parents[3] / "ai_layer" / "explanation_ai" / "reasoning"
    forbidden_prefixes = (
        "decision_layer", "risk_layer", "execution_layer", "strategy_layer", "database_layer", "platform_layer.telegram",
        "ai_layer.explanation_ai", "ai_layer.ai_service.content", "ai_layer.personal_ai.interaction_manager", "media_layer.telegram_broadcast", "media_layer.content_manager", "media_layer.translation",
    )

    for py_file in reasoning_dir.glob("*.py"):
        tree = ast.parse(py_file.read_text(), filename=str(py_file))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert not alias.name.startswith(forbidden_prefixes), f"{py_file}: {alias.name}"
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    assert not node.module.startswith(forbidden_prefixes), f"{py_file}: {node.module}"
