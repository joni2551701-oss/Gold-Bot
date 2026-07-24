"""
Translation Layer — Translation Manager (Phase 63.0: Senior Trading AI
Foundation, TASK 6).

`translate()` never translates -- it always returns a cleanly rejected
`TranslationResult`, honestly, rather than echoing the input text or
fabricating a translation. No Google/DeepL/Gemini/OpenAI import or
call anywhere in this module (Rule 4). A future, separately-approved
phase wires a real translation backend behind this exact contract.
"""

from translation.language_registry import is_supported
from translation.models import TranslationRequest, TranslationResult


class TranslationManager:
    def translate(self, request: TranslationRequest) -> TranslationResult:
        """Never raises. Always accepted=False this phase (Rule 4 -- no real translation backend exists yet)."""
        if not is_supported(request.source_language) or not is_supported(request.target_language):
            return TranslationResult(
                accepted=False, translated_text=None,
                reason="unsupported language", source_language=request.source_language,
                target_language=request.target_language,
            )

        return TranslationResult(
            accepted=False, translated_text=None,
            reason="translation not implemented -- foundation only (Phase 63.0)",
            source_language=request.source_language, target_language=request.target_language,
        )
