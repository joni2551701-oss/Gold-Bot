"""Phase 65.0 TASK 8 — voice/runtime.py: VoiceRuntime facade over VoiceManager. Extended Phase 65.1 TASK 7/8 — provider resolution, real generation, fallback."""

from voice.manager import VoiceManager
from voice.models import VoiceProviderStatus, VoiceProviderType, VoiceResultStatus
from voice.provider_adapters.local import LocalVoiceProvider
from voice.provider_adapters.openai import OpenAIVoiceProvider
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


# --- Phase 65.1 TASK 7: provider resolution + real generation ---

class _FakeSecretsWithKey:
    OPENAI_API_KEY = "sk-test"


class _FakeResponse:
    def __init__(self, status_code=200, content=b"AUDIO"):
        self.status_code = status_code
        self.content = content
        self.headers = {"Content-Type": "audio/mpeg"}


class _FakeSessionOK:
    def post(self, *args, **kwargs):
        return _FakeResponse()


class _FakeSessionFail:
    def post(self, *args, **kwargs):
        return _FakeResponse(status_code=500, content=b"")


def test_resolve_provider_for_profile_delegates_to_manager():
    manager = VoiceManager()
    runtime = VoiceRuntime(manager)
    assert runtime.resolve_provider_for_profile("Senior") == manager.provider_for_profile("Senior")


def test_generate_audio_rejected_when_validate_fails():
    runtime = VoiceRuntime(VoiceManager())
    request = runtime.build_request("r1", "Senior", VoiceProviderType.OPENAI, "hello")
    result = runtime.generate_audio(request)
    assert result.status == VoiceResultStatus.REJECTED


def test_generate_audio_rejected_when_no_adapter_registered():
    manager = VoiceManager()
    manager.set_provider_status(VoiceProviderType.OPENAI, VoiceProviderStatus.ENABLED)
    runtime = VoiceRuntime(manager)
    request = runtime.build_request("r1", "Senior", VoiceProviderType.OPENAI, "hello")

    result = runtime.generate_audio(request)

    assert result.status == VoiceResultStatus.REJECTED
    assert "no adapter registered" in result.reason


def test_generate_audio_ready_when_adapter_succeeds():
    manager = VoiceManager()
    manager.set_provider_status(VoiceProviderType.OPENAI, VoiceProviderStatus.ENABLED)
    manager.register_adapter(VoiceProviderType.OPENAI, OpenAIVoiceProvider(session=_FakeSessionOK(), secrets=_FakeSecretsWithKey()))
    runtime = VoiceRuntime(manager)
    request = runtime.build_request("r1", "Senior", VoiceProviderType.OPENAI, "hello")

    result = runtime.generate_audio(request)

    assert result.status == VoiceResultStatus.READY
    assert result.metadata["provider"] == "openai"


def test_generate_audio_rejected_when_adapter_raises():
    manager = VoiceManager()
    manager.set_provider_status(VoiceProviderType.OPENAI, VoiceProviderStatus.ENABLED)
    manager.register_adapter(VoiceProviderType.OPENAI, OpenAIVoiceProvider(session=_FakeSessionFail(), secrets=_FakeSecretsWithKey()))
    runtime = VoiceRuntime(manager)
    request = runtime.build_request("r1", "Senior", VoiceProviderType.OPENAI, "hello")

    result = runtime.generate_audio(request)

    assert result.status == VoiceResultStatus.REJECTED
    assert "openai" in result.reason


# --- Phase 65.1 TASK 8: fallback handling ---

def test_generate_with_fallback_returns_primary_result_when_ready():
    manager = VoiceManager()
    manager.set_provider_status(VoiceProviderType.OPENAI, VoiceProviderStatus.ENABLED)
    manager.register_adapter(VoiceProviderType.OPENAI, OpenAIVoiceProvider(session=_FakeSessionOK(), secrets=_FakeSecretsWithKey()))
    runtime = VoiceRuntime(manager)
    request = runtime.build_request("r1", "Senior", VoiceProviderType.OPENAI, "hello")

    result = runtime.generate_with_fallback(request, fallback_providers=[VoiceProviderType.LOCAL])

    assert result.status == VoiceResultStatus.READY
    assert result.metadata["provider"] == "openai"


def test_generate_with_fallback_tries_fallback_when_primary_fails():
    manager = VoiceManager()
    manager.set_provider_status(VoiceProviderType.OPENAI, VoiceProviderStatus.ENABLED)
    manager.set_provider_status(VoiceProviderType.LOCAL, VoiceProviderStatus.ENABLED)
    manager.register_adapter(VoiceProviderType.OPENAI, OpenAIVoiceProvider(session=_FakeSessionFail(), secrets=_FakeSecretsWithKey()))
    manager.register_adapter(VoiceProviderType.LOCAL, LocalVoiceProvider())
    runtime = VoiceRuntime(manager)
    request = runtime.build_request("r1", "Senior", VoiceProviderType.OPENAI, "hello")

    # LocalVoiceProvider is a skeleton that always raises -- confirms fallback is attempted
    # and its own failure becomes the returned (final) REJECTED result.
    result = runtime.generate_with_fallback(request, fallback_providers=[VoiceProviderType.LOCAL])

    assert result.status == VoiceResultStatus.REJECTED
    assert "local" in result.reason


def test_generate_with_fallback_no_fallbacks_returns_primary_rejection():
    runtime = VoiceRuntime(VoiceManager())
    request = runtime.build_request("r1", "Senior", VoiceProviderType.OPENAI, "hello")

    result = runtime.generate_with_fallback(request)

    assert result.status == VoiceResultStatus.REJECTED
