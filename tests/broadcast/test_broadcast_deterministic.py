"""Phase 63.8 TASK 2 — BroadcastManager's deterministic asset surface (create_broadcast/validate_broadcast/prepare_broadcast/get_broadcast/list_broadcasts), all additive to the existing, LOCKed would_broadcast()/prepare()."""

from ai.content.content_types import ContentType
from broadcast.broadcast_manager import BroadcastManager
from broadcast.models import BroadcastStatus


def test_create_broadcast_starts_draft_without_sending_anything():
    manager = BroadcastManager()
    asset = manager.create_broadcast(content_id="AI_MARKET_REPORT", media_id="m1", broadcast_type=ContentType.MARKET_UPDATE)
    assert asset.status == BroadcastStatus.DRAFT
    assert asset.content_id == "AI_MARKET_REPORT"
    assert asset.media_id == "m1"


def test_create_broadcast_stores_persona_name_and_metadata():
    manager = BroadcastManager()
    asset = manager.create_broadcast(
        content_id="c1", media_id="m1", broadcast_type=ContentType.EDUCATION,
        persona_name="Senior Trading AI", metadata={"lang": "uz"},
    )
    assert asset.persona_name == "Senior Trading AI"
    assert asset.metadata == {"lang": "uz"}


def test_create_broadcast_without_optional_fields_leaves_them_empty():
    manager = BroadcastManager()
    asset = manager.create_broadcast(content_id="c1", media_id="m1", broadcast_type=ContentType.EDUCATION)
    assert asset.persona_name is None
    assert asset.metadata == {}


def test_validate_broadcast_true_when_content_and_media_ids_present():
    manager = BroadcastManager()
    asset = manager.create_broadcast(content_id="c1", media_id="m1", broadcast_type=ContentType.EDUCATION)
    assert manager.validate_broadcast(asset) is True


def test_validate_broadcast_false_when_content_id_missing():
    manager = BroadcastManager()
    asset = manager.create_broadcast(content_id="", media_id="m1", broadcast_type=ContentType.EDUCATION)
    assert manager.validate_broadcast(asset) is False


def test_validate_broadcast_false_when_media_id_missing():
    manager = BroadcastManager()
    asset = manager.create_broadcast(content_id="c1", media_id="", broadcast_type=ContentType.EDUCATION)
    assert manager.validate_broadcast(asset) is False


def test_prepare_broadcast_transitions_to_ready():
    manager = BroadcastManager()
    asset = manager.create_broadcast(content_id="c1", media_id="m1", broadcast_type=ContentType.EDUCATION)
    prepared = manager.prepare_broadcast(asset)
    assert prepared.status == BroadcastStatus.READY
    assert prepared.id == asset.id


def test_prepare_broadcast_transitions_to_failed_when_invalid():
    manager = BroadcastManager()
    asset = manager.create_broadcast(content_id="", media_id="m1", broadcast_type=ContentType.EDUCATION)
    prepared = manager.prepare_broadcast(asset)
    assert prepared.status == BroadcastStatus.FAILED


def test_get_broadcast_returns_the_latest_stored_version():
    manager = BroadcastManager()
    asset = manager.create_broadcast(content_id="c1", media_id="m1", broadcast_type=ContentType.EDUCATION)
    assert manager.get_broadcast(asset.id) == asset
    prepared = manager.prepare_broadcast(asset)
    assert manager.get_broadcast(asset.id) == prepared
    assert manager.get_broadcast(asset.id) != asset


def test_get_broadcast_unknown_id_returns_none():
    manager = BroadcastManager()
    assert manager.get_broadcast("does-not-exist") is None


def test_list_broadcasts_starts_empty():
    manager = BroadcastManager()
    assert manager.list_broadcasts() == []


def test_list_broadcasts_records_every_create_broadcast_call():
    manager = BroadcastManager()
    first = manager.create_broadcast(content_id="c1", media_id="m1", broadcast_type=ContentType.EDUCATION)
    second = manager.create_broadcast(content_id="c2", media_id="m2", broadcast_type=ContentType.MARKET_UPDATE)
    assert manager.list_broadcasts() == [first, second]


def test_deterministic_methods_never_send_anything_externally():
    """create_broadcast/validate_broadcast/prepare_broadcast/get_broadcast/list_broadcasts only track in-memory state -- no send/publish/deliver method exists on BroadcastManager at all."""
    manager = BroadcastManager()
    asset = manager.create_broadcast(content_id="c1", media_id="m1", broadcast_type=ContentType.EDUCATION)
    prepared = manager.prepare_broadcast(asset)
    assert prepared.status == BroadcastStatus.READY
    assert not hasattr(manager, "send")
    assert not hasattr(manager, "publish")
    assert not hasattr(manager, "deliver")
