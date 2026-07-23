# V2 Phase 6 Freeze — Stage 1: Repository Freeze Audit

Status: **AUDIT ONLY**. Per the Director's Phase 6 Freeze instruction,
no new feature, no new module, no new handler, no new router, and no
Trading Core or Reply Menu design change happened while producing this
document. Repository inspection only.

Scope: `telegram/`, `translation/`, `tests/`, `docs/`.

## Method

For every top-level symbol (function, class, translation key) in the
audited scope, this pass cross-referenced its usage across the entire
repository (not just the defining file) via `grep`/AST parsing, to
distinguish real dead code from a symbol that is simply consumed by
name in another module. `python -m pyflakes $(git ls-files '*.py')`
(already clean, confirmed again below) covers unused imports; this
audit covers the class of issue pyflakes cannot see — unused
functions, unused translation keys, and duplicate/superseded logic.

## Findings

### F1 — `telegram/keyboards.py`: `settings_keyboard()` and `admin_panel_keyboard()` are unreachable from routing — CONFIRMED INTENTIONAL, no action

Neither function is imported by `telegram/command_router.py`,
`telegram/callback_router.py`, or `telegram/handlers.py`. Both are
superseded: `settings_keyboard()` (Phase 40's inline Settings hint) by
`telegram.reply_keyboard_manager.settings_keyboard()` (Phase 6.3's
Settings submenu Reply Keyboard); `admin_panel_keyboard()` (a
Phase 1.5 placeholder, never wired to a real Admin Panel UI) by
`telegram.reply_keyboard_manager.admin_submenu_keyboard()`.

This audit confirms the leftover is **already documented as
deliberate** in `telegram/keyboards.py`'s own module docstring (Phase
6.2): *"settings_keyboard() (the old inline Settings hint) is
superseded by telegram.reply_keyboard_manager's Settings Reply
Keyboard section (V2 Phase 6.3) -- it stays in place, unreferenced by
routing, only for its own isolated tests."* Both functions retain
dedicated test coverage in `tests/telegram/test_keyboards.py`
(4 tests). Removing a function whose retention was a specific,
recorded Director-era decision is not a Freeze-stage cleanup action —
**no change made.**

### F2 — `translation/ui_catalog.py`: `nav.back` / `nav.home` are genuinely orphaned — cleaned up (Stage 9)

