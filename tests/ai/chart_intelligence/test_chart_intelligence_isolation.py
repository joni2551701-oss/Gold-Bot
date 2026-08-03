"""
Phase 66.1 TASK 9 — ai/chart_intelligence/ stays isolated from every
Trading Core layer (Constitution Article 3, Rule 4 "AI faqat READ
ONLY"). Mirrors `tests/ai/trading_analyst/test_trading_analyst_isolation.py`'s
own AST-based pattern exactly.
"""

import ast
import pathlib


def _chart_intelligence_dir():
    return pathlib.Path(__file__).resolve().parents[3] / "ai_layer" / "vision_ai"


def _imported_names(py_file: pathlib.Path):
    tree = ast.parse(py_file.read_text(), filename=str(py_file))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                yield node.module


def test_chart_intelligence_never_imports_trading_core_layers():
    """Rule 1/2/4: decision/, risk/, execution/, strategies/, signals/, context/, monitoring/ -- zero exceptions, anywhere in this package."""
    forbidden_prefixes = (
        "decision_layer", "risk_layer", "execution_layer", "strategy_layer", "signal_layer", "context_layer", "core_layer.health_monitor",
    )

    for py_file in _chart_intelligence_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_chart_intelligence_never_imports_telegram_or_database():
    forbidden_prefixes = ("platform_layer.telegram", "database_layer")

    for py_file in _chart_intelligence_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_chart_intelligence_never_imports_ai_provider_or_llm_sdks():
    """Rule 4: no Vision API/LLM SDK anywhere in this Foundation-only phase."""
    forbidden_prefixes = ("ai_layer.ai_engine.providers", "ai_layer.ai_coordinator", "openai", "anthropic", "google.generativeai")

    for py_file in _chart_intelligence_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_chart_intelligence_never_imports_assistant_or_voice():
    """No cross-dependency with the Phase 65.x Personal Assistant/Voice sub-sequence -- a separate, sibling concern."""
    forbidden_prefixes = ("assistant", "voice")

    for py_file in _chart_intelligence_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_chart_intelligence_never_imports_core_package():
    for py_file in _chart_intelligence_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith("core."), f"{py_file}: {name}"


def test_content_media_broadcast_imports_confined_to_content_adapter():
    """ai.content/, media/, broadcast/ are only permitted in content_adapter.py -- every other file in this package never imports them."""
    widened_prefixes = ("ai_layer.ai_service.content", "media", "broadcast")
    adapter_file = _chart_intelligence_dir() / "content_adapter.py"

    for py_file in _chart_intelligence_dir().rglob("*.py"):
        if py_file == adapter_file:
            continue
        for name in _imported_names(py_file):
            assert not name.startswith(widened_prefixes), f"{py_file}: {name}"


def test_only_content_adapter_imports_ai_content():
    adapter_file = _chart_intelligence_dir() / "content_adapter.py"
    for py_file in _chart_intelligence_dir().rglob("*.py"):
        if py_file == adapter_file:
            continue
        for name in _imported_names(py_file):
            assert not name.startswith("ai_layer.ai_service.content"), f"{py_file}: {name}"


def test_trading_analyst_import_confined_to_trading_analyst_adapter():
    """TASK 5: ai.trading_analyst is only permitted in trading_analyst_adapter.py -- models.py, access.py, chart_runtime.py, content_adapter.py, vision_provider_types.py never import it."""
    adapter_file = _chart_intelligence_dir() / "trading_analyst_adapter.py"

    for py_file in _chart_intelligence_dir().rglob("*.py"):
        if py_file == adapter_file:
            continue
        for name in _imported_names(py_file):
            assert not name.startswith("ai_layer.ai_engine.trading_analyst"), f"{py_file}: {name}"


def test_only_trading_analyst_adapter_imports_ai_trading_analyst():
    adapter_file = _chart_intelligence_dir() / "trading_analyst_adapter.py"
    found = False
    for name in _imported_names(adapter_file):
        if name.startswith("ai_layer.ai_engine.trading_analyst"):
            found = True
    assert found


def test_chart_intelligence_never_imports_knowledge_memory_reasoning():
    """TASK 0's audit conclusion: knowledge/, ai.memory/, ai.reasoning/ are not composed by this phase."""
    forbidden_prefixes = ("knowledge", "ai_layer.knowledge_ai.memory_manager", "ai_layer.ai_engine.reasoning")

    for py_file in _chart_intelligence_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_chart_analysis_input_has_no_trading_core_object_field_type():
    """Belt-and-suspenders: no dataclass field on ChartAnalysisInput/ChartAnalysis/ChartContext may be typed as a Trading Core object -- every field is a primitive/enum/Sequence[str] only."""
    import dataclasses

    from ai_layer.vision_ai.models import ChartAnalysis, ChartAnalysisInput, ChartContext

    allowed_type_fragments = (
        "str", "float", "int", "bool", "Sequence", "ChartImageType", "ChartAnalysisType", "Optional",
    )
    for model in (ChartAnalysisInput, ChartAnalysis, ChartContext):
        for f in dataclasses.fields(model):
            type_str = str(f.type)
            assert any(fragment in type_str for fragment in allowed_type_fragments), f"{model.__name__}.{f.name}: {type_str}"


def test_chart_intelligence_package_has_no_image_byte_fields():
    """Director Note 4: no field anywhere in this package's models stores image bytes/binary data."""
    import dataclasses

    from ai_layer.vision_ai.models import ChartAnalysis, ChartAnalysisInput, ChartContext

    for model in (ChartAnalysisInput, ChartAnalysis, ChartContext):
        for f in dataclasses.fields(model):
            assert "bytes" not in f.name.lower()
            assert "image_data" not in f.name.lower()
            assert "binary" not in f.name.lower()
