"""
Platform Layer — platform model (PLATFORM-001: Platform Foundation &
Collaboration Infrastructure).

Foundation Reuse Audit (Constitution Article 11), all six "no":
1. Foundation — no `platforms/`-shaped package existed before this
   phase (confirmed by repo-wide search).
2. Manager — no `PlatformManager`/equivalent existed.
3. Contract — no dataclass describing a client platform existed.
4. Model — none.
5. Capability — `ai/capabilities/capability.py`'s `Capability` enum
   describes an AI capability, not a client platform; unrelated
   concern.
6. Registry — no platform registry existed (see
   `platform_layer/platform_service/platform_registry.py`'s own audit note).

Named `platforms/` (plural), not `platform/`, to avoid shadowing the
Python standard library's own `platform` module — a top-level
`platform/` package would take priority over the stdlib module for
any `import platform` in this process (repo root is on `sys.path`
when running `main.py`/pytest from the repo root). No current file in
this repo imports the stdlib module, but a future dependency doing so
would break silently; the plural name avoids the collision entirely
while keeping this repo's existing plural-package convention
(`assets/`, `strategies/`, `signals/`).

This module holds metadata only — it does not run, install, or ship
any client. It never imports `telegram/`, `database/`, or any Trading
Core package.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class PlatformName(Enum):
    TELEGRAM_BOT = "TELEGRAM_BOT"
    TELEGRAM_MINI_APP = "TELEGRAM_MINI_APP"
    ANDROID = "ANDROID"
    IOS = "IOS"
    DESKTOP = "DESKTOP"


class PlatformStatus(Enum):
    LIVE = "LIVE"
    PLANNED = "PLANNED"
    NOT_STARTED = "NOT_STARTED"


@dataclass(frozen=True)
class PlatformDefinition:
    """
    One client platform's own metadata record. `features` is a plain
    list of short capability labels (e.g. "signal_delivery",
    "settings") — a free-text summary for humans reading the
    registry, not a machine-checked contract; `platforms/
    capability_registry.py` is the machine-checked, per-module version
    of the same concern.
    """

    name: PlatformName
    status: PlatformStatus
    version: str
    features: List[str] = field(default_factory=list)
    compatibility: Optional[str] = None
