# V2 Phase 5 Stage 0 Audit — Reply Keyboard

Status: AUDIT ONLY. No implementation code in this document; per the
Director's instruction, implementation begins only after this audit
is reviewed and approved.

Scope authorized by the Director: existing `ReplyKeyboardMarkup`
usage, conflicts with `phone_share_keyboard()`, Reply Keyboard
lifecycle, handler reuse, Registration Wizard integration, coexistence
with Persistent Menu (Phase 4), localization, `ReplyKeyboardRemove`
placement, architecture diagram, risk analysis, reuse audit, open
questions.

---

## 1. Existing `ReplyKeyboardMarkup` Usage

Repo-wide search confirms exactly **one** `ReplyKeyboardMarkup` in the
entire codebase: `telegram/keyboards.py`'s `phone_share_keyboard()`
(Phase 61.5 TASK 4). Every other keyboard (`language_keyboard`,
`risk_keyboard`, `timeframe_keyboard`, `strategy_keyboard`,
`settings_keyboard`, `notifications_keyboard`, `admin_panel_keyboard`)
is `InlineKeyboardMarkup`.

`phone_share_keyboard()` is attached to a reply in exactly two places:

1. **`telegram/command_router.py`**'s `_start_keyboard()` — when
   `registration_step == "PHONE"`, `/start`'s `RouterResult.keyboard`
   is `phone_share_keyboard(language)`.
2. **`telegram/callback_router.py`**'s `_handle_language()` — after a
   language tap advances the Wizard from `LANGUAGE` to `PHONE`
   (`RegistrationService().advance_past_language()` returns `True`), a
   **new** message is sent via `callback.message.answer(t("registration.phone_prompt", ...), reply_markup=phone_share_keyboard(language))`.

`ReplyKeyboardRemove` — **zero occurrences anywhere in the codebase**.
No code path currently hides a `ReplyKeyboardMarkup` once shown; the
keyboard's own `one_time_keyboard=True` flag is the only "hide"
mechanism in effect today (Telegram clients auto-collapse a
`one_time_keyboard` after one tap, but the keyboard icon remains
available to reopen it manually until a new keyboard replaces it or
`ReplyKeyboardRemove` is sent).

---

## 2. Conflicts with `phone_share_keyboard()`

**Telegram platform constraint**: a chat has at most **one active
`ReplyKeyboardMarkup` at a time** — sending a message with a new
`ReplyKeyboardMarkup` silently replaces whatever custom keyboard was
showing before (there is no "stacking"; the previous one is simply
gone, no removal step needed for the replacement itself). This means
a persistent Reply Keyboard and `phone_share_keyboard()` **cannot both
be visible simultaneously** — whichever was sent most recently wins.

