"""
Voice Layer — Voice Manager (Phase 65.0, TASK 4; extended Phase 65.1,
TASK 6/7 -- real provider adapter registry + per-profile provider
selection).

Composes `VoiceProfileRegistry` (TASK 3) with its own provider status
tracking into the deterministic surface a future integration layer
would need. `register_profile()`/`get_profile()` delegate to the
injected `VoiceProfileRegistry` rather than re-implementing profile
storage (CLAUDE.md's "No duplicate logic" restriction --
`docs/PHASE65_0_AUDIT.md`'s own three-tier resolution). Provider
status tracking mirrors `media/media_manager.py`'s `MediaManager` and
`broadcast/provider_manager.py`'s `BroadcastProviderManager` exactly:
every provider starts `DISABLED`. No network call, no SDK, no audio
library import anywhere in this class (Rule 3, unchanged).

Phase 65.1 TASK 6/7 additions (all additive, Article 9): a real
`VoiceProviderContract` adapter registry (`register_adapter()`/
`get_adapter()`/`list_adapters()`) and per-profile provider selection
(`set_provider_for_profile()`/`provider_for_profile()`) -- both folded
into this existing class rather than a new `VoiceProviderManager`
sibling, per `docs/PHASE65_1_AUDIT.md`'s own "no duplicate Manager"
resolution. Selection falls back to `VoiceProfile.default_provider`
(Phase 65.0, LOCKed) when no explicit override is set -- an override
never mutates the static profile itself.
"""

from typing import Dict, List, Optional

from core_layer.logger.logger import setup_logger
from voice.models import VoiceProfile, VoiceProvider, VoiceProviderStatus, VoiceProviderType, VoiceRequest
from voice.provider_contract import VoiceProviderContract
from voice.providers import build_voice_provider_registry
from voice.registry import VoiceProfileRegistry

logger = setup_logger("VoiceManager")


class VoiceManager:
    """Every dependency is injectable, same convention as every other Phase 61.x-64.0 manager."""

    def __init__(self, profile_registry: Optional[VoiceProfileRegistry] = None) -> None:
        self._profiles = profile_registry or VoiceProfileRegistry()
        self._providers: Dict[VoiceProviderType, VoiceProvider] = {
            p.provider_type: p for p in build_voice_provider_registry()
        }
        self._provider_status: Dict[VoiceProviderType, VoiceProviderStatus] = {
            provider_type: VoiceProviderStatus.DISABLED for provider_type in self._providers
        }
        self._adapters: Dict[VoiceProviderType, VoiceProviderContract] = {}
        self._profile_provider_overrides: Dict[str, VoiceProviderType] = {}

    # --- Profiles: delegates to VoiceProfileRegistry, no duplicate storage ---

    def register_profile(self, profile: VoiceProfile) -> None:
        self._profiles.register(profile)

    def get_profile(self, name: str) -> Optional[VoiceProfile]:
        return self._profiles.get(name)

    # --- Providers: static descriptor + Owner-set ENABLED/DISABLED intent ---

    def register_provider(self, provider: VoiceProvider) -> None:
        """Registers/replaces a provider descriptor; a newly-registered provider starts DISABLED, matching every pre-seeded one."""
        self._providers[provider.provider_type] = provider
        self._provider_status.setdefault(provider.provider_type, VoiceProviderStatus.DISABLED)

    def get_provider(self, provider_type: VoiceProviderType) -> Optional[VoiceProvider]:
        """Never raises: an unregistered provider_type returns None rather than a fabricated descriptor."""
        return self._providers.get(provider_type)

    def set_provider_status(self, provider_type: VoiceProviderType, status: VoiceProviderStatus) -> None:
        """Unknown provider_type is silently ignored -- same fail-safe posture every other Phase 63.x provider manager uses."""
        if provider_type not in self._providers:
            logger.warning(f"set_provider_status called for an unregistered voice provider: {provider_type}")
            return
        self._provider_status[provider_type] = status

    def is_provider_enabled(self, provider_type: VoiceProviderType) -> bool:
        return self._provider_status.get(provider_type) == VoiceProviderStatus.ENABLED

    def list_providers(self) -> List[VoiceProvider]:
        return list(self._providers.values())

    # --- Deterministic request lifecycle ---

    def validate(self, request: VoiceRequest) -> bool:
        """Deterministic: True only when the profile exists, the provider is registered and enabled, and text is non-empty."""
        profile = self.get_profile(request.profile_name)
        provider = self.get_provider(request.provider_type)
        return bool(
            profile is not None and provider is not None
            and self.is_provider_enabled(request.provider_type) and request.text
        )

    def prepare(self, request: VoiceRequest) -> bool:
        """Never raises: returns validate()'s own result -- the one place TASK 4's own 'prepare' method lives; VoiceRuntime.prepare_voice() below builds the actual VoiceResult from this."""
        return self.validate(request)

    # --- Real provider adapter registry (Phase 65.1 TASK 6/7) ---

    def register_adapter(self, provider_type: VoiceProviderType, adapter: VoiceProviderContract) -> None:
        """Registers/replaces the real `VoiceProviderContract` implementation backing a given `VoiceProviderType`. Registering an adapter does not itself enable the provider -- `set_provider_status()` (Phase 65.0, unchanged) still owns Owner-set ENABLED/DISABLED intent."""
        self._adapters[provider_type] = adapter

    def get_adapter(self, provider_type: VoiceProviderType) -> Optional[VoiceProviderContract]:
        """Never raises: an unregistered provider_type returns None rather than a fabricated adapter."""
        return self._adapters.get(provider_type)

    def list_adapters(self) -> List[VoiceProviderType]:
        return list(self._adapters.keys())

    # --- Per-profile provider selection (Phase 65.1 TASK 6) ---

    def set_provider_for_profile(self, profile_name: str, provider_type: VoiceProviderType) -> None:
        """An explicit override -- never mutates the LOCKed static VoiceProfile.default_provider itself."""
        self._profile_provider_overrides[profile_name] = provider_type

    def provider_for_profile(self, profile_name: str) -> Optional[VoiceProviderType]:
        """Resolution order: explicit override (this method's own dict) first, else the profile's own `default_provider` (Phase 65.0), else None if the profile itself is unknown. Never raises."""
        if profile_name in self._profile_provider_overrides:
            return self._profile_provider_overrides[profile_name]
        profile = self.get_profile(profile_name)
        return profile.default_provider if profile is not None else None
