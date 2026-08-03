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

Phase 65.4 (Personal AI Runtime Integration) deliberately widened this
one file further: `ai_layer/ai_service/assistant/runtime_adapter.py` is now the single
exception permitted to import `voice/`, `ai.conversation/`, and
`ai.memory/` (real integration, per that phase's own brief). This
file's two affected tests below exempt `runtime_adapter.py`
accordingly; `tests/assistant/runtime/test_runtime_isolation.py` holds
the finer-grained checks confining that widening to exactly one file.
`ai.reasoning/`, `ai.explanation/`, `ai.persona/`, `knowledge/`,
`ai.content/`, `media/`, `broadcast/`, and `translation/` remain
forbidden everywhere in `assistant/`, including `runtime_adapter.py`.
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
    forbidden_prefixes = ("decision_layer", "risk_layer", "execution_layer", "strategy_layer", "signal_layer", "database_layer", "platform_layer.telegram")

    for py_file in _assistant_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_assistant_package_never_imports_downstream_intelligence_layers():
    """assistant/ sits before Conversation, so it must never import voice/, ai.conversation/, or ai.memory/ -- except runtime_adapter.py (Phase 65.4's one deliberate widening). ai.reasoning/, ai.explanation/, ai.persona/, knowledge/, ai.content/, media/, broadcast/, translation/ stay forbidden everywhere, zero exemptions."""
    always_forbidden_prefixes = (
        "ai_layer.ai_engine.reasoning", "ai_layer.explanation_ai", "ai_layer.personal_ai.persona_manager", "knowledge", "ai_layer.ai_service.content", "media_layer.content_manager", "media_layer.telegram_broadcast", "media_layer.translation",
    )
    widened_prefixes = ("voice", "ai_layer.personal_ai.interaction_manager", "ai_layer.knowledge_ai.memory_manager")
    adapter_file = _assistant_dir() / "runtime_adapter.py"

    for py_file in _assistant_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(always_forbidden_prefixes), f"{py_file}: {name}"
            if py_file != adapter_file:
                assert not name.startswith(widened_prefixes), f"{py_file}: {name}"


def test_assistant_package_never_imports_ai_provider_or_llm_sdks():
    """No direct AI provider call, no LLM SDK, anywhere in assistant/ -- this package (including runtime_adapter.py) never reaches ai.providers/ai.router/a raw SDK; the one real LLM-backed call it may reach is ConversationEngine.ask(), one layer removed."""
    forbidden_prefixes = ("ai_layer.ai_engine.providers", "ai_layer.ai_coordinator", "openai", "anthropic", "google.generativeai")

    for py_file in _assistant_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_assistant_package_only_reads_ai_access_permissions_type_outside_runtime_adapter():
    """Every file except runtime_adapter.py keeps Phase 65.3's rule: the only ai.* import is ai.access.permissions (AIRole) -- never ai.access.access_control (the Capability matrix TASK 7 deliberately does not reuse)."""
    adapter_file = _assistant_dir() / "runtime_adapter.py"

    for py_file in _assistant_dir().rglob("*.py"):
        if py_file == adapter_file:
            continue
        for name in _imported_names(py_file):
            if name.startswith("ai."):
                assert name == "ai_layer.ai_service.access.permissions", f"{py_file}: unexpected ai.* import {name}"
