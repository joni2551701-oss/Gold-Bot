"""Phase 63.2 TASK 4/8 — ai_layer/knowledge_ai/knowledge_base/knowledge_manager.py: KnowledgeManager (lookup/search/by_category/filter/list_all), dependency injection, isolation."""

from ai_layer.knowledge_ai.knowledge_base.knowledge_manager import KnowledgeManager
from ai_layer.knowledge_ai.knowledge_base.models import KnowledgeCategory, KnowledgeEntry
from ai_layer.knowledge_ai.knowledge_base.registry import all_entries


def test_lookup_returns_matching_entry():
    manager = KnowledgeManager()
    entry = manager.lookup("smc.bos")
    assert entry is not None
    assert entry.category == KnowledgeCategory.SMC


def test_lookup_returns_none_for_unknown_key():
    manager = KnowledgeManager()
    assert manager.lookup("does.not.exist") is None


def test_search_matches_title_case_insensitively():
    manager = KnowledgeManager()
    results = manager.search("spring")
    assert any(entry.key == "wyckoff.spring" for entry in results)
    results_upper = manager.search("SPRING")
    assert {e.key for e in results_upper} == {e.key for e in results}


def test_search_empty_query_returns_nothing():
    manager = KnowledgeManager()
    assert manager.search("") == ()
    assert manager.search("   ") == ()


def test_by_category_returns_only_that_category():
    manager = KnowledgeManager()
    wyckoff_entries = manager.by_category(KnowledgeCategory.WYCKOFF)
    assert len(wyckoff_entries) > 0
    assert all(entry.category == KnowledgeCategory.WYCKOFF for entry in wyckoff_entries)


def test_filter_applies_arbitrary_predicate():
    manager = KnowledgeManager()
    tagged = manager.filter(lambda entry: "fvg" in entry.tags)
    assert any(entry.key == "smc.fair_value_gap" for entry in tagged)


def test_list_all_returns_every_entry():
    manager = KnowledgeManager()
    assert len(manager.list_all()) == len(all_entries())


def test_default_entries_match_the_real_registry():
    manager = KnowledgeManager()
    assert manager.list_all() == list(all_entries())


def test_injected_entries_are_isolated_from_the_real_registry():
    """Dependency-injectable, same convention as every other Phase 61.x/63.x manager -- a test never needs the real static registry."""
    fake_entry = KnowledgeEntry(
        key="fake.entry",
        category=KnowledgeCategory.FAQ,
        title="Fake",
        summary="A fake entry for isolation testing.",
    )
    manager = KnowledgeManager(entries=[fake_entry])

    assert manager.list_all() == [fake_entry]
    assert manager.lookup("smc.bos") is None
    assert manager.lookup("fake.entry") is fake_entry


def test_knowledge_manager_never_imports_trading_layers():
    """knowledge/ stays pure static data even with a Manager added -- no dependency on decision/risk/execution/strategies/database/telegram."""
    import ast
    import pathlib

    manager_file = pathlib.Path(__file__).resolve().parents[2] / "ai_layer" / "knowledge_ai" / "knowledge_base" / "knowledge_manager.py"
    forbidden_prefixes = ("decision_layer", "risk_layer", "execution_layer", "strategy_layer", "database_layer", "platform_layer.telegram")

    tree = ast.parse(manager_file.read_text(), filename=str(manager_file))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert not alias.name.startswith(forbidden_prefixes), f"{manager_file}: {alias.name}"
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                assert not node.module.startswith(forbidden_prefixes), f"{manager_file}: {node.module}"
