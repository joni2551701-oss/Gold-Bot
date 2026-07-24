# V2 Phase 3 — Registration Wizard: Architecture & Reuse Audit (Stage 0)

**Status: AUDIT ONLY.** No code changed. Written per the Director's
Phase 3 Stage 0 task brief, in the same architecture-first discipline
Phase 3.0-style audits use elsewhere in this repo (`docs/PHASE*_AUDIT.md`).
Next stage (implementation) does not begin until the Director reviews
and approves this document.

## 1. Existing Registration Flow

### Current dispatch diagram (verified against the actual code, not assumed)

```
Telegram (text command "/start")
      |
telegram/polling.py            forwards Message, no branching
      |
telegram/command_router.py     route_message() -> route_command()
      |                        _parse_command() -> "start"
      |                        _required_level("start") -> USER
      |                        handler = handlers.start_handler
      |
telegram/handlers.py           start_handler(telegram_id, username)
      |                        -> UserService().register_user()
      |                        -> SubscriptionService().get_plan()  (best-effort)
      |
telegram/user_service.py       UserService.register_user()
      |                        -> UserRepository.get_user() (dup check)
      |                        -> UserRepository.create_user()
      |
database/user_repository.py    UserRepository.create_user()
      |                        INSERT INTO users (...)
      |
   Database (users table)

route_command() then attaches phone_share_keyboard(language) to the
/start reply via _KEYBOARD_BY_COMMAND (command_router.py:61-73) --
**the Phone Share prompt is already wired to every /start reply
today**, not a new step to invent.

Telegram (Message with .contact populated -- Phone Share button tap,
          OR a manually forwarded contact card)
      |
telegram/polling.py            message.contact is not None ->
      |                        route_contact(message), not route_message()
      |
telegram/command_router.py     route_contact(message)
      |                        no permission check (USER-level by design)
      |
telegram/handlers.py           contact_handler(telegram_id, phone_number)
      |                        -> UserService().register_phone()
      |
telegram/user_service.py       UserService.register_phone()
      |                        Phone Hash -> UserRecord -> Trial Check -> FREE account
      |                        -> core.phone_hash.hash_phone_number()
      |                        -> ai.access.identity_checker.is_phone_reused_by_another_account()
      |                        -> ai.access.trial_manager.trial_status_from_started_at()
      |
database/user_repository.py    set_phone_hash(), set_trial_started_at()
      |
   Database (users table: phone_hash, trial_started_at)
```

### Files read for this section

`telegram/handlers.py` (`start_handler` L207-241, `contact_handler`
L1141-1162), `telegram/command_router.py` (full file, 207 lines),
`telegram/user_service.py` (full file, 243 lines),
`database/user_repository.py` (schema-adjacent methods),
`telegram/polling.py` (contact-vs-text branching, L103-125),
`telegram/keyboards.py` (`phone_share_keyboard` L138-158).

### Key existing facts that change the Wizard's scope

1. **`/start` already creates the user AND already attaches the Phone
   Share keyboard to its own reply** (`command_router.py`'s
   `_KEYBOARD_BY_COMMAND["start"] = phone_share_keyboard`, added Phase
   61.5 TASK 4). The "Phone Share" step in the Director's proposed
   Wizard diagram is not a new step to build — it is already live.
2. **Phone registration (`register_phone`) is already real**: phone
   hash, trial start, "1 phone = 1 trial" reuse detection, idempotent
   re-share (never resets an existing trial). This is not a stub.
3. **Language selection already exists and is already independent of
   `/start`** — `/language` (V2 Phase 1, frozen) with its own inline
   keyboard and callback path (`telegram/callback_router.py`). It is
   not currently invoked *from* `start_handler`; a user's language
   defaults to `'UZ'` at row-creation time (`create_user()`'s
   `language: str = "UZ"` default) and is changed later, if ever, via
   `/language`.
4. **No "Profile Creation" step is missing** in the database sense —
   `create_user()` already creates the full profile row in one INSERT.
   What the Director's diagram calls "Profile Creation" is really
   "decide when in the flow to prompt for/confirm language" — there is
   no separate profile-assembly step to build.
5. **"Registration Complete" / "Dashboard" have no existing handler.**
   `start_handler`'s reply text (`start.created`) is the only
   "complete" signal today; there is no dashboard command yet (Phase 8
   territory per the roadmap) and nothing calls it after the phone
   step.

## 2. Database Audit

### Actual schema (`database/models.py::init_user_schema`, verified — this is the real `CREATE TABLE`, not the dataclass)

