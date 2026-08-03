"""
Voice Layer — Speech-To-Text Data Models (Phase 65.2, TASK 1).

Mirrors `ai_layer/voice_ai/models.py`'s `VoiceRequest`/`VoiceResult` shape,
applied to the opposite direction (audio -> text instead of text ->
audio). `STTRequest.audio` is the one field in this whole `voice/`
package that ever carries raw bytes -- deliberately: it exists only as
a construction argument and a `transcribe()` call parameter, never
persisted to disk or a database anywhere in this package (Rule 9 —
"audio default permanent storage emas").
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class STTResultStatus(Enum):
    """A single STTResult's own lifecycle state."""
    PENDING = "PENDING"
    READY = "READY"
    REJECTED = "REJECTED"


@dataclass(frozen=True)
class STTRequest:
    """`audio` is raw bytes, held only for the duration of one `transcribe()` call -- never written to disk, never stored on any other dataclass in this package."""
    id: str
    audio: bytes
    language: str = "en"
    requested_at: str = ""


@dataclass(frozen=True)
class STTResult:
    """Never fabricates `text` -- `status == READY` is the only state where `text` is non-None; a REJECTED result carries `reason` instead, the same "never fabricate" convention every other Phase 65.x result already uses."""
    request_id: str
    status: STTResultStatus
    text: Optional[str] = None
    reason: str = ""
    generated_at: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
