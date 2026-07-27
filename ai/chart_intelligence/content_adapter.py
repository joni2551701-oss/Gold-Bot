"""
AI Layer — Chart Intelligence Content Integration (Phase 66.1: AI
Chart Intelligence Foundation, TASK 6).

`prepare_content()` composes the same three real, unmodified Content
-> Media -> Broadcast functions `ai/trading_analyst/content_adapter.py`
and `ai/intelligence_runtime.py` already use -- zero new business
logic:

    ContentEngine.create()                              (existing, Phase 61.5)
    media.media_pipeline.prepare_media_from_content()    (existing, Phase 63.7)
    broadcast.broadcast_adapter.broadcast_asset_from_content_and_media()
        + BroadcastManager.prepare_broadcast()           (existing, Phase 63.8)

`ContentType.LIVE_ANALYSIS` (Phase 63.8, already reused by Phase 66.0's
own `TradingAnalysis` content integration) is reused a second time here
-- no new `ContentType` member (Module Reuse Principle, see
`docs/PHASE66_1_AUDIT.md`). `MediaType.IMAGE` (Phase 63.0) is used
instead of `MediaType.TEXT` -- a Chart Analysis is visually sourced,
even though this Foundation never stores the image itself.

This is the one file in `ai/chart_intelligence/` permitted to import
`ai.content/`, `media/`, and `broadcast/` -- `models.py`, `access.py`,
`chart_runtime.py`, `trading_analyst_adapter.py`, and
`vision_provider_types.py` never do.
"""

from typing import Optional

from ai.chart_intelligence.models import ChartAnalysis
from ai.content.content_adapter import ContentEngine
from ai.content.content_schema import ContentResult
from ai.content_types import ContentType
from broadcast.broadcast_adapter import broadcast_asset_from_content_and_media
from broadcast.broadcast_manager import BroadcastManager
from broadcast.models import BroadcastAsset
from media.media_manager import MediaManager
from media.media_pipeline import prepare_media_from_content
from media.media_types import MediaType
from media.models import MediaAsset


def chart_analysis_to_content_body(analysis: ChartAnalysis) -> str:
    """Pure formatting -- joins every populated field into one plain-text body, no new reasoning. Never returns an empty string: an analysis with no populated fields falls back to a bare "{symbol} {timeframe} chart analysis" line (same non-empty-body guarantee `ai/trading_analyst/content_adapter.py`'s own always-present `recommendation` field gives that package)."""
    lines = []
    if analysis.market_structure:
        lines.append(f"Market Structure: {analysis.market_structure}")
    if analysis.trend:
        lines.append(f"Trend: {analysis.trend}")
    if analysis.liquidity:
        lines.append(f"Liquidity: {analysis.liquidity}")
    if analysis.order_blocks:
        lines.append("Order Blocks: " + "; ".join(analysis.order_blocks))
    if analysis.fvg:
        lines.append("FVG: " + "; ".join(analysis.fvg))
    if analysis.support:
        lines.append("Support: " + "; ".join(analysis.support))
    if analysis.resistance:
        lines.append("Resistance: " + "; ".join(analysis.resistance))
    if analysis.notes:
        lines.append(analysis.notes)
    if not lines:
        lines.append(f"{analysis.symbol} {analysis.timeframe} chart analysis")
    return "\n".join(lines)


def prepare_content(
    analysis: ChartAnalysis,
    content_engine: ContentEngine,
    media_manager: MediaManager,
    broadcast_manager: BroadcastManager,
) -> Optional[BroadcastAsset]:
    """
    Never raises: any non-accepted stage returns None rather than
    fabricating a downstream asset -- same posture
    `ai/trading_analyst/content_adapter.py`'s own `prepare_content()`
    already uses.
    """
    content_result: ContentResult = content_engine.create(
        ContentType.LIVE_ANALYSIS,
        title=f"{analysis.symbol} Chart Analysis ({analysis.timeframe})",
        body=chart_analysis_to_content_body(analysis),
    )
    if not content_result.accepted:
        return None

    media_asset: Optional[MediaAsset] = prepare_media_from_content(content_result, media_manager, media_type=MediaType.IMAGE)
    if media_asset is None:
        return None

    broadcast_asset = broadcast_asset_from_content_and_media(
        content_result, media_asset, broadcast_manager, broadcast_type=ContentType.LIVE_ANALYSIS,
    )
    if broadcast_asset is None:
        return None
    return broadcast_manager.prepare_broadcast(broadcast_asset)