```sql
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id TEXT UNIQUE NOT NULL,
    username TEXT,
    language TEXT DEFAULT 'UZ',
    trading_style TEXT DEFAULT 'Intraday',
    risk_percent REAL DEFAULT 2.0,
    timeframe TEXT DEFAULT 'M15',
    created_at TEXT NOT NULL,
    updated_at TEXT,
    strategy TEXT DEFAULT 'Liquidity Sweep',
    notifications_enabled INTEGER DEFAULT 1,
    status TEXT DEFAULT 'NEW',
    last_activity TIMESTAMP,
    phone_hash TEXT,
    trial_started_at TEXT
);
```

`UserRecord` (`database/user_models.py`) mirrors this exactly (minus
`id`/`updated_at`, repository-internal).

### Director's example columns vs. what actually exists

| Director's example | Actual state |
|---|---|
| `telegram_id` | Exists (`TEXT UNIQUE NOT NULL`) |
| `language` | Exists (`DEFAULT 'UZ'`) |
| `phone` | **Does not exist, by design.** Only `phone_hash` exists — the raw phone number is deliberately never stored (see `user_service.py`'s own module docstring: "never stored, logged, or returned"). This is a privacy decision from Phase 61.5, not a gap. |
| `full_name` | **Does not exist.** Nothing in the current flow collects or needs a display name; Telegram's own `username`/first name is what handlers use today. |
| `registration_time` | Exists, named `created_at` (`TEXT NOT NULL`, ISO-8601 UTC). |

### Is a new column needed?

**No new column is required for the Wizard steps the Director listed
(Language / Phone Share / Validation / Profile Creation / Registration
Complete).** Every one of those is representable with existing columns:
- Language: `language` column.
- Phone Share: `phone_hash`, `trial_started_at` (already present).
- "Profile Creation": the existing single-row INSERT already is this.
- "Registration Complete": derivable from `phone_hash IS NOT NULL`
  (has the user completed the phone step) combined with `status` —
  no new column needed to represent "done", since completion is a
  function of existing columns, not new state.

**One column is a real gap, but for the *state machine*, not the
profile** — see Section 3.

## 3. Registration State Audit

**No FSM/state machine exists for registration today.** Verified via
a repo-wide grep for `FSM|StateMachine|pending_registration|
RegistrationState` — the 15 matches are all unrelated bounded
contexts: `ai/session/conversation_state.py` (AI conversation turns),
`ai/runtime/runtime_state.py` / `configuration/runtime_state.py`
(AI/feature runtime lifecycle), `core/emergency/emergency_state.py`
(trading pause/kill state), `lifecycle/signal_state.py` /
`lifecycle/trade_state.py` (paper-trade lifecycle),
`database/sync_state_models.py` (historical data sync), `assistant/
models.py`, `backtesting/replay_models.py`. None of these are
Telegram-registration-scoped, and per this repo's own layering rule
(`ai/` doesn't import `telegram/` and vice versa isn't the direction
either), `ai/session/conversation_state.py` is not reusable here even
though its name is superficially similar — it belongs to a different
layer and a different concern (AI conversation turn tracking, not
Telegram onboarding).

**Why a explicit "pending registration" concept barely matters today**:
the current flow already tolerates being interrupted at any point,
because each step is independently idempotent:
- `/start` a second time: `register_user()` returns
  `success=False, reason="User already exists"` and `start_handler`
  calls `touch_activity()` instead of erroring.
- Sharing a contact a second time: `register_phone()` explicitly never
  resets `trial_started_at` if already set (`user.trial_started_at is
  None` guard) — no double-registration side effect.

**What is genuinely missing, and would need new (minimal) state**:
there is no way today to know, *without re-deriving it from column
values*, "is this user mid-Wizard, and at which step" for cases where
the Wizard needs to prompt in a specific order (e.g. show the Language
picker only if the user hasn't set one yet, in the same turn as
`/start`). Two options, evaluated:

- **Option A (recommended): derive step from existing data, no new
  table/column.** "Needs Language prompt" = `language` column is at
  its unqualified factory default *and* the user has never run
  `/language` (this second condition cannot actually be distinguished
  from "user explicitly chose UZ" with the current schema — see Edge
  Case discussion below). "Needs Phone Share" = `phone_hash IS NULL`.
  "Complete" = `phone_hash IS NOT NULL`. This needs zero new database
  objects, only wizard-orchestration logic in a new
  `telegram/registration_service.py`-style file that reads existing
  `UserService`/`UserRepository` methods.
- **Option B: a minimal `registration_step` column** (`TEXT DEFAULT
  'LANGUAGE'`, values e.g. `LANGUAGE -> PHONE -> DONE`) if the
  Director wants an explicit, un-ambiguous "did the user ever see the
  language prompt" signal rather than inferring it from the `language`
  value's presence. This is the minimal-new-state option if Option A's
  inference gap (a user who explicitly picks UZ vs. one who never saw
  the prompt look identical) is judged unacceptable.

This audit does not choose between A and B — that is a Wizard Design
decision for the Director, recorded as an open question in Section 7.

## 4. Reuse Audit

| Component | Reused as-is | Notes |
|---|---|---|
| `translation/ui_catalog.py` (`t()`) | Yes | `start.*` (3 keys), `contact.*` (5 keys) already exist and cover most Wizard text. New keys only needed for any genuinely new prompt text (e.g. an explicit "Registration Complete" message, if the Director wants one distinct from `start.created`). |
| `telegram/keyboards.py::phone_share_keyboard()` | Yes | Already built, already wired to `/start`, already localized. |
| `telegram/keyboards.py::language_keyboard()` | Yes | Already built, already localized, already has a working callback path. |
| `telegram/callback_router.py` | Yes, as the dispatch *pattern* | `route_callback()`'s "translate callback_data to the same handler the text command already uses" principle is the template a Wizard's own callback handling (if any new callback_data is needed) should follow — not a new dispatch mechanism. |
| `telegram/user_service.py::UserService` | Yes | `register_user()`, `register_phone()`, `get_profile()`, `touch_activity()` cover every data operation the Wizard needs. No new service method is obviously required by the 5-step diagram as scoped. |
| `database/user_repository.py::UserRepository` | Yes | All needed reads/writes already exist. |
| `telegram/command_router.py`'s `_KEYBOARD_BY_COMMAND` pattern | Yes | The existing "attach a hint keyboard per command" mechanism is the natural place to extend from, not a parallel mechanism. |

**Not yet built, and would be new (kept to the minimum Section 3
recommends)**:
- A Wizard orchestration layer that decides *which* prompt to show
  next on `/start` (today `/start` always shows the same
  `phone_share_keyboard`, regardless of whether language was ever
  explicitly chosen). This is the one real gap between "what the
  Director's diagram wants" and "what exists".
- Optionally, the `registration_step` column (Section 3, Option B) if
  chosen over inference.

## 5. Wizard Design (Entry/Exit/Validation/Cancel/Restart per step)

This section describes the flow **as it should be**, cross-referencing
what already exists vs. what a Wizard orchestration layer would need
to add. No commitment yet — pending Director approval before any file
is created.

### Step 1 — `/start`
- **Entry**: any incoming `/start` command, new or existing user.
- **Exit**: `UserService.register_user()` returns (new row created, or
  existing row found) — always succeeds from the caller's perspective
  (never raises). Reply text differs by outcome (`start.created` vs.
  `start.already_exists`), already implemented.
- **Validation**: none needed — `telegram_id` comes from Telegram
  itself, trusted.
- **Cancel**: not applicable — a single command, not a multi-turn
  interaction.
- **Restart**: re-running `/start` is already safe and idempotent
  (verified above).

### Step 2 — Language (skip if already selected)
- **Entry**: immediately after Step 1, only if the Wizard decides the
  user "hasn't chosen a language yet" (Section 3's open inference
  question).
- **Exit**: `UserService.change_language()` (already exists, wraps
  `update_settings`) sets the `language` column; existing
  `language_keyboard()` + `callback_router.py`'s `_handle_language()`
  already do this end-to-end for `/language` — the Wizard would reuse
  the exact same callback handler, not a new one.
- **Validation**: `change_language()` doesn't currently validate the
  language code against `{UZ, RU, EN}` before writing it — `t()`'s own
  fallback chain (chosen language -> EN -> any entry) means an invalid
  value degrades gracefully at *read* time but is still stored as-is.
  Not a new gap (pre-exists in `/language` today), but worth the
  Director's awareness if the Wizard is the first place a raw,
  non-keyboard value could reach this path.
- **Cancel**: no existing concept of "cancel and keep the old value" —
  today `/language` always writes on tap; skipping requires the Wizard
  to simply not show the picker in the first place, not a mid-flow
  cancel.
- **Restart**: re-picking a language is already a no-op-safe operation
  (`language_status()` explicitly no-ops on re-selecting the current
  language, Phase 1.6).

### Step 3 — Phone Share
- **Entry**: `phone_share_keyboard()` already attached to `/start`'s
  reply today — no new entry logic needed, only (per Section 3) a
  decision on whether to *also* show it after the Language step
  finishes, if Language was shown.
- **Exit**: `route_contact()` -> `contact_handler()` ->
  `register_phone()`, already fully implemented (trial start/reuse
  detection/hash storage).
- **Validation**: **gap, see Section 6, Edge Case 4** — nothing
  currently checks that the shared `contact.user_id` matches
  `message.from_user.id` (i.e., that the user shared *their own*
  contact, not a forwarded card for someone else). `hash_phone_number()`
  would hash whatever number arrives regardless of whose it is.
- **Cancel**: the keyboard is `one_time_keyboard=True` and has no
  explicit "skip" button — a user can simply not tap it and continue
  using other commands; nothing currently forces phone sharing before
  other USER-tier commands work. This is consistent with "Phone Share"
  being optional-but-encouraged, not a hard gate — confirm with
  Director whether the Wizard should change this posture.
- **Restart**: re-sharing is already idempotent (never resets
  `trial_started_at`).

### Step 4 — Validation
- Not a separate step in the current architecture — validation is
  inline within `register_phone()` (phone-reuse check) and would stay
  that way; the Director's diagram's "Validation" box maps to existing
  code, not a new component.

### Step 5 — Profile Creation
- Already happens atomically inside Step 1's `create_user()` INSERT.
  No separate step to build.

### Step 6 — Registration Complete
- **Gap**: no existing message or handler represents this distinctly
  from `start.created`/the phone step's own reply. Would need: a new
  `t()` key (e.g. `registration.complete`) and a decision on *when* to
  show it — after Phone Share succeeds, or after Phone Share is
  skipped and some timeout/other trigger fires (the latter needs the
  state-tracking discussed in Section 3).

### Step 7 — Dashboard
- **Out of scope for Phase 3** per the Director's own roadmap (Phase 4
  is Persistent Menu, Phase 8 is Dashboards) — flagged here only so
  the Wizard's "Registration Complete" step doesn't accidentally reach
  into Phase 8 territory.

