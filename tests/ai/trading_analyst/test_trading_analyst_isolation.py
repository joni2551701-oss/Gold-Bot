"""
Phase 66.0 TASK 10 — ai/trading_analyst/ stays isolated from every
Trading Core layer (Constitution Article 3, Rule 4 "AI faqat READ
ONLY"). Mirrors `tests/assistant/test_assistant_isolation.py`'s own
AST-based pattern exactly.
"""

import ast
import pathlib


def _trading_analyst_dir():
    return pathlib.Path(__file__).resolve().parents[3] / "ai_layer" / "fundamental_ai" / "trading_analyst"


def _imported_names(py_file: pathlib.Path):
    tree = ast.parse(py_file.read_text(), filename=str(py_file))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                yield node.module


def test_trading_analyst_never_imports_trading_core_layers():
    """Rule 1/4: decision/, risk/, execution/, strategies/, signals/, context/, monitoring/ -- zero exceptions, anywhere in this package, per Constitution Article 3's zero-exception rule."""
    forbidden_prefixes = (
        "decision_layer", "risk_layer", "execution_layer", "strategy_layer", "signal_layer", "context_layer", "core_layer.health_monitor",
    )

    for py_file in _trading_analyst_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_trading_analyst_never_imports_telegram_or_database():
    forbidden_prefixes = ("platform_layer.telegram", "database_layer")

    for py_file in _trading_analyst_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_trading_analyst_never_imports_ai_provider_or_llm_sdks():
    forbidden_prefixes = ("ai_layer.ai_engine.providers", "ai_layer.ai_coordinator", "openai", "anthropic", "google.generativeai")

    for py_file in _trading_analyst_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_content_media_broadcast_imports_confined_to_content_adapter():
    """ai.content/, media/, broadcast/ are only permitted in content_adapter.py -- models.py, access.py, analyst_runtime.py never import them."""
    widened_prefixes = ("ai_layer.ai_service.content", "media", "broadcast")
    adapter_file = _trading_analyst_dir() / "content_adapter.py"

    for py_file in _trading_analyst_dir().rglob("*.py"):
        if py_file == adapter_file:
            continue
        for name in _imported_names(py_file):
            assert not name.startswith(widened_prefixes), f"{py_file}: {name}"


def test_trading_analyst_never_imports_assistant_or_voice():
    """No cross-dependency with the Phase 65.x Personal Assistant/Voice sub-sequence -- this is a separate, sibling concern."""
    forbidden_prefixes = ("assistant", "voice")

    for py_file in _trading_analyst_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_trading_analyst_never_imports_core_package():
    """core/ sits beneath the whole pipeline and every layer may depend on it in principle, but ai/trading_analyst/ has no need to -- confirming zero coupling keeps this package's dependency surface minimal."""
    for py_file in _trading_analyst_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith("core."), f"{py_file}: {name}"


def test_only_content_adapter_imports_ai_content():
    adapter_file = _trading_analyst_dir() / "content_adapter.py"
    for py_file in _trading_analyst_dir().rglob("*.py"):
        if py_file == adapter_file:
            continue
        for name in _imported_names(py_file):
            assert not name.startswith("ai_layer.ai_service.content"), f"{py_file}: {name}"


def test_trading_analysis_input_has_no_trading_core_object_field_type():
    """Belt-and-suspenders: no dataclass field on TradingAnalysisInput/TradingAnalysis may be typed as a Trading Core object -- every field is a primitive/enum/Sequence[str] only."""
    import dataclasses

    from ai_layer.ai_engine.trading_analyst.models import TradingAnalysis, TradingAnalysisInput

    allowed_type_fragments = ("str", "float", "int", "bool", "Sequence", "TradingRiskLevel", "Optional")
    for model in (TradingAnalysisInput, TradingAnalysis):
        for f in dataclasses.fields(model):
            type_str = str(f.type)
            assert any(fragment in type_str for fragment in allowed_type_fragments), f"{model.__name__}.{f.name}: {type_str}"
