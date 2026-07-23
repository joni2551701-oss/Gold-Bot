"""
Platform Layer — Universal Navigation model (PLATFORM-001).

A platform-agnostic navigation-tree contract: `NavigationNode` names a
screen/section by id and permission, lists which platforms it applies
to, and nests children -- no Telegram-specific concept (no
`callback_data`, no Reply Keyboard row, no aiogram type) anywhere in
this file.

**Foundation only, deliberately unwired.** This does NOT replace or
modify `telegram/reply_keyboard_manager.py` or `telegram/keyboards.py`
-- the Telegram product layer's Reply Keyboard remains GoldBot's sole
live navigation mechanism, and its layout is frozen per
`docs/PHASE6_FREEZE.md` Stage 5 (Director decision). This module is
not imported by any `telegram/*.py` file in this phase. A future,
separately-authorized task would adapt the live Telegram navigation
to consume this tree (or not) -- that decision is out of scope here.

Foundation Reuse Audit (Constitution Article 11): no prior Foundation/
Manager/Contract/Model/Capability/Registry describes a platform-
agnostic navigation tree in this repo -- `telegram/reply_keyboard_manager.py`
and `telegram/keyboards.py` are Telegram-specific implementations, not
a reusable cross-platform contract.

Never imports `telegram/`, `database/`, or any Trading Core package.
"""

from dataclasses import dataclass, field
from typing import List

from platforms.platform_model import PlatformName


@dataclass(frozen=True)
class NavigationNode:
    """
    id: a stable, unique node identifier (not a Telegram command name
    -- a future adapter maps id -> command/screen per platform).
    label_key: a translation-catalog key (see `translation/ui_catalog.py`'s
    `t()`), not a literal string -- keeps this contract localizable the
    same way the existing Telegram UI already is.
    permission: a tier label ("USER"/"ADMIN"/"OWNER") matching
    `telegram/permissions.py`'s `PermissionLevel` values by convention,
    not by import -- this module has no dependency on `telegram/`.
    """

    id: str
    label_key: str
    permission: str
    platforms: List[PlatformName] = field(default_factory=list)
    children: List["NavigationNode"] = field(default_factory=list)