## 6. Edge Cases

| Edge case | Current behavior (verified) | Gap? |
|---|---|---|
| `/start` pressed a second time | `register_user()` returns `success=False, reason="User already exists"`; `start_handler` calls `touch_activity()` and returns `start.already_exists`. Never raises, never duplicates the row (`UNIQUE` constraint + explicit pre-check + `IntegrityError` catch for the race case). | No gap. |
| Phone number already registered (on another account) | `register_phone()` detects via `is_phone_reused_by_another_account()`, still records the phone_hash on the new account (storage unconditional), returns `success=False, reason="This phone number is already registered on another account."`, mapped to a localized `contact.phone_reused` message. | No gap. |
| Contact not sent (user ignores the button) | No forcing mechanism exists — the user can keep using every other USER-tier command. This is today's actual product behavior, not a bug, but the Wizard Design (Step 3) should have the Director explicitly confirm this stays optional. | Design decision needed, not a code gap. |
| **User shares someone else's contact** (forwards a contact card instead of tapping the button) | **Not validated anywhere.** `route_contact()` reads `message.contact.phone_number` unconditionally; nothing compares `message.contact.user_id` to `message.from_user.id`. `register_phone()` would hash and store whatever number arrives, potentially attaching a stranger's phone number/trial eligibility check to the sender's account. | **Real gap** — recommend adding a `message.contact.user_id == message.from_user.id` check in `route_contact()` (Telegram layer, no new service method needed) before this phase implements anything new. |
| Registration left half-done (e.g. `/start` done, phone never shared) | Fully representable today — `phone_hash IS NULL` is exactly this state, and nothing blocks the user from operating in it indefinitely. | No gap in *data*; only in whether the Wizard should re-prompt (Section 3). |
| Restart (`/start` again mid-way) | Same as "second /start" above — safe, idempotent. | No gap. |
| Callback timeout (inline button tapped after the message/keyboard context is stale) | `callback_router.py`'s `_handle_language()` already handles a stale-message edit failure by falling back to `message.answer()` instead of crashing (`edit_text` failure caught, logged, falls back). The Phone Share keyboard is a `ReplyKeyboardMarkup`, which has no server-side "timeout" concept the way inline callback data can (Telegram itself doesn't expire reply-keyboard taps), so this specific risk is inline-keyboard-only and already covered by existing code. | No gap. |
| Blocked (BANNED) user goes through `/start` again | **Explicitly documented as unenforced today**: `telegram/handlers.py`'s own module docstring states "No command blocks a BANNED user yet (`ban_user()`/`activate_user()` exist on `UserService` for a future phase's enforcement)." A BANNED user can currently still run `/start`/share a phone/etc. | **Known, pre-existing gap, not introduced by this phase** — flagged for Director awareness; likely out of scope for the Wizard itself (it's a router/permission-layer enforcement question, not a registration-flow one) unless the Director wants it folded in here. |

