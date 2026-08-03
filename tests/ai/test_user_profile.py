"""
Phase 55 — AIUserProfile foundation tests.

Pure data model -- no database access anywhere in
ai/profiles/user_profile.py, matching this phase's explicit
"Databasega ulanmasin" scope.
"""

from ai_layer.personal_ai.user_profile.user_profile import AIUserProfile


def test_profile_requires_only_telegram_id():
    profile = AIUserProfile(telegram_id="123")

    assert profile.telegram_id == "123"
    assert profile.experience_level is None
    assert profile.preferred_strategy is None
    assert profile.risk_style is None
    assert profile.language is None


def test_profile_accepts_all_fields():
    profile = AIUserProfile(
        telegram_id="123", experience_level="intermediate",
        preferred_strategy="Liquidity Sweep", risk_style="moderate", language="RU",
    )

    assert profile.experience_level == "intermediate"
    assert profile.preferred_strategy == "Liquidity Sweep"
    assert profile.risk_style == "moderate"
    assert profile.language == "RU"


def test_profile_is_immutable():
    import pytest

    profile = AIUserProfile(telegram_id="123")
    with pytest.raises(Exception):
        profile.telegram_id = "456"


def test_user_profile_has_no_database_import():
    import inspect
    from ai_layer.personal_ai.user_profile import user_profile

    for name, module in inspect.getmembers(user_profile, inspect.ismodule):
        assert not module.__name__.startswith("database"), f"unexpected database import: {module.__name__}"
    for line in inspect.getsource(user_profile).splitlines():
        stripped = line.strip()
        assert not stripped.startswith("import sqlite3")
        assert not stripped.startswith("from database")
