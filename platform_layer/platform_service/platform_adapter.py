"""
Platform Layer — Platform Adapter interface (TASK-002D, per the
approved `docs/NAVIGATION_ARCHITECTURE.md` §8 and Director's TASK-002D
brief: "Platform Layer ichidagi adapter integratsiyasi").

**Interface only.** `PlatformAdapterBase` is an abstract contract for
what a per-platform adapter must implement -- there is no concrete
Telegram/Android/iOS/Desktop/Mini-App subclass in this file or
anywhere in this task. Building a concrete `TelegramAdapter` would
mean importing `telegram/` types, which is exactly the boundary this
module (and every other file in `platforms/`) stays on the far side
of; that wiring is a future, separately-authorized task per ADR-003's
own framing ("today's Telegram code still creates its own Reply
Keyboards directly, unchanged, until a future, separately-approved
task adapts it").

The Adapter touches UI only, never Business Logic (Director's Q2
answer at TASK-002B): `UI -> Platform Adapter -> Navigation Core ->
Application -> Business Logic`. Concretely, a subclass's job is to
turn a `platform_layer.platform_service.menu_registry.MenuDefinition` (what `NavigationCore`
resolved) into whatever that platform's real UI actually shows -- it
never itself decides permission, never itself holds Navigation State,
and never calls into Business Logic directly (ADR-001's Universal UI
Abstraction rule).

No hardcoded platform-specific logic in *this* file -- each concrete
subclass, when one is eventually built, is where a specific
platform's own behavior lives; this file defines only the shared shape
every one of them must implement.

Foundation Reuse Audit (Constitution Article 11): no prior Foundation/
Manager/Contract/Model/Capability/Registry defines a cross-platform
adapter interface in this repo -- `platform_layer/telegram/reply_keyboard_manager.py`/
`platform_layer/telegram/keyboards.py` are a concrete, Telegram-specific
implementation of what an adapter eventually does, not a reusable
abstract contract.

Never imports `telegram/`, `database/`, or any Trading Core package.
"""

from abc import ABC, abstractmethod

from platform_layer.platform_service.menu_registry import MenuDefinition


class PlatformAdapterBase(ABC):
    """Every concrete platform adapter (none exist yet) implements these three methods; nothing here renders anything itself."""

    @abstractmethod
    def render_screen(self, screen: MenuDefinition) -> None:
        """Show the given screen using this platform's own real UI. Never constructs a Screen itself (ADR-003) -- only renders one NavigationCore already resolved."""

    @abstractmethod
    def render_permission_denied(self) -> None:
        """Show this platform's own "not allowed" UI. Called only after NavigationCore.navigate() returns a PERMISSION_DENIED result -- never a pre-check performed by the adapter itself."""

    @abstractmethod
    def render_navigation_failed(self, message: str) -> None:
        """Show this platform's own error UI for an unregistered screen or an empty back-stack. `message` is the human-readable reason NavigationCore already computed -- never fabricated by the adapter."""
