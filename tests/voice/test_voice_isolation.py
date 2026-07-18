"""
Phase 65.0 TASK 10, extended Phase 65.1 TASK 9 — voice/ stays isolated
from trading layers (Constitution Article 3) and downstream/parallel
Intelligence layers (Intelligence Dependency Principle) permanently.

Phase 65.1 change (documented, not a violation -- see
`docs/PHASE65_1_AUDIT.md`'s own Dependency Compliance section):
`media`/`broadcast`/`ai.conversation`/`ai.session` are no longer
forbidden -- `voice/adapter.py`'s three new TASK 9 functions read
those packages' types (type-only, read-only), the same posture
`voice/adapter.py` already used for `ai.content` since Phase 65.0.
`translation`, and every trading-layer prefix, remain permanently
forbidden. Scans `voice/**/*.py` (recursive) so `voice/provider_adapters/`
is covered, not just `voice/*.py`'s direct children.
"""

import ast
import pathlib


def _voice_dir():
    return pathlib.Path(__file__).resolve().parents[2] / "voice"


def test_voice_package_never_imports_trading_or_translation_layers():
    forbidden_prefixes = (
        "decision", "risk", "execution", "strategies", "signals", "database", "telegram",
        "translation",
    )

    for py_file in _voice_dir().rglob("*.py"):
        tree = ast.parse(py_file.read_text(), filename=str(py_file))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert not alias.name.startswith(forbidden_prefixes), f"{py_file}: {alias.name}"
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    assert not node.module.startswith(forbidden_prefixes), f"{py_file}: {node.module}"


def test_voice_package_never_imports_speech_or_llm_sdks():
    """Rule 3/Rule 5 regression guard: no Speech/Microphone/Whisper SDK import, no AIService import, anywhere in voice/. Checks actual import statements only -- 'elevenlabs'/'openai' as a free-text provider name/string (e.g. VoiceProviderType.ELEVENLABS, name='elevenlabs') is legitimate metadata, not an SDK import; 'requests' is allowed (Phase 65.1's own real HTTP call convention, same library ai/providers/openai_provider.py already uses -- no SDK dependency added)."""
    forbidden_import_prefixes = ("whisper", "speech_recognition", "pyaudio", "ai.runtime")

    for py_file in _voice_dir().rglob("*.py"):
        tree = ast.parse(py_file.read_text(), filename=str(py_file))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert not alias.name.startswith(forbidden_import_prefixes), f"{py_file}: {alias.name}"
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    assert not node.module.startswith(forbidden_import_prefixes), f"{py_file}: {node.module}"


def test_voice_package_media_broadcast_conversation_imports_are_type_only_adapter_reads():
    """Phase 65.1 TASK 9 regression guard: only voice/adapter.py may import media/broadcast/ai.session -- every other voice/*.py file stays exactly as isolated as Phase 65.0 left it."""
    allowed_prefixes = ("media", "broadcast", "ai.session", "ai.conversation")
    adapter_file = _voice_dir() / "adapter.py"

    for py_file in _voice_dir().rglob("*.py"):
        if py_file == adapter_file:
            continue
        tree = ast.parse(py_file.read_text(), filename=str(py_file))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert not alias.name.startswith(allowed_prefixes), f"{py_file}: {alias.name}"
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    assert not node.module.startswith(allowed_prefixes), f"{py_file}: {node.module}"
