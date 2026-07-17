"""Phase 63.0 TASK 4 — Broadcast Foundation. No real API/OBS/RTMP/streaming anywhere -- provider/trigger state is Owner-set intent only, prepare() never sends."""

from datetime import datetime, timezone

from ai.content.broadcast_output import BroadcastReadyContent
from ai.content.content_types import ContentType
from broadcast.broadcast_manager import BroadcastManager
from broadcast.models import BroadcastProviderStatus, BroadcastProviderType, BroadcastTrigger
from broadcast.provider_manager import BroadcastProviderManager, build_broadcast_provider_registry
from broadcast.trigger_manager import BroadcastTriggerManager


def test_provider_registry_has_all_six_director_named_types():
    registry = build_broadcast_provider_registry()
    types = {d.provider_type for d in registry}
    assert types == {
        BroadcastProviderType.YOUTUBE, BroadcastProviderType.OBS, BroadcastProviderType.RTMP,
        BroadcastProviderType.TWITCH, BroadcastProviderType.KICK, BroadcastProviderType.CUSTOM,
    }


def test_every_provider_starts_disabled():
    manager = BroadcastProviderManager()
    for name in manager.list_providers():
        assert manager.status_of(name) == BroadcastProviderStatus.DISABLED
        assert manager.is_enabled(name) is False


def test_set_status_enables_a_provider():
    manager = BroadcastProviderManager()
    manager.set_status("youtube", BroadcastProviderStatus.ENABLED)
    assert manager.is_enabled("youtube") is True


def test_set_status_on_unknown_provider_is_silently_ignored():
    manager = BroadcastProviderManager()
    manager.set_status("not-a-real-provider", BroadcastProviderStatus.ENABLED)
    assert manager.status_of("not-a-real-provider") is None


def test_trigger_manager_starts_with_nothing_armed():
    manager = BroadcastTriggerManager()
    assert manager.is_armed(ContentType.WEEKLY_OUTLOOK) is False


def test_trigger_manager_register_and_is_armed():
    manager = BroadcastTriggerManager()
    manager.register(BroadcastTrigger(content_type=ContentType.WEEKLY_OUTLOOK, enabled=True))
    assert manager.is_armed(ContentType.WEEKLY_OUTLOOK) is True
    assert manager.is_armed(ContentType.DAILY_BRIEF) is False


def test_broadcast_manager_would_not_broadcast_by_default():
    manager = BroadcastManager()
    assert manager.would_broadcast(ContentType.WEEKLY_OUTLOOK, "youtube") is False


def test_broadcast_manager_would_broadcast_when_both_armed_and_enabled():
    provider_manager = BroadcastProviderManager()
    provider_manager.set_status("youtube", BroadcastProviderStatus.ENABLED)
    trigger_manager = BroadcastTriggerManager()
    trigger_manager.register(BroadcastTrigger(content_type=ContentType.WEEKLY_OUTLOOK, enabled=True))
    manager = BroadcastManager(provider_manager=provider_manager, trigger_manager=trigger_manager)

    assert manager.would_broadcast(ContentType.WEEKLY_OUTLOOK, "youtube") is True


def test_prepare_returns_none_when_not_armed_or_enabled():
    manager = BroadcastManager()
    content = BroadcastReadyContent(content_type="AI_WEEKLY_OUTLOOK", title="t", body="b", prepared_at=datetime.now(timezone.utc).isoformat())

    assert manager.prepare(content, ContentType.WEEKLY_OUTLOOK, "youtube") is None


def test_prepare_builds_a_request_never_sends_it():
    provider_manager = BroadcastProviderManager()
    provider_manager.set_status("youtube", BroadcastProviderStatus.ENABLED)
    trigger_manager = BroadcastTriggerManager()
    trigger_manager.register(BroadcastTrigger(content_type=ContentType.WEEKLY_OUTLOOK, enabled=True))
    manager = BroadcastManager(provider_manager=provider_manager, trigger_manager=trigger_manager)
    content = BroadcastReadyContent(content_type="AI_WEEKLY_OUTLOOK", title="t", body="b", prepared_at=datetime.now(timezone.utc).isoformat())

    request = manager.prepare(content, ContentType.WEEKLY_OUTLOOK, "youtube")

    assert request is not None
    assert request.content == content
    assert request.provider_type == BroadcastProviderType.YOUTUBE
