"""
Phase 66.5 TASK 8/9 — ai/performance/ stays isolated from every Trading
Core layer and every out-of-scope package named in the brief's own
isolation list, plus the wider house-convention list every prior
`66.x` isolation test already enforces. Mirrors
`tests/ai/coaching/test_ai_coaching_isolation.py`'s own AST-based
pattern exactly.
"""

import ast
import pathlib


def _performance_dir():
    return pathlib.Path(__file__).resolve().parents[3] / "ai" / "performance"


def _imported_names(py_file: pathlib.Path):
    tree = ast.parse(py_file.read_text(), filename=str(py_file))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                yield node.module


def test_performance_never_imports_trading_core_layers():
    """TASK 8: decision/, risk/, execution/, strategies/, signals/ -- zero exceptions."""
    forbidden_prefixes = ("decision", "risk", "execution", "strategies", "signals")

    for py_file in _performance_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_performance_never_imports_context_telegram_database():
    """TASK 8: context/, telegram/, database/ -- zero exceptions."""
    forbidden_prefixes = ("context", "telegram", "database")

    for py_file in _performance_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_performance_never_imports_voice_assistant_media_broadcast():
    """TASK 8: voice/, assistant/, media/, broadcast/ -- zero exceptions."""
    forbidden_prefixes = ("voice", "assistant", "media", "broadcast")

    for py_file in _performance_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_performance_never_imports_academy_portfolio_research():
    """TASK 8: academy/, portfolio/, research/ -- none of these packages exist yet, but the import is checked regardless."""
    forbidden_prefixes = ("academy", "portfolio", "research")

    for py_file in _performance_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_performance_never_imports_core_package():
    """TASK 8: core/ -- zero exceptions."""
    for py_file in _performance_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith("core."), f"{py_file}: {name}"


def test_performance_never_imports_monitoring():
    for py_file in _performance_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith("monitoring"), f"{py_file}: {name}"


def test_performance_never_imports_sql_or_persistence_libraries():
    """Foundation is in-memory only -- no SQLite/Postgres/Redis client library anywhere in this package."""
    forbidden_prefixes = ("sqlite3", "psycopg2", "redis", "sqlalchemy")

    for py_file in _performance_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_performance_never_imports_the_top_level_learning_or_analytics_packages_except_analytics_adapter():
    """analytics/ is only permitted in analytics_adapter.py (TASK 6's own directly-reusable primitive); the top-level learning/ package is never imported anywhere in this package."""
    adapter_file = _performance_dir() / "analytics_adapter.py"

    for py_file in _performance_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not (name == "learning" or name.startswith("learning.")), f"{py_file}: {name}"
            if py_file != adapter_file:
                assert not name.startswith("analytics"), f"{py_file}: {name}"


def test_performance_never_imports_ai_provider_or_llm_sdks():
    """TASK 3: 'GPT chaqirmaydi' -- no LLM SDK anywhere in this Foundation-only phase."""
    forbidden_prefixes = ("ai.providers", "ai.router", "openai", "anthropic", "google.generativeai")

    for py_file in _performance_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"

    for py_file in _performance_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert "requests" != name and "httpx" != name and "urllib" not in name, f"{py_file}: {name} (no network)"


def test_performance_never_imports_ai_memory():
    """TASK 9: 'ai.memory import qilinmaydi' -- zero exceptions."""
    forbidden_prefixes = ("ai.memory",)

    for py_file in _performance_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_performance_never_imports_knowledge_ai_reasoning_chart_or_trading_analyst():
    """docs/PHASE66_5_AUDIT.md: only ai.trade_journal and ai.coaching are named as Performance input/output sources -- Knowledge, Reasoning, Chart Intelligence, and Trading Analyst are never composed here."""
    forbidden_prefixes = ("knowledge", "ai.reasoning", "ai.chart_intelligence", "ai.trading_analyst")

    for py_file in _performance_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_performance_never_imports_ai_content_or_ai_conversation():
    forbidden_prefixes = ("ai.content", "ai.conversation", "ai.explanation")

    for py_file in _performance_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_performance_never_imports_ai_coaching_models_or_runtime():
    """coaching_adapter.py returns a plain untyped Dict -- it never imports ai.coaching.models or ai.coaching.coaching_runtime (Rule: 'Faqat structure')."""
    for py_file in _performance_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith("ai.coaching"), f"{py_file}: {name}"


def test_trade_journal_import_confined_to_journal_adapter():
    """TASK 4: ai.trade_journal is only permitted in journal_adapter.py -- models.py, access.py, performance_runtime.py, coaching_adapter.py, analytics_adapter.py, memory_adapter.py never import it."""
    adapter_file = _performance_dir() / "journal_adapter.py"

    for py_file in _performance_dir().rglob("*.py"):
        if py_file == adapter_file:
            continue
        for name in _imported_names(py_file):
            assert not name.startswith("ai.trade_journal"), f"{py_file}: {name}"


def test_only_journal_adapter_imports_ai_trade_journal():
    adapter_file = _performance_dir() / "journal_adapter.py"
    imported = list(_imported_names(adapter_file))
    assert any(name.startswith("ai.trade_journal") for name in imported)


def test_performance_runtime_module_has_no_persistence_import():
    """Belt-and-suspenders: performance_runtime.py itself (the one file with a stateful store) imports nothing beyond ai.access/ai.performance/configuration/stdlib."""
    runtime_file = _performance_dir() / "performance_runtime.py"
    allowed_prefixes = ("ai.access", "ai.performance", "goldbot.core_layer.configuration", "dataclasses", "datetime", "typing")
    for name in _imported_names(runtime_file):
        assert name.startswith(allowed_prefixes), f"{runtime_file}: {name}"


def test_performance_record_has_no_trading_core_object_field_type():
    """Belt-and-suspenders: no dataclass field on PerformanceRecord may be typed as a Trading Core object -- every field is a primitive/Optional only."""
    import dataclasses

    from ai.performance.models import PerformanceRecord

    allowed_type_fragments = ("str", "float", "bool", "Optional")
    for f in dataclasses.fields(PerformanceRecord):
        type_str = str(f.type)
        assert any(fragment in type_str for fragment in allowed_type_fragments), f"PerformanceRecord.{f.name}: {type_str}"
