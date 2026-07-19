from assistant.identity import AssistantIdentity


def test_assistant_identity_holds_expected_fields():
    identity = AssistantIdentity(
        name="Senior", display_name="Senior Trading AI", description="test",
        default_voice="Senior", default_avatar="senior_avatar_v1", supported_languages=("en",),
    )
    assert identity.name == "Senior"
    assert identity.display_name == "Senior Trading AI"
    assert identity.default_voice == "Senior"
    assert identity.default_avatar == "senior_avatar_v1"
    assert identity.supported_languages == ("en",)


def test_assistant_identity_default_supported_languages_is_en():
    identity = AssistantIdentity(
        name="X", display_name="X", description="x", default_voice="X", default_avatar="x_avatar",
    )
    assert identity.supported_languages == ("en",)


def test_assistant_identity_is_frozen():
    identity = AssistantIdentity(
        name="Senior", display_name="Senior Trading AI", description="test",
        default_voice="Senior", default_avatar="senior_avatar_v1",
    )
    try:
        identity.name = "Changed"
        assert False, "AssistantIdentity should be frozen"
    except AttributeError:
        pass


def test_assistant_identity_has_no_persona_fields():
    """Regression guard: AssistantIdentity must never carry a Persona-shaped field (tone/system_identity/disclaimer/language_style/role) -- Rule 3 Persona Protection."""
    field_names = set(AssistantIdentity.__dataclass_fields__.keys())
    forbidden = {"tone", "system_identity", "disclaimer", "language_style", "role", "persona", "persona_name"}
    assert field_names.isdisjoint(forbidden)
