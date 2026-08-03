# V2 Phase 3 Review — Registration Wizard

Review requested by the Director after Phase 3 implementation (commit
`ef2144a`) went green on GitHub Actions. This is a **Review**, not a
Freeze — per the Director's own framing, a Freeze only follows if no
blocking issue is found; an important-but-non-blocking issue becomes a
Phase 3.x fix first.

Scope reviewed: `telegram/registration_service.py`,
`telegram/command_router.py`, `telegram/callback_router.py`,
`telegram/handlers.py` (start_handler/_registration_step/
contact_handler), `database_layer/database_manager/models.py` (migration + backfill),
`database_layer/user_repository/user_repository.py`, `database_layer/user_repository/user_models.py`,
`translation/ui_catalog.py` (new keys), `telegram/keyboards.py`
(phone_share_keyboard), and the full Phase 3 test suite.

---

## 1. Architecture Review

**RegistrationService** (`telegram/registration_service.py`, 93
lines): a sibling service to `UserService`, same "own a lazy
repository" shape (`UserRepository()` constructed on first use, not in
`__init__`). Three methods only: `current_step()`,
`advance_past_language()`, `complete()`. All three wrap their body in
try/except and degrade to a safe default — matches the codebase-wide
never-raises contract.

**Wizard flow / State Machine**: `registration_step` moves
LANGUAGE → PHONE → COMPLETE, driven by two triggers —
`advance_past_language()` (called from `callback_router._handle_language()`
after a language tap) and `complete()` (called from
`handlers.contact_handler()` after a successful phone registration).
No separate FSM class exists; the "machine" is just these two
guarded transitions plus a stored string column. This is intentionally
minimal — appropriate for a 3-state linear flow, would **not** scale
past ~4-5 states without becoming ad hoc (see Remaining Issues if a
future phase needs a longer flow).

**command_router.py**: keyboard-per-step is a plain dict lookup
(`_START_KEYBOARD_BY_STEP`), consistent with the existing
`_KEYBOARD_BY_COMMAND` pattern already used for every other command.
No new dispatch mechanism was introduced.

**callback_router.py**: the Wizard-advance call is a single `try`
block appended to the existing `_handle_language()` function, not a
new handler — reuses the "one backend, two entry points" principle
already documented at the top of the file.

**Code simplicity**: yes — no class hierarchy, no event bus, no
extra abstraction layer for a 3-state flow. **No duplicate logic**
found: keyboard selection, step advancement, and completion each have
exactly one call site.

**Subscription Wizard reuse**: straightforward. The same shape —
a `SubscriptionStep` class of string constants, a
`SubscriptionService` with `current_step()`/`advance()`/`complete()`
methods owning a lazy repository, a `_SUBSCRIPTION_KEYBOARD_BY_STEP`
dict in `command_router.py` — would drop in without touching
`RegistrationService` itself. The one thing a second Wizard would
need to duplicate today is the "read a `*_step` column, look it up in
a dict, fall back to `None`" pattern in `_start_keyboard()`/
`_registration_step()` — small enough (a handful of lines) that
extracting a shared helper now would be premature; worth doing once a
second Wizard actually exists (Module Reuse Principle: extend, don't
pre-abstract).

**Verdict: no blocking architecture issue.**

---

## 2. Database Review

**Columns**: `registration_step TEXT DEFAULT 'LANGUAGE'`,
`registration_completed INTEGER DEFAULT 0` — both added to
`init_user_schema()`'s CREATE TABLE and to `_migrate_users_schema()`'s
idempotent `ALTER TABLE ADD COLUMN` list (guarded by `PRAGMA
table_info` existence check, matching every prior migration in this
file).

