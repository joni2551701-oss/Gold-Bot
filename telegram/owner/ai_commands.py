"""
Telegram Layer — Owner AI Commands (Phase 61.4: AI Product & Control
Layer, TASK 3; extended TASK 6; extended Phase 61.5: AI Production
Integration Foundation, TASK 2/3 -- `ai_health()` added, and this
module is now REGISTERED into `telegram/commands.py`'s
`OWNER_COMMANDS` and called from real `telegram/handlers.py` handler
functions).

Real, tested, standalone service-shaped functions. Mirrors
`telegram/owner/provider_commands.py`'s own shape (standalone
functions returning a small "never raises" result object) rather than
inventing a new pattern. Every `ai/` object is injectable -- this
module never constructs a live `AIService` or reaches into its
internal state; it formats already-built `ProviderManager`/
`ProviderHealthTracker`/`CapabilityManager`/`UsageLimiter` instances a
caller passes in.
"""

from typing import Dict, Optional

from ai.access.permissions import AIRole
from ai.access.usage_limits import UsageLimiter
from ai.audit.provider_stats import ProviderStats
from ai.audit.usage_accounting import UserUsageStats
from ai.capabilities.capability import Capability
from ai.capabilities.capability_manager import CapabilityManager
from ai.providers.provider_health import ProviderHealthTracker
from ai.providers.provider_manager import ProviderManager
from ai.router.provider_score import score_providers
from ai.router.routing_rules import get_candidate_providers
from core.logger import setup_logger

logger = setup_logger("AICommands")

_ROLE_ALIASES = {role.value.lower(): role for role in AIRole}


class AICommandResult:
    """Never raises: every function below returns one of these, matching telegram/owner/provider_commands.py's ProviderCommandResult convention."""

    def __init__(self, success: bool, message: str):
        self.success = success
        self.message = message

    def __repr__(self):
        return f"AICommandResult(success={self.success}, message={self.message!r})"


def _resolve_role(name: str) -> Optional[AIRole]:
    return _ROLE_ALIASES.get(name.strip().lower())


def resolve_capability(name: str) -> Optional[Capability]:
    """Public (Phase 61.5 TASK 3): the future /ai_provider handler needs the same string->Capability resolution ai_disable()/ai_enable() already use -- reused, not re-implemented."""
    normalized = name.strip().upper()
    try:
        return Capability(normalized)
    except ValueError:
        return None


def ai_status(
    provider_manager: Optional[ProviderManager] = None,
    health_tracker: Optional[ProviderHealthTracker] = None,
    capability_manager: Optional[CapabilityManager] = None,
) -> AICommandResult:
    """
    The future /ai_status command's payload. "Runtime: Online" is
    derived from whether at least one registered provider is healthy
    -- never a hardcoded constant, matching this codebase's "never
    fabricate a status" convention.
    """
    provider_manager = provider_manager or ProviderManager()
    health_tracker = health_tracker or ProviderHealthTracker()
    capability_manager = capability_manager or CapabilityManager()

    try:
        names = provider_manager.list_providers()
        provider_lines = [
            f"{name.title()} {'🟢' if health_tracker.is_available(name) else '⚪'}"
            for name in names
        ]
        runtime_online = any(health_tracker.is_available(name) for name in names)

        capability_lines = [
            f"{'✅' if capability_manager.is_enabled(capability) else '❌'} {capability.value.title()}"
            for capability in Capability
        ]

        message = (
            "AI CORE STATUS\n"
            f"Runtime:\n{'🟢 Online' if runtime_online else '🔴 Offline'}\n"
            "Providers:\n" + ("\n".join(provider_lines) if provider_lines else "No providers registered.") + "\n"
            "Capabilities:\n" + "\n".join(capability_lines)
        )
        return AICommandResult(success=True, message=message)
    except Exception as e:
        logger.warning(f"ai_status failed: {e}")
        return AICommandResult(success=False, message=f"Error: {e}")


def ai_provider(
    capability: Capability,
    provider_manager: Optional[ProviderManager] = None,
    health_tracker: Optional[ProviderHealthTracker] = None,
    provider_stats: Optional[Dict[str, ProviderStats]] = None,
) -> AICommandResult:
    """
    The future /ai_provider command's payload for one capability.
    "Current"/"Fallback" come from ai/router/routing_rules.py's
    already-declared candidate order (never re-derived); "Health" is
    ai/audit/provider_stats.py's real success_rate when call history
    exists for that provider, or "N/A" when it does not -- never a
    fabricated percentage.
    """
    provider_manager = provider_manager or ProviderManager()
    health_tracker = health_tracker or ProviderHealthTracker()
    provider_stats = provider_stats or {}

    try:
        candidates = get_candidate_providers(capability)
        registered = set(provider_manager.list_providers())
        available_candidates = [
            name for name in candidates
            if name in registered and health_tracker.is_available(name)
        ]

        if not available_candidates:
            return AICommandResult(success=True, message=f"No available provider for {capability.value}.")

        current = available_candidates[0]
        fallback = available_candidates[1] if len(available_candidates) > 1 else "None"

        stats = provider_stats.get(current)
        health_display = f"{stats.success_rate * 100:.0f}%" if stats is not None else "N/A"

        message = (
            f"Current Provider:\n{current.title()}\n"
            f"Fallback:\n{fallback if fallback == 'None' else fallback.title()}\n"
            f"Health:\n{health_display}"
        )
        return AICommandResult(success=True, message=message)
    except Exception as e:
        logger.warning(f"ai_provider failed: {e}")
        return AICommandResult(success=False, message=f"Error: {e}")


