# V2 Phase 4 Freeze — Persistent Menu

## Summary

Phase 4 delivered Telegram's native Menu Button (Persistent Menu) in
two stages:

- **Stage 0 (Audit)**: presented to the Director as a chat-only
  report per that stage's explicit "no commits" rule — repository/
  command/registration/reuse audit, confirmed no
  `BotCommand`/`setMyCommands`/`MenuButton` infrastructure existed,
  confirmed every USER-tier command handler was already reusable
  as-is.
- **Stage 1 (Implementation, commit `56f6878`)**: new
  `telegram/menu_commands.py` registers the Menu Button via
  `Bot.set_my_commands()` — `BotCommandScopeDefault` for the localized
  (UZ/RU/EN) USER menu (🏠 Home / 👤 Profile / 📊 Signals / 💳
  Subscription / ⚙️ Settings / ❓ Help), `BotCommandScopeChat` per
  known ADMIN/OWNER for their richer menu in their own stored
  language. Registered once at bot startup
  (`telegram/polling.py`). No change to `command_router.py`,
  `handlers.py`, `callback_router.py`, or the Registration Wizard.
  Trading Core: zero-diff. 15 new tests, GitHub Actions green.

## Production Manual Test Finding

During Production Manual Test the Director exercised the live menu
end-to-end and found:

> Persistent Menu to'liq ishlaydi. Ammo `/settings` ichidagi `risk_*`,
> `strategy_*`, `timeframe_*` va `notifications_*` inline callback
> tugmalari hali implementatsiya qilinmagan (faqat `lang_*` callback
> mavjud). Bu avvaldan mavjud cheklov bo'lib, Phase 4 regressiyasi
> emas. Ushbu ish alohida bosqichga rejalashtirilsin.

Confirmed against the code: `telegram/callback_router.py`'s
`_RECOGNIZED_PREFIXES` has always listed `risk_`, `strategy_`,
`timeframe_`, `notifications_`, `settings_`, and `admin_` as
"recognized category, not yet implemented" — only `lang_uz`/`lang_ru`/
`lang_en` route to real logic (`_handle_language()`); every other
prefix just clears the Telegram client's loading spinner
(`callback.answer()`) and does nothing else, exactly as that module's
own docstring has documented since before this phase:

> "Scope (V1 Language Callback Fix; UX polished in V1.1 Language UX
> Polish): only the lang_uz/lang_ru/lang_en callbacks from
> telegram.keyboards.language_keyboard() are implemented. Every other
> keyboard's callback_data (risk_*, timeframe_*, strategy_*,
> notifications_*, settings_*, admin_*) is recognized here as a
> category ready for a future phase, but not yet handled..."

**This is not a Phase 4 regression.** Persistent Menu did exactly its
job: the Menu Button appeared, `/settings` opened, `settings_handler()`
ran, and the (pre-existing) inline keyboard rendered. The gap is
entirely inside `/settings`'s own inline callbacks — a limitation that
predates Phase 4 by many phases and would be identically present
whether or not Persistent Menu ever shipped.

## Freeze Decision

**Phase 4 is Frozen.** The finding above is real and is not being
hidden, but it is out of Phase 4's own scope (Persistent Menu never
touched `callback_router.py`'s dispatch logic — see Stage 1's own
"qat'iy taqiqlar" compliance in commit `56f6878`) and holding Phase 4
open for it would be incorrect project management, per the Director's
own decision.

## Roadmap

```
V2 Phase 4 Freeze
        ↓
Phase 4.1 — Registration Access Policy
        ↓
Phase 5 — Reply Keyboard
        ↓
Phase 5.x — Settings Callback Completion
    (risk_*, strategy_*, timeframe_*, notifications_* callbacks
    implemented the same way lang_* already is)
```

Settings Callback Completion scope (for whichever phase slot it lands
in): wire `risk_*`/`strategy_*`/`timeframe_*`/`notifications_*`
callback_data to real `UserService`/`NotificationService` calls in
`telegram/callback_router.py`, mirroring `_handle_language()`'s
existing shape — no new architecture, a direct extension of the
pattern already proven for language.
