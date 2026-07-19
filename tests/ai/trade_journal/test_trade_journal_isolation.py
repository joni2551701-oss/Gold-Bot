"""
Phase 66.2 TASK 9 — ai/trade_journal/ stays isolated from every
Trading Core layer (Constitution Article 3, Rule 2 "READ ONLY", Rule 3
"database emas"). Mirrors
`tests/ai/chart_intelligence/test_chart_intelligence_isolation.py`'s
own AST-based pattern exactly.
"""

import ast
import pathlib


def _trade_journal_dir():
    return pathlib.Path(__file__).resolve().parents[3] / "ai" / "trade_journal"


def _imported_names(py_file: pathlib.Path):
    tree = ast.parse(py_file.read_text(), filename=str(py_file))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                yield node.module


def test_trade_journal_never_imports_trading_core_layers():
    """Rule 1/2: decision/, risk/, execution/, strategies/, signals/, context/, monitoring/ -- zero exceptions."""
    forbidden_prefixes = (
        "decision", "risk", "execution", "strategies", "signals", "context", "monitoring",
    )

    for py_file in _trade_journal_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_trade_journal_never_imports_telegram_or_database():
    """Rule 3: Journal is a Foundation, not a database -- no telegram/ or database/ import anywhere."""
    forbidden_prefixes = ("telegram", "database")

    for py_file in _trade_journal_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_trade_journal_never_imports_sql_or_persistence_libraries():
    """Rule 3: no SQLite/Postgres/Redis client library anywhere in this package."""
    forbidden_prefixes = ("sqlite3", "psycopg2", "redis", "sqlalchemy")

    for py_file in _trade_journal_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_trade_journal_never_imports_ai_provider_or_llm_sdks():
    forbidden_prefixes = ("ai.providers", "ai.router", "openai", "anthropic", "google.generativeai")

    for py_file in _trade_journal_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_trade_journal_never_imports_assistant_or_voice():
    forbidden_prefixes = ("assistant", "voice")

    for py_file in _trade_journal_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_trade_journal_never_imports_ai_memory():
    """TASK 6: Memory o'zgarmaydi -- ai.memory is never imported anywhere in this package, not even memory_adapter.py."""
    for py_file in _trade_journal_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith("ai.memory"), f"{py_file}: {name}"


def test_trade_journal_never_imports_knowledge_or_reasoning():
    forbidden_prefixes = ("knowledge", "ai.reasoning")

    for py_file in _trade_journal_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_trade_journal_never_imports_ai_content_media_broadcast():
    """This phase never composes Content/Media/Broadcast -- distinct from ai/trading_analyst/ and ai/chart_intelligence/, which do."""
    forbidden_prefixes = ("ai.content", "media", "broadcast")

    for py_file in _trade_journal_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_trade_journal_never_imports_core_package():
    for py_file in _trade_journal_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith("core."), f"{py_file}: {name}"


def test_trading_analyst_and_chart_intelligence_imports_confined_to_adapter():
    """TASK 5: ai.trading_analyst and ai.chart_intelligence are only permitted in trading_analyst_adapter.py."""
    adapter_file = _trade_journal_dir() / "trading_analyst_adapter.py"
    widened_prefixes = ("ai.trading_analyst", "ai.chart_intelligence")

    for py_file in _trade_journal_dir().rglob("*.py"):
        if py_file == adapter_file:
            continue
        for name in _imported_names(py_file):
            assert not name.startswith(widened_prefixes), f"{py_file}: {name}"


def test_only_trading_analyst_adapter_imports_upstream_packages():
    adapter_file = _trade_journal_dir() / "trading_analyst_adapter.py"
    imported = list(_imported_names(adapter_file))
    assert any(name.startswith("ai.trading_analyst") for name in imported)
    assert any(name.startswith("ai.chart_intelligence") for name in imported)


def test_trade_journal_entry_has_no_trading_core_object_field_type():
    """Belt-and-suspenders: no dataclass field on TradeJournalEntry/ReplayContext may be typed as a Trading Core object."""
    import dataclasses

    from ai.trade_journal.models import ReplayContext, TradeJournalEntry

    allowed_type_fragments = ("str", "float", "int", "Sequence", "Optional")
    for model in (TradeJournalEntry, ReplayContext):
        for f in dataclasses.fields(model):
            type_str = str(f.type)
            assert any(fragment in type_str for fragment in allowed_type_fragments), f"{model.__name__}.{f.name}: {type_str}"


def test_trade_journal_runtime_module_has_no_persistence_import():
    """Rule 3 belt-and-suspenders: journal_runtime.py itself (the one file with a stateful store) imports nothing beyond ai.access/ai.trade_journal/configuration/stdlib."""
    runtime_file = _trade_journal_dir() / "journal_runtime.py"
    allowed_prefixes = ("ai.access", "ai.trade_journal", "configuration", "dataclasses", "datetime", "typing")
    for name in _imported_names(runtime_file):
        assert name.startswith(allowed_prefixes), f"{runtime_file}: {name}"