## 7. File Change Plan (proposed, pending approval — nothing created yet)

| File | Change | Reuse vs. new |
|---|---|---|
| `telegram/registration_service.py` (new) | Orchestrates "what's the next Wizard step for this user" (Option A inference, or reads the new column if Option B is chosen). Calls existing `UserService` methods only — no new repository methods anticipated. | New file, but composes only existing services (Module Reuse Principle step 2 satisfied: extending is possible via a thin orchestration layer, not a new package). |
| `telegram/command_router.py` | `start_handler`'s post-processing gains a call into `registration_service` to decide which keyboard to attach (`phone_share_keyboard` vs. `language_keyboard` vs. neither), replacing the current unconditional `phone_share_keyboard` mapping for `"start"`. | Extends existing dispatch table, no new mechanism. |
| `telegram/command_router.py::route_contact()` | Add the `contact.user_id == from_user.id` check (Edge Case 4 fix). | Extends existing function. |
| `translation/ui_catalog.py` | Add `registration.complete` (and any other net-new prompt text the Director approves in Step 6) — UZ/RU/EN, same convention as every other key. | Extends existing catalog. |
| `database/models.py` | **Only if Option B is chosen**: add `registration_step TEXT DEFAULT 'LANGUAGE'` to `init_user_schema()` + a migration branch in `_migrate_users_schema()`, mirroring how `phone_hash`/`trial_started_at` were added in Phase 61.4/61.5. | Extends existing schema function; no new table. |
| `database/user_models.py` / `user_repository.py` | **Only if Option B**: add `registration_step` to `UserRecord`, `_row_to_record()`, `_USER_SELECT_COLUMNS`. | Extends existing dataclass/repository, same pattern as `phone_hash`. |
| `tests/telegram/test_registration_service.py` (new) | Tests for the new orchestration file. | New test file for new code, per CLAUDE.md's "add tests" rule. |
| `tests/telegram/test_phone_registration.py` | Add a test for the Edge Case 4 fix (contact.user_id mismatch is rejected). | Extends existing test file. |

