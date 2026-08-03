"""Phase 63.8 TASK 1 — media_layer/telegram_broadcast/models.py: BroadcastStatus/BroadcastAsset/BroadcastTriggerType, and ai.content_types.ContentType.LIVE_ANALYSIS."""

from ai.content_types import ContentType
from media_layer.telegram_broadcast.models import (
    BroadcastAsset,
    BroadcastStatus,
    BroadcastTrigger,
    BroadcastTriggerType,
)


def _asset(**overrides):
    defaults = dict(
        id="b1", content_id="AI_MARKET_REPORT", media_id="m1",
        broadcast_type=ContentType.MARKET_UPDATE, status=BroadcastStatus.DRAFT,
    )
    defaults.update(overrides)
    return BroadcastAsset(**defaults)


def test_broadcast_asset_defaults():
    asset = _asset()
    assert asset.persona_name is None
    assert asset.metadata == {}
    assert asset.created_at == ""


def test_broadcast_asset_accepts_explicit_values():
    asset = _asset(persona_name="Senior Trading AI", metadata={"lang": "en"}, created_at="2026-01-01T00:00:00+00:00")
    assert asset.persona_name == "Senior Trading AI"
    assert asset.metadata == {"lang": "en"}
    assert asset.created_at == "2026-01-01T00:00:00+00:00"


def test_broadcast_asset_is_frozen():
    asset = _asset()
    try:
        asset.status = BroadcastStatus.READY
        assert False, "BroadcastAsset should be frozen"
    except AttributeError:
        pass


def test_broadcast_asset_to_dict_is_json_serializable_shape():
    asset = _asset(persona_name="Senior Trading AI", metadata={"lang": "en"}, created_at="2026-01-01T00:00:00+00:00")
    d = asset.to_dict()
    assert d == {
        "id": "b1", "content_id": "AI_MARKET_REPORT", "media_id": "m1",
        "broadcast_type": "MARKET_UPDATE", "status": "DRAFT",
        "persona_name": "Senior Trading AI", "metadata": {"lang": "en"},
        "created_at": "2026-01-01T00:00:00+00:00",
    }


def test_broadcast_status_has_five_lifecycle_values():
    assert {s.value for s in BroadcastStatus} == {"DRAFT", "READY", "PUBLISHED", "FAILED", "ARCHIVED"}


def test_broadcast_trigger_type_has_four_values():
    assert {t.value for t in BroadcastTriggerType} == {"MANUAL", "SCHEDULED", "EVENT", "MARKET"}


def test_broadcast_trigger_defaults_to_manual_trigger_type():
    trigger = BroadcastTrigger(content_type=ContentType.MARKET_UPDATE, enabled=True)
    assert trigger.trigger_type == BroadcastTriggerType.MANUAL


def test_broadcast_trigger_accepts_explicit_trigger_type():
    trigger = BroadcastTrigger(content_type=ContentType.MARKET_UPDATE, enabled=True, trigger_type=BroadcastTriggerType.MARKET)
    assert trigger.trigger_type == BroadcastTriggerType.MARKET


def test_content_type_includes_live_analysis():
    assert ContentType.LIVE_ANALYSIS.value == "LIVE_ANALYSIS"
