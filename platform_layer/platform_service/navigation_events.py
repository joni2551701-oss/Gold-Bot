"""
Platform Layer — Navigation Event Bus interface (TASK-002C, per
ADR-004: `communication/decisions/ADR-004.md`).

**Interface only — no dispatcher, no publish/subscribe implementation,
no wired consumer.** This defines the event vocabulary every platform
will eventually emit; it does not deliver, queue, or store a single
event. Matches this repo's own "foundation, not wired yet" posture at
introduction (`assets/`, `configuration/`, `platforms/` itself in
PLATFORM-001).

Foundation Reuse Audit (Constitution Article 11): no prior Foundation/
Manager/Contract/Model/Capability/Registry describes a navigation
event vocabulary in this repo -- `monitoring/`'s existing event-shaped
tables (`monitoring_error_events`, `monitoring_decision_pipeline`) are
Trading Core / system observability, not Platform navigation; a
distinct concern, not a duplicate.

Never imports `telegram/`, `database/`, or any Trading Core package.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from platform_layer.platform_service.platform_model import PlatformName


class NavigationEventType(Enum):
    """The fixed vocabulary named in ADR-004 -- every platform emits from this same set, never its own ad hoc event names."""

    SCREEN_OPENED = "ScreenOpened"
    SCREEN_CLOSED = "ScreenClosed"
    BACK_PRESSED = "BackPressed"
    PERMISSION_DENIED = "PermissionDenied"
    NAVIGATION_FAILED = "NavigationFailed"
    DEEP_LINK_OPENED = "DeepLinkOpened"
    SESSION_EXPIRED = "SessionExpired"


@dataclass(frozen=True)
class NavigationEvent:
    """
    A single navigation event envelope. `screen_id` is the
    ADR-002 Universal Screen ID this event concerns, when applicable
    (e.g. `None` for a `SESSION_EXPIRED` event, which concerns no
    specific screen). `details` is a free-text, optional explanation
    (e.g. a `NavigationFailed` event's reason) -- never structured data
    a future consumer is expected to parse; a richer contract is a
    future task's decision, not this one's.
    """

    event_type: NavigationEventType
    platform: PlatformName
    screen_id: Optional[str] = None
    details: Optional[str] = None
