"""
Phase 66.3 TASK 9 — ai/learning/ stays isolated from every Trading
Core layer (Constitution Article 3, Rule 2's own wider forbidden-import
list, Rule 3 "database emas"). Mirrors
`tests/ai/trade_journal/test_trade_journal_isolation.py`'s own
AST-based pattern exactly.
"""

import ast
import pathlib


def _learning_dir():
    return pathlib.Path(__file__).resolve().parents[3] / "ai_layer" / "knowledge_ai" / "learning_engine"


def _imported_names(py_file: pathlib.Path):
    tree = ast.parse(py_file.read_text(), filename=str(py_file))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                yield node.module


def test_learning_never_imports_trading_core_layers():
    """Rule 2: decision/, risk/, execution/, signals/, strategies/ -- zero exceptions."""
    forbidden_prefixes = ("decision_layer", "risk_layer", "execution_layer", "signal_layer", "strategy_layer")

    for py_file in _learning_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_learning_never_imports_telegram_database_or_monitoring():
    """Rule 2/3: telegram/, database/, monitoring/ -- zero exceptions."""
    forbidden_prefixes = ("platform_layer.telegram", "database_layer", "core_layer.health_monitor")

    for py_file in _learning_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_learning_never_imports_context_package():
    for py_file in _learning_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith("context"), f"{py_file}: {name}"


def test_learning_never_imports_sql_or_persistence_libraries():
    """Rule 3: no SQLite/Postgres/Redis client library anywhere in this package."""
    forbidden_prefixes = ("sqlite3", "psycopg2", "redis", "sqlalchemy")

    for py_file in _learning_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_learning_never_imports_the_top_level_learning_package():
    """docs/PHASE66_3_AUDIT.md: ai/learning/ never imports the pre-existing, unrelated top-level learning/ package (DB-persisted, different concern)."""
    for py_file in _learning_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not (name == "learning" or name.startswith("learning.")), f"{py_file}: {name}"


def test_learning_never_imports_analytics():
    for py_file in _learning_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith("analytics"), f"{py_file}: {name}"


def test_learning_never_imports_ai_provider_or_llm_sdks():
    """Rule 4: no LLM SDK anywhere in this Foundation-only phase."""
    forbidden_prefixes = ("ai_layer.ai_engine.providers", "ai_layer.ai_coordinator", "openai", "anthropic", "google.generativeai")

    for py_file in _learning_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"

    for py_file in _learning_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert "requests" != name and "httpx" != name and "urllib" not in name, f"{py_file}: {name} (Rule 5: no network)"


def test_learning_never_imports_assistant_voice_or_ai_memory():
    forbidden_prefixes = ("assistant", "voice", "ai_layer.knowledge_ai.memory_manager")

    for py_file in _learning_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_learning_never_imports_knowledge_ai_reasoning_chart_or_trading_analyst():
    """TASK 4 only names ai.trade_journal as the Learning input source -- Chart Intelligence and Trading Analyst are audited but never composed here."""
    forbidden_prefixes = ("knowledge", "ai_layer.ai_engine.reasoning", "ai_layer.vision_ai", "ai_layer.ai_engine.trading_analyst")

    for py_file in _learning_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_learning_never_imports_ai_content_media_broadcast():
    forbidden_prefixes = ("ai_layer.ai_service.content", "media_layer.content_manager", "media_layer.telegram_broadcast")

    for py_file in _learning_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_learning_never_imports_core_package():
    for py_file in _learning_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith("core."), f"{py_file}: {name}"


def test_trade_journal_import_confined_to_journal_adapter():
    """TASK 4: ai.trade_journal is only permitted in journal_adapter.py -- models.py, access.py, learning_runtime.py, memory_adapter.py never import it."""
    adapter_file = _learning_dir() / "journal_adapter.py"

    for py_file in _learning_dir().rglob("*.py"):
        if py_file == adapter_file:
            continue
        for name in _imported_names(py_file):
            assert not name.startswith("ai_layer.knowledge_ai.knowledge_base.trade_journal"), f"{py_file}: {name}"


def test_only_journal_adapter_imports_ai_trade_journal():
    adapter_file = _learning_dir() / "journal_adapter.py"
    imported = list(_imported_names(adapter_file))
    assert any(name.startswith("ai_layer.knowledge_ai.knowledge_base.trade_journal") for name in imported)


def test_memory_adapter_never_imports_ai_memory():
    """TASK 5: 'Memory Runtime chaqirilmaydi' -- confirmed even in the one file named for it."""
    memory_adapter_file = _learning_dir() / "memory_adapter.py"
    for name in _imported_names(memory_adapter_file):
        assert not name.startswith("ai_layer.knowledge_ai.memory_manager"), f"{memory_adapter_file}: {name}"


def test_learning_runtime_module_has_no_persistence_import():
    """Rule 3 belt-and-suspenders: learning_runtime.py itself (the one file with a stateful store) imports nothing beyond ai.access/ai.learning/configuration/stdlib."""
    runtime_file = _learning_dir() / "learning_runtime.py"
    allowed_prefixes = ("ai_layer.ai_service.access", "ai_layer.knowledge_ai.learning_engine", "core_layer.configuration", "dataclasses", "datetime", "typing")
    for name in _imported_names(runtime_file):
        assert name.startswith(allowed_prefixes), f"{runtime_file}: {name}"


def test_learning_record_has_no_trading_core_object_field_type():
    """Belt-and-suspenders: no dataclass field on LearningRecord may be typed as a Trading Core object -- every field is a primitive/enum only."""
    import dataclasses

    from ai_layer.knowledge_ai.learning_engine.models import LearningRecord

    allowed_type_fragments = (
        "str", "float", "int", "LearningTopic", "LearningLevel", "LearningSource", "LearningStatus", "Optional",
    )
    for f in dataclasses.fields(LearningRecord):
        type_str = str(f.type)
        assert any(fragment in type_str for fragment in allowed_type_fragments), f"LearningRecord.{f.name}: {type_str}"
