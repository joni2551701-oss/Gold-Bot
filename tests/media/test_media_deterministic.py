"""Phase 63.7 TASK 2/3 — media_registry.get()/exists() and MediaManager's create_asset/validate_asset/prepare_asset/get_asset, all additive to the existing list_types()/descriptor_of()/is_enabled()/set_enabled()."""

from media.media_manager import MediaManager
from media.media_registry import exists, get
from media.media_types import MediaType
from media.models import MediaAssetStatus


def test_registry_get_returns_the_real_descriptor():
    descriptor = get(MediaType.VOICE)
    assert descriptor is not None
    assert descriptor.name == "voice"


def test_registry_exists_is_true_for_every_media_type():
    for media_type in MediaType:
        assert exists(media_type) is True


def test_create_asset_starts_pending_without_rendering_anything():
    manager = MediaManager()
    asset = manager.create_asset(content_id="AI_MARKET_REPORT", media_type=MediaType.TEXT, title="Gold Report", description="Bullish.")
    assert asset.status == MediaAssetStatus.PENDING
    assert asset.content_id == "AI_MARKET_REPORT"
    assert asset.title == "Gold Report"


def test_create_asset_stores_metadata():
    manager = MediaManager()
    asset = manager.create_asset(content_id="c1", media_type=MediaType.TEXT, title="t", metadata={"lang": "uz"})
    assert asset.metadata == {"lang": "uz"}


def test_create_asset_without_metadata_leaves_it_empty():
    manager = MediaManager()
    asset = manager.create_asset(content_id="c1", media_type=MediaType.TEXT, title="t")
    assert asset.metadata == {}


def test_validate_asset_true_for_enabled_type_with_title():
    manager = MediaManager()
    asset = manager.create_asset(content_id="c1", media_type=MediaType.TEXT, title="t")
    assert manager.validate_asset(asset) is True


def test_validate_asset_false_for_disabled_type():
    manager = MediaManager()
    asset = manager.create_asset(content_id="c1", media_type=MediaType.VOICE, title="t")
    assert manager.validate_asset(asset) is False


def test_validate_asset_false_for_empty_title():
    manager = MediaManager()
    asset = manager.create_asset(content_id="c1", media_type=MediaType.TEXT, title="")
    assert manager.validate_asset(asset) is False


def test_prepare_asset_transitions_to_ready():
    manager = MediaManager()
    asset = manager.create_asset(content_id="c1", media_type=MediaType.TEXT, title="t")
    prepared = manager.prepare_asset(asset)
    assert prepared.status == MediaAssetStatus.READY
    assert prepared.id == asset.id


def test_prepare_asset_transitions_to_rejected_for_disabled_type():
    manager = MediaManager()
    asset = manager.create_asset(content_id="c1", media_type=MediaType.IMAGE, title="t")
    prepared = manager.prepare_asset(asset)
    assert prepared.status == MediaAssetStatus.REJECTED


def test_get_asset_returns_the_latest_stored_version():
    manager = MediaManager()
    asset = manager.create_asset(content_id="c1", media_type=MediaType.TEXT, title="t")
    assert manager.get_asset(asset.id) == asset
    prepared = manager.prepare_asset(asset)
    assert manager.get_asset(asset.id) == prepared
    assert manager.get_asset(asset.id) != asset


def test_get_asset_unknown_id_returns_none():
    manager = MediaManager()
    assert manager.get_asset("does-not-exist") is None


def test_deterministic_methods_never_touch_external_providers():
    """create_asset/validate_asset/prepare_asset/get_asset only track in-memory state -- no render/upload/publish call exists on MediaManager at all."""
    manager = MediaManager()
    asset = manager.create_asset(content_id="c1", media_type=MediaType.TEXT, title="t")
    prepared = manager.prepare_asset(asset)
    assert prepared.status == MediaAssetStatus.READY
    assert not hasattr(manager, "render")
    assert not hasattr(manager, "upload")
    assert not hasattr(manager, "publish")
