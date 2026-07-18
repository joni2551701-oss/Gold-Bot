"""Phase 63.7 TASK 4/5 — media/media_adapter.py and media/media_pipeline.py: Content (upstream, type-only) integration."""

from ai.content.content_schema import ContentResult
from media.media_adapter import content_result_to_media_asset
from media.media_manager import MediaManager
from media.media_pipeline import prepare_media_from_content
from media.media_types import MediaType
from media.models import MediaAssetStatus


def _accepted_result(**overrides):
    defaults = dict(
        accepted=True, content_type="AI_MARKET_REPORT", title="Gold Report",
        body="Bullish on H1.", reason="ok", generated_at="2026-01-01T00:00:00+00:00",
    )
    defaults.update(overrides)
    return ContentResult(**defaults)


def test_content_result_to_media_asset_reads_title_and_body():
    manager = MediaManager()
    result = _accepted_result()

    asset = content_result_to_media_asset(result, manager)

    assert asset is not None
    assert asset.title == "Gold Report"
    assert asset.description == "Bullish on H1."
    assert asset.content_id == "AI_MARKET_REPORT"
    assert asset.media_type == MediaType.TEXT


def test_content_result_to_media_asset_carries_metadata():
    manager = MediaManager()
    result = _accepted_result(metadata={"provider": "gemini"})
    asset = content_result_to_media_asset(result, manager)
    assert asset.metadata == {"provider": "gemini"}


def test_content_result_to_media_asset_returns_none_for_rejected_result():
    manager = MediaManager()
    result = ContentResult(
        accepted=False, content_type="AI_MARKET_REPORT", title="Gold Report",
        body=None, reason="no runtime method mapping yet", generated_at="2026-01-01T00:00:00+00:00",
    )
    assert content_result_to_media_asset(result, manager) is None


def test_content_result_to_media_asset_returns_none_for_accepted_but_empty_body():
    manager = MediaManager()
    result = _accepted_result(body=None)
    assert content_result_to_media_asset(result, manager) is None


def test_content_result_to_media_asset_accepts_explicit_media_type():
    manager = MediaManager()
    result = _accepted_result()
    asset = content_result_to_media_asset(result, manager, media_type=MediaType.IMAGE)
    assert asset.media_type == MediaType.IMAGE


def test_prepare_media_from_content_returns_a_ready_asset_for_text():
    manager = MediaManager()
    result = _accepted_result()
    asset = prepare_media_from_content(result, manager)
    assert asset.status == MediaAssetStatus.READY


def test_prepare_media_from_content_returns_a_rejected_asset_for_disabled_type():
    manager = MediaManager()
    result = _accepted_result()
    asset = prepare_media_from_content(result, manager, media_type=MediaType.VIDEO)
    assert asset.status == MediaAssetStatus.REJECTED


def test_prepare_media_from_content_returns_none_for_rejected_content_result():
    manager = MediaManager()
    result = ContentResult(
        accepted=False, content_type="AI_MARKET_REPORT", title="Gold Report",
        body=None, reason="rejected", generated_at="2026-01-01T00:00:00+00:00",
    )
    assert prepare_media_from_content(result, manager) is None


def test_media_adapter_module_never_imports_translation_or_broadcast():
    """Per the Intelligence Dependency Principle, media/ may read ai.content (upstream) but must never import translation/broadcast (downstream/parallel)."""
    import ast
    import pathlib

    for filename in ("media_adapter.py", "media_pipeline.py"):
        module_file = pathlib.Path(__file__).resolve().parents[2] / "media" / filename
        tree = ast.parse(module_file.read_text(), filename=str(module_file))
        forbidden_prefixes = ("translation", "broadcast")
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert not alias.name.startswith(forbidden_prefixes), f"{module_file}: {alias.name}"
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    assert not node.module.startswith(forbidden_prefixes), f"{module_file}: {node.module}"
