"""
Phase B.0 -- isolation tests for the new monitoring/ modules
(resource_monitor.py, health_monitor.py, performance_collector.py,
access.py). Mirrors `tests/monitoring/test_monitoring_isolation.py`'s
own AST-based pattern exactly.
"""

import ast
import pathlib

NEW_FILES = ("resource_monitor.py", "health_monitor.py", "performance_collector.py", "access.py")


def _monitoring_dir():
    return pathlib.Path(__file__).resolve().parents[2] / "monitoring"


def _imported_names(py_file: pathlib.Path):
    tree = ast.parse(py_file.read_text(), filename=str(py_file))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                yield node.module


def test_phase_b0_files_never_import_decision_risk_execution_strategies_signals():
    forbidden_prefixes = ("decision", "risk", "execution", "strategies", "signals")
    for filename in NEW_FILES:
        py_file = _monitoring_dir() / filename
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_phase_b0_files_never_import_ai_package():
    for filename in NEW_FILES:
        py_file = _monitoring_dir() / filename
        for name in _imported_names(py_file):
            assert not name.startswith("ai."), f"{py_file}: {name}"


def test_phase_b0_files_never_import_context_or_core_pipeline():
    """Rule 1: monitoring never touches core/pipeline.py -- confirmed no context/ or core.pipeline import."""
    for filename in NEW_FILES:
        py_file = _monitoring_dir() / filename
        for name in _imported_names(py_file):
            assert name != "core.pipeline", f"{py_file}: {name}"
            assert not name.startswith("context"), f"{py_file}: {name}"


def test_resource_monitor_confined_to_stdlib_core_logger_database_and_monitoring():
    py_file = _monitoring_dir() / "resource_monitor.py"
    allowed_prefixes = ("threading", "datetime", "typing", "core.logger", "database.monitoring_repository", "monitoring.models", "monitoring.system_monitor", "resource")
    for name in _imported_names(py_file):
        assert name.startswith(allowed_prefixes), f"{py_file}: {name}"


def test_health_monitor_confined_to_stdlib_and_monitoring_models():
    py_file = _monitoring_dir() / "health_monitor.py"
    allowed_prefixes = ("typing", "monitoring.models")
    for name in _imported_names(py_file):
        assert name.startswith(allowed_prefixes), f"{py_file}: {name}"


def test_performance_collector_confined_to_stdlib_and_monitoring_models():
    py_file = _monitoring_dir() / "performance_collector.py"
    allowed_prefixes = ("time", "typing", "monitoring.models")
    for name in _imported_names(py_file):
        assert name.startswith(allowed_prefixes), f"{py_file}: {name}"


def test_access_confined_to_configuration_feature_flags():
    py_file = _monitoring_dir() / "access.py"
    allowed_prefixes = ("goldbot.core_layer.configuration.feature_flags",)
    for name in _imported_names(py_file):
        assert name.startswith(allowed_prefixes), f"{py_file}: {name}"


def test_health_monitor_never_imports_database():
    """health_monitor.py is a pure function over already-known facts -- it reads no database of its own."""
    py_file = _monitoring_dir() / "health_monitor.py"
    for name in _imported_names(py_file):
        assert not name.startswith("database"), f"{py_file}: {name}"


def test_performance_collector_never_imports_database():
    """PerformanceCollector is in-memory only, per its own docstring -- no persistence import."""
    py_file = _monitoring_dir() / "performance_collector.py"
    for name in _imported_names(py_file):
        assert not name.startswith("database"), f"{py_file}: {name}"
