from assistant.identity_registry import SENIOR_IDENTITY, SENIORITA_IDENTITY, build_identity_registry


def test_build_identity_registry_returns_exactly_two_entries():
    registry = build_identity_registry()
    assert len(registry) == 2


def test_build_identity_registry_contains_senior_and_seniorita():
    names = {i.name for i in build_identity_registry()}
    assert names == {"Senior", "Seniorita"}


def test_senior_identity_fields():
    assert SENIOR_IDENTITY.name == "Senior"
    assert SENIOR_IDENTITY.default_voice == "Senior"
    assert SENIOR_IDENTITY.default_avatar == "senior_avatar_v1"


def test_seniorita_identity_fields():
    assert SENIORITA_IDENTITY.name == "Seniorita"
    assert SENIORITA_IDENTITY.default_voice == "Seniorita"
    assert SENIORITA_IDENTITY.default_avatar == "seniorita_avatar_v1"


def test_build_identity_registry_never_raises_and_is_a_list():
    registry = build_identity_registry()
    assert isinstance(registry, list)


def test_identity_registry_has_no_narrator_mentor_or_coach_this_phase():
    """Rule 4: only Senior/Seniorita this phase -- Narrator/Mentor/Coach are named as possible future additions, not built."""
    names = {i.name for i in build_identity_registry()}
    assert "Narrator" not in names
    assert "Mentor" not in names
    assert "Coach" not in names
