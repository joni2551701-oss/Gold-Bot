"""
Phase 65.4 TASK 9 — assistant/ isolation, updated for the one
deliberate widening this phase introduces: `runtime_adapter.py` is now
the single file in `assistant/` permitted to import
`ai.conversation.conversation_engine`, `ai.intelligence_runtime`,
`ai.memory.memory_runtime`/`ai.memory.models`, and
`voice.runtime`/`voice.models`. Every other file in `assistant/`
(`identity.py`, `identity_registry.py`, `identity_manager.py`,
`models.py`, `access.py`, `assistant_manager.py`,
`conversation_adapter.py`) must still import nothing downstream at
all -- Phase 65.3's own posture, unchanged. Mirrors
`tests/voice/test_voice_isolation.py`'s own AST-based pattern.
"""

import ast
import pathlib


def _assistant_dir():
    return pathlib.Path(__file__).resolve().parents[3] / "assistant"


def _imported_names(py_file: pathlib.Path):
    tree = ast.parse(py_file.read_text(), filename=str(py_file))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                yield node.module


def test_assistant_package_still_never_imports_trading_telegram_or_database_layers():
    """Rule 2 (Trading Core ZERO DIFF) -- unaffected by this phase's widening, zero exemptions including runtime_adapter.py."""
    forbidden_prefixes = ("decision", "risk", "execution", "strategies", "signals", "database", "telegram")

    for py_file in _assistant_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_downstream_intelligence_imports_confined_to_runtime_adapter():
    """The strict rule this phase updates: voice/, ai.conversation/, ai.memory/, ai.intelligence_runtime are now permitted, but only in runtime_adapter.py -- every other file keeps zero downstream imports."""
    widened_prefixes = ("voice", "ai.conversation", "ai.memory", "ai.intelligence_runtime")
    adapter_file = _assistant_dir() / "runtime_adapter.py"

    for py_file in _assistant_dir().rglob("*.py"):
        if py_file == adapter_file:
            continue
        for name in _imported_names(py_file):
            assert not name.startswith(widened_prefixes), f"{py_file}: {name} (only runtime_adapter.py may import this)"


def test_still_permanently_forbidden_layers_even_in_runtime_adapter():
    """ai.reasoning, ai.explanation, ai.persona, knowledge, ai.content, media, broadcast, translation stay forbidden everywhere in assistant/ -- including runtime_adapter.py, which reaches Reasoning/Explanation/Content/Media/Broadcast only indirectly through IntelligenceRuntime.run()."""
    forbidden_prefixes = (
        "ai.reasoning", "ai.explanation", "ai.persona", "knowledge",
        "ai.content", "media", "broadcast", "translation",
    )

    for py_file in _assistant_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_ai_conversation_engine_real_call_confined_to_runtime_adapter():
    """The strictest guard: the real ai.conversation.conversation_engine module is imported by exactly one file in assistant/ -- runtime_adapter.py."""
    adapter_file = _assistant_dir() / "runtime_adapter.py"

    for py_file in _assistant_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            if name.startswith("ai.conversation.conversation_engine"):
                assert py_file == adapter_file, f"{py_file}: {name} (only runtime_adapter.py may import this)"


def test_only_permitted_ai_access_import_outside_runtime_adapter():
    """Every file except runtime_adapter.py keeps the Phase 65.3 rule: the only ai.* import allowed is ai.access.permissions."""
    adapter_file = _assistant_dir() / "runtime_adapter.py"

    for py_file in _assistant_dir().rglob("*.py"):
        if py_file == adapter_file:
            continue
        for name in _imported_names(py_file):
            if name.startswith("ai."):
                assert name == "ai.access.permissions", f"{py_file}: unexpected ai.* import {name}"
