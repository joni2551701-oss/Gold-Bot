"""Phase 63.5 TASK 10 — ai/conversation/ stays isolated from trading layers (Constitution Article 3) and downstream Intelligence layers (Intelligence Dependency Principle)."""

import ast
import pathlib


def _conversation_dir():
    return pathlib.Path(__file__).resolve().parents[3] / "ai_layer" / "personal_ai" / "interaction_manager"


def test_conversation_package_never_imports_trading_or_downstream_intelligence_layers():
    forbidden_prefixes = (
        "decision_layer", "risk_layer", "execution_layer", "strategy_layer", "database_layer", "platform_layer.telegram",
        "ai_layer.explanation_ai", "ai_layer.ai_service.content", "media_layer.telegram_broadcast", "media_layer.content_manager", "media_layer.translation",
    )

    for py_file in _conversation_dir().glob("*.py"):
        tree = ast.parse(py_file.read_text(), filename=str(py_file))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert not alias.name.startswith(forbidden_prefixes), f"{py_file}: {alias.name}"
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    assert not node.module.startswith(forbidden_prefixes), f"{py_file}: {node.module}"
