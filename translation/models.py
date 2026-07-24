"""
Translation Layer — Data Models (Phase 63.0: Senior Trading AI
Foundation, TASK 6).

Contract only. No Google/DeepL/Gemini/OpenAI translation call anywhere
in this package (Rule 4).
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Language(Enum):
    """The three languages this phase names -- vocabulary only, no translation for any of them."""
    UZ = "UZ"
    RU = "RU"
    EN = "EN"


@dataclass(frozen=True)
class TranslationRequest:
    text: str
    source_language: Language
    target_language: Language


@dataclass(frozen=True)
class TranslationResult:
    """
    accepted: always False this phase -- `TranslationManager.translate()`
        never actually translates anything (Rule 4), same "never
        fabricate" convention `ai.runtime.runtime_response.RuntimeResponse`
        already established for a rejected AI call.
    translated_text: always None while `accepted` is False.
    """
    accepted: bool
    translated_text: Optional[str]
    reason: str
    source_language: Language
    target_language: Language
