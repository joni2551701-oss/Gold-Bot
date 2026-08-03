# V2 Phase 6 Freeze

Status: **FROZEN**. Type: Freeze Phase (Audit + Cleanup + Documentation
only). No new feature, no new module, no new handler, no new router,
no Trading Core change, no Reply Menu design change happened in this
phase — confirmed section by section below.

Scope authorized by the Director: `telegram/`, `translation/`,
`tests/`, `docs/`.

---

## Executive Summary

Phase 6 (Interactive Navigation Framework) closes with this document.
It ran across four sub-phases:

| Sub-phase | Delivered |
|---|---|
| 6.0 Navigation Audit | `docs/PHASE6_NAVIGATION_AUDIT.md` — architecture survey, identified the inline-callback gap and the missing Back/Home concept |
| 6.1 → 6.1.1 → 6.3 Navigation Framework | Reply Keyboard established as GoldBot's sole navigation mechanism (`platform_layer/telegram/reply_keyboard_manager.py`); Phase 6.1's inline edit-in-place Navigation Controller (`telegram/navigation.py`) was built, then retired outright by Phase 6.3's Director-approved "Dynamic Reply Keyboard Navigation" decision |
| 6.2 Settings Callback Completion | `docs/PHASE6_2_SETTINGS_CALLBACK_COMPLETION.md` — wired the four remaining "dead" inline callbacks (`risk_*`/`strategy_*`/`timeframe_*`/`notifications_*`) to real DB updates, current-value display, and in-place picker redraw |
| **6 Freeze** (this document) | Full audit, two-line cleanup, and this freeze record |

Net result: every Settings/Profile/Signals/Admin/Owner screen the
Reply Keyboard exposes today is fully wired end-to-end — no dead
callback, no orphan handler, no unresolved navigation path. The one
remaining unreachable UI surface (`platform_layer/telegram/keyboards.py`'s
Phase-40-era inline Settings/Admin pickers) is confirmed intentionally
retained, not a defect (see Stage 1 below).

