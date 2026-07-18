"""Phase 65.0 TASK 7 — voice/adapter.py: content_result_to_voice_request()."""

from ai.content.content_schema import ContentResult
from voice.adapter import content_result_to_voice_request
from voice.manager import VoiceManager
from voice.models import VoiceProviderType, VoiceSettings


def _accepted_result(**overrides):
    defaults = dict(
        accepted=True, content_type="AI_MARKET_REPORT", title="Gold Report",
        body="Bullish on H1.", reason="ok", generated_at="2026-01-01T00:00:00+00:00",
    )
    defaults.update(overrides)
    return ContentResult(**defaults)


def test_content_result_to_voice_request_reads_body_and_content_type():
    manager = VoiceManager()
    result = _accepted_result()

    request = content_result_to_voice_request(result, manager, "Senior", VoiceProviderType.OPENAI)

    assert request is not None
    assert request.text == "Bullish on H1."
    assert request.id == "AI_MARKET_REPORT"
    assert request.profile_name == "Senior"
    assert request.provider_type == VoiceProviderType.OPENAI
    assert request.requested_at == "2026-01-01T00:00:00+00:00"


def test_content_result_to_voice_request_returns_none_for_rejected_result():
    manager = VoiceManager()
    result = ContentResult(
        accepted=False, content_type="AI_MARKET_REPORT", title="Gold Report",
        body=None, reason="rejected", generated_at="2026-01-01T00:00:00+00:00",
    )
    assert content_result_to_voice_request(result, manager, "Senior", VoiceProviderType.OPENAI) is None


def test_content_result_to_voice_request_returns_none_for_accepted_but_empty_body():
    manager = VoiceManager()
    result = _accepted_result(body=None)
    assert content_result_to_voice_request(result, manager, "Senior", VoiceProviderType.OPENAI) is None


def test_content_result_to_voice_request_returns_none_for_unknown_profile():
    manager = VoiceManager()
    result = _accepted_result()
    assert content_result_to_voice_request(result, manager, "Unknown", VoiceProviderType.OPENAI) is None


def test_content_result_to_voice_request_default_settings():
    manager = VoiceManager()
    result = _accepted_result()
    request = content_result_to_voice_request(result, manager, "Senior", VoiceProviderType.OPENAI)
    assert request.settings == VoiceSettings()


def test_content_result_to_voice_request_accepts_explicit_settings():
    manager = VoiceManager()
    result = _accepted_result()
    settings = VoiceSettings(language="fr", speed=1.5)
    request = content_result_to_voice_request(result, manager, "Senior", VoiceProviderType.OPENAI, settings=settings)
    assert request.settings == settings
