"""
AI Layer — Trading Analyst Content Integration (Phase 66.0: AI
Trading Analyst Foundation, TASK 8).

`prepare_content()` composes three real, unmodified functions/methods
— zero new business logic, the exact same Content -> Media -> Broadcast
sequence `ai_layer/ai_engine/intelligence_runtime.py`'s `IntelligenceRuntime.run()`
already uses for its own CONTENT/MEDIA/BROADCAST stages:

    ContentEngine.create()                        (existing, Phase 61.5)
    media.media_pipeline.prepare_media_from_content()  (existing, Phase 63.7)
    broadcast.broadcast_adapter.broadcast_asset_from_content_and_media()
        + BroadcastManager.prepare_broadcast()     (existing, Phase 63.8)

`ContentType.LIVE_ANALYSIS` (Phase 63.8) is reused as-is for a
`TradingAnalysis` — no new `ContentType` member needed.

This is the one file in `ai/trading_analyst/` permitted to import
`ai.content/`, `media/`, and `broadcast/` — `models.py`, `access.py`,
and `analyst_runtime.py` never do.
"""

from typing import Optional

from ai_layer.ai_service.content.content_adapter import ContentEngine
from ai_layer.ai_service.content.content_schema import ContentResult
from ai_layer.ai_service.content.content_type_vocabulary import ContentType
from ai_layer.ai_engine.trading_analyst.models import TradingAnalysis
from media_layer.telegram_broadcast.broadcast_adapter import broadcast_asset_from_content_and_media
from media_layer.telegram_broadcast.broadcast_manager import BroadcastManager
from media_layer.telegram_broadcast.models import BroadcastAsset
from media_layer.content_manager.media_manager import MediaManager
from media_layer.content_manager.media_pipeline import prepare_media_from_content
from media_layer.content_manager.media_types import MediaType
from media_layer.content_manager.models import MediaAsset


def trading_analysis_to_content_body(analysis: TradingAnalysis) -> str:
    """Pure formatting -- joins strengths/weaknesses/recommendation into one plain-text body, no new reasoning."""
    lines = [analysis.summary]
    if analysis.strengths:
        lines.append("Strengths: " + "; ".join(analysis.strengths))
    if analysis.weaknesses:
        lines.append("Weaknesses: " + "; ".join(analysis.weaknesses))
    lines.append(analysis.recommendation)
    if analysis.educational_note:
        lines.append(analysis.educational_note)
    return "\n".join(lines)


def prepare_content(
    analysis: TradingAnalysis,
    content_engine: ContentEngine,
    media_manager: MediaManager,
    broadcast_manager: BroadcastManager,
) -> Optional[BroadcastAsset]:
    """
    Never raises: any non-accepted stage returns None rather than
    fabricating a downstream asset -- same posture
    `IntelligenceRuntime.run()`'s own MEDIA/BROADCAST stages already
    use.
    """
    content_result: ContentResult = content_engine.create(
        ContentType.LIVE_ANALYSIS,
        title=f"{analysis.symbol} Trading Analysis",
        body=trading_analysis_to_content_body(analysis),
    )
    if not content_result.accepted:
        return None

    media_asset: Optional[MediaAsset] = prepare_media_from_content(content_result, media_manager, media_type=MediaType.TEXT)
    if media_asset is None:
        return None

    broadcast_asset = broadcast_asset_from_content_and_media(
        content_result, media_asset, broadcast_manager, broadcast_type=ContentType.LIVE_ANALYSIS,
    )
    if broadcast_asset is None:
        return None
    return broadcast_manager.prepare_broadcast(broadcast_asset)
