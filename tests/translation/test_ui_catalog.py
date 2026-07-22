"""
Translation Layer -- UI string catalog tests (V1 Language Foundation,
Phase 1.3 Translation Engine). translation.ui_catalog.t() is the single
lookup used by every localized telegram handler: caller's language ->
EN -> whatever entry exists, never raising, a missing key surfacing
itself rather than crashing or silently disappearing.
"""

from translation.ui_catalog import t


def test_t_returns_the_requested_language():
    assert t("start.created", "UZ") == "Profil yaratildi."
    assert t("start.created", "RU") == "Профиль создан."
    assert t("start.created", "EN") == "Profile created."


def test_t_is_case_insensitive_on_language_code():
    assert t("start.created", "uz") == "Profil yaratildi."


def test_t_defaults_to_en_when_language_is_none():
    assert t("start.created", None) == "Profile created."


def test_t_falls_back_to_en_for_an_unknown_language_code():
    assert t("start.created", "FR") == "Profile created."


def test_t_formats_placeholders():
    assert t("risk.updated", "UZ", percent="3") == "Risk 3% ga o'zgartirildi."
    assert t("risk.updated", "EN", percent="3") == "Risk updated to 3%."


def test_t_never_raises_on_a_bad_placeholder():
    # "start.created" has no placeholders -- passing one anyway must not raise.
    assert t("start.created", "EN", unexpected="x") == "Profile created."


def test_t_returns_the_key_itself_for_an_unknown_key():
    assert t("totally.unknown.key", "EN") == "totally.unknown.key"


def test_every_catalog_entry_has_uz_ru_and_en():
    from translation.ui_catalog import _CATALOG

    for key, entry in _CATALOG.items():
        assert "UZ" in entry, f"{key} missing UZ"
        assert "RU" in entry, f"{key} missing RU"
        assert "EN" in entry, f"{key} missing EN"