**Where this actually collides**: only during the Registration
Wizard's `PHONE` step. `phone_share_keyboard()` is `one_time_keyboard=True`
by design (Phase 61.5's own docstring: "the keyboard hides itself
after one tap, same 'don't linger' convention"), and it is the
**only** UI surface that can produce a `Contact` share
(`KeyboardButton(request_contact=True)` — no `InlineKeyboardButton`
can request a contact). If a persistent Reply Keyboard is shown to a
user who is still mid-Wizard (`registration_step` is `LANGUAGE` or
`PHONE`), it would silently replace `phone_share_keyboard()` and the
user would lose the only button that can complete registration.

**No conflict outside the Wizard**: once `registration_step == "COMPLETE"`,
`phone_share_keyboard()` is never attached to anything again (per
`_START_KEYBOARD_BY_STEP`'s own design — `RegistrationStep.COMPLETE`
has no entry, so `_start_keyboard()` returns `None`). A persistent
Reply Keyboard for a fully-registered user has nothing to collide
with.

**Conclusion**: the Reply Keyboard must be **withheld during
registration** (`registration_step != "COMPLETE"`) and only take over
once the Wizard reaches `COMPLETE` — see Section 5.

---

## 3. Reply Keyboard Lifecycle

- **Creation**: `ReplyKeyboardMarkup(keyboard=[[KeyboardButton(...), ...], ...], resize_keyboard=True, one_time_keyboard=<bool>)` — same constructor `phone_share_keyboard()` already uses. `resize_keyboard=True` is the established convention (fits the button row to content rather than full-height).
- **Replacement**: automatic and free — any message sent with a *different* `ReplyKeyboardMarkup` replaces the visible one. No explicit teardown step is needed to swap one Reply Keyboard for another.
- **Removal**: requires sending `ReplyKeyboardRemove()` as a message's `reply_markup` — the one operation with no current call site in this codebase (Section 1). A persistent Reply Keyboard, by definition, is not expected to be removed under normal use; `ReplyKeyboardRemove` would only matter for a BANNED user (Section 5) or an explicit "hide keyboard" affordance, neither of which exists as a command today.
- **Attachment point**: identical to every other keyboard type — `RouterResult.keyboard` (already a generic `Optional[object]`, per `telegram/command_router.py`'s own dataclass) flows straight into `message.answer(result.text, reply_markup=result.keyboard)` in `telegram/polling.py`'s `_on_message`. `reply_markup` accepts `InlineKeyboardMarkup`, `ReplyKeyboardMarkup`, or `ReplyKeyboardRemove` interchangeably — no dispatch-layer change needed to attach a Reply Keyboard instead of an inline one.

---

## 4. Handler Reuse

No handler needs to change. `RouterResult(text, keyboard)`'s
`keyboard` field is already polymorphic — every existing USER-tier
handler (`start_handler`, `help_handler`, `profile_handler`, etc.)
returns plain text; `command_router.py` decides the keyboard
independently via `_KEYBOARD_BY_COMMAND`/`_start_keyboard()`. A
persistent Reply Keyboard is purely an **attachment-point change** in
`command_router.py` (which builder gets called for which command),
exactly the same shape as Phase 3's `_start_keyboard()` addition and
Phase 4's `menu_commands.py` — no new module touches `handlers.py`.

---

## 5. Registration Wizard Integration

Per Section 2, the Reply Keyboard must be conditional on
`registration_step`:

| `registration_step` | Reply Keyboard shown |
|---|---|
| `LANGUAGE` | None (inline `language_keyboard` only, existing behavior) |
| `PHONE` | `phone_share_keyboard()` only (existing behavior, unchanged) |
| `COMPLETE` | New persistent Reply Keyboard |

This mirrors `_START_KEYBOARD_BY_STEP`'s existing dict-lookup shape in
`command_router.py` — a new step-to-keyboard mapping alongside it, not
a replacement of it. `handlers._registration_step()` (already
public) is the exact same read Phase 3/4 already use — no new
registration-state plumbing needed.

**BANNED users**: `RegistrationService.current_step()` already
returns `None` for a BANNED user, which today means "no Wizard
keyboard." A persistent Reply Keyboard keyed only on `registration_step == COMPLETE`
would need its own BANNED check (a BANNED user could theoretically
have `registration_completed=True` from before being banned) — this
is the one place `ReplyKeyboardRemove` plausibly earns a first real
call site: hiding the persistent keyboard for a BANNED user's `/start`
reply.

---

## 6. Coexistence with Persistent Menu (Phase 4)

**No conflict** — these are two structurally independent Telegram UI
surfaces:

- **Persistent Menu** (Phase 4, `telegram/menu_commands.py`): a
  `BotCommand` list attached to the client's own "/" menu-button /
  command-suggestion UI, set once via `Bot.set_my_commands()`. It does
  not occupy the message compose area.
- **Reply Keyboard** (this phase): a `ReplyKeyboardMarkup` that
  replaces the device's own keyboard in the message compose area,
  attached per-message via `reply_markup`.

A user can have both active at once with no platform-level exclusivity
rule between them — tapping a Persistent Menu command still works
identically regardless of what Reply Keyboard is currently shown
(confirmed by Section 3: Reply Keyboard never blocks text/command
entry, it only offers convenience buttons). The two phases are
additive, not competing for the same UI slot the way Reply Keyboard
and `phone_share_keyboard()` are (Section 2).

---

## 7. Localization

Existing pattern, no new mechanism needed:
`translation.ui_catalog.t(key, language)` — `phone_share_keyboard()`
already resolves its one button's label via `t("keyboard.phone_share", language)`.
A persistent Reply Keyboard's buttons would add new catalog keys
(e.g. `keyboard.persistent.*`) following the exact `menu.*` precedent
Phase 4 just established, resolved the same way every other
USER-tier keyboard already is (`_current_language()`/
`UserRecord.language`, never Telegram's own client `language_code`).

---

## 8. Where `ReplyKeyboardRemove` Should Be Used

Two concrete candidates surfaced by this audit (neither exists today):

1. **BANNED `/start`** (Section 5) — hide a persistent Reply Keyboard
   for a user who was banned after completing registration.
2. **Wizard re-entry edge case**: if a completed user's Reply Keyboard
   is showing and something forces them back into an earlier Wizard
   step (no such path exists today — `advance_past_language()`'s own
   no-op guard prevents a completed registration from reopening, per
   Phase 3's Review), `ReplyKeyboardRemove` would be the correct way
   to clear it before showing `phone_share_keyboard()` again. Flagged
   for completeness; not an active requirement given the existing
   no-reopen guarantee.

No other command in `telegram/commands.py`'s `COMMANDS` registry
implies "the user wants their keyboard cleared" — this is a small
surface, not a general mechanism.

---

## 9. Architecture / Navigation Diagram

```
Telegram User (registration_step == COMPLETE)
        ↓
Reply Keyboard button tapped
        ↓
Telegram Client sends button text as an ordinary text message
        ↓
telegram/polling.py  (_on_message, message.contact is None)
        ↓
telegram/command_router.route_message()
        ↓
telegram/command_router.route_command()
        ├─ _parse_command() -- ONLY IF the button's text is a "/command"
        │                        (same constraint Phase 4's analysis
        │                        already established for Persistent Menu)
        ├─ existing permission/handler dispatch, UNCHANGED
        └─ keyboard selection: registration_step-aware lookup (Section 5)
                instead of unconditionally re-showing the previous keyboard
        ↓
RouterResult(text, keyboard)
        ↓
message.answer(result.text, reply_markup=result.keyboard)
```

**Design constraint this diagram exposes**: a `ReplyKeyboardMarkup`
button's `text` is sent as a plain message — it is **not** a
`callback_query`. For a Reply Keyboard button to actually invoke a
command, its `text` must literally be a `/command` string (e.g.
`"/profile"`), exactly like Persistent Menu's own mechanism (Phase 4
Stage 0 Audit, Section 5 "Design"). A Reply Keyboard button labeled
with an emoji + localized word (e.g. "👤 Profil") would **not** route
anywhere unless `command_router.py` is taught to recognize that label
as an alias for `/profile` — this is a design decision Section 12
raises as an Open Question, since it directly affects whether new
"business logic" (label→command mapping) needs to live in
`command_router.py`, which the Director's Phase 4 rules were careful
to keep untouched for callback dispatch.

---

## 10. Risk Analysis

| Area | Risk | Assessment |
|---|---|---|
| Trading Core | None | Not touched by any Reply Keyboard candidate design |
| Registration Wizard | Real, addressed in Section 5 | Must gate the persistent keyboard to `registration_step == COMPLETE`; already-existing `advance_past_language()` no-op guard protects against re-triggering the Wizard |
| Language System | None | Reuses existing `t()`/`UserRecord.language` pattern |
| `callback_router.py` | None expected | Reply Keyboard buttons are text messages, not `callback_query` -- no new callback dispatch needed |
| Persistent Menu (Phase 4) | None | Structurally independent UI surfaces (Section 6) |
| `phone_share_keyboard()` | Real, addressed in Section 2 | Must never be replaced by the persistent keyboard while `registration_step != COMPLETE` |
| Label→command mapping | Open design question (Section 9/12) | If Reply Keyboard buttons use localized emoji labels rather than literal `/command` text, `command_router.py` needs a small alias table -- scope and placement not yet decided by the Director |

---

## 11. Reuse Audit

| Existing asset | Reusable as-is? |
|---|---|
| `RouterResult(text, keyboard)` | ✅ Already polymorphic, no change needed |
| `command_router.py`'s `_KEYBOARD_BY_COMMAND` dict-lookup pattern | ✅ Same shape extends to a new step-aware table |
| `_START_KEYBOARD_BY_STEP` / `_start_keyboard()` | ✅ Direct precedent for the `registration_step`-gated logic Section 5 needs |
| `translation.ui_catalog.t()` | ✅ No change |
| `handlers._registration_step()` | ✅ No change, already public |
| `telegram/keyboards.py` | ✅ New builder function(s) added the same way `phone_share_keyboard()` was (Phase 61.5), `notifications_keyboard()` was (Phase 43), etc. |
| `phone_share_keyboard()` itself | ✅ Unchanged, still the PHONE-step keyboard |

**No new top-level module needed.** Everything fits inside
`telegram/keyboards.py` (new builder) and `telegram/command_router.py`
(new attachment logic) — the same two files every prior keyboard
phase (40, 41, 43, 61.5, V2 Phase 3) has extended.

---

## 12. Open Questions for the Director

1. **Button trigger mechanism**: should persistent Reply Keyboard
   buttons send a literal `/command` string (routes through the
   existing dispatch untouched, but the visible button label can't
   simultaneously be both the literal command text and a nicer
   localized label unless `command_router.py` also accepts label
   aliases), or a localized label that `command_router.py` must learn
   to map to a command (a small, contained addition to
   `command_router.py`, not `handlers.py`/`callback_router.py`)?
2. **Content**: which commands appear on the persistent Reply
   Keyboard? Section 6 confirms it doesn't need to duplicate
   Persistent Menu's set — should it mirror the same six
   (Home/Profile/Signals/Subscription/Settings/Help), a subset, or a
   different set entirely?
3. **BANNED-user keyboard removal** (Section 5/8): is adding this one
   `ReplyKeyboardRemove` call in scope for Phase 5, or deferred
   (mirroring how Phase 3 deferred the broader BANNED-enforcement gap
   to a future phase)?
4. **ADMIN/OWNER**: does the persistent Reply Keyboard differ by
   permission tier the way Phase 4's Persistent Menu does (USER vs
   ADMIN vs OWNER), or is it USER-tier only, with ADMIN/OWNER
   continuing to rely on the existing inline `admin_panel_keyboard()`
   and typed commands?

No implementation begins until the Director responds to this
document.

---

## 13. Phase 5.1 — Reply Keyboard UX Polish & Command Abstraction (Director Approved)

Status: **Implemented.** Reverses Open Question 1's original answer
(Section 12): Phase 5 shipped with the literal-`/command` option
(buttons showed `/profile`, `/signal`, etc.); the Director subsequently
approved Phase 5.1 to replace that with localized labels, since a user
should never see a raw slash command on the persistent keyboard.

### Navigation Mapping

`telegram/keyboards.py` owns the mapping, right next to the keyboard
builders it serves — no new top-level module, per the Module Reuse
Principle:

- `_REPLY_LABEL_KEYS`: `command -> translation.ui_catalog key`. The
  six USER-tier entries reuse Phase 4 Persistent Menu's own `"menu.*"`
  keys verbatim (`menu.home`, `menu.profile`, `menu.signals`,
  `menu.subscription`, `menu.settings`, `menu.help`) — identical labels
  in both surfaces by construction, not by convention. `menu.admin`/
  `menu.owner` are Phase 5.1's own additions (language-invariant, same
  posture as `menu_commands.py`'s `_ADMIN_EXTRA`/`_OWNER_EXTRA`).
- `NAVIGATION_MAP`: built once at import time — every label, in every
  supported language (EN/UZ/RU), mapped to its `"/command"` string.
- `resolve_navigation_command(text)`: the lookup function. Returns
  `None` for anything that isn't a known label (an ordinary message, or
  a literal `"/command"` typed by hand — those still go through
  `_parse_command()` unchanged).

### Dispatch flow

```
Reply Keyboard tap ("👤 Profil")
    -> aiogram Message (.text = "👤 Profil")
    -> command_router.route_message() -> route_command()
    -> resolve_navigation_command("👤 Profil") -> "/profile"
    -> _parse_command("/profile") -> ("profile", "")
    -> existing profile_handler() (unchanged)
```

`route_command()` calls `resolve_navigation_command()` as its very
first step, before `_parse_command()`. No second dispatch path exists:
a tapped label and a typed `/profile` produce byte-identical
`RouterResult.text` (see
`tests/telegram/test_phone_registration.py::test_navigation_label_from_the_reply_keyboard_routes_to_the_same_handler_as_its_command`).
`telegram/handlers.py` and `telegram/callback_router.py` are untouched.

### Reply Keyboard lifecycle (unchanged from Phase 5)

Still exactly the flow Section 8/9 already established — Phase 5.1
only changes what the buttons *say*, not *when* they appear:

```
/start -> Language step -> Phone Share Keyboard -> Registration COMPLETE
    -> persistent Reply Keyboard (now with localized labels)
```

`_persistent_reply_keyboard()` (`telegram/command_router.py`) now
resolves the caller's language (`handlers._current_language()`, the
same lookup every other localized keyboard builder in this module
already performs) and passes it to `reply_keyboard()`/
`admin_reply_keyboard()`/`owner_reply_keyboard()`, each of which
gained an optional `language` parameter. BANNED still gets
`ReplyKeyboardRemove()` first, checked independently, exactly as
before — Section 5/8's reasoning is unaffected by this phase.

### Telegram Menu coexistence

Unaffected: `telegram/menu_commands.py`'s native `☰ Menu` (Phase 4,
`Bot.set_my_commands()`) is a structurally separate Telegram surface
from `ReplyKeyboardMarkup` (Section 2's platform-constraint finding
still holds — this phase touches neither `menu_commands.py` nor its
registration call in `telegram/polling.py`). A user who prefers typing
`/profile` via the `☰ Menu` still reaches the exact same
`command_router.route_command()` path the Reply Keyboard now also
funnels through via Navigation Mapping.
