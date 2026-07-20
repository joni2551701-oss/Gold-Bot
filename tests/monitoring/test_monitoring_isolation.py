"""
GoldBot Core Owner Monitoring Alpha, TASK 8 -- monitoring/ (and
telegram/owner/monitoring_commands.py) stay isolated from Trading Core
decision-making layers. Mirrors the AST-based isolation test pattern
this codebase's `ai/*/test_*_isolation.py` suites already established.

Per the brief's own TASK 8 list: decision/, risk/, execution/ are
forbidden. `docs/PHASE_CORE_MONITORING_AUDIT.md` additionally confirms
`monitoring/decision_logger.py` never imports `signals`/`context`
either (a primitive-only contract boundary, stricter than the brief's
own minimum).
"""

import ast
import pathlib


def _monitoring_dir():
    return pathlib.Path(__file__).resolve().parents[2] / "monitoring"


def _owner_commands_file():
    return pathlib.Path(__file__).resolve().parents[2] / "telegram" / "owner" / "monitoring_commands.py"


def _imported_names(py_file: pathlib.Path):
    tree = ast.parse(py_file.read_text(), filename=str(py_file))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                yield node.module


def test_monitoring_never_imports_decision_risk_execution():
    forbidden_prefixes = ("decision", "risk", "execution")
    for py_file in _monitoring_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_monitoring_commands_never_imports_decision_risk_execution():
    forbidden_prefixes = ("decision", "risk", "execution")
    for name in _imported_names(_owner_commands_file()):
        assert not name.startswith(forbidden_prefixes), f"{_owner_commands_file()}: {name}"


def test_decision_logger_never_imports_signals_or_context():
    """Belt-and-suspenders: the one file most likely to be tempted to import SignalQualityResult directly stays primitive-only."""
    decision_logger_file = _monitoring_dir() / "decision_logger.py"
    forbidden_prefixes = ("signals", "context")
    for name in _imported_names(decision_logger_file):
        assert not name.startswith(forbidden_prefixes), f"{decision_logger_file}: {name}"


def test_monitoring_models_are_primitive_only():
    """Belt-and-suspenders: monitoring/models.py itself imports no Trading Core or upstream-object modules at all -- only stdlib."""
    models_file = _monitoring_dir() / "models.py"
    allowed_prefixes = ("dataclasses", "enum", "typing")
    for name in _imported_names(models_file):
        assert name.startswith(allowed_prefixes), f"{models_file}: {name}"


def test_monitoring_never_imports_ai_package():
    """Monitoring observes GoldBot Core, not the AI Layer -- no ai.* import anywhere in this package."""
    for py_file in _monitoring_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith("ai."), f"{py_file}: {name}"


def test_monitoring_never_imports_strategies_or_signals_directly_in_models_or_runtimes():
    """system_monitor.py/market_monitor.py/signal_monitor.py/error_monitor.py never import signals/ or strategies/ -- only decision_logger.py's own audited exception (primitive-only, see its own docstring) is even close to that concern, and it stays clear too (see test_decision_logger_never_imports_signals_or_context)."""
    forbidden_prefixes = ("strategies", "signals")
    for filename in ("system_monitor.py", "market_monitor.py", "signal_monitor.py", "error_monitor.py", "models.py"):
        py_file = _monitoring_dir() / filename
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_monitoring_repository_module_confined_to_database_and_stdlib():
    """database/monitoring_repository.py imports only database/, core.logger, and stdlib -- no Trading Core, no monitoring/ (repository stays below monitoring/, never imports back up)."""
    repo_file = pathlib.Path(__file__).resolve().parents[2] / "database" / "monitoring_repository.py"
    allowed_prefixes = ("database", "core.logger", "datetime", "typing")
    for name in _imported_names(repo_file):
        assert name.startswith(allowed_prefixes), f"{repo_file}: {name}"
