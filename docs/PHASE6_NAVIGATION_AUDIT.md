# V2 Phase 6 Stage 0 Audit — Interactive Navigation Framework

Status: **AUDIT ONLY**. No implementation code in this document; per
the Director's instruction, no coding, refactor, optimization,
handler modification, router modification, or database migration
happened while producing it. Repository inspection, architecture
analysis, and documentation only.

Scope authorized by the Director: `telegram/`, `translation/`,
`tests/telegram/`, `docs/`. `core/`, `decision/`, `execution/`,
`risk/`, `signals/`, `strategies/`, `context/`, `ai/`, `database/`
were not touched — confirmed at the end of this document (Section
"Trading Core Zero-Diff").

---

## Executive Summary

GoldBot's Telegram navigation today is three independently-shipped
layers that already agree on one thing: every one of them ultimately
calls `telegram.command_router.route_command()`, which calls one of
`telegram/handlers.py`'s `*_handler()` functions, which returns a
plain string. Nothing in `handlers.py` ever touches a `Message` object
directly — confirmed by a repo-wide search (zero
`.answer(`/`.edit_text(`/`.edit_reply_markup(` calls in that file).
That single fact is why a unified Navigation Framework is a **low-risk
composition problem, not a rewrite**: every proposed Phase 6 component
can sit *above* `command_router.py` and `handlers.py` without changing
either.

The three shipped layers:

- **Phase 4 — Native Telegram Menu** (`telegram/menu_commands.py`):
  registers `Bot.set_my_commands()` once at startup. A tap just sends
  the command as ordinary text — no special handling needed anywhere
  else.
- **Phase 5 — Persistent Reply Keyboard** (`telegram/keyboards.py`):
  shown once registration reaches `COMPLETE`; tier-aware
  (USER/ADMIN/OWNER), owned end-to-end by `command_router.py`.
- **Phase 5.1 — Navigation Mapping**: reply-keyboard buttons show
  localized labels; `resolve_navigation_command()` translates a tapped
  label back to its `/command` *before* `route_command()` parses it.
  This is the exact pattern this audit recommends extending to inline
  keyboards in Phase 6 (see Task 7/9).

What Phase 6 actually needs to add, and what it does not:

- **Does not need**: new handlers, a new router, a rewrite of
  `command_router.py`, or any change to Trading Core.
- **Does need**: (1) inline-keyboard callbacks currently stubbed
  (`risk_*`, `strategy_*`, `timeframe_*`, `settings_*`, `admin_*`) wired
  to real handler calls, following the exact shape
  `callback_router._handle_language()` already establishes for
  language; and (2) a small, new "edit vs. send" decision layer, since
  today *every* router-originated reply is a brand-new message except
  the one inline language-picker flow, which edits in place.

No Back/Cancel/Close/Home navigation concept exists anywhere in the
codebase today (confirmed by repo-wide search, Task 6) — this is a
gap, not a bug, and is the single largest genuinely-new piece of work
a full navigation framework would add.

---

## Task 1 — Repository Navigation Audit

Every navigation entry point found, with its file and shape:

| Entry point | File | Shape |
|---|---|---|
| Native Telegram Menu (`☰`) | `telegram/menu_commands.py` | `Bot.set_my_commands()`, USER/ADMIN/OWNER scopes, registered once at startup (`telegram/polling.py::run_polling()`) |
| Persistent Reply Keyboard | `telegram/keyboards.py` (`reply_keyboard`/`admin_reply_keyboard`/`owner_reply_keyboard`) | `ReplyKeyboardMarkup`, tier-aware, localized labels (Phase 5.1) |
| Navigation Mapping | `telegram/keyboards.py` (`NAVIGATION_MAP`/`resolve_navigation_command()`) | Stateless dict, label → `/command`, consulted by `command_router.route_command()` |
| Inline Keyboards | `telegram/keyboards.py` (`language_keyboard`, `risk_keyboard`, `strategy_keyboard`, `timeframe_keyboard`, `settings_keyboard`, `notifications_keyboard`, `admin_panel_keyboard`) | `InlineKeyboardMarkup`, `callback_data` strings |
| `/start` | `telegram/handlers.py::start_handler` + `command_router._start_keyboard()` | Registration Wizard entry point; keyboard depends on `registration_step` |
| `callback_query` | `telegram/callback_router.py::route_callback()` | Single entry point for every inline-keyboard tap; only `lang_*` implemented today |
| `RouterResult.keyboard` | `telegram/command_router.py` (`RouterResult` dataclass) | The one place any keyboard object (inline, reply, or `ReplyKeyboardRemove`) is attached to a text reply |
| `ReplyKeyboardRemove` | `telegram/command_router.py::_start_keyboard()` | BANNED-user path only (Phase 5 Decision 3) |
| `message.answer()` | `telegram/polling.py::_on_message`, `telegram/callback_router.py::_handle_language` (fallback + phone prompt) | Sends a brand-new message |
| `message.edit_text()` | `telegram/callback_router.py::_handle_language` only | The *only* place any existing code edits a message in place |
| `message.edit_reply_markup()` | **Not used anywhere in the codebase** | Confirmed absent by repo-wide search — a real gap (see Task 5) |

