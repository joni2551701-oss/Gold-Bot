"""
Platform Layer — Universal Navigation model (PLATFORM-001; extended
TASK-002C per the approved `docs/NAVIGATION_ARCHITECTURE.md` and
ADR-002 Universal Screen Identity).

A platform-agnostic navigation-tree contract: `NavigationNode` names a
screen/section by id and permission, lists which platforms it applies
to, and nests children -- no Telegram-specific concept (no
`callback_data`, no Reply Keyboard row, no aiogram type) anywhere in
this file.

**Foundation only, deliberately unwired.** This does NOT replace or
modify `platform_layer/telegram/reply_keyboard_manager.py` or `platform_layer/telegram/keyboards.py`
-- the Telegram product layer's Reply Keyboard remains GoldBot's sole
live navigation mechanism, and its layout is frozen per
`docs/PHASE6_FREEZE.md` Stage 5 (Director decision). This module is
not imported by any `telegram/*.py` file in this phase. A future,
separately-authorized task would adapt the live Telegram navigation
to consume this tree (or not) -- that decision is out of scope here.

Foundation Reuse Audit (Constitution Article 11): no prior Foundation/
Manager/Contract/Model/Capability/Registry describes a platform-
agnostic navigation tree in this repo -- `platform_layer/telegram/reply_keyboard_manager.py`
and `platform_layer/telegram/keyboards.py` are Telegram-specific implementations, not
a reusable cross-platform contract.

Never imports `telegram/`, `database/`, or any Trading Core package.
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional

from platform_layer.platform_service.platform_model import PlatformName

# ADR-002 Universal Screen Identity: dotted, lowercase, "<category>.<name>"
# -- e.g. "settings.language", "signals.upgrade". Stable across every
# platform; never changes per platform (ADR-002's own wording).
_SCREEN_ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)+$")


def is_valid_screen_id(screen_id: str) -> bool:
    """
    Never raises: a non-string or empty input simply returns False.
    Checked explicitly against new TASK-002C registry entries (see
    `platform_layer/platform_service/menu_registry.py`'s `DEFAULT_MENUS`) -- not enforced
    retroactively inside `NavigationNode`/`MenuDefinition` construction,
    since TASK-001's already-approved, frozen registrations predate
    ADR-002 and are not required to be renamed to match it (No Silent
    Decisions Policy: retroactively rejecting a previously-valid id
    would be a breaking contract change, which this function does not
    attempt).
    """
    if not isinstance(screen_id, str) or not screen_id:
        return False
    return bool(_SCREEN_ID_PATTERN.match(screen_id))


@dataclass(frozen=True)
class NavigationNode:
    """
    id: a stable, unique node identifier -- new callers should follow
    ADR-002's Universal Screen Identity convention
    (`is_valid_screen_id()` above), though this is not enforced at
    construction time (see that function's own docstring for why).
    label_key: a translation-catalog key (see `media_layer/translation/ui_catalog.py`'s
    `t()`), not a literal string -- keeps this contract localizable the
    same way the existing Telegram UI already is.
    permission: a tier label ("USER"/"ADMIN"/"OWNER") matching
    `platform_layer/telegram/permissions.py`'s `PermissionLevel` values by convention,
    not by import -- this module has no dependency on `telegram/`.
    category: which section this node groups under (e.g. "settings",
    "signals") -- the Screen Model concept from
    `docs/NAVIGATION_ARCHITECTURE.md` §2, added TASK-002C. `None` when
    not yet categorized (fully optional, additive field).
    content_type: what kind of content this screen shows (e.g. "list",
    "form", "message") -- data-driven, never a rendering instruction.
    Added TASK-002C, fully optional.
    """

    id: str
    label_key: str
    permission: str
    platforms: List[PlatformName] = field(default_factory=list)
    children: List["NavigationNode"] = field(default_factory=list)
    category: Optional[str] = None
    content_type: Optional[str] = None
