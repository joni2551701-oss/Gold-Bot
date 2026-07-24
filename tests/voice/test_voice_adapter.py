"""Phase 65.0 TASK 7 — voice/adapter.py: content_result_to_voice_request(). Extended Phase 65.1 TASK 9 — media/broadcast/conversation integration points."""

from datetime import datetime, timezone

from ai.content.content_schema import ContentResult
from ai.content.content_types import ContentType
from ai.session.conversation_state import ConversationTurn
from broadcast.models import BroadcastAsset, BroadcastStatus
from media.media_types import MediaType
from media.models import MediaAsset, MediaAssetStatus
from voice.adapter import (
    broadcast_asset_to_voice_request,
    content_result_to_voice_request,
    conversation_turn_to_voice_request,
    media_asset_to_voice_request,
)
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


# --- Phase 65.1 TASK 9: media_asset_to_voice_request() ---

def _ready_media_asset(**overrides):
    defaults = dict(
        id="m1", content_id="c1", media_type=MediaType.TEXT,
        status=MediaAssetStatus.READY, title="Gold Report", description="Bullish setup on gold.",
        created_at="2026-01-01T00:00:00+00:00",
    )
    defaults.update(overrides)
    return MediaAsset(**defaults)


def test_media_asset_to_voice_request_reads_description():
    manager = VoiceManager()
    asset = _ready_media_asset()
    request = media_asset_to_voice_request(asset, manager, "Senior", VoiceProviderType.OPENAI)
    assert request is not None
    assert request.text == "Bullish setup on gold."
    assert request.id == "m1"
    assert request.requested_at == "2026-01-01T00:00:00+00:00"


def test_media_asset_to_voice_request_returns_none_for_non_ready_asset():
    manager = VoiceManager()
    asset = _ready_media_asset(status=MediaAssetStatus.PENDING)
    assert media_asset_to_voice_request(asset, manager, "Senior", VoiceProviderType.OPENAI) is None


def test_media_asset_to_voice_request_returns_none_for_empty_description():
    manager = VoiceManager()
    asset = _ready_media_asset(description="")
    assert media_asset_to_voice_request(asset, manager, "Senior", VoiceProviderType.OPENAI) is None


def test_media_asset_to_voice_request_returns_none_for_unknown_profile():
    manager = VoiceManager()
    asset = _ready_media_asset()
    assert media_asset_to_voice_request(asset, manager, "Unknown", VoiceProviderType.OPENAI) is None


# --- Phase 65.1 TASK 9: broadcast_asset_to_voice_request() ---

def _ready_broadcast_asset(**overrides):
    defaults = dict(
        id="b1", content_id="c1", media_id="m1", broadcast_type=ContentType.MARKET_UPDATE,
        status=BroadcastStatus.READY, created_at="2026-01-01T00:00:00+00:00",
    )
    defaults.update(overrides)
    return BroadcastAsset(**defaults)


def test_broadcast_asset_to_voice_request_uses_explicit_text_parameter():
    manager = VoiceManager()
    asset = _ready_broadcast_asset()
    request = broadcast_asset_to_voice_request(asset, "Weekly gold report narration.", manager, "Seniorita", VoiceProviderType.ELEVENLABS)
    assert request is not None
    assert request.text == "Weekly gold report narration."
    assert request.id == "b1"


def test_broadcast_asset_to_voice_request_accepts_published_status():
    manager = VoiceManager()
    asset = _ready_broadcast_asset(status=BroadcastStatus.PUBLISHED)
    request = broadcast_asset_to_voice_request(asset, "text", manager, "Seniorita", VoiceProviderType.ELEVENLABS)
    assert request is not None


def test_broadcast_asset_to_voice_request_returns_none_for_draft_status():
    manager = VoiceManager()
    asset = _ready_broadcast_asset(status=BroadcastStatus.DRAFT)
    assert broadcast_asset_to_voice_request(asset, "text", manager, "Seniorita", VoiceProviderType.ELEVENLABS) is None


def test_broadcast_asset_to_voice_request_returns_none_for_empty_text():
    manager = VoiceManager()
    asset = _ready_broadcast_asset()
    assert broadcast_asset_to_voice_request(asset, "", manager, "Seniorita", VoiceProviderType.ELEVENLABS) is None


# --- Phase 65.1 TASK 9: conversation_turn_to_voice_request() ---

def _assistant_turn(**overrides):
    defaults = dict(role="assistant", content="Here is the market update.", at=datetime(2026, 1, 1, tzinfo=timezone.utc))
    defaults.update(overrides)
    return ConversationTurn(**defaults)


def test_conversation_turn_to_voice_request_reads_assistant_content():
    manager = VoiceManager()
    turn = _assistant_turn()
    request = conversation_turn_to_voice_request(turn, manager, "Senior", VoiceProviderType.OPENAI)
    assert request is not None
    assert request.text == "Here is the market update."
    assert request.id == "2026-01-01T00:00:00+00:00"


def test_conversation_turn_to_voice_request_returns_none_for_user_role():
    manager = VoiceManager()
    turn = _assistant_turn(role="user", content="what about gold?")
    assert conversation_turn_to_voice_request(turn, manager, "Senior", VoiceProviderType.OPENAI) is None


def test_conversation_turn_to_voice_request_returns_none_for_empty_content():
    manager = VoiceManager()
    turn = _assistant_turn(content="")
    assert conversation_turn_to_voice_request(turn, manager, "Senior", VoiceProviderType.OPENAI) is None


def test_conversation_turn_to_voice_request_returns_none_for_unknown_profile():
    manager = VoiceManager()
    turn = _assistant_turn()
    assert conversation_turn_to_voice_request(turn, manager, "Unknown", VoiceProviderType.OPENAI) is None