---

## Task 2 — Navigation Inventory

| Source | Destination | Handler | Current Keyboard | Reusable? |
|---|---|---|---|---|
| Native Menu `/start` | Registration / Home | `start_handler` | `_start_keyboard()` (LANGUAGE/PHONE/persistent/`ReplyKeyboardRemove`) | Yes — already shared |
| Native Menu `/profile` | Profile screen | `profile_handler` | None | Yes |
| Native Menu `/signal` | Latest signal | `signal_handler` | None | Yes |
| Native Menu `/subscription` | Subscription status | `subscription_handler` | None | Yes |
| Native Menu `/settings` | Settings menu | `settings_handler` | `settings_keyboard` (inline, dead callbacks) | Yes |
| Native Menu `/help` | Command reference | `help_handler` | None | Yes |
| Native Menu `/admin` (ADMIN/OWNER) | Admin panel | `admin_handler` | `admin_panel_keyboard` (inline, dead callbacks) | Yes |
| Native Menu `/owner` (OWNER) | Owner dashboard | `owner_handler` | None | Yes |
| Reply Keyboard tap (any localized label) | Same as its mapped `/command` above | Same handler, via `resolve_navigation_command()` | Same as above | Yes — this *is* the reuse pattern |
| Inline `language_keyboard` tap (`lang_uz`/`lang_ru`/`lang_en`) | Language updated | `handlers.language_status()` | Edits message in place; keyboard removed once change takes effect | Yes — working today |
| Inline `risk_keyboard`/`strategy_keyboard`/`timeframe_keyboard`/`settings_keyboard`/`notifications_keyboard`/`admin_panel_keyboard` tap | (intended: value applied) | None — `callback_router` only clears the tap spinner | N/A | **Not yet** — needs Task 7's extension |
| Phone Share Keyboard tap | Registration COMPLETE | `contact_handler` | Persistent Reply Keyboard attached directly (no explicit `ReplyKeyboardRemove` step) | Yes |
| BANNED `/start` | Blocked message | `start_handler` | `ReplyKeyboardRemove()` | Yes |

---

## Task 3 — Inline Keyboard Audit

| Keyboard | `callback_data` prefix | Category | Notes |
|---|---|---|---|
| `language_keyboard` | `lang_` | **Working** | Only fully implemented inline flow; edits message, removes keyboard on success |
| `risk_keyboard` | `risk_` | **Dead callback** | Recognized by `callback_router._RECOGNIZED_PREFIXES`, spinner cleared, no action; real change requires typing `/risk 5` |
| `strategy_keyboard` | `strategy_` | **Dead callback** | Same as above; requires typing `/strategy <name>` |
| `timeframe_keyboard` | `timeframe_` | **Dead callback** | Same as above; requires typing `/timeframe M15` |
| `settings_keyboard` | `settings_` | **Dead callback** | This is the exact gap the Director flagged in the Phase 4 Freeze's Production Manual Test finding, already roadmapped as **Phase 5.x — Settings Callback Completion** (not yet delivered) |
| `notifications_keyboard` | `notifications_` | **Future callback / orphaned** | Not even attached to any reply — `command_router._KEYBOARD_BY_COMMAND` never wires it in, so it is currently unreachable in the running system, deeper than a dead callback |
| `admin_panel_keyboard` | `admin_` | **Dead callback** | Recognized, spinner cleared, no action; real actions require typing `/users`, `/stats`, `/system`, `/broadcast` |