`grep -rlE` across every `.py` file for `nav.back`/`nav.home` (as a
quoted string literal, either quote style) found **zero** references
outside `translation/ui_catalog.py` itself. Their own inline comment
attributes them to *"V2 Phase 6.1 -- Navigation Controller ... See
telegram/navigation.py"* — that module was deleted outright when V2
Phase 6.3 (Director Approved: Dynamic Reply Keyboard Navigation)
retired the inline Navigation Controller (`telegram/
reply_keyboard_manager.py`'s own docstring: *"This retires Phase 6.1's
inline Navigation Controller entirely (telegram/navigation.py,
EDITABLE_COMMANDS, edit-in-place delivery, nav_back/nav_home
callbacks) -- Director's explicit 'INLINE CLEANUP' instruction."*).
Confirmed via `ls telegram/navigation.py` (does not exist) and a
repo-wide search for `EDITABLE_COMMANDS`/`nav_back`/`nav_home`/
`MessageLifecycleTracker` (only the retirement narration in
`reply_keyboard_manager.py`'s docstring remains). No test references
either key. Unlike F1, no comment marks this pair as intentionally
retained — it is debris the Phase 6.3 "INLINE CLEANUP" pass missed.
**Removed in Stage 9** (see below) — a two-line, zero-blast-radius
deletion consistent with the Phase 6.3 cleanup this omission belongs
to.

### F3 — Two `resolve_navigation_command()` functions, two `settings_keyboard()` names — CONFIRMED cooperating layers, not duplication

`telegram/keyboards.py` and `telegram/reply_keyboard_manager.py` each
define a `resolve_navigation_command()`. These are **not** duplicate
logic: `keyboards.resolve_navigation_command()` resolves Main-tier
labels (Home/Profile/Signals/Subscription/Settings/Help/Admin/Owner —
Phase 5.1's `NAVIGATION_MAP`), while `reply_keyboard_manager.
resolve_navigation_command()` resolves submenu labels (Settings/Admin/
Owner/Profile/Signals section buttons — Phase 6.3's `_SECTION_MAPS`).
`command_router.route_command()` tries the first, then falls back to
the second — both are live, both are necessary, confirmed by reading
`command_router.py:234-238`. Likewise `reply_keyboard_manager.py`
imports `reply_keyboard()`/`admin_reply_keyboard()`/
`owner_reply_keyboard()` from `keyboards.py` and wraps them in
`main_keyboard()` — reuse, not duplication (the module's own docstring
cites this as a deliberate Module Reuse Principle application). Also
confirmed: `settings_keyboard` exists in both modules by name, but
`keyboards.settings_keyboard()` is F1's dead inline picker while
`reply_keyboard_manager.settings_keyboard()` is the live Settings
submenu Reply Keyboard — same name, unrelated, non-conflicting
(different modules, never imported together under the same name). **No
action.**

### F4 — Command ↔ Handler wiring: 1:1, no orphans

Cross-referenced every command name across `telegram/commands.py`'s
`COMMANDS`/`OWNER_COMMANDS`/`ADMIN_COMMANDS` (50 distinct commands)
against every `async def *_handler(...)` in `telegram/handlers.py` (51
functions). Every command has a matching handler. The one handler with
no command entry, `contact_handler`, is expected — it is not a
`/command`, it is `telegram.command_router.route_contact()`'s target
for a `Message.contact` payload (phone-share button), documented as
such in its own docstring. **No orphan handlers, no missing
handlers.**

### F5 — Translation catalog: no duplicate keys, no missing-language entries

AST-parsed `translation/ui_catalog.py`'s `_CATALOG` dict (113 keys):
zero duplicate dict keys (a duplicate would have silently shadowed the
first at Python parse time — none exist), zero keys missing any of
EN/UZ/RU. Full detail in Stage 4's Translation Coverage Report below.

### F6 — Service-layer result/config dataclasses: false-positive check, no action

An automated same-module-only-reference scan flagged `UserServiceResult`,
`PhoneRegistrationResult`, `NotificationServiceResult`,
`AdminStatistics`, `UserSummary`, `SystemStatus`, `BroadcastResult`,
`SignalServiceResult`, `SubscriptionServiceResult`,
`FeedbackServiceResult`, `FormatterConfig`, `NotifierConfig`,
`NotifierResult`, `ResultHandlerConfig`, `ResultHandlerResult`,
`BotConfig`, `BotResult` as having no reference outside their own
file. Manually verified: every one is a `@dataclass` return type used
by attribute access (`.success`, `.profile`, etc.) from its own
module's service methods — Python does not require importing a class
name to consume its instances by attribute, so this is expected
dataclass style, not dead code. **False positive, no action.**

### F7 — Duplicate test function names: none

Every test file in `tests/telegram/` and `tests/telegram/owner/` was
AST-parsed for `test_*` function names; no file defines the same test
name twice (a real duplicate would silently shadow the first,
reducing coverage without any visible symptom). **Clean.**

### F8 — `docs/PHASE6_NAVIGATION_AUDIT.md`: historical snapshot, not a "documentation mismatch"

This Stage-0 audit (pre-implementation) still describes `risk_*`/
`strategy_*`/`timeframe_*`/`notifications_*` as "dead callback" —
accurate for the point in time it was written, now superseded by V2
Phase 6.2 (`docs/PHASE6_2_SETTINGS_CALLBACK_COMPLETION.md`) and V2
Phase 6.3's Reply Keyboard Navigation work. This matches every other
Phase's established `*_AUDIT.md` → `*_FREEZE.md` convention in this
repo (the audit is a point-in-time snapshot; the freeze document is
the current-state summary) — not something to edit retroactively.
This document (`PHASE6_FREEZE.md`, Stage 10) is the current
authoritative state for Phase 6. **No action; documented for
clarity.**

### F9 — pyflakes: clean

`python -m pyflakes $(git ls-files '*.py')` reports nothing (re-run as
part of this audit, same as every prior phase's Commit Protocol run).
No unused imports anywhere in the repository, including the freshly
audited `telegram/`/`translation/`/`tests/` scope.

## Summary

| # | Area | Finding | Action |
|---|---|---|---|
| F1 | `keyboards.py` inline Settings/Admin pickers | Unreachable from routing, but explicitly documented as intentionally retained | None — confirmed intentional |
| F2 | `nav.back`/`nav.home` translation keys | Orphaned debris from deleted `telegram/navigation.py` | Removed (Stage 9) |
| F3 | Two `resolve_navigation_command()` / `settings_keyboard` names | Cooperating two-tier navigation, not duplication | None — confirmed by design |
| F4 | Command ↔ Handler wiring | 1:1, one expected exception (`contact_handler`) | None |
| F5 | Translation catalog structure | No duplicates, no missing languages | None |
| F6 | Service-layer dataclasses | False-positive orphan scan, all in active use | None |
| F7 | Test function names | No duplicates | None |
| F8 | `PHASE6_NAVIGATION_AUDIT.md` | Historical snapshot, matches repo convention | None |
| F9 | pyflakes | Clean | None |

Net Stage 9 cleanup from this audit: **two orphaned translation keys
removed** (`nav.back`, `nav.home`). No production code path changes as
a result — both keys had zero readers.
