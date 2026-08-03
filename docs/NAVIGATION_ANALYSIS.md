# Navigation Analysis (TASK-002A)

Step 1 of `docs/PLATFORM_WORKFLOW.md`'s "Architecture First" process,
applied to Navigation (TASK-002). **This document proposes nothing.**
It records what exists today, what a genuinely cross-platform
Navigation needs to account for, and the open questions TASK-002B
(Navigation Architecture) must resolve — with Director approval —
before any design decision is made.

## 1. What exists today (Telegram-specific, live)

Two cooperating maps, both in the Telegram product layer:

- **Main tier** — `platform_layer/telegram/keyboards.py`'s `NAVIGATION_MAP`: six
  USER-tier destinations (Home/Profile/Signals/Subscription/Settings/
  Help), ADMIN adds "Admin", OWNER adds "Owner" — a fixed superset per
  tier, built from `_REPLY_LABEL_KEYS` (command → `media_layer/translation/ui_catalog.py`
  key).
- **Submenu tier** — `platform_layer/telegram/reply_keyboard_manager.py`'s
  `_SECTION_BY_COMMAND`/`_SECTION_LABEL_KEYS`: five submenus (Settings/
  Admin/Owner/Profile/Signals), each a fixed list of action buttons
  plus one trailing "◀️ Ortga" (Back) row that unconditionally returns
  to `/start` → Main (Director decision: no separate Home button).

**Mechanism**: a Telegram Reply Keyboard is a physical on-screen
keyboard whose buttons send their label text as an ordinary chat
message. Navigation is resolved by **text lookup**, not a UI event:
`resolve_navigation_command()` (two implementations — one per tier)
maps a localized label string back to a `"/command"` string, which
`command_router.route_command()` then dispatches exactly as if typed.
Per-chat "current submenu" state (`_LAST_SECTION`) is process-local,
in-memory only — never persisted, lost on restart (a documented,
accepted fallback: an untracked tap searches every section's map,
first hit wins).

**What it resolves to**: a `"/command"` string — i.e., Telegram
navigation's destination type is "a command name," not a generic
screen identifier.

**Full trace, section builders, keyboard-switching rule, and BANNED/
registration-wizard interaction**: `docs/PLATFORM_ARCHITECTURE.md` §5,
`docs/PHASE6_FREEZE.md` Stages 2–3 (already-verified, current state —
not re-derived here).

**Frozen by Director decision** (`docs/PHASE6_FREEZE.md` Stage 5): the
current Reply Keyboard layout does not change to accommodate a future
module. A new module gets a reserved slot / "Coming Soon" placeholder
until wired — never a menu redesign. This freeze is a hard constraint
on TASK-002B, not something Navigation work reopens.

**Test coverage today**: `tests/telegram/test_keyboards.py` (38
tests), navigation-relevant slices of `tests/telegram/test_polling.py`/
`test_phone_registration.py`/`test_registration_service.py` (per
`docs/PHASE6_FREEZE.md` Stage 8) — whatever TASK-002B proposes must
not require any of these to change unless the Director separately
authorizes touching `platform_layer/telegram/reply_keyboard_manager.py` or
`platform_layer/telegram/keyboards.py`.

## 2. What TASK-001 already built (foundation, unwired)

`platform_layer/platform_service/navigation_model.py`'s `NavigationNode` (id, label_key,
permission, platforms, children) — a static, platform-agnostic tree
*description*. It is not a state machine, has no label-resolution
logic, no per-user "current position" concept, and is not populated
with GoldBot's real menu tree yet (`docs/PLATFORM_FOUNDATION.md`'s own
"Known Limitations" already says so). `platform_layer/platform_service/menu_registry.py`'s
`MenuDefinition`/`MenuRegistry` is the adjacent, also-unpopulated
registry for the same real tree.

## 3. Gaps between "what exists" and "universal," by concern

Recorded as open questions, not answered here — TASK-002B decides:

**a. Destination type.** Telegram resolves to a `"/command"` string.
Android/iOS/Desktop would resolve to a screen/route/window, not a
command string. `NavigationNode.id` is already command-agnostic, but
nothing today maps an `id` to a per-platform concrete target. Whether
that mapping is part of Navigation itself or a separate, later concern
is undecided.

