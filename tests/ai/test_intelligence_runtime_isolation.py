"""Phase 64.0 TASK 5 — ai_layer/ai_engine/intelligence_runtime.py stays isolated from trading layers (Constitution Article 3 / Rule 1). This is the one file in the codebase permitted to import every Intelligence layer at once (the composition root) -- what it must never import is the trading pipeline itself."""

import ast
import pathlib


def test_intelligence_runtime_never_imports_trading_layers():
    forbidden_prefixes = ("decision_layer", "risk_layer", "execution_layer", "strategy_layer", "signal_layer", "database_layer", "platform_layer.telegram")

    module_file = pathlib.Path(__file__).resolve().parents[2] / "ai_layer" / "ai_engine" / "intelligence_runtime.py"
    tree = ast.parse(module_file.read_text(), filename=str(module_file))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert not alias.name.startswith(forbidden_prefixes), alias.name
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                assert not node.module.startswith(forbidden_prefixes), node.module
