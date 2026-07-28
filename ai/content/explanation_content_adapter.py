"""
AI Layer — Explanation-to-Content Adapter (Phase 63.1, TASK 6).

`ai/content/`, `broadcast/`, `media/`, `translation/` are not touched
by this phase (per the brief's own "buzilmaydi" rule) -- this is a
one-way adapter from `ExplanationOutput` into the existing
`ai.content.broadcast_output.BroadcastReadyContent` contract
(Phase 61.5), reusing it rather than inventing a parallel
"ContentInput" shape (Article 7/11 Reuse Principle). Nothing calls
this adapter from a live process loop this phase -- foundation only.
"""

from datetime import datetime, timezone

from ai.content.broadcast_output import BroadcastReadyContent
from ai.explanation.explanation_output import ExplanationOutput


def explanation_to_broadcast_ready(explanation: ExplanationOutput) -> BroadcastReadyContent:
    """Never raises: every `ExplanationOutput` has a non-empty `title`/`body` by construction, so this never needs to reject one the way `ai.content.broadcast_output.prepare_broadcast()` rejects a non-accepted `ContentResult`."""
    content_type = explanation.content_type.value if explanation.content_type else "EXPLANATION"
    return BroadcastReadyContent(
        content_type=content_type,
        title=explanation.title,
        body=explanation.body,
        prepared_at=datetime.now(timezone.utc).isoformat(),
        provider_name=None,
    )