---

## Task 4 — Reply Keyboard Audit

- **`reply_keyboard()` / `admin_reply_keyboard()` / `owner_reply_keyboard()`**
  (`telegram/keyboards.py`): appear the moment `registration_step ==
  COMPLETE` — either on a subsequent `/start` (`_start_keyboard()`) or
  immediately on the phone-share message that completes registration
  (`route_contact()`). Owned exclusively by `command_router.py`
  (`_persistent_reply_keyboard()`); no other module attaches or clears
  it.
- **Navigation Mapping** (`NAVIGATION_MAP`/`resolve_navigation_command()`):
  stateless, built once at import time from `_REPLY_LABEL_KEYS` × 3
  languages; consulted per-call inside `route_command()`. Owns no
  runtime state.
- **Registration Keyboard** (`language_keyboard` while
  `registration_step == LANGUAGE`, `phone_share_keyboard` while
  `PHONE`): sequenced by `_START_KEYBOARD_BY_STEP` + `_start_keyboard()`,
  driven by `RegistrationService`'s DB-persisted `registration_step` —
  not in-memory state.
- **Phone Share Keyboard**: `one_time_keyboard=True` (Telegram
  client auto-hides after one tap); replaced directly by the
  persistent Reply Keyboard on a successful contact share — no
  explicit `ReplyKeyboardRemove()` call needed (Telegram platform
  constraint documented in `docs/PHASE5_AUDIT.md` Section 3: only one
  active `ReplyKeyboardMarkup` per chat, a new one silently replaces
  the old one).
- **Lifecycle ownership**: `command_router.py` is the single owner of
  every Reply Keyboard transition today (`_start_keyboard()`,
  `_persistent_reply_keyboard()`, `route_contact()`).
  `callback_router.py` owns Inline Keyboard lifecycle, but only for
  the one working flow (language).
- **When removed**: only for a BANNED user (`ReplyKeyboardRemove()`).
  Once a completed user's Reply Keyboard is shown, nothing in the
  codebase ever removes or downgrades it again short of a ban.

---

## Task 5 — Message Lifecycle Audit

- **Every** `RouterResult` (from `route_command()`, `route_message()`,
  or `route_contact()`) is delivered via `telegram/polling.py`'s
  `_on_message`, which unconditionally calls
  `message.answer(result.text, reply_markup=result.keyboard)` — a
  **brand-new message**, every single time, regardless of command.
- The **only** place any existing code edits a message in place is
  `callback_router._handle_language()`, which edits the language
  picker's own prompt message via `callback.message.edit_text()`,
  falling back to a new message if the edit fails (e.g. the message is
  too old to edit).
- No handler in `telegram/handlers.py` ever touches a `Message` object
  — confirmed by repo-wide search (zero `.answer(`/`.edit_text(`/
  `.edit_reply_markup(` occurrences in that file, only a docstring
  mention of `ReplyKeyboardRemove` as a concept). This is precisely
  why a navigation/delivery layer can be layered in without touching a
  single handler.
- **Net effect today**: every Native-Menu tap, every Reply-Keyboard
  tap, and every hand-typed command produces a new chat bubble.
  Only the one inline language-picker flow ever updates an existing
  bubble.
- **Which screens should edit instead** (Task 5's stated goal —
  app-like navigation): any screen a user pages through repeatedly —
  Settings and its five sub-screens, Profile, Subscription, the Admin
  panel — is a natural edit-candidate once its inline buttons are
  wired up (Task 3). One-off/first-contact screens (`/start`, `/help`,
  a hand-typed command) are naturally send-new, since there is no
  prior screen to update.

---

## Task 6 — Back Navigation Audit

A repo-wide search for `back`, `cancel`, `close`, `home` (word-bounded,
excluding false positives like `callback`/`bot.close()`/`asyncio
.cancel()`) found **zero** navigation-purpose matches anywhere in
`telegram/`. There is no Back, Cancel, Close, or Home concept in the
codebase today:

