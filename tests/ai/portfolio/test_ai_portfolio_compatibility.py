"""
Phase 66.7 TASK 8 — Future Compatibility confirmation. Permanently
confirms none of the brief's own ten future directions (Multi
Portfolio, Capital Allocation, Asset Allocation, Cross-Asset, Portfolio
Correlation, Diversification, Portfolio Optimization, Portfolio
Benchmark, Portfolio Simulation, Portfolio Recommendation) exists as a
module, class, or method anywhere in `ai/portfolio/` -- this
Foundation only classifies and stores individual portfolio metadata
records. Mirrors
`tests/ai/strategy/test_ai_strategy_compatibility.py`'s own pattern.
"""

import pathlib

import ai_layer.ai_engine.portfolio as portfolio_package
from ai_layer.ai_engine.portfolio.models import PortfolioRecord
from ai_layer.ai_engine.portfolio.portfolio_runtime import PortfolioRuntime

FORBIDDEN_NAMES = (
    "CapitalAllocation",
    "AssetAllocation",
    "CrossAsset",
    "PortfolioCorrelation",
    "Diversification",
    "PortfolioOptimization",
    "Optimizer",
    "PortfolioBenchmark",
    "Benchmark",
    "PortfolioSimulation",
    "Simulator",
    "PortfolioRecommendation",
    "Recommendation",
)


def _portfolio_dir():
    return pathlib.Path(portfolio_package.__file__).resolve().parent


def test_no_future_concept_module_files_exist():
    filenames = {p.stem for p in _portfolio_dir().glob("*.py")}
    expected = {
        "__init__", "models", "access", "portfolio_runtime",
        "performance_adapter", "strategy_adapter", "memory_adapter",
    }
    assert filenames == expected


def test_portfolio_record_carries_no_forbidden_future_field():
    import dataclasses

    field_names = {f.name for f in dataclasses.fields(PortfolioRecord)}
    forbidden = {
        "capital_allocation", "asset_allocation", "cross_asset",
        "correlation_matrix", "diversification_score",
        "optimization_score", "benchmark_score", "simulation_id",
        "recommendation", "account_type",
    }
    assert field_names.isdisjoint(forbidden)


def test_portfolio_runtime_has_no_future_concept_method():
    public_methods = {name for name in dir(PortfolioRuntime) if not name.startswith("_")}
    forbidden = {
        "optimize", "benchmark", "simulate", "recommend", "correlate",
        "allocate", "diversify", "compare",
    }
    assert public_methods.isdisjoint(forbidden)


def test_no_forbidden_future_concept_class_defined_anywhere_in_package():
    import ast

    for py_file in _portfolio_dir().glob("*.py"):
        tree = ast.parse(py_file.read_text(), filename=str(py_file))
        defined_names = {
            node.name for node in ast.walk(tree)
            if isinstance(node, (ast.ClassDef, ast.FunctionDef))
        }
        assert defined_names.isdisjoint(FORBIDDEN_NAMES), f"{py_file}: {defined_names & set(FORBIDDEN_NAMES)}"


def test_no_multi_portfolio_account_type_classification_exists_yet():
    """Multi Portfolio (Personal/Prop Firm/Investor) is Director-noted future scope -- no account_type-shaped field exists on PortfolioRecord today."""
    import dataclasses

    field_names = {f.name for f in dataclasses.fields(PortfolioRecord)}
    assert "account_type" not in field_names
    assert "portfolio_type" not in field_names
