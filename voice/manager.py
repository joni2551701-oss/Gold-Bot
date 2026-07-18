"""
Voice Layer — Voice Manager (Phase 65.0, TASK 4).

Composes `VoiceProfileRegistry` (TASK 3) with its own provider status
tracking into the deterministic surface a future integration layer
would need. `register_profile()`/`get_profile()` delegate to the
injected `VoiceProfileRegistry` rather than re-implementing profile
storage (CLAUDE.md's "No duplicate logic" restriction --
`docs/PHASE65_0_AUDIT.md`'s own three-tier resolution). Provider
status tracking mirrors `media/media_manager.py`'s `MediaManager` and
`broadcast/provider_manager.py`'s `BroadcastProviderManager` exactly:
every provider starts `DISABLED`. No network call, no SDK, no audio
library import anywhere in this class (Rule 3).
"""

from typing import Dict, List, Optional

from core.logger import setup_logger
from voice.models import VoiceProfile, VoiceProvider, VoiceProviderStatus, VoiceProviderType, VoiceRequest
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
