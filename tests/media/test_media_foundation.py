"""Phase 63.0 TASK 5 — Media Foundation. No TTS/voice/image/video processing anywhere -- Owner-set intent only."""

from media.media_manager import MediaManager
from media.media_registry import build_media_registry
from media.media_types import MediaType


def test_media_registry_has_all_five_director_named_types():
    registry = build_media_registry()
    types = {d.media_type for d in registry}
    assert types == {MediaType.TEXT, MediaType.VOICE, MediaType.IMAGE, MediaType.VIDEO, MediaType.LIVE}


def test_text_starts_enabled_everything_else_starts_disabled():
    manager = MediaManager()
    assert manager.is_enabled(MediaType.TEXT) is True
    for media_type in (MediaType.VOICE, MediaType.IMAGE, MediaType.VIDEO, MediaType.LIVE):
        assert manager.is_enabled(media_type) is False


def test_set_enabled_toggles_a_media_type():
    manager = MediaManager()
    manager.set_enabled(MediaType.VOICE, True)
    assert manager.is_enabled(MediaType.VOICE) is True
    manager.set_enabled(MediaType.VOICE, False)
    assert manager.is_enabled(MediaType.VOICE) is False


def test_descriptor_of_returns_the_real_descriptor():
    manager = MediaManager()
    descriptor = manager.descriptor_of(MediaType.TEXT)
    assert descriptor is not None
    assert descriptor.name == "text"


def test_list_types_returns_all_five():
    manager = MediaManager()
    assert set(manager.list_types()) == {MediaType.TEXT, MediaType.VOICE, MediaType.IMAGE, MediaType.VIDEO, MediaType.LIVE}
