"""Phase 61.1 TASK 7 — AI Context Version. Additive, backwards compatible."""

from ai.context.context_builder import build_ai_context


def test_default_context_has_version_1_0():
    ctx = build_ai_context()
    assert ctx.schema_version == "1.0"
    assert ctx.context_version == "1.0"


def test_context_version_is_settable():
    ctx = build_ai_context(context_version="2.0")
    assert ctx.context_version == "2.0"
    assert ctx.schema_version == "1.0"


def test_to_dict_includes_version_fields():
    ctx = build_ai_context()
    data = ctx.to_dict()
    assert data["schema_version"] == "1.0"
    assert data["context_version"] == "1.0"


def test_built_at_still_serves_as_created_at():
    ctx = build_ai_context()
    assert ctx.built_at is not None
