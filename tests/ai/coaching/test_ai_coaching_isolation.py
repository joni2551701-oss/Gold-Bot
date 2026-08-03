"""
Phase 66.4 TASK 8/9 — ai/coaching/ stays isolated from every Trading
Core layer and every out-of-scope package named in the brief's own
TASK 8 isolation list, plus the wider house-convention list every
prior `66.x` isolation test already enforces. Mirrors
`tests/ai/learning/test_ai_learning_isolation.py`'s own AST-based
pattern exactly.
"""

import ast
import pathlib


def _coaching_dir():
    return pathlib.Path(__file__).resolve().parents[3] / "ai" / "coaching"


def _imported_names(py_file: pathlib.Path):
    tree = ast.parse(py_file.read_text(), filename=str(py_file))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                yield node.module


def test_coaching_never_imports_trading_core_layers():
    """TASK 8: decision/, risk/, execution/, strategies/, signals/ -- zero exceptions."""
    forbidden_prefixes = ("decision", "risk", "execution", "strategies", "signals")

    for py_file in _coaching_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_coaching_never_imports_context_telegram_database():
    """TASK 8: context/, telegram/, database/ -- zero exceptions."""
    forbidden_prefixes = ("context", "telegram", "database")

    for py_file in _coaching_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_coaching_never_imports_voice_assistant_media_broadcast():
    """TASK 8: voice/, assistant/, media/, broadcast/ -- zero exceptions."""
    forbidden_prefixes = ("voice", "assistant", "media", "broadcast")

    for py_file in _coaching_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_coaching_never_imports_academy_performance_portfolio_research():
    """TASK 8: academy/, performance/, portfolio/, research/ -- none of these packages exist yet, but the import is checked regardless."""
    forbidden_prefixes = ("academy", "performance", "portfolio", "research")

    for py_file in _coaching_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_coaching_never_imports_core_package():
    """TASK 8: core/ -- zero exceptions."""
    for py_file in _coaching_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith("core."), f"{py_file}: {name}"


def test_coaching_never_imports_monitoring():
    for py_file in _coaching_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith("monitoring"), f"{py_file}: {name}"


def test_coaching_never_imports_sql_or_persistence_libraries():
    """Foundation is in-memory only -- no SQLite/Postgres/Redis client library anywhere in this package."""
    forbidden_prefixes = ("sqlite3", "psycopg2", "redis", "sqlalchemy")

    for py_file in _coaching_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_coaching_never_imports_the_top_level_learning_or_analytics_packages():
    """Same "reviewed, not reused" conclusion docs/PHASE66_4_AUDIT.md already reached for the pre-existing top-level learning/ package and analytics/."""
    for py_file in _coaching_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not (name == "learning" or name.startswith("learning.")), f"{py_file}: {name}"
            assert not name.startswith("analytics"), f"{py_file}: {name}"


def test_coaching_never_imports_ai_provider_or_llm_sdks():
    """TASK 3: 'LLM yo'q' -- no LLM SDK anywhere in this Foundation-only phase."""
    forbidden_prefixes = ("ai.providers", "ai.router", "openai", "anthropic", "google.generativeai")

    for py_file in _coaching_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"

    for py_file in _coaching_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert "requests" != name and "httpx" != name and "urllib" not in name, f"{py_file}: {name} (no network)"


def test_coaching_never_imports_ai_memory():
    forbidden_prefixes = ("ai.memory",)

    for py_file in _coaching_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_coaching_never_imports_knowledge_ai_reasoning_chart_or_trading_analyst():
    """docs/PHASE66_4_AUDIT.md: only ai.learning and ai.trade_journal are named as Coaching input sources -- Knowledge, Reasoning, Chart Intelligence, and Trading Analyst are audited but never composed here."""
    forbidden_prefixes = ("knowledge", "ai.reasoning", "ai.chart_intelligence", "ai.trading_analyst")

    for py_file in _coaching_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_coaching_never_imports_ai_content_or_ai_conversation():
    forbidden_prefixes = ("ai.content", "ai.conversation", "ai.explanation")

    for py_file in _coaching_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_learning_import_confined_to_learning_adapter():
    """TASK 4: ai.learning is only permitted in learning_adapter.py -- models.py, access.py, coaching_runtime.py, journal_adapter.py never import it."""
    adapter_file = _coaching_dir() / "learning_adapter.py"

    for py_file in _coaching_dir().rglob("*.py"):
        if py_file == adapter_file:
            continue
        for name in _imported_names(py_file):
            assert not name.startswith("ai.learning"), f"{py_file}: {name}"


def test_only_learning_adapter_imports_ai_learning():
    adapter_file = _coaching_dir() / "learning_adapter.py"
    imported = list(_imported_names(adapter_file))
    assert any(name.startswith("ai.learning") for name in imported)


def test_trade_journal_import_confined_to_journal_adapter():
    """TASK 5: ai.trade_journal is only permitted in journal_adapter.py -- models.py, access.py, coaching_runtime.py, learning_adapter.py never import it."""
    adapter_file = _coaching_dir() / "journal_adapter.py"

    for py_file in _coaching_dir().rglob("*.py"):
        if py_file == adapter_file:
            continue
        for name in _imported_names(py_file):
            assert not name.startswith("ai.trade_journal"), f"{py_file}: {name}"


def test_only_journal_adapter_imports_ai_trade_journal():
    adapter_file = _coaching_dir() / "journal_adapter.py"
    imported = list(_imported_names(adapter_file))
    assert any(name.startswith("ai.trade_journal") for name in imported)


def test_coaching_runtime_module_has_no_persistence_import():
    """Belt-and-suspenders: coaching_runtime.py itself (the one file with a stateful store) imports nothing beyond ai.access/ai.coaching/configuration/stdlib."""
    runtime_file = _coaching_dir() / "coaching_runtime.py"
    allowed_prefixes = ("ai.access", "ai.coaching", "core_layer.configuration", "dataclasses", "datetime", "typing")
    for name in _imported_names(runtime_file):
        assert name.startswith(allowed_prefixes), f"{runtime_file}: {name}"


def test_coaching_recommendation_has_no_trading_core_object_field_type():
    """Belt-and-suspenders: no dataclass field on CoachingRecommendation may be typed as a Trading Core object -- every field is a primitive/enum/Mapping only."""
    import dataclasses

    from ai.coaching.models import CoachingRecommendation

    allowed_type_fragments = (
        "str", "float", "int", "CoachingTopic", "CoachingPriority", "CoachingType", "CoachingStatus",
        "Optional", "Mapping",
    )
    for f in dataclasses.fields(CoachingRecommendation):
        type_str = str(f.type)
        assert any(fragment in type_str for fragment in allowed_type_fragments), f"CoachingRecommendation.{f.name}: {type_str}"
