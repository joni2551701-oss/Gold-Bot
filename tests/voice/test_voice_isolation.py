"""
Phase 65.0 TASK 10, extended Phase 65.1 TASK 9 and Phase 65.2 TASK 4/9
— voice/ stays isolated from trading layers (Constitution Article 3)
and upstream Intelligence layers it must never reach directly
(Intelligence Dependency Principle / Phase 65.2 Rule 2: "Voice faqat
yuqori qatlam natijasini qabul qiladi").

Phase 65.1 change (documented, not a violation -- see
`docs/PHASE65_1_AUDIT.md`'s own Dependency Compliance section):
`media`/`broadcast`/`ai.conversation`/`ai.session` are allowed, but
confined to `voice/adapter.py` (type-only reads) and, as of Phase
65.2, `voice/conversation_bridge.py` (the one composition-root file
permitted to call the real `ConversationEngine`). `translation`, every
trading-layer prefix, and — new this phase, per Rule 2's explicit
"Voice -> Knowledge (X), Voice -> Reasoning (X)" — `ai.memory`,
`ai.reasoning`, `ai.explanation`, and top-level `knowledge` remain
permanently forbidden everywhere in `voice/`, with zero exemptions
(not even `conversation_bridge.py`, which only ever calls
`ConversationEngine.ask()` -- it never reaches Knowledge/Memory/
Reasoning/Explanation directly itself). Scans `voice/**/*.py`
(recursive) so `voice/provider_adapters/`, `voice/stt/`,
`voice/intents/`, `voice/session/` are all covered.
"""

import ast
import pathlib


def _voice_dir():
    return pathlib.Path(__file__).resolve().parents[2] / "voice"


def _imported_names(py_file: pathlib.Path):
    """Yields every top-level dotted import name/module referenced by an Import or ImportFrom node in py_file."""
    tree = ast.parse(py_file.read_text(), filename=str(py_file))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                yield node.module


def test_voice_package_never_imports_trading_translation_or_upstream_intelligence_layers():
    forbidden_prefixes = (
        "decision", "risk", "execution", "strategies", "signals", "database", "telegram",
        "translation", "ai.memory", "ai.reasoning", "ai.explanation", "knowledge",
    )

    for py_file in _voice_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_prefixes), f"{py_file}: {name}"


def test_voice_package_never_imports_speech_or_llm_sdks():
    """Rule 3/Rule 5 regression guard: no Speech/Microphone/Whisper SDK import, no AIService import, anywhere in voice/. Checks actual import statements only -- 'elevenlabs'/'openai' as a free-text provider name/string (e.g. VoiceProviderType.ELEVENLABS, name='elevenlabs') is legitimate metadata, not an SDK import; 'requests' is allowed (Phase 65.1's own real HTTP call convention, same library ai/providers/openai_provider.py already uses -- no SDK dependency added)."""
    forbidden_import_prefixes = ("whisper", "speech_recognition", "pyaudio", "ai.runtime")

    for py_file in _voice_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            assert not name.startswith(forbidden_import_prefixes), f"{py_file}: {name}"


def test_voice_package_media_broadcast_session_conversation_imports_confined_to_two_files():
    """Phase 65.1 TASK 9 + Phase 65.2 TASK 4 regression guard: only voice/adapter.py (type-only reads) and voice/conversation_bridge.py (the real ConversationEngine call) may import media/broadcast/ai.session/ai.conversation -- every other voice/*.py file stays exactly as isolated as Phase 65.0 left it."""
    allowed_prefixes = ("media", "broadcast", "ai.session", "ai.conversation")
    exempt_files = {_voice_dir() / "adapter.py", _voice_dir() / "conversation_bridge.py"}

    for py_file in _voice_dir().rglob("*.py"):
        if py_file in exempt_files:
            continue
        for name in _imported_names(py_file):
            assert not name.startswith(allowed_prefixes), f"{py_file}: {name}"


def test_conversation_engine_real_call_confined_to_conversation_bridge():
    """The strictest guard: the real, LLM-backed ai.conversation.conversation_engine module is imported by exactly one file in this package -- voice/adapter.py only ever reads ai.conversation.models/ai.session.conversation_state (type-only, never the engine itself)."""
    bridge_file = _voice_dir() / "conversation_bridge.py"

    for py_file in _voice_dir().rglob("*.py"):
        for name in _imported_names(py_file):
            if name.startswith("ai.conversation.conversation_engine"):
                assert py_file == bridge_file, f"{py_file}: {name} (only conversation_bridge.py may import this)"
