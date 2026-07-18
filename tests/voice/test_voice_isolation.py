"""Phase 65.0 TASK 10 — voice/ stays isolated from trading layers (Constitution Article 3) and downstream/parallel Intelligence layers (Intelligence Dependency Principle). Per docs/PHASE65_0_AUDIT.md's own dependency-compliance decision, voice/ also does not import media/ or broadcast/ this phase."""

import ast
import pathlib


def _voice_dir():
    return pathlib.Path(__file__).resolve().parents[2] / "voice"


def test_voice_package_never_imports_trading_or_downstream_intelligence_layers():
    forbidden_prefixes = (
        "decision", "risk", "execution", "strategies", "signals", "database", "telegram",
        "broadcast", "translation", "media",
    )

    for py_file in _voice_dir().glob("*.py"):
        tree = ast.parse(py_file.read_text(), filename=str(py_file))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert not alias.name.startswith(forbidden_prefixes), f"{py_file}: {alias.name}"
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    assert not node.module.startswith(forbidden_prefixes), f"{py_file}: {node.module}"


def test_voice_package_never_imports_speech_or_llm_sdks():
    """Rule 3/Rule 5 regression guard: no Speech/Microphone/Whisper/OpenAI-TTS/ElevenLabs SDK import, no AIService import, anywhere in voice/. Checks actual import statements only -- 'elevenlabs'/'openai' as a free-text provider name/string (e.g. VoiceProviderType.ELEVENLABS, name='elevenlabs') is legitimate metadata, not an SDK import."""
    forbidden_import_prefixes = ("whisper", "speech_recognition", "pyaudio", "elevenlabs", "ai.runtime")

    for py_file in _voice_dir().glob("*.py"):
        tree = ast.parse(py_file.read_text(), filename=str(py_file))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert not alias.name.startswith(forbidden_import_prefixes), f"{py_file}: {alias.name}"
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    assert not node.module.startswith(forbidden_import_prefixes), f"{py_file}: {node.module}"
