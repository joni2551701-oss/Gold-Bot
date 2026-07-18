"""
Voice Layer — Data Models (Phase 65.0: AI Voice Intelligence
Foundation, TASK 2).

Pure data. No network client, no audio SDK, no Speech/Microphone/
Whisper/TTS import anywhere in this package (Rule 3 — "Hech qanday
Speech, Microphone, Whisper, OpenAI TTS, ElevenLabs API yozilmaydi").
Every field on every dataclass below is a primitive, an enum defined
in this same file, or another dataclass defined in this same file --
no `ContentResult`, `MediaAsset`, `BroadcastAsset`, `Persona`,
`DecisionResult`, `RiskResult`, or MT5/trading object is a valid field
type here.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Sequence


class VoiceProviderType(Enum):
    """The voice-synthesis backend types a future integration may deliver through -- vocabulary only, no client for any of them."""
    OPENAI = "OPENAI"
    ELEVENLABS = "ELEVENLABS"
    LOCAL = "LOCAL"
    CUSTOM = "CUSTOM"


class VoiceProviderStatus(Enum):
    """Owner-set intent only -- ENABLED never means "connected," since no provider has a real connection this phase."""
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class VoiceResultStatus(Enum):
    """A VoiceResult's own lifecycle state -- distinct from VoiceProviderStatus (provider intent, not per-request)."""
    PENDING = "PENDING"
    READY = "READY"
    REJECTED = "REJECTED"


@dataclass(frozen=True)
class VoiceProvider:
    """A descriptor, not a client -- `supports_*` fields are advertised capability vocabulary only, never checked against a real backend this phase."""
    provider_type: VoiceProviderType
    name: str
    supports_stream: bool = False
    supports_clone: bool = False
    supports_emotion: bool = False
    supports_ssml: bool = False
    status: VoiceProviderStatus = VoiceProviderStatus.DISABLED


@dataclass(frozen=True)
class VoiceProfile:
    """
    `name` is a free-text identifier (e.g. "Senior", "Seniorita",
    "Narrator") -- never an embedded `ai.persona.persona.Persona`
    object, and creating this profile never creates a matching
    `Persona`. See `docs/PHASE65_0_AUDIT.md`'s own Persona relationship
    section for why "Seniorita" here is not the same thing as a
    (nonexistent) `Persona` named "Seniorita".
    """
    name: str
    display_name: str
    description: str = ""
    supported_languages: Sequence[str] = field(default_factory=tuple)
    supported_modes: Sequence[str] = field(default_factory=tuple)
    default_provider: Optional[VoiceProviderType] = None


@dataclass(frozen=True)
class VoiceSettings:
    language: str = "en"
    speed: float = 1.0
    pitch: float = 1.0


@dataclass(frozen=True)
class VoiceRequest:
    """The one shape a future real synthesis layer would consume -- built by VoiceManager/VoiceRuntime below, never sent anywhere this phase."""
    id: str
    profile_name: str
    provider_type: VoiceProviderType
    text: str
    settings: VoiceSettings = field(default_factory=VoiceSettings)
    requested_at: str = ""


@dataclass(frozen=True)
class VoiceResult:
    """Never carries synthesized audio -- no such thing exists this phase (Rule 3). `reason` explains PENDING/READY/REJECTED, the same "never fabricate" convention every other Phase 63.x-64.0 result/asset dataclass already uses."""
    request_id: str
    status: VoiceResultStatus
    reason: str = ""
    generated_at: str = ""
