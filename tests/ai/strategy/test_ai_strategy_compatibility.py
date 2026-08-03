"""
Phase 66.6 TASK 8 — Future Compatibility confirmation. Permanently
confirms none of the brief's own nine future directions (Strategy
Versioning history, Market Regime, Strategy Evolution History, A/B
Testing, Optimization, Auto Benchmark, Simulation, Recommendation,
Correlation) exists as a module, class, or method anywhere in
`ai/strategy/` -- this Foundation only classifies and stores individual
strategy metadata records. Mirrors
`tests/ai/coaching/test_ai_coaching_compatibility.py`'s own pattern.
"""

import pathlib

import ai_layer.ai_engine.strategy as strategy_package
from ai_layer.ai_engine.strategy.models import StrategyRecord
from ai_layer.ai_engine.strategy.strategy_runtime import StrategyRuntime

FORBIDDEN_NAMES = (
    "StrategyVersionHistory",
    "MarketRegime",
    "StrategyEvolution",
    "ABTest",
    "ABTesting",
    "Optimization",
    "Optimizer",
    "Benchmark",
    "Simulation",
    "Simulator",
    "Recommendation",
    "Correlation",
)


def _strategy_dir():
    return pathlib.Path(strategy_package.__file__).resolve().parent


def test_no_future_concept_module_files_exist():
    filenames = {p.stem for p in _strategy_dir().glob("*.py")}
    expected = {
        "__init__", "models", "access", "strategy_runtime",
        "performance_adapter", "journal_adapter", "memory_adapter",
    }
    assert filenames == expected


def test_strategy_record_carries_no_forbidden_future_field():
    import dataclasses

    field_names = {f.name for f in dataclasses.fields(StrategyRecord)}
    forbidden = {
        "market_regime", "version_history", "evolution_history",
        "ab_test_group", "optimization_score", "benchmark_score",
        "simulation_id", "recommendation", "correlation_id",
    }
    assert field_names.isdisjoint(forbidden)


def test_strategy_runtime_has_no_future_concept_method():
    public_methods = {name for name in dir(StrategyRuntime) if not name.startswith("_")}
    forbidden = {
        "optimize", "benchmark", "simulate", "recommend", "correlate",
        "detect_regime", "compare", "ab_test",
    }
    assert public_methods.isdisjoint(forbidden)


def test_no_forbidden_future_concept_class_defined_anywhere_in_package():
    import ast

    for py_file in _strategy_dir().glob("*.py"):
        tree = ast.parse(py_file.read_text(), filename=str(py_file))
        defined_names = {
            node.name for node in ast.walk(tree)
            if isinstance(node, (ast.ClassDef, ast.FunctionDef))
        }
        assert defined_names.isdisjoint(FORBIDDEN_NAMES), f"{py_file}: {defined_names & set(FORBIDDEN_NAMES)}"
