"""
Media Layer — Media Types (Phase 63.0: Senior Trading AI Foundation,
TASK 5).

Pure vocabulary. No TTS/voice synthesis, no image generation, no video
processing anywhere in this package (Rule 3).
"""

from enum import Enum


class MediaType(Enum):
    TEXT = "TEXT"
    VOICE = "VOICE"
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    LIVE = "LIVE"
