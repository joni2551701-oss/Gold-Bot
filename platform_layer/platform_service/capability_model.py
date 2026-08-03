"""
Platform Layer — capability model (PLATFORM-001).

Foundation Reuse Audit (Constitution Article 11): `ai/capabilities/
capability.py`'s `Capability` enum describes an AI capability
(analysis, chart reading, etc.), not a client platform's own
per-module support status — a different concern, not a duplicate.
No existing Foundation/Manager/Contract/Model/Capability/Registry
describes "does module X work on platform Y" before this phase.

Declares the Director's required per-module x per-platform contract:
`SUPPORTED`, or `NOT_SUPPORTED`/`PLANNED` with a mandatory `reason`
(and optionally a `future_plan`) — never a bare "doesn't work" with no
explanation. `platform_layer/platform_service/cross_platform_checker.py` is the validator
that enforces the "reason required" rule; this module only defines
the shape.

Never imports `telegram/`, `database/`, or any Trading Core package.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from platform_layer.platform_service.platform_model import PlatformName


class SupportStatus(Enum):
    SUPPORTED = "SUPPORTED"
    NOT_SUPPORTED = "NOT_SUPPORTED"
    PLANNED = "PLANNED"


@dataclass(frozen=True)
class PlatformCapability:
    """
    One (module, platform) pair's support declaration. `reason` and
    `future_plan` are optional at the dataclass level -- deliberately,
    since a `SUPPORTED` entry has nothing to explain -- but
    `cross_platform_checker.check_module_capabilities()` requires
    `reason` to be non-empty for any non-SUPPORTED entry.
    """

    platform: PlatformName
    status: SupportStatus
    reason: Optional[str] = None
    future_plan: Optional[str] = None