- The Reply Keyboard's `🏠 Home` button (Phase 4/5 content decision)
  maps to `/start` — a full re-invocation of `start_handler`
  (re-registration-status check), not a "return to a menu" primitive.
- Settings' five sub-screens (Language/Risk/Strategy/Timeframe/
  Notifications) have no way back to the Settings screen itself; the
  user must retype `/settings`.
- There is no forward/back stack, no breadcrumb, no cancel-in-progress
  concept anywhere.

**Missing architecture, documented for the Director's decision**: this
gap is real and is the largest net-new surface area Phase 6 could add
— see Open Questions 1–2 and the Risk/Roadmap sections below.

---

## Task 7 — Router Reuse Audit

- `command_router.route_command()` is already the single authoritative
  dispatch point for both typed text and (as of Phase 5.1) Reply
  Keyboard taps — confirmed reused, zero duplicate logic.
- `callback_router.route_callback()` is the single dispatch point for
  inline-keyboard taps. Its own docstring already states the intended
  design: "one backend, two entry points" — funnel into the same
  `handlers.*_handler()` functions `command_router` uses. Today this
  is only realized for language (`_handle_language()` calls
  `handlers.language_status()`); every other prefix is recognized but
  stubbed.
- **A unified Navigation Controller can be added without rewriting
  either router or any handler.** The two concrete pieces of new logic
  Phase 6 would need are:
  1. Extend `callback_router`'s dead-callback prefixes into real calls
     — either directly to the matching `handlers.*_handler()` (mirroring
     `_handle_language`'s existing shape), or by routing the implied
     `/command args` string through `command_router.route_command()`
     itself (mirroring Phase 5.1's own `resolve_navigation_command()`
     pattern, applied to `callback_data` instead of Reply Keyboard
     text).
  2. A small Response Delivery layer that decides send-vs-edit per
     call site — today hardcoded (`polling.py` always sends,
     `callback_router` always edits-then-falls-back).
  Neither touches a single function in `telegram/handlers.py`.

---

## Task 8 — Navigation State Audit

- Everything routed today is **stateless per call**. The only
  persistent "where is this user" state is `RegistrationStep`
  (`LANGUAGE`/`PHONE`/`COMPLETE`), and it already lives in the
  database (`users.registration_step`) via `RegistrationService`, not
  in memory. Permission tier and language are resolved fresh on every
  call.
- No handler, router, or keyboard builder holds any per-user session
  state today.
- **For Back/Cancel/breadcrumb support** (if the Director wants it —
  see Task 6), some minimal state is unavoidable: "Back" cannot be
  answered without recording where the user came from.
- **Recommendation**: a single "last screen" marker, not a full
  history/stack. The deepest flow that exists today is two levels
  (Settings → one sub-setting); a full breadcrumb/screen-stack would
  be over-engineering for that depth. If state is needed, store it the
  same way `registration_step` already is (a DB column keyed by
  `telegram_id`), keeping the existing "state lives in the database,
  not in a process-local dict" precedent this codebase already follows
  everywhere else. A full stack should be deferred unless/until a
  3+-level flow is actually designed — recommend the Director revisit
  this only if Task 6's Back/Home questions are answered "yes" with a
  design deeper than one level.

---

## Task 9 — Architecture Proposal

Proposal only — no implementation.

```
Reply Keyboard / Native Menu / Inline Keyboard tap
    |
    v
Navigation Resolver
    (existing: resolve_navigation_command() in telegram/keyboards.py,
     consulted by command_router.route_command() -- Phase 5.1)
    (proposed extension: same resolver pattern consulted from
     callback_router.route_callback() for callback_data)
    |
    v
command_router.route_command()          <-- UNCHANGED, already authoritative
    |
    v
existing telegram.handlers.*_handler()   <-- UNCHANGED, still pure text-returning
    |
    v
RouterResult(text, keyboard)             <-- UNCHANGED
    |
    v
proposed: Response Delivery Layer (new, thin)
    decides edit-vs-send based on:
      - triggering update type (message vs callback_query)
      - a per-command "editable" hint
    |
    v
Reply Keyboard / Inline Keyboard / message.edit_text() / message.answer()
    (aiogram calls stay exactly where they are today: polling.py and
     callback_router.py -- never inside handlers.py)
```

The only genuinely new component is the Response Delivery Layer. Every
other box in the diagram already exists and is already reused across
Phase 4/5/5.1.

---

## Task 10 — Reuse Report

| Component | Already exists? | Can reuse? | Need wrapper? | Need rewrite? | Need replacement? |
|---|---|---|---|---|---|
| Navigation Resolver (Reply Keyboard/Menu) | Yes (`resolve_navigation_command`) | Yes, as-is | No | No | No |
| Navigation Resolver (Inline callback_data) | Partially (`callback_router._RECOGNIZED_PREFIXES`) | Yes, extend the same pattern | Small extension | No | No |
| `command_router.route_command()` | Yes | Yes, as-is | No | No | No |
| `telegram/handlers.py::*_handler()` | Yes | Yes, as-is | No | No | No |
| `callback_router.route_callback()` | Yes | Yes, extend (fill stubbed prefixes) | No | No | No |
| Response Delivery Layer (send vs. edit) | **No** | N/A | **Yes — new, thin wrapper** | No | No |
| Back/Cancel/Home navigation | **No** | N/A | New, small | No | No |
| Screen stack / breadcrumbs | **No** | N/A | **Recommend NOT building** (Task 8) | No | No |

Reuse is the default outcome for 6 of 8 components; only the Response
Delivery Layer is unambiguously new, and Back/Home navigation is new
but small and contingent on the Director's Open-Question answers.

---

## Task 11 — Risk Analysis

| Area | Risk | Why |
|---|---|---|
| Reply Keyboard | **Low** | Phase 5/5.1 already shipped and stable; Phase 6 only wraps `RouterResult` delivery, no change to `reply_keyboard()`/`NAVIGATION_MAP` needed |
| Inline Keyboard | **Medium** | Filling in dead callbacks touches `callback_router.py`, which already has one live production flow (language); extension must not regress `_handle_language`'s edit/fallback behavior |
| Telegram Menu | **Low** | `menu_commands.py` is registration-only (startup `set_my_commands()`); a tapped Menu item is just ordinary text — Phase 6 doesn't need to touch this file at all |
| Registration Wizard | **Medium** | `_start_keyboard()`/`_persistent_reply_keyboard()` are exactly the functions a Response Delivery Layer would call through; a careless change here could reintroduce the BANNED/COMPLETE ambiguity Phase 5 already resolved — must be reused, not touched |
| Settings | **Medium-High** | This is where the real new behavior (wiring dead `settings_*` callbacks) lands; it's also the exact gap already flagged in the Phase 4 Freeze and roadmapped as Phase 5.x — Settings Callback Completion. Phase 6 should coordinate with, not duplicate, that roadmap item |
| Subscriptions | **Low** | `subscription_handler` has no keyboard today; unaffected by any proposed component |
| Signal Layer | **Low** | `signal_handler`/`history_handler` have no keyboard; Trading Core's own signal delivery (`notifier.py`, `signal_formatter.py`) is a separate, forbidden-scope system, untouched |
| Localization | **Low** | `translation.ui_catalog.t()` and its `menu.*`/`keyboard.*` key families already cover every reused label; at most new keys (e.g. `menu.back`) get added, following the exact `menu.admin`/`menu.owner` precedent from Phase 5.1 |
| Permission Layer | **Low** | `get_permission_level()`/`_required_level()` are read-only lookups every proposed component calls through unchanged |
| Trading Core | **None** | Zero references to `core/`, `decision/`, `execution/`, `risk/`, `signals/`, `strategies/`, `context/`, `ai/`, or database business logic found anywhere in this audit's inspection of `telegram/keyboards.py`, `command_router.py`, or `callback_router.py` |

---

## Task 12 — Implementation Roadmap Proposal

Proposal only — no coding, no commitment implied.

```
Phase 6.0 -- Navigation Controller foundation
    Extend callback_router.route_callback() to resolve the dead
    prefixes through the same resolver pattern Phase 5.1 established.
    Still send-only for router-originated replies (matches current
    behavior exactly -- zero delivery-layer risk yet).
        |
        v
Phase 6.1 -- Response Delivery Layer
    Introduce the edit-vs-send decision. Suggested first target:
    Settings + its 5 sub-screens, since that's the already-flagged
    Phase 5.x gap -- this phase could subsume or directly satisfy
    Phase 5.x Settings Callback Completion rather than duplicate it.
        |
        v
Phase 6.2 -- Back/Cancel/Home navigation (CONDITIONAL)
    Only if the Director confirms this is wanted (Open Questions
    1-2, 4). Adds the minimal "last screen" state from Task 8 plus
    new translation keys/commands.
        |
        v
Phase 6 Freeze
    Full regression + Trading Core zero-diff re-verification, docs
    update, Director sign-off.
```

Ordering, scope, and whether 6.2 happens at all are entirely the
Director's call — this is a proposal, not a plan awaiting only a
rubber stamp.

---

## Dependency Diagram

```
                    Telegram Update
                          |
        +-----------------+-----------------+
        |                 |                 |
   text message      callback_query     contact message
        |                 |                 |
        v                 v                 v
  route_message()   route_callback()   route_contact()
        |                 |                 |
        v                 |                 v
  route_command()          |         contact_handler()
        |                 |                 |
        |    (Phase 6:    |                 |
        |   same resolver |                 |
        | pattern reused) |                 |
        |                 |                 |
        v                 v                 v
   handlers.*_handler()  (today: only handlers.language_status()
        |                 for lang_*; Phase 6 extends this for
        |                 risk_/strategy_/timeframe_/settings_/admin_)
        v
   RouterResult(text, keyboard)
        |
        v
  polling.py: message.answer()          <-- always send today
  callback_router: message.edit_text()  <-- always edit today (language only)
        |
        v
  (Phase 6 proposed: Response Delivery Layer decides per call site)
```

---

## Open Questions

The Worker has **not** answered these — prepared for Director review
only.

1. Should a Back button exist, and if so, does it return to the
   previous screen or always to a fixed parent (e.g. Settings)?
2. Should Home always exist (persistent `🏠` button) even on
   sub-screens like Settings' inline choices?
3. Should Settings (and its sub-screens) open by editing the
   triggering message, or always send a new one?
4. Should the Reply Keyboard always remain visible, or should certain
   screens (e.g. deep Settings sub-menus) temporarily hide it in favor
   of an inline-only flow?
5. Should an inline keyboard disappear (via `edit_reply_markup`
   removing buttons) after a selection is made, the way
   `language_keyboard` already does today for a successful language
   change?
6. Should the dead `settings_*`/`risk_*`/`strategy_*`/`timeframe_*`/
   `notifications_*`/`admin_*` callbacks be wired up as part of Phase
   6, or does Phase 6 stay navigation-framework-only and defer that to
   the already-roadmapped Phase 5.x — Settings Callback Completion?
7. Is any navigation state worth persisting (Task 8), or should Phase
   6 commit to staying fully stateless?

---

## Worker Recommendation

Not an answer to the Open Questions above — a summary judgment on
audit quality and next-step shape only, for the Director's decision:

The codebase's existing "one backend, multiple entry points" pattern
(explicitly documented in `callback_router.py`'s own docstring, and
concretely proven by Phase 5.1's `resolve_navigation_command()`) means
a unified Navigation Framework is achievable with **no handler
rewrites and no router rewrites** — only an extension of
`callback_router.py`'s stubbed callbacks and one new, small delivery
component. The highest-value, lowest-risk first slice is **Phase 6.0
+ 6.1 as scoped above**, since 6.1 directly closes the
already-Director-flagged Settings gap. Phase 6.2 (Back/Home/Cancel) is
a real, coherent, but separable feature; recommend the Director treat
it as an explicit go/no-go decision rather than an assumed part of
Phase 6, since Task 8's state analysis shows it's the one piece that
requires genuinely new persistent state.

---

## Trading Core Zero-Diff

This audit involved repository inspection only. No file outside
`telegram/`, `translation/`, `tests/telegram/`, or `docs/` was read
for the purpose of modification, and none was modified.
`git diff --cached --stat -- core/ decision/ risk/ execution/
strategies/ signals/ context/ ai/ database/` is empty for this commit
— verified as part of the Commit Protocol below.

No implementation begins until the Director responds to this document.
