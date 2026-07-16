"""
AI Layer — AI Runtime Request (Phase 61.2: AI Runtime Foundation,
TASK 6).

The one input shape `ai.runtime.ai_service.AIService.ask()` accepts --
composes already-existing foundation types
(`ai.capabilities.capability.Capability`, `ai.context.context_snapshot.AIContext`,
`ai.access.permissions.AIRole`) rather than re-declaring any of them.
"""

from dataclasses import dataclass
from typing import Optional

from ai.access.permissions import AIRole
from ai.capabilities.capability import Capability
from ai.context.context_snapshot import AIContext


@dataclass(frozen=True)
class RuntimeRequest:
    """
    prompt: explicit prompt text override. When omitted, `AIService`
        derives one from `ai_context.market_context` via
        `ai.prompts.prompt_manager.PromptManager` (the existing
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
