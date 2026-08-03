"""PLATFORM-001 -- Cross Platform Checker foundation tests (platforms/)."""

from platform_layer.platform_service.capability_model import PlatformCapability, SupportStatus
from platform_layer.platform_service.platform_model import PlatformName
from platform_layer.platform_service.cross_platform_checker import (
    check_module_capabilities,
    format_capability_violations,
)


def _complete_declaration():
    return {
        PlatformName.TELEGRAM_BOT: PlatformCapability(platform=PlatformName.TELEGRAM_BOT, status=SupportStatus.SUPPORTED),
        PlatformName.TELEGRAM_MINI_APP: PlatformCapability(
            platform=PlatformName.TELEGRAM_MINI_APP, status=SupportStatus.NOT_SUPPORTED, reason="No Mini App client exists yet."
        ),
        PlatformName.ANDROID: PlatformCapability(
            platform=PlatformName.ANDROID, status=SupportStatus.NOT_SUPPORTED, reason="No Android client exists yet."
        ),
        PlatformName.IOS: PlatformCapability(
            platform=PlatformName.IOS, status=SupportStatus.NOT_SUPPORTED, reason="No iOS client exists yet."
        ),
        PlatformName.DESKTOP: PlatformCapability(
            platform=PlatformName.DESKTOP, status=SupportStatus.NOT_SUPPORTED, reason="No Desktop client exists yet."
        ),
    }


def test_complete_declaration_passes():
    result = check_module_capabilities(_complete_declaration())
    assert result.ok is True
    assert result.violations == ()
    assert format_capability_violations(result) == "Complete cross-platform declaration -- no violations."


def test_missing_platform_is_a_violation():
    declaration = _complete_declaration()
    del declaration[PlatformName.DESKTOP]

    result = check_module_capabilities(declaration)
    assert result.ok is False
    assert any(v.platform == PlatformName.DESKTOP for v in result.violations)


def test_not_supported_without_reason_is_a_violation():
    declaration = _complete_declaration()
    declaration[PlatformName.ANDROID] = PlatformCapability(platform=PlatformName.ANDROID, status=SupportStatus.NOT_SUPPORTED)

    result = check_module_capabilities(declaration)
    assert result.ok is False
    assert any(v.platform == PlatformName.ANDROID for v in result.violations)


def test_format_lists_every_violation():
    declaration = _complete_declaration()
    del declaration[PlatformName.DESKTOP]
    declaration[PlatformName.ANDROID] = PlatformCapability(platform=PlatformName.ANDROID, status=SupportStatus.NOT_SUPPORTED)

    result = check_module_capabilities(declaration)
    text = format_capability_violations(result)
    assert "DESKTOP" in text
    assert "ANDROID" in text
