"""Phase 63.8 TASK 7 — broadcast/ stays isolated from trading layers (Constitution Article 3 / Rule 1)."""

import ast
import pathlib


def _broadcast_dir():
    return pathlib.Path(__file__).resolve().parents[2] / "broadcast"


def test_broadcast_package_never_imports_trading_layers():
    forbidden_prefixes = (
        "decision", "risk", "execution", "strategies", "signals", "database", "telegram",
    )

    for py_file in _broadcast_dir().glob("*.py"):
        tree = ast.parse(py_file.read_text(), filename=str(py_file))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert not alias.name.startswith(forbidden_prefixes), f"{py_file}: {alias.name}"
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    assert not node.module.startswith(forbidden_prefixes), f"{py_file}: {node.module}"
