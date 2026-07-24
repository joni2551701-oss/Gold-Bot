"""
Phase 66.7 TASK 9 — ai/portfolio/ stays isolated from every Trading
Core layer and every out-of-scope package named in the brief's own
TASK 9 isolation list, plus the wider house-convention list every
prior `66.x` isolation test already enforces. Mirrors
`tests/ai/strategy/test_ai_strategy_isolation.py`'s own AST-based
pattern exactly.
"""

import ast
import pathlib


def _portfolio_dir():
    return pathlib.Path(__file__).resolve().parents[3] / "ai" / "portfolio"


def _imported_names(py_file: pathlib.Path):
    tree = ast.parse(py_file.read_text(), filename=str(py_file))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                yield node.module


def test_portfolio_never_imports_trading_core_layers():
    """TASK 9: decision/, risk/, execution/, signals/, strategies/ -- zero exceptions."""
    forbidden_prefixes = ("decision", "risk", "execution", "signals", "strategies")

    for py_file in _portfolio_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_portfolio_never_imports_context_telegram_database():
    """TASK 9: context/, telegram/, database/ -- zero exceptions."""
    forbidden_prefixes = ("context", "telegram", "database")

    for py_file in _portfolio_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_portfolio_never_imports_assistant_voice():
    """TASK 9: assistant/, voice/ -- zero exceptions."""
    forbidden_prefixes = ("assistant", "voice")

    for py_file in _portfolio_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_portfolio_never_imports_media_broadcast_academy_research():
    forbidden_prefixes = ("media", "broadcast", "academy", "research")

    for py_file in _portfolio_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_portfolio_never_imports_core_package():
    """TASK 9: core/ -- zero exceptions."""
    for py_file in _portfolio_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith("core."), f"{py_file}: {name}"


def test_portfolio_never_imports_monitoring():
    """Rule 1's own Trading Core list also names monitoring/."""
    for py_file in _portfolio_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith("monitoring"), f"{py_file}: {name}"


def test_portfolio_never_imports_sql_or_persistence_libraries():
    """Rule 3: in-memory only -- no SQLite/Postgres/Redis client library anywhere in this package."""
    forbidden_prefixes = ("sqlite3", "psycopg2", "redis", "sqlalchemy")

    for py_file in _portfolio_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_portfolio_never_imports_analytics_or_the_top_level_learning_package():
    """No adapter task requests analytics/ this phase -- reviewed but not reused, mirroring Phase 66.6's own precedent."""
    for py_file in _portfolio_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not (name == "learning" or name.startswith("learning.")), f"{py_file}: {name}"
            assert not name.startswith("analytics"), f"{py_file}: {name}"


def test_portfolio_never_imports_ai_provider_or_llm_sdks():
    """Rule 4: 'LLM ishlatilmaydi. GPT/Claude/Gemini/Reasoning/Inference YO'Q' -- no LLM SDK anywhere in this Foundation-only phase."""
    forbidden_prefixes = (
        "ai.providers", "ai.router", "ai.reasoning", "openai", "anthropic", "google.generativeai",
    )

    for py_file in _portfolio_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"

    for py_file in _portfolio_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert "requests" != name and "httpx" != name and "urllib" not in name, f"{py_file}: {name} (no network)"


def test_portfolio_never_imports_ai_memory():
    """TASK 6: 'ai.memory import qilish TAQIQLANADI' -- zero exceptions."""
    forbidden_prefixes = ("ai.memory",)

    for py_file in _portfolio_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_portfolio_never_imports_knowledge_chart_intelligence_or_trading_analyst():
    """docs/PHASE66_7_AUDIT.md: only ai.performance and ai.strategy are named as Portfolio input sources -- Knowledge, Chart Intelligence, Trading Analyst, and Coaching are audited but never composed here."""
    forbidden_prefixes = ("knowledge", "ai.chart_intelligence", "ai.trading_analyst", "ai.coaching")

    for py_file in _portfolio_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_portfolio_never_imports_ai_content_conversation_or_trade_journal():
    forbidden_prefixes = ("ai.content", "ai.conversation", "ai.explanation", "ai.trade_journal", "ai.learning")

    for py_file in _portfolio_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_performance_import_confined_to_performance_adapter():
    """TASK 4: ai.performance is only permitted in performance_adapter.py -- models.py, access.py, portfolio_runtime.py, strategy_adapter.py, memory_adapter.py never import it."""
    adapter_file = _portfolio_dir() / "performance_adapter.py"

    for py_file in _portfolio_dir().rglob("*.py"):
        if py_file == adapter_file:
            continue
        for name in _imported_names(py_file):
            assert not name.startswith("ai.performance"), f"{py_file}: {name}"


def test_only_performance_adapter_imports_ai_performance():
    adapter_file = _portfolio_dir() / "performance_adapter.py"
    imported = list(_imported_names(adapter_file))
    assert any(name.startswith("ai.performance") for name in imported)


def test_performance_adapter_never_imports_performance_runtime():
    """TASK 4's own instruction: 'Type-only.'"""
    adapter_file = _portfolio_dir() / "performance_adapter.py"
    imported = list(_imported_names(adapter_file))
    assert not any(name == "ai.performance.performance_runtime" for name in imported)


def test_strategy_import_confined_to_strategy_adapter():
    """TASK 5: ai.strategy is only permitted in strategy_adapter.py -- models.py, access.py, portfolio_runtime.py, performance_adapter.py, memory_adapter.py never import it."""
    adapter_file = _portfolio_dir() / "strategy_adapter.py"

    for py_file in _portfolio_dir().rglob("*.py"):
        if py_file == adapter_file:
            continue
        for name in _imported_names(py_file):
            assert not name.startswith("ai.strategy"), f"{py_file}: {name}"


def test_only_strategy_adapter_imports_ai_strategy():
    adapter_file = _portfolio_dir() / "strategy_adapter.py"
    imported = list(_imported_names(adapter_file))
    assert any(name.startswith("ai.strategy") for name in imported)


def test_strategy_adapter_never_imports_strategy_runtime():
    """TASK 5's own instruction: 'Type-only.'"""
    adapter_file = _portfolio_dir() / "strategy_adapter.py"
    imported = list(_imported_names(adapter_file))
    assert not any(name == "ai.strategy.strategy_runtime" for name in imported)


def test_portfolio_runtime_module_has_no_persistence_import():
    """Belt-and-suspenders: portfolio_runtime.py itself (the one file with a stateful store) imports nothing beyond ai.access/ai.portfolio/configuration/stdlib."""
    runtime_file = _portfolio_dir() / "portfolio_runtime.py"
    allowed_prefixes = ("ai.access", "ai.portfolio", "configuration", "dataclasses", "datetime", "typing")
    for name in _imported_names(runtime_file):
        assert name.startswith(allowed_prefixes), f"{runtime_file}: {name}"


def test_portfolio_record_has_no_trading_core_object_field_type():
    """Belt-and-suspenders: no dataclass field on PortfolioRecord may be typed as a Trading Core object -- every field is a primitive/enum/Optional only."""
    import dataclasses

    from ai.portfolio.models import PortfolioRecord

    allowed_type_fragments = ("str", "int", "PortfolioStatus", "PortfolioRiskLevel", "PortfolioHealth", "Optional")
    for f in dataclasses.fields(PortfolioRecord):
        type_str = str(f.type)
        assert any(fragment in type_str for fragment in allowed_type_fragments), f"PortfolioRecord.{f.name}: {type_str}"
