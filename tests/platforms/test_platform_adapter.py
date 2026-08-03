"""TASK-002D -- Platform Adapter interface tests (platforms/). No concrete adapter exists yet -- these confirm the abstract contract itself."""

import pytest

from platform_layer.platform_service.menu_registry import MenuDefinition
from platform_layer.platform_service.platform_adapter import PlatformAdapterBase
from platform_layer.platform_service.platform_model import PlatformName


def test_platform_adapter_base_cannot_be_instantiated_directly():
    with pytest.raises(TypeError):
        PlatformAdapterBase()


class _RecordingAdapter(PlatformAdapterBase):
    """Minimal concrete adapter for this test only -- not a real per-platform implementation, never exported."""

    def __init__(self):
        self.rendered_screens = []
        self.permission_denied_calls = 0
        self.failure_messages = []

    def render_screen(self, screen):
        self.rendered_screens.append(screen)

    def render_permission_denied(self):
        self.permission_denied_calls += 1

    def render_navigation_failed(self, message):
        self.failure_messages.append(message)


def test_concrete_subclass_implements_all_three_methods():
    adapter = _RecordingAdapter()
    screen = MenuDefinition(id="settings.main", permission="USER", platforms=[PlatformName.TELEGRAM_BOT])

    adapter.render_screen(screen)
    adapter.render_permission_denied()
    adapter.render_navigation_failed("Screen not registered")

    assert adapter.rendered_screens == [screen]
    assert adapter.permission_denied_calls == 1
    assert adapter.failure_messages == ["Screen not registered"]


def test_incomplete_subclass_cannot_be_instantiated():
    class _IncompleteAdapter(PlatformAdapterBase):
        def render_screen(self, screen):
            pass
        # render_permission_denied / render_navigation_failed deliberately omitted

    with pytest.raises(TypeError):
        _IncompleteAdapter()