**b. Navigation shape.** Telegram's model is **flat and mode-switching**:
tapping a submenu button replaces the entire physical keyboard;
"Back" always returns to Main, never to an intermediate screen — there
is no multi-level stack, no breadcrumb, no arbitrary depth. Native
apps conventionally use a **real navigation stack** (arbitrary depth,
Back returns to the actual previous screen). `NavigationNode.children`
already allows nesting — but nothing states whether that nesting means
"Telegram-style flat sections" or "native-style deep stack," and those
are genuinely different behaviors, not just different renderings of
the same idea.

**c. State locality.** Telegram's "current section" is process-local,
in-memory, per `telegram_id`. A cross-platform model must decide
whether navigation position is tracked per-client (each platform keeps
its own local state, as Telegram does today) or centrally (a shared
"where is this user" record `platforms/` or `database/` holds). This
changes where state lives and who can read/write it — a real
architectural choice, not a detail.

**d. Permission resolution.** `NavigationNode.permission` is a plain
string matching `platform_layer/telegram/permissions.py`'s `PermissionLevel` values
"by convention," not by import (confirmed in the model's own
docstring — `platforms/` has zero dependency on `telegram/`). Today,
tier resolution happens once, inside the Telegram process
(`get_permission_level()`). Whether every future client independently
resolves its own tier, or a shared resolution point is needed, is open.

**e. Onboarding/lifecycle gating is not a Navigation concept today —
it's baked into Telegram's own keyboard-selection code.** Registration
Wizard step (LANGUAGE/PHONE/COMPLETE) and BANNED status both override
normal keyboard resolution inside `command_router._start_keyboard()`
(`docs/PHASE6_FREEZE.md` Stage 2) — neither is expressed anywhere in
`NavigationNode`. Whether a universal model absorbs this gating or
treats it as a client-specific pre-check that runs *before* consulting
Navigation is undecided.

**f. Localization already generalizes cleanly.** `label_key` already
follows the `media_layer/translation/ui_catalog.py` convention — no gap here, both
existing Telegram maps and the new foundation model agree on this
point.

## 4. A named risk: designing for platforms that don't exist yet

Only Telegram Bot is `LIVE` (`platform_layer/platform_service/platform_registry.py`,
TASK-001); Telegram Mini App, Android, iOS, and Desktop are all
`NOT_STARTED` — zero code, zero UI framework chosen, zero constraints
known. A "universal" architecture designed against four platforms with
no real requirements yet is unvalidated by construction — the same
kind of mistake the Director is trying to avoid by staging this task
carefully, just from the opposite direction (guessing wrong now vs.
moving too fast now). Worth naming as an open question for TASK-002B:
should the architecture target genuine universality immediately, or
validate against the next concrete platform on the roadmap (Telegram
Mini App, v0.8) before generalizing further to Android/iOS/Desktop,
none of which have a chosen tech stack yet?

## Open questions for TASK-002B (not answered here)

1. Destination type: command string, generic route id, or both via an
   adapter?
2. Flat mode-switch (Telegram's actual UX) vs. real navigation stack —
   does `NavigationNode.children` mean one, the other, or must it
   support both per-platform?
3. Where does "current position" state live — per-client or central?
4. Does permission-tier resolution stay per-client, or centralize?
5. Does onboarding/BANNED gating belong inside Navigation, or stay an
   adjacent, client-specific pre-check?
6. Validate against Telegram Mini App next, or design for all five
   platforms at once?

## Constraints TASK-002B must not violate

- No change to `platform_layer/telegram/reply_keyboard_manager.py`'s or
  `platform_layer/telegram/keyboards.py`'s live behavior without a separate, explicit
  Director decision — the Phase 6 Freeze stands.
- No Reply Menu layout change (Director's UI Stability Principle).
- Stays foundation-only unless the Director explicitly authorizes live
  wiring.
- Any new public API, contract change, or folder-structure change
  TASK-002B's architecture proposes requires a
  `communication/decisions/PROPOSED-DECISION-XXXX.md` ticket and
  Director approval before TASK-002D (Implementation) starts, per the
  No Silent Decisions Policy.

## Related

- `docs/PLATFORM_ARCHITECTURE.md` §5 — the live Telegram navigation
  system in full.
- `docs/PHASE6_FREEZE.md` — the freeze this analysis treats as a hard
  constraint.
- `docs/PLATFORM_FOUNDATION.md` — `platform_layer/platform_service/navigation_model.py`'s
  own known limitations, restated here in more detail.
- `communication/task_queue/TASK-002A.md` — this task's own record.
