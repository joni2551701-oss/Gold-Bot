"""
Translation Layer — Language Registry (Phase 63.0: Senior Trading AI
Foundation, TASK 6).

Static catalog, same "descriptor + build function" pattern this
phase's other new packages already established (Rule 8).
"""

from dataclasses import dataclass
from typing import List

from media_layer.translation.models import Language


@dataclass(frozen=True)
class LanguageDescriptor:
    language: Language
    display_name: str


def build_language_registry() -> List[LanguageDescriptor]:
    """Never raises. The three languages this phase names -- no more, no fewer."""
    return [
        LanguageDescriptor(language=Language.UZ, display_name="O'zbekcha"),
        LanguageDescriptor(language=Language.RU, display_name="Русский"),
        LanguageDescriptor(language=Language.EN, display_name="English"),
    ]


def is_supported(language: Language) -> bool:
    """Never raises: any Language enum member is supported by definition -- this exists for symmetry with a future phase that may narrow support per-feature."""
    return language in {d.language for d in build_language_registry()}
