"""Phase 63.6 TASK 3 — ContentEngine's deterministic surface (create/format/preview/validate/history), all additive to the existing, LOCKed generate()."""

from ai.content.content_adapter import ContentEngine
from ai.content_types import ContentType
from ai.content.content_schema import ContentResult
from ai.content.models import ContentMetadata


def test_create_builds_an_accepted_result_without_calling_ai_service():
    engine = ContentEngine()
    result = engine.create(ContentType.EDUCATION, title="What is a BOS?", body="A structural break in price.")

    assert result.accepted is True
    assert result.title == "What is a BOS?"
    assert result.body == "A structural break in price."
    assert result.content_type == "EDUCATION"
    assert result.reason == "created directly, no AI generation"
    assert result.generated_at is not None


def test_create_stores_metadata_as_a_dict():
    engine = ContentEngine()
    metadata = ContentMetadata(category="SMC", language="uz", priority=1, tags=("gold",))

    result = engine.create(ContentType.MARKET_UPDATE, title="Gold Update", body="Bullish on H1.", metadata=metadata)

    assert result.metadata == {"category": "SMC", "language": "uz", "priority": 1, "tags": ("gold",)}


def test_create_without_metadata_leaves_it_none():
    engine = ContentEngine()
    result = engine.create(ContentType.EDUCATION, title="t", body="b")
    assert result.metadata is None


def test_format_joins_title_and_body():
    engine = ContentEngine()
    result = engine.create(ContentType.EDUCATION, title="Title", body="Body text")
    assert engine.format(result) == "Title\n\nBody text"


def test_format_falls_back_to_reason_when_body_is_missing():
    result = ContentResult(
        accepted=False, content_type="AI_MARKET_REPORT", title="Market Report",
        body=None, reason="no runtime method mapping yet", generated_at="2026-01-01T00:00:00+00:00",
    )
    engine = ContentEngine()
    assert engine.format(result) == "Market Report\n\n(not generated: no runtime method mapping yet)"


def test_preview_returns_full_text_when_under_max_length():
    engine = ContentEngine()
    result = engine.create(ContentType.EDUCATION, title="Title", body="short body")
    assert engine.preview(result) == "Title\n\nshort body"


def test_preview_truncates_and_appends_ellipsis_when_over_max_length():
    engine = ContentEngine()
    result = engine.create(ContentType.EDUCATION, title="Title", body="x" * 300)
    preview = engine.preview(result, max_length=50)
    assert len(preview) == 50
    assert preview.endswith("…")


def test_validate_true_for_accepted_result_with_title_and_body():
    engine = ContentEngine()
    result = engine.create(ContentType.EDUCATION, title="Title", body="Body")
    assert engine.validate(result) is True


def test_validate_false_for_unaccepted_result():
    result = ContentResult(
        accepted=False, content_type="AI_MARKET_REPORT", title="Market Report",
        body=None, reason="rejected", generated_at="2026-01-01T00:00:00+00:00",
    )
    engine = ContentEngine()
    assert engine.validate(result) is False


def test_validate_false_when_body_is_empty():
    result = ContentResult(
        accepted=True, content_type="EDUCATION", title="Title",
        body="", reason="created directly, no AI generation", generated_at="2026-01-01T00:00:00+00:00",
    )
    engine = ContentEngine()
    assert engine.validate(result) is False


def test_history_starts_empty():
    engine = ContentEngine()
    assert engine.history() == ()


def test_history_records_every_create_call_oldest_first():
    engine = ContentEngine()
    first = engine.create(ContentType.EDUCATION, title="First", body="1")
    second = engine.create(ContentType.MARKET_UPDATE, title="Second", body="2")

    history = engine.history()

    assert history == (first, second)


def test_deterministic_methods_never_call_ai_service():
    """create/format/preview/validate/history never touch AIService -- verified by never passing an ai_context, unlike generate()."""
    engine = ContentEngine()
    result = engine.create(ContentType.EDUCATION, title="no ai_context needed", body="deterministic only")
    assert engine.validate(result) is True
    assert engine.preview(result) is not None
    assert len(engine.history()) == 1
