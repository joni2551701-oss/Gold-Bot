"""
Phase 55 — ContextMemory foundation tests.

In-memory only -- no database integration anywhere in
ai/memory/context_memory.py, matching this phase's explicit
"Database integration: QILINMASIN" scope.
"""

from ai.memory.context_memory import ContextMemory


def test_save_and_load_round_trip():
    memory = ContextMemory()
    memory.save("user-1", {"last_topic": "risk settings"})

    assert memory.load("user-1") == {"last_topic": "risk settings"}


def test_load_missing_key_returns_none():
    memory = ContextMemory()
    assert memory.load("does-not-exist") is None


def test_save_overwrites_existing_value():
    memory = ContextMemory()
    memory.save("user-1", "first")
    memory.save("user-1", "second")

    assert memory.load("user-1") == "second"


def test_clear_single_key():
    memory = ContextMemory()
    memory.save("user-1", "a")
    memory.save("user-2", "b")

    memory.clear("user-1")

    assert memory.load("user-1") is None
    assert memory.load("user-2") == "b"


def test_clear_all_keys():
    memory = ContextMemory()
    memory.save("user-1", "a")
    memory.save("user-2", "b")

    memory.clear()

    assert memory.load("user-1") is None
    assert memory.load("user-2") is None


def test_two_instances_do_not_share_state():
    """No module-level global store -- each ContextMemory() is independent."""
    first = ContextMemory()
    second = ContextMemory()

    first.save("user-1", "only in first")

    assert second.load("user-1") is None


def test_context_memory_has_no_database_import():
    """Static contract check matching this phase's 'no database integration' rule."""
    import inspect
    from ai.memory import context_memory

    source = inspect.getsource(context_memory)
    assert "import sqlite3" not in source
    assert "from database" not in source
