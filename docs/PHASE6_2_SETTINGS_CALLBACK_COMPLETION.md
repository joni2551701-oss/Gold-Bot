# V2 Phase 6.2 — Settings Callback Completion

Status: **IMPLEMENTED**. Scope authorized by the Director: `telegram/`,
`translation/`, `tests/`, `docs/`. Trading Core (`core/`, `decision/`,
`risk/`, `execution/`, `strategies/`, `signals/`, `context/`, `ai/`)
was not touched — confirmed at the end of this document ("Trading Core
Zero-Diff").

## Objective

Before this phase, the Settings page showed Risk/Strategy/Timeframe/
Notifications buttons whose inline-keyboard callbacks (`risk_*`,
`strategy_*`, `timeframe_*`, `notifications_*`) were recognized by
`callback_router.py` but not dispatched anywhere — tapping them just
cleared the Telegram loading spinner and did nothing (`docs/
PHASE6_NAVIGATION_AUDIT.md` documented this as "dead callback"). This
phase makes every one of those buttons actually update the database,
show the caller's real current values, and redraw itself in place.

## Reuse Audit (Stage 0)

Before writing any code, the following were re-read and confirmed:

| Symbol | File | Existing shape used |
|---|---|---|
| `settings_handler()` | `telegram/handlers.py` | extended, not replaced — now reads `_current_profile()` instead of a static string |
| `settings_keyboard()` | `telegram/keyboards.py` | untouched — it only opens the Settings submenu, unrelated to this phase |
| `callback_router.py` `route_callback()`/`_handle_language()` | `telegram/callback_router.py` | the edit-in-place + always-`answer()` pattern is reused verbatim for the new `_handle_setting()` |
| `command_router.py` `_KEYBOARD_BY_COMMAND` | `telegram/command_router.py` | extended from `{command: builder}` to `{command: (builder, current_value_accessor)}`, not replaced |
| `notifications_keyboard()` | `telegram/keyboards.py` | existed since Phase 43 as a display-only asset; this phase wires it in, it does not recreate it |
| DB user settings (`risk_percent`, `strategy`, `timeframe`, `notifications_enabled`) | `database_layer/user_repository/user_models.py` | all four fields already existed — no schema change |
| `UserService.change_risk/change_strategy/change_timeframe`, `NotificationService.enable_notifications/disable_notifications` | `telegram/user_service.py`, `telegram/notification_service.py` | reused as-is, already called by the pre-existing `/risk`, `/strategy`, `/timeframe`, `/notifications` text commands |
| Translation keys (`risk.*`, `strategy.*`, `timeframe.*`, `notifications.*`) | `translation/ui_catalog.py` | reused as-is; only `settings.menu` (extended with placeholders) and the new `settings.saved` key were added |

Conclusion: every requirement was satisfied by extending an existing
module (Module Reuse Principle step 2) — no new top-level file, class,
or dispatch mechanism was created.

## Architecture

No new layer was introduced. The existing three-part pattern
(`*_status()` rich result → thin `*_handler()` string wrapper →
router dispatch) established for `/language` in V1.1 Language UX
Polish is extended verbatim to Risk/Strategy/Timeframe/Notifications:

```
telegram/keyboards.py          risk_keyboard()/strategy_keyboard()/
                                timeframe_keyboard()/notifications_keyboard()
                                (selected= param added, Stage 6)
        |
telegram/command_router.py     _KEYBOARD_BY_COMMAND -- attaches the
                                keyboard with selected= from the
                                caller's current DB value (Stage 5)
        |
telegram/handlers.py           risk_status()/strategy_status()/
                                timeframe_status()/notifications_status()
                                -- rich (text, show_keyboard) result,
                                reusing LanguageUpdateResult as-is
        |                          \
   *_handler() (text command)       callback_router._handle_setting()
   -- thin `.text` wrapper          (inline callback -- edit-in-place,
                                      Stage 6)
        |                                      |
telegram/user_service.py /             UserService / NotificationService
telegram/notification_service.py       (unchanged)
        |
database_layer/user_repository/user_repository.py    (unchanged -- no schema change)
```

## Callback Flow (Stage 1-4, 6)

`telegram/callback_router.py` gained one dict, `_SETTING_CALLBACKS`,
mapping each prefix (`risk`, `strategy`, `timeframe`, `notifications`)
to its `handlers.*_status` name, its `keyboards.*_keyboard` builder,
its `handlers._current_*` accessor name, and a `parse` function that
turns the callback_data suffix into the same `args` string the
equivalent text command would receive. `route_callback()` now checks
this dict (after the existing `lang_*` check, before the
recognized-but-unimplemented fallback) and dispatches to a new
`_handle_setting()` helper.

`status_fn`/`current_value` are stored as attribute **names**, looked
up on `handlers` at call time (`getattr(handlers, entry["status_fn"])`)
rather than captured as direct function references at import time —
this mirrors `_handle_language()`'s own `handlers.language_status(...)`
call, which is a live attribute lookup, not a bound reference. This
matters for testability (`monkeypatch.setattr(handlers, "risk_status",
fake)` only works against a live lookup) and was caught by a failing
test during implementation (see "Test Coverage" below).

Example: a tap on the "Aggressive" risk button sends `callback_data =
"risk_5"`. `_handle_setting()`:

1. Parses `"5"` from the suffix (risk's `parse` is identity).
2. Calls `handlers.risk_status(telegram_id, args="5")` — the exact
   function `/risk 5` already calls.
3. Always calls `callback.answer()` (clears the Telegram spinner).
4. If the update succeeded (`result.show_keyboard is False`), appends
   `"\n\n" + t("settings.saved", language)` to the reply text.
5. Reads the caller's *fresh* current value via
   `handlers._current_risk(telegram_id)` — not the tapped value — so
   a failed update still shows the true DB state.
6. Rebuilds the keyboard via `risk_keyboard(language, selected=...)`
   and always reattaches it (`callback.message.edit_text(text,
   reply_markup=keyboard)`), unlike the language picker's own
   `_handle_language()`, which drops its keyboard once a language is
   actually chosen. Risk/Strategy/Timeframe/Notifications are settings
   the caller may keep adjusting, so their picker never disappears.
7. Falls back to `callback.message.answer(...)` (a new message) if
   `edit_text()` fails, matching every other router path.

Strategy is the one prefix whose `parse` is not the identity function:
its keyboard callback_data uses underscore slugs
(`strategy_liquidity_sweep`) while `handlers._STRATEGY_OPTIONS`' keys
use spaces (`"liquidity sweep"`), so `parse` does
`suffix.replace("_", " ")`.

## Database Flow

No schema change. Each `*_status()` function calls the same service
method the pre-existing text command already called:

- `risk_status()` → `UserService().change_risk(telegram_id, float(percent))`
- `strategy_status()` → `UserService().change_strategy(telegram_id, display_name)`
- `timeframe_status()` → `UserService().change_timeframe(telegram_id, timeframe)`
- `notifications_status()` → `NotificationService().enable_notifications()` / `.disable_notifications()`

An invalid choice (e.g. `risk_99` reaching the router from a stale
client-cached keyboard) never reaches these calls — validated against
`_RISK_OPTIONS`/`_STRATEGY_OPTIONS`/`_TIMEFRAME_OPTIONS` first, same as
the text command path.

## Current Value Display (Stage 5)

`telegram/handlers.py` gained `_current_profile()` (one best-effort
`UserService().get_profile()` call, never raises) and four thin
accessors on top of it: `_current_risk()`, `_current_timeframe()`,
`_current_strategy_slug()`, `_current_notifications_choice()`.
`settings_handler()` now renders `settings.menu` with the caller's
real `language_value`/`risk_value`/`strategy_value`/`timeframe_value`/
`notifications_value` (falling back to `common.na` for an unregistered
caller), instead of the previous static command-list text.
`command_router.py`'s `_KEYBOARD_BY_COMMAND` pairs each builder with
its accessor so `/risk`, `/strategy`, `/timeframe`, `/notifications`
(the text-command path) also open their picker pre-marked with the
caller's current choice.

## Inline UX (Stage 6)

`telegram/keyboards.py` gained a private `_radio_label(label, value,
selected)` helper: `selected=None` (every pre-existing call site)
returns the label unchanged — byte-identical to pre-Phase-6.2 output,
verified against every existing exact-text assertion in
`tests/telegram/test_keyboards.py`. Passing a `selected` value prefixes
each button with `●` (match) or `○` (no match), giving the
"○ Conservative / ● Moderate / ○ Aggressive" behavior the Director
specified. `risk_keyboard()`, `strategy_keyboard()`,
`timeframe_keyboard()`, `notifications_keyboard()` all gained a
`selected=None` parameter that threads into `_radio_label()`.
`language_keyboard()` also gained the parameter (accepted, ignored) so
`command_router.py`'s single generic call site
(`builder(language, selected=selected)`) works uniformly across all
five pickers — language has no "current value you are adjusting"
radio concept.

## Navigation (Stage 7)

Unchanged. The Reply Keyboard Navigation Framework (V2 Phase 6.3) and
its section tracker live entirely in `command_router.py`'s `else`
branch (non-inline-picker commands); this phase only touched the `if`
branch that attaches an inline value-picker keyboard, which was never
part of Reply Keyboard navigation to begin with. No `◀️ Ortga`/`🏠 Bosh
sahifa` behavior was modified.

## Translation (Stage 8)

`translation/ui_catalog.py` changes, EN/UZ/RU for all three:

- `settings.menu` rewritten with `{language_value}`/`{risk_value}`/
  `{strategy_value}`/`{timeframe_value}`/`{notifications_value}`
  placeholders (previously a static command-list string).
- New `settings.saved` key (✅ Saved / ✅ Saqlandi / ✅ Сохранено), shown
  under the confirmation text after a successful inline update.

No hardcoded strings were introduced in `callback_router.py` or
`handlers.py` — every reply string routes through `t()`.

## Test Coverage (Stage 9)

New/updated files:

- `tests/telegram/test_callback_router.py` — `risk_1`/`strategy_fvg`/
  `timeframe_h1`/`notifications_on` were removed from the "recognized
  but unimplemented" test (they are implemented now); 18 new tests
  cover per-prefix dispatch shape (mocked `*_status`, mirroring the
  existing `_patch_language_status` pattern), keyboard-always-attached,
  "✅ Saved" appended only on real success, edit-fails-falls-back-to-
  new-message, always-`answer()`, never-raises, and four real-DB
  end-to-end persistence tests (risk/strategy/timeframe/notifications).
- `tests/telegram/test_settings_callbacks.py` — new file, 18 tests
  against the real `UserService`/`UserRepository` (mirroring
  `test_language_handler.py`'s convention): valid/invalid choice for
  each of the four settings, DB persistence, DB *not* changing on an
  invalid choice, the `*_handler()` thin-wrapper contract (`str`
  return, matching CLAUDE.md's no-breaking-changes rule),
  three-language translation coverage for `risk.updated`,
  `settings_handler()`'s real current-value display, and the `N/A`
  fallback for an unregistered caller.
- `tests/telegram/test_keyboards.py` — 9 new tests for the `selected=`
  parameter: `selected=None` byte-identical to pre-Phase-6.2 output
  for risk/notifications, correct `●`/`○` marking for
  risk/timeframe/strategy/notifications, callback_data unaffected, and
  `language_keyboard()` accepting-but-ignoring `selected`.

Total: **45 new tests** (18 + 18 + 9).

One defect surfaced by this test-writing process itself:
`_SETTING_CALLBACKS` initially stored `handlers.risk_status` (etc.) as
a direct function reference, captured once at module import — tests
monkeypatching `handlers.risk_status` had no effect on it, because
`_handle_setting()` was calling the captured reference, not doing a
fresh lookup. Fixed by storing attribute *names* and calling
`getattr(handlers, name)` inside `_handle_setting()`, matching
`_handle_language()`'s existing live-lookup shape. All 45 new tests
plus the full pre-existing `tests/telegram/` and
`tests/security/test_input_validation.py` suites pass after the fix.

## Rollback

Every change in this phase is additive or a signature extension with a
backward-compatible default (`selected=None`), confined to `telegram/`
and `translation/`. Reverting the four touched files
(`telegram/handlers.py`, `telegram/keyboards.py`,
`telegram/command_router.py`, `telegram/callback_router.py`) plus
`translation/ui_catalog.py` and the three new/updated test files
returns the bot to the exact pre-Phase-6.2 "recognized but
unimplemented" callback state — no database migration was introduced,
so no down-migration is needed.

## Trading Core Zero-Diff Confirmation

`core/`, `decision/`, `risk/`, `execution/`, `strategies/`, `signals/`,
`context/`, `ai/` were not read or modified during this phase. Every
change is confined to `telegram/`, `translation/`, `tests/`, and
`docs/`, as authorized.
