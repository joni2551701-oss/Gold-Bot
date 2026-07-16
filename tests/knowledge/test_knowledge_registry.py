"""Phase 61.3 TASK 3 — knowledge/ registry: lookup, category filter, search, isolation."""

from knowledge.models import KnowledgeCategory, KnowledgeEntry
from knowledge.registry import all_entries, entries_by_category, get_entry, search


def test_all_entries_nonempty_for_every_category():
    entries = all_entries()
    assert len(entries) > 0
    categories_present = {entry.category for entry in entries}
    assert categories_present == set(KnowledgeCategory)


def test_no_duplicate_keys_across_categories():
    entries = all_entries()
    keys = [entry.key for entry in entries]
    assert len(keys) == len(set(keys))


def test_get_entry_returns_matching_entry():
    entry = get_entry("smc.bos")
    assert entry is not None
    assert entry.category == KnowledgeCategory.SMC
    assert "Break of Structure" in entry.title


def test_get_entry_returns_none_for_unknown_key():
    assert get_entry("does.not.exist") is None


def test_entries_by_category_returns_only_that_category():
    wyckoff_entries = entries_by_category(KnowledgeCategory.WYCKOFF)
    assert len(wyckoff_entries) > 0
    assert all(entry.category == KnowledgeCategory.WYCKOFF for entry in wyckoff_entries)


def test_search_matches_title_case_insensitively():
    results = search("spring")
    assert any(entry.key == "wyckoff.spring" for entry in results)

    results_upper = search("SPRING")
    assert {e.key for e in results_upper} == {e.key for e in results}


def test_search_matches_tags():
    results = search("fomo")
    assert any(entry.key == "psychology.fomo" for entry in results)


def test_search_empty_query_returns_nothing():
    assert search("") == ()
    assert search("   ") == ()


def test_search_no_match_returns_empty_tuple():
    assert search("nonexistent_query_xyz") == ()


def test_risk_category_reflects_final_gate_rule():
    risk_entries = entries_by_category(KnowledgeCategory.RISK)
    assert any("Risk Manager" in entry.title for entry in risk_entries)
    final_gate = get_entry("risk.final_gate")
    assert final_gate is not None
    assert "shortcut" in final_gate.summary.lower()


def test_faq_confirms_ai_is_advisory_only():
    entry = get_entry("faq.does_ai_place_trades")
    assert entry is not None
    assert entry.summary.strip().startswith("No.")


def test_knowledge_module_never_imports_trading_layers():
    """knowledge/ is pure static data -- no dependency on decision/risk/execution/strategies/database/telegram."""
    import ast
    import pathlib

    knowledge_dir = pathlib.Path(__file__).resolve().parents[2] / "knowledge"
    forbidden_prefixes = ("decision", "risk", "execution", "strategies", "database", "telegram")

    for py_file in knowledge_dir.glob("*.py"):
        tree = ast.parse(py_file.read_text(), filename=str(py_file))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert not alias.name.startswith(forbidden_prefixes), f"{py_file}: {alias.name}"
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    assert not node.module.startswith(forbidden_prefixes), f"{py_file}: {node.module}"


def test_knowledge_entry_is_frozen():
    entry = get_entry("smc.bos")
    try:
        entry.title = "mutated"
        assert False, "KnowledgeEntry should be frozen"
    except AttributeError:
        pass


def test_duplicate_key_detection_raises():
    from knowledge.registry import _build_index

    dup = KnowledgeEntry(key="dup", category=KnowledgeCategory.FAQ, title="A", summary="a")
    dup2 = KnowledgeEntry(key="dup", category=KnowledgeCategory.FAQ, title="B", summary="b")
    try:
        _build_index((dup, dup2))
        assert False, "expected ValueError on duplicate key"
    except ValueError:
        pass
