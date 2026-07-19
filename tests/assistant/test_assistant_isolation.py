"""
Phase 65.3 TASK 10 — assistant/ stays isolated from every downstream
Intelligence layer and every trading/telegram/database layer
(Constitution Article 3, Intelligence Dependency Principle applied one
layer earlier than it has ever been applied before -- see
`docs/PHASE65_3_AUDIT.md`'s "core architectural resolution" section).
`assistant/` sits *before* Conversation in the brief's own diagram, so
it may depend on nothing after it: not `voice/`, not
`ai.conversation/`, not `ai.memory/`, not `ai.reasoning/`, not
`ai.explanation/`, not `ai.persona/` (Rule 3: Persona Protection), not
`knowledge/`, not `ai.content/`, not `media/`, not `broadcast/`, not
`translation/` -- with zero exemptions, mirroring
`tests/voice/test_voice_isolation.py`'s own AST-based pattern exactly.
"""

import ast
import pathlib


def _assistant_dir():
    return pathlib.Path(__file__).resolve().parents[2] / "assistant"


def _imported_names(py_file: pathlib.Path):
    tree = ast.parse(py_file.read_text(), filename=str(py_file))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                yield node.module


def test_assistant_package_never_imports_trading_telegram_or_database_layers():
    forbidden_prefixes = ("decision", "risk", "execution", "strategies", "signals", "database", "telegram")

    for py_file in _assistant_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_assistant_package_never_imports_downstream_intelligence_layers():
    """The strict rule this phase adds: assistant/ sits before Conversation, so it must never import voice/, ai.conversation/, ai.memory/, ai.reasoning/, ai.explanation/, ai.persona/, knowledge/, ai.content/, media/, broadcast/, or translation/ -- zero exemptions, not even conversation_adapter.py (which produces plain dicts/strings only)."""
    forbidden_prefixes = (
        "voice", "ai.conversation", "ai.memory", "ai.reasoning", "ai.explanation",
        "ai.persona", "knowledge", "ai.content", "media", "broadcast", "translation",
    )

    for py_file in _assistant_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_assistant_package_never_imports_ai_runtime_or_llm_sdks():
    """No AI provider call, no LLM SDK, anywhere in assistant/ -- this package is pure identity/profile metadata, same posture ai/persona/ already commits to."""
    forbidden_prefixes = ("ai.runtime", "ai.providers", "ai.router", "openai", "anthropic", "google.generativeai")

    for py_file in _assistant_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_assistant_package_only_reads_ai_access_permissions_type():
    """The one permitted ai.* import across this whole package is ai.access.permissions (AIRole -- an access-control type, orthogonal to the content chain) -- never ai.access.access_control (the Capability matrix TASK 7 deliberately does not reuse)."""
    for py_file in _assistant_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            if name.startswith("ai."):
                assert name == "ai.access.permissions", f"{py_file}: unexpected ai.* import {name}"
