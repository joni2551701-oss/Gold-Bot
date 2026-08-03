"""
Voice Layer — Voice Providers (Phase 65.0, TASK 6).

Static catalog, same "descriptor list + build function" pattern
`media_layer/content_manager/media_registry.py` and `media_layer/telegram_broadcast/provider_manager.py` already
established (Rule 8 — reuse the pattern). No network client, no SDK
import (Rule 3). Consolidated into one file rather than the brief's
literal `providers/openai.py`/`elevenlabs.py`/`local.py`/`custom.py`
layout -- see `docs/PHASE65_0_AUDIT.md`'s own file-layout resolution.

`VoiceProviderType.OPENAI`'s descriptor here is unrelated to
`ai/providers/openai_provider.py`'s `OpenAIProvider` -- that is a
real, `AIService`-calling LLM/chat provider; this is a non-connected
voice-synthesis capability descriptor. Different package, different
concern, no shared code.
"""

from typing import List

from ai_layer.voice_ai.models import VoiceProvider, VoiceProviderType


def build_voice_provider_registry() -> List[VoiceProvider]:
    """Never raises. One descriptor per VoiceProviderType -- the fixed catalog this phase, matching Rule 3's four named backend types exactly, no more, no fewer."""
    return [
        VoiceProvider(
            provider_type=VoiceProviderType.OPENAI, name="openai",
            supports_stream=True, supports_clone=False, supports_emotion=False, supports_ssml=True,
        ),
        VoiceProvider(
            provider_type=VoiceProviderType.ELEVENLABS, name="elevenlabs",
            supports_stream=True, supports_clone=True, supports_emotion=True, supports_ssml=True,
        ),
        VoiceProvider(
            provider_type=VoiceProviderType.LOCAL, name="local",
            supports_stream=False, supports_clone=False, supports_emotion=False, supports_ssml=False,
        ),
        VoiceProvider(
            provider_type=VoiceProviderType.CUSTOM, name="custom",
            supports_stream=False, supports_clone=False, supports_emotion=False, supports_ssml=False,
        ),
    ]
