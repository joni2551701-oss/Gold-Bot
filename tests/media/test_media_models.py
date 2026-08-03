"""Phase 63.7 TASK 1 — media_layer/content_manager/models.py: MediaAsset/MediaAssetStatus."""

from media_layer.content_manager.media_types import MediaType
from media_layer.content_manager.models import MediaAsset, MediaAssetStatus


def _asset(**overrides):
    defaults = dict(
        id="a1", content_id="AI_MARKET_REPORT", media_type=MediaType.TEXT,
        status=MediaAssetStatus.PENDING, title="Gold Report",
    )
    defaults.update(overrides)
    return MediaAsset(**defaults)


def test_media_asset_defaults():
    asset = _asset()
    assert asset.description == ""
    assert asset.metadata == {}
    assert asset.created_at == ""


def test_media_asset_accepts_explicit_values():
    asset = _asset(description="Bullish", metadata={"lang": "en"}, created_at="2026-01-01T00:00:00+00:00")
    assert asset.description == "Bullish"
    assert asset.metadata == {"lang": "en"}
    assert asset.created_at == "2026-01-01T00:00:00+00:00"


def test_media_asset_is_frozen():
    asset = _asset()
    try:
        asset.title = "mutated"
        assert False, "MediaAsset should be frozen"
    except AttributeError:
        pass


def test_media_asset_to_dict_is_json_serializable_shape():
    asset = _asset(description="Bullish", metadata={"lang": "en"}, created_at="2026-01-01T00:00:00+00:00")
    d = asset.to_dict()
    assert d == {
        "id": "a1", "content_id": "AI_MARKET_REPORT", "media_type": "TEXT",
        "status": "PENDING", "title": "Gold Report", "description": "Bullish",
        "metadata": {"lang": "en"}, "created_at": "2026-01-01T00:00:00+00:00",
    }


def test_media_asset_status_has_three_values():
    assert {s.value for s in MediaAssetStatus} == {"PENDING", "READY", "REJECTED"}
