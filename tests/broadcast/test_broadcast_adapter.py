"""Phase 63.8 TASK 6 — broadcast/broadcast_adapter.py: Content/Media (upstream, type-only) integration, optional Persona reference."""

from ai.content.content_schema import ContentResult
from ai.content.content_types import ContentType
from ai.persona.persona_registry import SENIOR_TRADING_AI
from broadcast.broadcast_adapter import broadcast_asset_from_content_and_media
from broadcast.broadcast_manager import BroadcastManager
from broadcast.models import BroadcastStatus
from media.media_types import MediaType
from media.models import MediaAsset, MediaAssetStatus


def _accepted_result(**overrides):
    defaults = dict(
        accepted=True, content_type="AI_MARKET_REPORT", title="Gold Report",
        body="Bullish on H1.", reason="ok", generated_at="2026-01-01T00:00:00+00:00",
    )
    defaults.update(overrides)
    return ContentResult(**defaults)


def _media_asset(**overrides):
    defaults = dict(id="m1", content_id="AI_MARKET_REPORT", media_type=MediaType.TEXT, status=MediaAssetStatus.READY, title="Gold Report")
    defaults.update(overrides)
    return MediaAsset(**defaults)


def test_broadcast_asset_from_content_and_media_reads_content_id_and_media_id():
    manager = BroadcastManager()
    asset = broadcast_asset_from_content_and_media(_accepted_result(), _media_asset(), manager)

    assert asset is not None
    assert asset.content_id == "AI_MARKET_REPORT"
    assert asset.media_id == "m1"
    assert asset.status == BroadcastStatus.DRAFT


def test_broadcast_asset_from_content_and_media_carries_content_metadata():
    manager = BroadcastManager()
    result = _accepted_result(metadata={"provider": "gemini"})
    asset = broadcast_asset_from_content_and_media(result, _media_asset(), manager)
    assert asset.metadata == {"provider": "gemini"}


def test_broadcast_asset_from_content_and_media_returns_none_for_rejected_content():
    manager = BroadcastManager()
    result = ContentResult(
        accepted=False, content_type="AI_MARKET_REPORT", title="Gold Report",
        body=None, reason="no runtime method mapping yet", generated_at="2026-01-01T00:00:00+00:00",
    )
    assert broadcast_asset_from_content_and_media(result, _media_asset(), manager) is None


def test_broadcast_asset_from_content_and_media_returns_none_for_accepted_but_empty_body():
    manager = BroadcastManager()
    result = _accepted_result(body=None)
    assert broadcast_asset_from_content_and_media(result, _media_asset(), manager) is None


def test_broadcast_asset_from_content_and_media_defaults_broadcast_type_to_explanation():
    manager = BroadcastManager()
    asset = broadcast_asset_from_content_and_media(_accepted_result(), _media_asset(), manager)
    assert asset.broadcast_type == ContentType.EXPLANATION


def test_broadcast_asset_from_content_and_media_accepts_explicit_broadcast_type():
    manager = BroadcastManager()
    asset = broadcast_asset_from_content_and_media(
        _accepted_result(), _media_asset(), manager, broadcast_type=ContentType.MARKET_UPDATE,
    )
    assert asset.broadcast_type == ContentType.MARKET_UPDATE


def test_broadcast_asset_from_content_and_media_reads_persona_name_type_only():
    manager = BroadcastManager()
    asset = broadcast_asset_from_content_and_media(
        _accepted_result(), _media_asset(), manager, persona=SENIOR_TRADING_AI,
    )
    assert asset.persona_name == "Senior Trading AI"


def test_broadcast_asset_from_content_and_media_persona_name_is_none_without_persona():
    manager = BroadcastManager()
    asset = broadcast_asset_from_content_and_media(_accepted_result(), _media_asset(), manager)
    assert asset.persona_name is None


def test_broadcast_adapter_module_never_imports_decision_risk_execution():
    """Rule 3: broadcast/ may read media/, ai/content/, ai/ (type-only) -- never decision/risk/execution/strategies/signals."""
    import ast
    import pathlib

    adapter_file = pathlib.Path(__file__).resolve().parents[2] / "broadcast" / "broadcast_adapter.py"
    tree = ast.parse(adapter_file.read_text(), filename=str(adapter_file))
    forbidden_prefixes = ("decision", "risk", "execution", "strategies", "signals", "database", "telegram")
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert not alias.name.startswith(forbidden_prefixes), alias.name
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                assert not node.module.startswith(forbidden_prefixes), node.module
