"""Phase 63.6 TASK 2 — ai/content/models.py: ContentMode/ContentMetadata/ContentContext."""

from ai_layer.ai_service.content.content_type_vocabulary import ContentType
from ai_layer.ai_service.content.models import ContentContext, ContentMetadata, ContentMode


def test_content_metadata_defaults():
    metadata = ContentMetadata()
    assert metadata.category == ""
    assert metadata.language == "en"
    assert metadata.priority == 0
    assert metadata.tags == ()


def test_content_metadata_accepts_explicit_values():
    metadata = ContentMetadata(category="SMC", language="uz", priority=2, tags=("gold", "bos"))
    assert metadata.category == "SMC"
    assert metadata.language == "uz"
    assert metadata.priority == 2
    assert metadata.tags == ("gold", "bos")


def test_content_context_defaults():
    context = ContentContext(content_type=ContentType.EDUCATION, mode=ContentMode.GENERAL)
    assert context.audience == ""
    assert context.tone == ""
    assert context.purpose == ""
    assert context.metadata == ContentMetadata()


def test_content_context_is_frozen():
    context = ContentContext(content_type=ContentType.EDUCATION, mode=ContentMode.GENERAL)
    try:
        context.purpose = "mutated"
        assert False, "ContentContext should be frozen"
    except AttributeError:
        pass


def test_content_mode_has_the_three_brief_named_values():
    assert {m.value for m in ContentMode} == {"GENERAL", "MARKET", "EDUCATION"}


def test_content_type_includes_trade_replay():
    assert ContentType.TRADE_REPLAY.value == "TRADE_REPLAY"