**Migration rollback safety**: the migration is purely additive
(`ALTER TABLE ADD COLUMN`, no column renamed or dropped, no existing
column's type or default changed). Reverting the Phase 3 commit
(code rollback) while the database already has these two columns is
safe — pre-Phase-3 code's `_USER_SELECT_COLUMNS` names its columns
explicitly (never `SELECT *`), so it simply never reads the two new
columns; their presence is inert to old code. There is no scenario
where rollback corrupts or loses data — the two columns simply become
unused, not invalid.

**Old users**: verified via `tests/test_registration_migration.py`
(4 tests) using a hand-built pre-Phase-3 schema. `_backfill_registration_state()`
runs exactly once, gated on `"registration_step" not in existing_columns`,
so it never re-runs (and never re-flips state) on a second startup
against an already-migrated table — confirmed by
`test_backfill_never_reopens_a_completed_registration_on_second_migration_call`.

**NULL states**: none possible. The backfill's two `UPDATE` statements
partition every existing row by `phone_hash IS NOT NULL` /
`phone_hash IS NULL` — together they cover 100% of rows, so no row is
left with a NULL `registration_step`. New rows get the CREATE TABLE
column defaults (`'LANGUAGE'`, `0`) — also never NULL.
`registration_completed` is written only via `update_user()`'s
`bool` values, `_row_to_record()` explicitly casts with `bool(row[...])`,
never leaves a bare NULL/None as a possible value in `UserRecord`.

**Verdict: no blocking database issue.**

---

## 3. Security Review

**Contact Ownership**: `command_router.route_contact()` now rejects
any contact whose `message.contact.user_id` doesn't equal the
sender's own `telegram_id` before `contact_handler`/`register_phone()`
is ever called — confirmed by dedicated tests
(`test_route_contact_rejects_a_contact_for_a_different_person`,
`test_route_contact_rejects_a_contact_with_no_user_id`). A forwarded
contact card for someone else can never register that phone number
under the forwarder's account.

**BANNED flow**: `start_handler()` stops a BANNED user (localized
reply, no `touch_activity()`, no Wizard keyboard) exactly per the
Director's specified flow: `/start → User exists? → BANNED? → Stop`.
`RegistrationService.current_step()` independently also returns
`None` for a BANNED user, so no code path can hand a BANNED user a
Wizard keyboard even if some future caller forgets the `start_handler`
check.

Pre-existing, out-of-scope note (already flagged in the Stage 0
audit, not changed by Phase 3): a BANNED user is only stopped at
`/start` — other commands (`/profile`, `/signal`, etc.) still have no
BANNED check of their own. This is documented in
`telegram/handlers.py`'s own module docstring since before Phase 3 and
was not part of what the Director authorized fixing this phase
(the Director's flow was specifically `/start`-scoped).

**Registration bypass — real finding.** The Stage 0 audit's Open
Question 2 asked: *"Should Phone Share remain optional, or does the
Wizard make it a hard gate before other USER-tier commands work?"*
The Director's answer ("Phone Share — Majburiy. Telefon raqamisiz
Registration tugamaydi") makes phone sharing mandatory **for
`registration_step` to ever reach `COMPLETE`** — but no code change
was made to `command_router.py`'s permission logic, so a user who
completes Language and then never taps Phone Share can still freely
run `/profile`, `/settings`, `/plan`, `/subscription`, `/history`,
and (subject to the pre-existing FREE-plan gate) `/signal` — every
USER-tier command remains reachable with `registration_step="PHONE"`
forever. Nothing in the current code prevents a user from operating
indefinitely in this half-registered state, matching what the audit
already flagged as `tests`-confirmed-possible in Section 6 ("Registration
left half-done"). **This is not a data-integrity or auth bypass
(no attacker can act as another user) — it is the Wizard's own
"required" step not being enforced as a functional gate**, so a
user's read of "Registration doesn't complete without phone" and the
bot's actual behavior ("but you can use most of the bot without
completing it") diverge.

**Callback spoofing**: `callback.from_user.id` comes from Telegram's
own signed update payload — it cannot be set by the tapping user to
someone else's id. `_handle_language()`'s `RegistrationService().advance_past_language(telegram_id)`
call always operates on the real tapper's own row. No cross-user
mutation path exists.

**Wizard restart**: repeated `/start` while mid-Wizard is idempotent —
the "already exists" branch in `start_handler()` never touches
`registration_step`, so re-running `/start` cannot revert or corrupt
Wizard state (`test_start_reply_carries_the_phone_share_keyboard`-style
coverage confirms the keyboard stays consistent with the stored step).

**Verdict: no blocking security issue, but the Registration-bypass
finding above is a real product-behavior gap the Director should
explicitly decide on** (see Remaining Issues / Freeze
Recommendation).

---

## 4. UX Review

**New user flow**: `/start` → language picker (inline buttons) → tap
→ message edited in place with confirmation, **then** a *new* message
is sent with the Phone Share prompt and the ReplyKeyboardMarkup
button (`registration.phone_prompt` in UZ/RU/EN) → tap "Share Phone
Number" → phone hash stored, trial started, Wizard marked COMPLETE,
one final confirmation message (`contact.trial_active`/
`contact.trial_ended`, already-existing Phase 61.5 text, unchanged).
This reads as a natural, linear 3-step flow with no dead ends.

**Language selection**: unchanged from the existing V1.1 Language UX
Polish behavior for a user *not* in the Wizard (edit-in-place,
duplicate-selection guard, keyboard-removal-on-success) — the Phase 3
addition (Phone Share prompt) is strictly additive, appended after
the existing logic, not a replacement of it.

**Phone Share**: uses `ReplyKeyboardMarkup` with
`one_time_keyboard=True` (pre-existing `phone_share_keyboard()`,
unchanged) — hides itself after one tap, standard Telegram UX for a
contact-request button.

**Completion**: no dedicated "Registration Complete!" message exists
— completion is silent (only the pre-existing trial-active/trial-ended
text from `contact_handler()` is shown, which was already the reply
for phone registration before Phase 3). The Director's Stage 0 wizard
design named a distinct "Registration Complete" step before
"Dashboard"; in the shipped implementation this step has no visible
text of its own — it is inferred by the user from the trial
confirmation message. Minor, non-blocking, but worth a Director
decision: is a distinct completion message wanted, or is the existing
trial message considered sufficient?

**Dashboard**: no dashboard command/screen exists yet in this
codebase (Phase 8 on the roadmap) — Phase 3 correctly stops at
Registration Complete and does not fabricate a Dashboard step ahead
of its own phase.

**Verdict: flow is natural and understandable; one minor, non-blocking
observation (no distinct completion message) noted above.**

---

## 5. Recovery Review

**Bot process restart / VPS restart / polling restart**: Wizard state
lives entirely in the `users.registration_step`/`registration_completed`
columns in SQLite — there is no in-memory state anywhere in
`RegistrationService`, `command_router.py`, or `callback_router.py`.
A process restart at any point mid-Wizard loses nothing: the next
`/start` re-reads `registration_step` from the database and shows
the matching keyboard exactly where the user left off
(`_start_keyboard()` → `handlers._registration_step()` →
`RegistrationService.current_step()` → `UserRepository.get_user()`).

**Half-finished registration (Language done, Phone never shared)**:
correctly resumes at PHONE on the next `/start` — this is exactly the
`registration_step == "PHONE"` case `_START_KEYBOARD_BY_STEP` maps to
`phone_share_keyboard`. Confirmed by
`test_start_keyboard_is_the_phone_share_keyboard_once_at_the_phone_step`.

**Recovery finding (linked to the text-`/language` edge case below)**:
recovery via `/start` works correctly in every case *except* one
narrow path — see Remaining Issues #2.

**Verdict: no blocking recovery issue** for the restart scenarios the
Director asked about (process/VPS/polling restart, half-finished
registration all resume correctly from the database). One related
non-blocking edge case is noted below.

---

## 6. Regression Review

- **Language Foundation**: unchanged behavior for language selection
  outside the Wizard (already-registered users) — confirmed by
  `test_lang_uz_after_registration_complete_does_not_reopen_the_wizard`
  and the full pre-existing `test_callback_router.py`/`test_user.py`
  language suites, all still passing.
- **Translation**: 3 new catalog keys (`start.banned`,
  `contact.wrong_owner`, `registration.phone_prompt`), each with
  UZ/RU/EN entries — verified present in `translation/ui_catalog.py`.
  No existing key was modified.
- **Keyboards**: `phone_share_keyboard()` (pre-existing, Phase 61.5)
  and `language_keyboard()` (pre-existing) are both reused as-is, no
  changes to either function — only *which one* gets attached to
  `/start`'s reply changed.
- **Previous commands**: `_KEYBOARD_BY_COMMAND` still serves every
  other command unchanged; `"start"` was removed from that dict and
  handled by the new `_start_keyboard()` special case (mirroring the
  pre-existing `"admin"` special case already in the same function) —
  no other command's routing path was touched.
- **Full suite**: 4520/4520 tests passing (29 net new vs. the
  4491-test Phase 2 baseline).

**Verdict: no regression found.**

---

## 7. Trading Core Review

```
git diff 53a05e3 ef2144a --stat -- core/ decision/ risk/ execution/ strategies/ signals/ context/ ai/
```

Output: **empty** — zero changes to any Trading Core path across the
entirety of Phase 3 (Stage 0 audit commit `7f30ec8` through
implementation commit `ef2144a`), re-verified for this Review against
the pre-Phase-3 baseline (`53a05e3`, the Phase 2 commit), not just the
most recent commit.

**Verdict: zero diff confirmed.**

---

## 8. Deliverables Summary

| Report | Result |
|---|---|
| Architecture Review | No blocking issue. Simple, no duplication, Subscription Wizard reuse is straightforward. |
| Database Review | No blocking issue. Migration is additive/rollback-safe, old users backfilled correctly, no NULL states possible. |
| Security Review | No blocking issue, but **Registration bypass** (Open Question 2 from Stage 0 was never actually enforced as a command gate) is a real, non-blocking finding — see below. |
| Recovery Review | No blocking issue for restart/half-finished-registration scenarios. One related non-blocking edge case (below). |
| UX Review | Flow is natural. One minor, non-blocking observation: no distinct "Registration Complete" message. |
| Regression Review | No regression. 4520/4520 tests passing. |
| Trading Core | Zero diff confirmed (re-verified against pre-Phase-3 baseline). |

### Remaining Issues (non-blocking, Director decision requested)

1. **Registration bypass is not enforced.** `registration_step`
   staying at `"PHONE"` never blocks any USER-tier command — a user
   can use the bot indefinitely without ever sharing their phone.
   This was an open question in the Stage 0 audit (Question 2) that
   the Director's "Phone Share is mandatory" decision did not
   explicitly resolve one way or the other (mandatory *for
   `registration_step` to reach `COMPLETE`*, vs. mandatory *as a
   hard gate on other commands*). Fixing this would mean
   `command_router.py` denying (or redirecting to the Wizard) any
   USER-tier command while `registration_step != "COMPLETE"` — a
   larger, `command_router.py`-permission-logic change, exactly as
   flagged in the original audit.

2. **Wizard can stall if the user types `/language UZ` instead of
   tapping the inline keyboard button.** `advance_past_language()` is
   only called from `callback_router._handle_language()` (the inline
   button's callback handler) — the plain-text `/language` command
   path (`handlers.language_status()`/`language_handler()`) updates
   the `language` column but never touches `registration_step`. A
   brand-new user who types `/language UZ` instead of tapping the
   picker button sets their language successfully, but
   `registration_step` remains `"LANGUAGE"` — every subsequent
   `/start` keeps re-showing the language picker, and the user is
   never routed to Phone Share through that path. This is a narrow
   edge case (the Wizard's own inline keyboard is what `/start`
   shows first, so a user would have to deliberately type the text
   command instead of tapping), but it is a real stuck-state path,
   found while tracing the Recovery Review.

Neither issue causes a crash, data loss, or lets one user act as
another — both are scoped to the Wizard's own completeness, not
Trading Core, not cross-user security.

### Freeze Recommendation

No blocking issue was found. Per the Director's own decision
criterion, Phase 3 is eligible for Freeze as-is. However, both
Remaining Issues above bear directly on whether "Registration Wizard"
means what its name promises (a wizard that actually gates
progression) — recommending the Director choose between:

- **(a) Freeze now**, treat both Remaining Issues as accepted,
  known, documented limitations (consistent with how the Stage 0
  audit's own pre-existing-BANNED-gap was treated); or
- **(b) Phase 3.1**, a small, separately-authorized fix for one or
  both issues before Freeze (Issue 2 is a small, contained fix —
  route `/language`'s text-command path through the same
  `advance_past_language()` call the callback path already uses;
  Issue 1 is the larger `command_router.py` permission-logic change
  the original audit flagged as scope-expanding).

This Review takes no position on which — it is a Director decision,
per this repository's governance rules.