**No file is proposed for deletion or refactor beyond what's listed.**
Trading Core (`core/`, `decision/`, `risk/`, `execution/`,
`strategies/`, `signals/`, `context/`, `ai/`) is untouched by every
item above except *reading* (never modifying) `ai.access.
identity_checker`/`ai.access.trial_manager` — both already-existing
read-only dependencies of `register_phone()`, unchanged by this
phase.

## Implementation Order (proposed)

1. Edge Case 4 fix (`route_contact()` contact-ownership check) — small,
   independent, arguably should land regardless of the rest of the
   Wizard.
2. Director decision: Option A (inference, no schema change) vs.
   Option B (`registration_step` column) — blocks step 3.
3. `telegram/registration_service.py` (new orchestration file).
4. `command_router.py` wiring (conditional keyboard selection on
   `/start`).
5. `translation/ui_catalog.py` new keys (Step 6 message).
6. Tests for all of the above.
7. Full Commit Protocol (pyflakes/compileall/pytest/main.py smoke/
   Trading Core zero-diff) + push + CI confirm.

## Open Questions for the Director

1. **Option A vs. Option B** (Section 3) — infer Wizard step from
   existing columns, or add a minimal `registration_step` column?
2. Should Phone Share remain **optional** (today's actual behavior) or
   does the Wizard make it a **hard gate** before other USER-tier
   commands work? Changing this would touch `command_router.py`'s
   permission logic, a larger change than the rest of this plan.
3. Is the Edge-Case-4 fix (contact ownership check) wanted as part of
   Phase 3, or as its own small, separately-authorized fix landed
   first (per the Implementation Order above, it doesn't depend on
   the Option A/B decision)?
4. Is the BANNED-user enforcement gap (Section 6) in scope for Phase 3
   at all, or explicitly deferred (as it already implicitly has been
   since Phase 45)?

**No implementation begins until the Director responds to this
document.**
