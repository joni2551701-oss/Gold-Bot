"""Phase 63.6 TASK 10 — ai/content/ stays isolated from trading layers (Constitution Article 3) and downstream Intelligence layers (Intelligence Dependency Principle)."""

import ast
import pathlib


def _content_dir():
    return pathlib.Path(__file__).resolve().parents[3] / "ai" / "content"


def test_content_package_never_imports_trading_or_downstream_intelligence_layers():
    forbidden_prefixes = (
        "decision", "risk", "execution", "strategies", "database", "telegram",
        "translation", "media", "broadcast",
    )

    for py_file in _content_dir().glob("*.py"):
        tree = ast.parse(py_file.read_text(), filename=str(py_file))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert not alias.name.startswith(forbidden_prefixes), f"{py_file}: {alias.name}"
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    assert not node.module.startswith(forbidden_prefixes), f"{py_file}: {node.module}"
