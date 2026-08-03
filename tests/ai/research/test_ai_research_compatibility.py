"""
Phase 66.8 TASK 9 — Future Compatibility confirmation. Permanently
confirms none of the brief's own eleven future directions (Research
Dataset, Pattern Mining, Market Regime Detection, Knowledge Graph
Integration, Paper Generator, Backtest Dataset, AI Dataset Builder,
Research Report, Research Versioning, Research Export, Research
Archive) exists as a module, class, or method anywhere in
`ai/research/` -- this Foundation only classifies and stores individual
research-item metadata records. Mirrors
`tests/ai/portfolio/test_ai_portfolio_compatibility.py`'s own pattern.
"""

import pathlib

import ai_layer.fundamental_ai as research_package
from ai_layer.fundamental_ai.models import ResearchRecord
from ai_layer.fundamental_ai.research_runtime import ResearchRuntime

FORBIDDEN_NAMES = (
    "ResearchDataset",
    "Dataset",
    "PatternMining",
    "PatternMiner",
    "MarketRegimeDetection",
    "RegimeDetector",
    "KnowledgeGraph",
    "KnowledgeGraphIntegration",
    "PaperGenerator",
    "BacktestDataset",
    "AIDatasetBuilder",
    "DatasetBuilder",
    "ResearchReport",
    "ReportGenerator",
    "ResearchVersioning",
    "Versioning",
    "ResearchExport",
    "Exporter",
    "ResearchArchive",
    "ArchiveManager",
)


def _research_dir():
    return pathlib.Path(research_package.__file__).resolve().parent


def test_no_future_concept_module_files_exist():
    filenames = {p.stem for p in _research_dir().glob("*.py")}
    expected = {
        "__init__", "models", "access", "research_runtime",
        "performance_adapter", "strategy_adapter", "portfolio_adapter", "memory_adapter",
    }
    assert filenames == expected


def test_research_record_carries_no_forbidden_future_field():
    import dataclasses

    field_names = {f.name for f in dataclasses.fields(ResearchRecord)}
    forbidden = {
        "dataset", "dataset_id", "pattern", "patterns", "regime",
        "market_regime", "knowledge_graph", "paper", "backtest_dataset",
        "report", "report_id", "version", "version_number", "export_path",
        "export_format", "archive_id",
    }
    assert field_names.isdisjoint(forbidden)


def test_research_runtime_has_no_future_concept_method():
    public_methods = {name for name in dir(ResearchRuntime) if not name.startswith("_")}
    forbidden = {
        "mine", "detect_regime", "build_dataset", "generate_report",
        "generate_paper", "export", "version", "build_knowledge_graph",
        "backtest",
    }
    assert public_methods.isdisjoint(forbidden)


def test_no_forbidden_future_concept_class_defined_anywhere_in_package():
    import ast

    for py_file in _research_dir().glob("*.py"):
        tree = ast.parse(py_file.read_text(), filename=str(py_file))
        defined_names = {
            node.name for node in ast.walk(tree)
            if isinstance(node, (ast.ClassDef, ast.FunctionDef))
        }
        assert defined_names.isdisjoint(FORBIDDEN_NAMES), f"{py_file}: {defined_names & set(FORBIDDEN_NAMES)}"


def test_no_research_dataset_or_pattern_mining_capability_exists_yet():
    """Research Dataset / Pattern Mining are Director-noted future scope -- no dataset- or pattern-shaped field exists on ResearchRecord today."""
    import dataclasses

    field_names = {f.name for f in dataclasses.fields(ResearchRecord)}
    assert "dataset" not in field_names
    assert "pattern" not in field_names
    assert "patterns" not in field_names
