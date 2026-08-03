"""
AI Layer — AI Runtime Request (Phase 61.2: AI Runtime Foundation,
TASK 6).

The one input shape `ai_layer.ai_engine.runtime.ai_service.AIService.ask()` accepts --
composes already-existing foundation types
(`ai_layer.ai_engine.capabilities.capability.Capability`, `ai_layer.ai_engine.context.context_snapshot.AIContext`,
`ai_layer.ai_service.access.permissions.AIRole`) rather than re-declaring any of them.
"""

from dataclasses import dataclass
from typing import Optional

from ai_layer.ai_service.access.permissions import AIRole
from ai_layer.ai_engine.capabilities.capability import Capability
from ai_layer.ai_engine.context.context_snapshot import AIContext


@dataclass(frozen=True)
class RuntimeRequest:
    """
    prompt: explicit prompt text override. When omitted, `AIService`
        derives one from `ai_context.market_context` via
        `ai_layer.ai_engine.prompts.prompt_manager.PromptManager` (the existing
        template registry, reused rather than re-implemented) --
        required for a capability with no market context available
        (e.g. free-form CHAT).
    telegram_id: optional, carried through to `ai/audit/` logging and
        `ai/access/usage_limits.UsageLimiter` -- never used for
        anything else.
    """
    capability: Capability
    ai_context: AIContext
    role: AIRole
    prompt: Optional[str] = None
    telegram_id: Optional[str] = None
