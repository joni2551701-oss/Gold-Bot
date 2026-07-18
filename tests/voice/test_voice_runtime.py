"""Phase 65.0 TASK 8 — voice/runtime.py: VoiceRuntime facade over VoiceManager."""

from voice.manager import VoiceManager
from voice.models import VoiceProviderStatus, VoiceProviderType, VoiceResultStatus
from voice.runtime import VoiceRuntime


def test_resolve_profile_delegates_to_manager():
    manager = VoiceManager()
    runtime = VoiceRuntime(manager)
    assert runtime.resolve_profile("Senior") == manager.get_profile("Senior")


def test_resolve_profile_unknown_returns_none():
    runtime = VoiceRuntime()
    assert runtime.resolve_profile("Unknown") is None


def test_resolve_provider_delegates_to_manager():
    manager = VoiceManager()
    runtime = VoiceRuntime(manager)
    assert runtime.resolve_provider(VoiceProviderType.OPENAI) == manager.get_provider(VoiceProviderType.OPENAI)


def test_build_request_is_pure_construction():
    runtime = VoiceRuntime()
    request = runtime.build_request("r1", "Senior", VoiceProviderType.OPENAI, "hello")
    assert request.id == "r1"
    assert request.profile_name == "Senior"
    assert request.provider_type == VoiceProviderType.OPENAI
    assert request.text == "hello"


def test_validate_delegates_to_manager():
    manager = VoiceManager()
    manager.set_provider_status(VoiceProviderType.OPENAI, VoiceProviderStatus.ENABLED)
    runtime = VoiceRuntime(manager)
    request = runtime.build_request("r1", "Senior", VoiceProviderType.OPENAI, "hello")
    assert runtime.validate(request) == manager.validate(request) is True


def test_build_result_ready_when_ok():
    runtime = VoiceRuntime()
    request = runtime.build_request("r1", "Senior", VoiceProviderType.OPENAI, "hello")
    result = runtime.build_result(request, ok=True)
    assert result.status == VoiceResultStatus.READY
    assert result.request_id == "r1"


def test_build_result_rejected_when_not_ok():
    runtime = VoiceRuntime()
    request = runtime.build_request("r1", "Senior", VoiceProviderType.OPENAI, "hello")
    result = runtime.build_result(request, ok=False, reason="disabled")
    assert result.status == VoiceResultStatus.REJECTED
    assert result.reason == "disabled"


def test_prepare_voice_ready_for_valid_request():
    manager = VoiceManager()
    manager.set_provider_status(VoiceProviderType.OPENAI, VoiceProviderStatus.ENABLED)
    runtime = VoiceRuntime(manager)
    request = runtime.build_request("r1", "Senior", VoiceProviderType.OPENAI, "hello")

    result = runtime.prepare_voice(request)

    assert result.status == VoiceResultStatus.READY
    assert result.reason == ""


def test_prepare_voice_rejected_for_disabled_provider():
    runtime = VoiceRuntime(VoiceManager())
    request = runtime.build_request("r1", "Senior", VoiceProviderType.OPENAI, "hello")

    result = runtime.prepare_voice(request)

    assert result.status == VoiceResultStatus.REJECTED
    assert result.reason != ""


def test_prepare_voice_carries_generated_at():
    manager = VoiceManager()
    manager.set_provider_status(VoiceProviderType.OPENAI, VoiceProviderStatus.ENABLED)
    runtime = VoiceRuntime(manager)
    request = runtime.build_request("r1", "Senior", VoiceProviderType.OPENAI, "hello")

    result = runtime.prepare_voice(request, generated_at="2026-01-01T00:00:00+00:00")

    assert result.generated_at == "2026-01-01T00:00:00+00:00"