This document is the authoritative current-state record for Phase 6;
`docs/PHASE6_NAVIGATION_AUDIT.md` remains as the Stage-0 historical
snapshot per this repo's established `*_AUDIT.md` → `*_FREEZE.md`
convention (see every prior Phase's docs for the same pattern).

---

## Stage 1 — Repository Freeze Audit

Full findings in `docs/PHASE6_FREEZE_AUDIT.md` (9 findings, F1-F9).
Summary: no duplicate translation keys, no missing-language entries,
1:1 command↔handler wiring (one expected exception), no duplicate test
names, pyflakes clean. One confirmed-intentional unreachable UI pair
(`keyboards.settings_keyboard()`/`admin_panel_keyboard()`, already
self-documented as deliberately retained). One genuine orphan removed:
`nav.back`/`nav.home` translation keys, debris from the already-deleted
`telegram/navigation.py` module that Phase 6.3's "INLINE CLEANUP" pass
missed.

---

## Stage 2 — Telegram UI Audit

Every Reply Keyboard section and every lifecycle transition was traced
through `platform_layer/telegram/command_router.py`, `platform_layer/telegram/handlers.py`,
`platform_layer/telegram/reply_keyboard_manager.py`, and `platform_layer/telegram/polling.py`.

### Section inventory (confirmed live, all six)

| Section | Keyboard builder | Commands routed to it |
|---|---|---|
| Main | `reply_keyboard_manager.main_keyboard()` (tier-aware: USER/ADMIN/OWNER superset via `platform_layer.telegram.keyboards.reply_keyboard/admin_reply_keyboard/owner_reply_keyboard`) | `/start`, and the implicit default for any command not listed in `_SECTION_BY_COMMAND` |
| Settings | `settings_keyboard()` | `/settings`, `/language`, `/risk`, `/strategy`, `/timeframe`, `/notifications` |
| Admin | `admin_submenu_keyboard()` | `/admin`, `/users`, `/stats`, `/system`, `/broadcast`, `/removeadmin` |
| Owner | `owner_submenu_keyboard()` | `/owner`, `/runtime`, `/health`, `/performance`, `/errors`, `/pipeline`, `/report` |
| Profile | `profile_keyboard()` | `/profile`, `/subscription` |
| Signals | `signals_keyboard()` | `/signal`, `/history`, `/upgrade` |

Every section keyboard's action buttons resolve through
`_SECTION_LABEL_KEYS` (a `command -> translation key` map, localized
across EN/UZ/RU) and every section carries a trailing "◀️ Ortga" row
(`rkm.back`), confirmed rendered by `_submenu_rows()` for every section
except Profile, which builds its rows inline with the identical
pattern (2 action buttons instead of a `_submenu_rows()`-eligible even
count, so it is hand-built — same shape, same trailing Back row,
verified by reading `profile_keyboard()` directly).

### Keyboard switching

`command_router.route_command()`'s tail (lines 263-291) decides the
outgoing keyboard in exactly three ways, verified mutually exclusive
by reading the branch structure:

1. `command == "start"` → `_start_keyboard()` (registration-step-aware,
   see below).
2. `command` is a Settings/Risk/Strategy/Timeframe/Notifications/
   Language inline value-picker (`_KEYBOARD_BY_COMMAND`) → the inline
   `InlineKeyboardMarkup` picker, `selected=` pre-marked to the
   caller's current DB value. The Reply Keyboard section tracker is
   deliberately left untouched here (confirmed by comment and code —
   an inline picker is a value choice, not a screen transition).
3. Everything else → `reply_keyboard_manager.keyboard_for_command()`,
   which looks up the command's section (default Main), calls that
   section's builder, and records the resulting section via
   `record_section()`.

### `ReplyKeyboardRemove`

Two, and only two, code paths ever send `ReplyKeyboardRemove()`,
confirmed by a repo-wide search for the symbol:

- `command_router._start_keyboard()` — a BANNED user's `/start` reply
  (checked first, independent of registration step).
- `command_router.route_contact()` — the phone-share reply, the instant
  registration completes (Director Decision 7's explicit two-message
  "remove, then reattach" sequence — see Registration below).

### Registration Wizard lifecycle

`/start`'s keyboard depends on `RegistrationStep`
(`platform_layer/telegram/registration_service.py`), read via
`handlers._registration_step()`:

```
new user  --/start-->  LANGUAGE  --(lang_xx tap)-->  PHONE  --(share contact)-->  COMPLETE
              |                        |                         |
       language_keyboard()    phone_share_keyboard()      Main Reply Keyboard
```

- `LANGUAGE` step → `language_keyboard()` (inline picker).
- `PHONE` step → `phone_share_keyboard()` (a `ReplyKeyboardMarkup` with
  one `request_contact=True` button, `one_time_keyboard=True` — hides
  itself after one tap).
- `COMPLETE` (or any OWNER/ADMIN account, checked before Wizard step —
  see `_start_keyboard()`'s Phase 6.1.1 bugfix docstring) →
  `reply_keyboard_manager.main_keyboard()`.

### Phone Share → Registration Complete sequence

`route_contact()` validates `contact.user_id == telegram_id` (rejects
a forwarded stranger's contact card), calls
`handlers.contact_handler()` (which internally calls
`RegistrationService.complete()`), then branches:

- Registration did **not** complete this call (e.g. phone already
  registered elsewhere) → plain text reply, no keyboard change.
- Registration **did** complete → `RouterResult(keyboard=
  ReplyKeyboardRemove(), followup=RouterResult(text=
  "navigation.menu_ready", keyboard=main_keyboard()))`. `polling.py`'s
  `_deliver()` sends both as two independent, individually-guarded
  messages (a failure in one never silently drops the other).

### BANNED lifecycle

A BANNED account is stopped in three independent, defense-in-depth
places, confirmed by reading each:

1. `handlers.start_handler()` — checked before `touch_activity()` or
   `SubscriptionService` are ever called; returns `start.banned` text.
2. `command_router._start_keyboard()` — `handlers._is_banned()` checked
   first, before registration-step or OWNER/ADMIN tier logic; returns
   `ReplyKeyboardRemove()` unconditionally.
3. `handlers._registration_step()` returns `None` for a BANNED account
   too (it can't distinguish BANNED from COMPLETE on its own — this is
   why check #2 exists as an independent, authoritative check rather
   than relying on this fallthrough).

### Restart (`/start` on an existing account)

`register_user()`'s "already exists" branch carries the already-fetched
profile (no second query for the BANNED check). A non-BANNED existing
user hits `touch_activity()` (promotes NEW→ACTIVE, updates
`last_activity`) and gets `start.already_exists` text plus whatever
keyboard `_start_keyboard()` resolves to for their current tier/step
(almost always Main, since a returning user is COMPLETE).

**Stage 2 conclusion: no gap.** Every state (new/mid-wizard/complete/
banned/owner/admin) has an unambiguous keyboard resolution path, and
every transition between them was traced to a specific line of code.

---

## Stage 3 — Navigation Audit

Every Main ↔ submenu transition, traced through
`reply_keyboard_manager.resolve_navigation_command()` and
`keyboard_for_command()`:

```
                    ┌────────────────────────────────────────────┐
                    │                    MAIN                     │
                    │  🏠 Home  👤 Profil  📊 Signal  💳 Obuna     │
                    │  ⚙️ Sozlamalar  ❓ Yordam  [🛠Admin][👑Owner] │
                    └───┬────────┬─────────┬──────────┬───────┬──┘
                        │        │         │          │       │
                 ⚙️Sozlamalar 👤Profil  📊Signal  🛠Admin  👑Owner
                        ▼        ▼         ▼          ▼       ▼
                 ┌──────────┐┌────────┐┌────────┐┌────────┐┌────────┐
                 │ SETTINGS ││PROFILE ││SIGNALS ││ ADMIN  ││ OWNER  │
                 │ Til      ││Profil  ││Live    ││Users   ││Runtime │
                 │ Risk     ││Obuna   ││History ││Stats   ││Health  │
                 │ Strategy ││        ││Premium ││System  ││Perf    │
                 │ Timeframe││        ││        ││Broadcast││Errors │
                 │ Notif.   ││        ││        ││Admin Mgmt││Pipeline│
                 │ ◀️Ortga  ││◀️Ortga ││◀️Ortga ││◀️Ortga ││Reports │
                 └────┬─────┘└───┬────┘└───┬────┘└───┬────┘│◀️Ortga │
                      │          │         │         │     └───┬────┘
                      └──────────┴─────────┴─────────┴─────────┘
                                    ◀️ Ortga (always -> /start -> MAIN)
```

Findings:

- **Every submenu's "◀️ Ortga" resolves unconditionally to `/start`**
  (`reply_keyboard_manager._BACK_LABELS`/`resolve_navigation_command()`
  — checked first, before section-specific lookup, and independent of
  `current_section()`), confirmed against Director Decision:
  *"Alohida Home tugmasi kerak emas. Ortga -> Main Keyboard."* No
  section has a different Back target.
- **Two-tier resolution, confirmed non-conflicting**: Main-tier labels
  (Home/Profile/Signals/Subscription/Settings/Help/Admin/Owner) are
  resolved by `platform_layer.telegram.keyboards.resolve_navigation_command()` first;
  only if that returns `None` does `command_router.route_command()`
  fall back to `reply_keyboard_manager.resolve_navigation_command()`
  for a submenu-section label. No label exists in both maps (verified
  by the `_REPLY_LABEL_KEYS` vs. `_SECTION_LABEL_KEYS` key sets — zero
  overlap), so there is no ambiguity to resolve.
- **Admin Management does not directly perform an action** — the Admin
  submenu's "Admin Management" button maps to `/admin` (re-opens the
  Admin Panel text listing, itself containing a "👑 Admin Management"
  line), never directly to `/addadmin` — Director Review correction 1,
  confirmed still in place in `_SECTION_LABEL_KEYS[SECTION_ADMIN]`.
- **Profile has no Statistics button** — Director Review correction 2
  (Variant B), confirmed: `profile_keyboard()` hand-builds exactly two
  rows (Profile, Subscription) plus Back, no Statistics entry anywhere
  in Profile's map.
- **Section tracking is process-local, with a safe fallback** —
  `_LAST_SECTION` is an in-memory dict (never persisted), so a stray
  or post-restart submenu-label tap with no tracked section falls back
  to a check across every section's map (first hit wins) rather than
  failing to resolve — confirmed in
  `resolve_navigation_command()`'s tail loop.
- **Inline pickers do not change section** — tapping a Risk/Strategy/
  Timeframe/Notifications option redraws that same inline keyboard in
  place (Phase 6.2's edit-in-place, `callback_router._handle_setting()`)
  and never touches `record_section()` — confirmed by reading
  `command_router.py`'s `_KEYBOARD_BY_COMMAND` branch, which has no
  `record_section()` call, unlike the `else` branch.

**Stage 3 conclusion: no dead end, no ambiguous transition, no
orphaned Back target.**

---

## Stage 4 — Translation Freeze

AST-parsed `media_layer/translation/ui_catalog.py`'s `_CATALOG` (post-cleanup: 111
keys, was 113 before Stage 9's two-key removal):

| Check | Result |
|---|---|
| Duplicate dict keys | 0 |
| Keys missing EN | 0 |
| Keys missing UZ | 0 |
| Keys missing RU | 0 |
| Keys with zero references outside `ui_catalog.py` | 0 (post-cleanup; was 2: `nav.back`/`nav.home`) |

Namespace breakdown (111 keys):

| Prefix | Count | Owner |
|---|---|---|
| `keyboard.*` | 22 | Inline picker button labels (language/risk/timeframe/strategy/notifications) |
| `rkm.*` | 21 | Reply Keyboard Manager submenu labels (Settings/Admin/Owner/Profile/Signals) |
| `menu.*` | 8 | Main-tier Reply Keyboard + Persistent Menu labels |
| `notifications.*` | 7 | `/notifications` command replies |
| `contact.*` | 6 | Phone-share flow replies |
| `language.*` | 4 | `/language` command replies |
| `risk.*` / `strategy.*` / `timeframe.*` | 4 each | Settings sub-command replies |
| `start.*` | 4 | `/start` replies (created/already_exists/banned/error) |
| `common.*` | 3 | Shared fallbacks (`na`/`on`/`off`) |
| `feedback.*` / `profile.*` / `signal.*` | 3 each | Their respective command replies |
| `settings.*` | 2 | `settings.menu` (current-value display) + `settings.saved` (Phase 6.2) |
| `plan.*` / `subscription.*` | 2 each | Plan/subscription replies |
| `about.*` / `help.*` / `history.*` / `navigation.*` / `registration.*` / `status.*` / `upgrade.*` | 1 each | Single-string replies |

**Stage 4 conclusion: catalog is clean and fully covered.** No
follow-up action needed beyond Stage 9's two-key removal (already
reflected in the counts above).

---

## Stage 5 — Reply Menu Freeze

**Director decision, recorded here as binding for the remainder of V2:**
the current Main Reply Keyboard layout is frozen. Future modules do
not trigger a menu redesign — they occupy a reserved slot (Stage 6)
and ship as a **Coming Soon** placeholder until their real handler
exists, at which point that same button is rewired to the live module.
This is the GoldBot UI Stability Principle the Director named when
approving this Freeze phase; it is recorded here and is intended for
formal inclusion in GoldBot Constitution v2.0.

Current Main Reply Keyboard (tier-aware; USER shown, ADMIN adds
🛠 Admin, OWNER adds 🛠 Admin + 👑 Owner — unchanged from Phase 5.1's
own superset policy):

```
🏠 Home        👤 Profile
📊 Signals     💳 Subscription
⚙️ Settings    ❓ Help
```

The Director's target future layout for V2 (from the Phase 6 Freeze
task) additionally names: 📈 Chart, 🤖 AI Assistant, 📰 News,
📅 Calendar, 🎓 Academy, 💎 Premium. **None of these six exist as Reply
Keyboard buttons today** — they are not implemented in this phase
(Phase 6 Freeze is audit/cleanup only, no new feature). Their landing
slots and Coming Soon behavior are Stage 6's Future Module Reservation
Table; actually adding a "Coming Soon" placeholder button for each is
explicitly out of scope for this Freeze (it would be a Reply Menu
change, disallowed by this phase's own rules) and is deferred to
whichever future phase the Director schedules for the "Coming Soon
Framework" step of the roadmap.

---

## Stage 6 — Future Module Reservation Table

Per the Director's list. "Reserved slot" records intent, not a live
UI element — no button exists for any of these yet (adding one would
be a Reply Menu design change, out of scope for this Freeze).

| Module | Reserved section | Status | Landing command (future) |
|---|---|---|---|
| Chart | Main (new button) | Not started | `/chart` |
| AI Assistant | Main (new button) | Foundation exists (`assistant/`, `ai/conversation/`, `voice/`) — not Telegram-wired | `/assistant` |
| AI Analyst | Main or AI Assistant sub-flow | Foundation exists (`ai/trading_analyst/`) — not Telegram-wired | via AI Assistant |
| Economic Calendar | Main (new button) | Not started (fundamental data exists in `context_layer/fundamental/economic_events.py`, no Telegram surface) | `/calendar` |
| News Center | Main (new button) | Not started | `/news` |
| Academy | Main (new button) | Foundation exists (`ai/learning/`) — not Telegram-wired | `/academy` |
| Analytics | Owner submenu (extend) | Partially live (`/performance`, `/report` exist under Owner) | already reachable |
| Portfolio | Main or Profile sub-flow | Foundation exists (`ai/portfolio/`) — not Telegram-wired | `/portfolio` |
| Trade Journal | Main or Profile sub-flow | Foundation exists (`ai/trade_journal/`) — not Telegram-wired | `/journal` |
| Trade Replay | Owner submenu (extend) | Foundation exists (`backtesting/replay_*`, `platform_layer/telegram/owner/replay_commands.py`) — Owner-only, not Reply-Keyboard-wired | already partially reachable (Owner tier) |
| Market Scanner | Main (new button) | Not started | `/scanner` |
| Notifications Center | Settings sub-flow (extend) | Partially live (`/notifications` on/off exists; no per-category center) | already reachable |
| Community | Main (new button) | Not started | `/community` |
| Marketplace | Main (new button) | Not started | `/marketplace` |
| Settings | Settings section | **Live** | `/settings` |
| Premium | Signals submenu (existing: "💎 Premium" → `/upgrade`) | **Live** | already reachable |

Two rows ("Settings", "Premium") are already fully live and listed
here only because the Director's module list named them explicitly —
no reservation action needed for those two.

---

## Stage 7 — Trading Core Verification

```
git diff --cached --stat -- core/ decision/ risk/ execution/ strategies/ signals/ context/ ai/ database/
```

Empty result (verified as part of this phase's own Commit Protocol
run, see Final section below). No file under `core/`, `decision/`,
`risk/`, `execution/`, `strategies/`, `signals/`, `context/`, `ai/`,
or `database/` was read for modification or changed during this
Freeze — every change in this phase is confined to `translation/
ui_catalog.py` (Stage 9's two-line removal) and `docs/` (this
document plus `docs/PHASE6_FREEZE_AUDIT.md`).

**ZERO DIFF confirmed.**

---

## Stage 8 — Test Audit

Full suite: `python -m pytest tests/` → **4609 passed**, 0 failures,
run both before and after Stage 9's cleanup (identical result — the
removed translation keys had no test referencing them, confirming
Stage 1's F2 finding was accurate before any code was touched).

`tests/telegram/` alone: 465 tests across 13 files:

| File | Tests | Covers |
|---|---|---|
| `test_polling.py` | 42 | Dispatcher wiring, `_deliver()`, startup notification, heartbeat, secret presence |
| `test_keyboards.py` | 38 | Every inline/reply keyboard builder, localization, `selected=` radio markers, navigation map |
| `test_callback_router.py` | 30 | `lang_*` + `risk_*`/`strategy_*`/`timeframe_*`/`notifications_*` dispatch, edit-in-place, never-raises |
| `test_phone_registration.py` | 26 | Registration Wizard phone step, contact ownership validation, **BANNED** |
| `test_runtime_monitor.py` | 23 | Telegram runtime status/heartbeat (not UI, adjacent) |
| `test_settings_callbacks.py` | 18 | `risk_status`/`strategy_status`/`timeframe_status`/`notifications_status`, DB persistence, translation coverage |
| `test_menu_commands.py` | 14 | Persistent Menu (Phase 4) registration |
| `test_language_handler.py` | 13 | `language_status`/`language_handler` |
| `test_registration_service.py` | 10 | Wizard state machine, **BANNED** interaction |
| `test_ai_dashboard_commands.py` | 9 | AI Owner dashboard dispatch |
| `test_ai_command_permission_matrix.py` | 7 | **ADMIN**/**OWNER** tier gating for AI commands |
| `test_runtime_owner_dispatch.py` | 4 | Owner runtime command dispatch |
| `test_ai_explanation_status_dispatch.py` | 1 | AI explanation status dispatch |

Plus `tests/platform_layer/telegram/owner/` (27 files, one per `platform_layer/telegram/owner/*.py`
module — Admin/Owner command surface, already exercised by prior
phases' own Commit Protocols, unmodified and re-verified passing in
this phase's full-suite run).

**BANNED** coverage confirmed present in `test_keyboards.py`,
`test_phone_registration.py`, `test_registration_service.py` (`grep
-rli banned`). Coverage matches Stage 2/3's traced lifecycle: no gap
between what was audited and what is tested.

---

## Stage 9 — Cleanup

Exactly one change, directly evidenced by Stage 1's F2 finding:
removed the orphaned `nav.back`/`nav.home` translation keys (2 lines)
from `media_layer/translation/ui_catalog.py` — debris from the already-deleted
`telegram/navigation.py` module. No test referenced either key; the
full suite (4609 tests) passes unchanged before and after.

No other cleanup action was taken. Stage 1's other findings (F1, F3-F9)
were each confirmed either intentional, already correct, or a false
positive — see `docs/PHASE6_FREEZE_AUDIT.md` for the evidence behind
each. No new feature, module, handler, or router was created; no
Trading Core file was touched; no Reply Menu design changed.

---

## Remaining Known Limitations

- `platform_layer/telegram/keyboards.py`'s `settings_keyboard()`/`admin_panel_keyboard()`
  remain in the codebase, unreachable from routing, kept only for their
  own isolated test coverage (Stage 1 F1). A future phase may choose to
  remove them outright once Constitution v2.0's cleanup posture is
  decided — deliberately left untouched in this Freeze rather than
  making that call unilaterally.
- The six future-module Reply Keyboard buttons named in Stage 5
  (Chart/AI Assistant/News/Calendar/Academy — Premium already exists)
  do not exist yet, not even as "Coming Soon" placeholders. Adding them
  is explicitly deferred to the "Coming Soon Framework" step of the
  Director's own roadmap, not this Freeze.
- Several Stage 6 modules (AI Assistant, AI Analyst, Portfolio, Trade
  Journal, Academy) have real backend foundations already built in
  prior phases but zero Telegram-facing entry point — this is expected
  (those were explicitly scoped as "not live-wired" scaffolding in
  their own phases) and not a Phase 6 regression.

---

## Freeze Decision

Phase 6 (Interactive Navigation Framework) is **FROZEN**, effective at
the commit that includes this document. All ten stages' exit criteria
are met:

- Repository Audit ✅ (`docs/PHASE6_FREEZE_AUDIT.md`)
- Telegram UI Audit ✅ (Stage 2)
- Navigation Audit ✅ (Stage 3)
- Translation Audit ✅ (Stage 4)
- Future Module Reservation ✅ (Stage 6)
- Trading Core Zero-Diff ✅ (Stage 7)
- Test Audit ✅ (Stage 8 — 4609/4609)
- Cleanup ✅ (Stage 9 — two-line orphan removal)
- `docs/PHASE6_FREEZE.md` ✅ (this document)
- GitHub CI / Production Deployment — pending confirmation on the
  commit that includes this document (see the Worker's final report).

Per the Director's own roadmap, **GoldBot Constitution v2.0** begins
next.
