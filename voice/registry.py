"""
Voice Layer — Voice Profile Registry (Phase 65.0, TASK 3).

A real, runtime-mutable registry -- same "class wrapping a dict,
pre-seeded from the static catalog, with a genuine register()" shape
`media_layer/telegram_broadcast/trigger_manager.py`'s `BroadcastTriggerManager` already
established (the one existing Phase 63.0 class with a real,
runtime-mutable `register()`, as opposed to `media_layer/content_manager/media_registry.py`'s
deliberately-fixed catalog). No processing logic, no audio, no client
(Rule 3).
"""

from typing import Dict, List, Optional

from voice.models import VoiceProfile
from voice.profiles import SENIOR_VOICE, build_voice_profile_registry


class VoiceProfileRegistry:
    """Every dependency is injectable, same convention as every other Phase 61.x-64.0 manager/registry."""

    def __init__(self, profiles: Optional[List[VoiceProfile]] = None, default_name: str = SENIOR_VOICE.name) -> None:
        seed = profiles if profiles is not None else build_voice_profile_registry()
        self._profiles: Dict[str, VoiceProfile] = {p.name: p for p in seed}
        self._default_name = default_name

    def register(self, profile: VoiceProfile) -> None:
        self._profiles[profile.name] = profile

    def get(self, name: str) -> Optional[VoiceProfile]:
        """Never raises: an unknown name returns None rather than a fabricated profile."""
        return self._profiles.get(name)

    def exists(self, name: str) -> bool:
        return name in self._profiles

    def list_all(self) -> List[VoiceProfile]:
        return list(self._profiles.values())

    def default(self) -> Optional[VoiceProfile]:
        """Never raises: if the configured default name was never registered, returns None rather than fabricating one."""
        return self._profiles.get(self._default_name)