def ai_disable(
    capability_name: str,
    capability_manager: Optional[CapabilityManager] = None,
) -> AICommandResult:
    """The future /ai_disable <capability> command. Unknown capability names are rejected, never silently ignored."""
    capability_manager = capability_manager or CapabilityManager()

    capability = resolve_capability(capability_name)
    if capability is None:
        return AICommandResult(success=False, message=f"Unknown capability: {capability_name}")

    try:
        capability_manager.disable(capability)
        return AICommandResult(success=True, message=f"{capability.value} disabled.")
    except Exception as e:
        logger.warning(f"ai_disable failed for {capability_name}: {e}")
        return AICommandResult(success=False, message=f"Error: {e}")


def ai_enable(
    capability_name: str,
    capability_manager: Optional[CapabilityManager] = None,
) -> AICommandResult:
    """The future /ai_enable <capability> command -- the reverse of ai_disable(), same validation."""
    capability_manager = capability_manager or CapabilityManager()

    capability = resolve_capability(capability_name)
    if capability is None:
        return AICommandResult(success=False, message=f"Unknown capability: {capability_name}")

    try:
        capability_manager.enable(capability)
        return AICommandResult(success=True, message=f"{capability.value} enabled.")
    except Exception as e:
        logger.warning(f"ai_enable failed for {capability_name}: {e}")
        return AICommandResult(success=False, message=f"Error: {e}")


def ai_limit(
    role_name: str,
    limit: int,
    usage_limiter: Optional[UsageLimiter] = None,
) -> AICommandResult:
    """The future /ai_limit <role> <n> command. Unknown role names or a negative limit are rejected."""
    usage_limiter = usage_limiter or UsageLimiter()

    role = _resolve_role(role_name)
    if role is None:
        return AICommandResult(success=False, message=f"Unknown role: {role_name}")
    if limit < 0:
        return AICommandResult(success=False, message="Limit must be zero or positive.")

    try:
        usage_limiter.set_limit(role, limit)
        return AICommandResult(success=True, message=f"{role.value} daily limit set to {limit if limit else 'unlimited'}.")
    except Exception as e:
        logger.warning(f"ai_limit failed for {role_name}={limit}: {e}")
        return AICommandResult(success=False, message=f"Error: {e}")


def ai_cost(provider_stats: Dict[str, ProviderStats]) -> AICommandResult:
    """
    The future /ai_cost command's payload -- matches the Director's
    own worked example shape exactly ("Today AI Cost: Gemini $12.40 /
    GPT $8.20 / Total $20.60"). `provider_stats` is
    `ai.audit.provider_stats.compute_provider_stats()`'s own,
    unmodified output -- this function only formats it, never
    recomputes a cost. An empty dict (no calls logged yet) reports
    $0.00, not an error.
    """
    try:
        lines = [f"{name.title()}:\n${stats.total_cost:.2f}" for name, stats in sorted(provider_stats.items())]
        total = sum(stats.total_cost for stats in provider_stats.values())
        message = "Today AI Cost:\n" + ("\n".join(lines) + "\n" if lines else "") + f"Total:\n${total:.2f}"
        return AICommandResult(success=True, message=message)
    except Exception as e:
        logger.warning(f"ai_cost failed: {e}")
        return AICommandResult(success=False, message=f"Error: {e}")


def ai_usage(telegram_id: str, user_usage: Dict[str, UserUsageStats]) -> AICommandResult:
    """
    The future /ai_usage <telegram_id> command's payload. `user_usage`
    is `ai.audit.usage_accounting.compute_user_usage()`'s own,
    unmodified output. A telegram_id with no logged calls reports zero
    usage, not an error -- absence of activity is not a failure.
    """
    try:
        stats = user_usage.get(telegram_id)
        if stats is None:
            return AICommandResult(success=True, message=f"No AI usage recorded for {telegram_id}.")

        provider_lines = "\n".join(f"{name.title()}: ${cost:.2f}" for name, cost in sorted(stats.cost_by_provider.items()))
        message = (
            f"AI Usage — {telegram_id}\n"
            f"Calls:\n{stats.total_calls}\n"
            f"Tokens:\n{stats.total_tokens}\n"
            f"Cost:\n${stats.total_cost:.2f}\n"
            f"By provider:\n{provider_lines if provider_lines else 'N/A'}"
        )
        return AICommandResult(success=True, message=message)
    except Exception as e:
        logger.warning(f"ai_usage failed for {telegram_id}: {e}")
        return AICommandResult(success=False, message=f"Error: {e}")


def ai_health(
    provider_manager: Optional[ProviderManager] = None,
    provider_stats: Optional[Dict[str, ProviderStats]] = None,
    health_tracker: Optional[ProviderHealthTracker] = None,
) -> AICommandResult:
    """
    The /ai_health command's payload (Phase 61.5 TASK 2/3). Best-first
    ranking via `ai.router.provider_score.score_providers()` --
    recommendation/analytics only, matching that module's own
    docstring: `AIRouter.route()` is never called or influenced by
    this. `provider_names` comes from `provider_manager.list_providers()`
    so a provider with zero call history still appears in the ranking.
    """
    provider_manager = provider_manager or ProviderManager()
    health_tracker = health_tracker or ProviderHealthTracker()
    provider_stats = provider_stats or {}

    try:
        names = provider_manager.list_providers()
        ranked = score_providers(names, provider_stats, health_tracker)
        lines = [
            f"{s.provider_name.title()}: {s.score:.2f} ({s.health_status.value if s.health_status else 'UNKNOWN'})"
            for s in ranked
        ]
        message = "AI Provider Health Ranking:\n" + ("\n".join(lines) if lines else "No providers registered.")
        return AICommandResult(success=True, message=message)
    except Exception as e:
        logger.warning(f"ai_health failed: {e}")
        return AICommandResult(success=False, message=f"Error: {e}")
