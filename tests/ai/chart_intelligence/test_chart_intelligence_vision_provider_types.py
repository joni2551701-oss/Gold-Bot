from ai_layer.vision_ai.vision_provider_types import ChartVisionProviderType


def test_has_five_members():
    assert len(list(ChartVisionProviderType)) == 5


def test_members_match_task_8_vocabulary():
    values = {m.value for m in ChartVisionProviderType}
    assert values == {"NONE", "OPENAI_VISION", "GEMINI_VISION", "CLAUDE_VISION", "LOCAL_VISION"}


def test_none_is_the_default_no_provider_state():
    assert ChartVisionProviderType.NONE.value == "NONE"


def test_is_pure_enum_no_methods_beyond_standard():
    assert ChartVisionProviderType.OPENAI_VISION.name == "OPENAI_VISION"


def test_every_member_is_a_plain_string_value():
    for member in ChartVisionProviderType:
        assert isinstance(member.value, str)
