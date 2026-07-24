"""Phase 63.0 TASK 6 — Translation Foundation. No Google/DeepL/Gemini/OpenAI call anywhere -- translate() always cleanly rejects."""

from translation.language_registry import build_language_registry, is_supported
from translation.models import Language, TranslationRequest
from translation.translation_manager import TranslationManager


def test_language_registry_has_all_three_director_named_languages():
    registry = build_language_registry()
    languages = {d.language for d in registry}
    assert languages == {Language.UZ, Language.RU, Language.EN}


def test_is_supported_is_true_for_every_registered_language():
    for language in Language:
        assert is_supported(language) is True


def test_translate_never_translates_always_rejects():
    manager = TranslationManager()
    request = TranslationRequest(text="Gold is rallying.", source_language=Language.EN, target_language=Language.UZ)

    result = manager.translate(request)

    assert result.accepted is False
    assert result.translated_text is None
    assert "not implemented" in result.reason


def test_translate_never_echoes_the_input_text():
    manager = TranslationManager()
    request = TranslationRequest(text="Gold is rallying.", source_language=Language.EN, target_language=Language.RU)

    result = manager.translate(request)

    assert result.translated_text != request.text
    assert result.translated_text is None
