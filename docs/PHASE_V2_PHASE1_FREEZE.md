# V2 Phase 1 Freeze — Language Foundation

Freeze Tag: **V2 Phase 1 Freeze**. Director-approved incremental
delivery (Phase 1.0 → 1.6, each independently code-reviewed, tested,
CI-confirmed, and production-deployed before the next sub-phase
started). This document is the single freeze record for the whole
phase — per-commit detail lives in the commit messages themselves;
this is the roll-up.

## Freeze Criteria (Director's own, verbatim scope)

> 🌐 User tanlagan til avtomatik yuklanadi.
> 🌐 Har bir handler user.language orqali matn chiqaradi.
> 🌐 UZ/RU ishlaydi (EN fallback bo'lishi mumkin).
> 🌐 Barcha tugmalar (inline va keyinchalik reply) localization orqali yaratiladi.
> 🌐 Hardcoded user-facing string qolmaydi — Director later scoped this
> down to "no hardcoded string on the two flows explicitly named
> blocking" (`/language`, `contact_handler`), not literally zero
> across the whole USER-tier surface. See Deferred Items below for
> what's intentionally still hardcoded.

All five are met on the scope the Director explicitly approved for
Phase 1 (USER-tier commands + keyboards; `/language` and
`contact_handler` self-localization). OWNER/ADMIN-tier commands were
never in scope and remain English by design (Director decision).

## Changelog

### Phase 1.0/1.1 — Language Callback Fix + UX Polish
Commits: `31493da`, `cabed8c`.
- Wired `/language`'s inline keyboard to a real `callback_query`
  handler (`telegram/callback_router.py`, new file) — previously the
  keyboard existed but taps did nothing.
- `language_status()`/`LanguageUpdateResult` added to
  `telegram/handlers.py`: shows the caller's current language with no
  args, no-ops on re-selecting the current language, removes the
  picker keyboard once a change actually lands.

### Phase 1.3/1.4 — Translation Engine + Localized Handlers
Commit: `c3f86f6`.
- New `translation/ui_catalog.py`: a static UZ/RU/EN string catalog
  and `t(key, language, **kwargs)` lookup (caller's language → EN →
  any entry; never raises).
- All 17 `COMMANDS`-registry USER-tier handlers
  (`telegram/handlers.py`) rewired to route text through `t()` instead
  of hardcoded English.
- Director's explicit, load-bearing decision recorded here: the DB
  schema default (`users.language = 'UZ'`) was **not** changed to
  make English tests pass — the ~15 affected tests were updated to the
  new Uzbek-default product spec instead ("Testlar mahsulotni emas,
  mahsulot spetsifikatsiyasini aks ettirishi kerak").
- OWNER/ADMIN-tier handlers (`telegram/owner/*.py`, `admin_handler`,
  `broadcast_handler`, etc.) deliberately left untouched — flagged to
  the Director as a scope decision, confirmed: OWNER/ADMIN stays
  English-only, permanently, not a future phase.

### Phase 1.5 — Localized Keyboards
Commit: `db7dffd`.
- Every USER-tier keyboard in `telegram/keyboards.py` (language, risk,
  timeframe, strategy, settings, notifications, phone_share) takes an
  optional `language` and resolves labels via `t()`; `callback_data`
  never changes with language. `admin_panel_keyboard()` explicitly
  excluded — stays English, zero-arg signature unchanged.
- `telegram/command_router.py` and `telegram/callback_router.py`
  resolve and pass the caller's stored language into the keyboard
  builders.

### Phase 1.6 — `/language` self-localization + `contact_handler` fix
Commit: `5c1f806`.
- `language_status()`/`language_handler()`'s own reply text (the one
  place that had stayed hardcoded English through 1.3/1.4, since it
  predates the Translation Engine) now routes through `t()`. The
  success confirmation renders in the newly-selected language; every
  other branch renders in the caller's pre-existing language.
- `contact_handler`'s failure path no longer echoes
  `UserService.register_phone()`'s raw English `.reason` string — its
  two known failure reasons map to new `contact.not_registered`/
  `contact.phone_reused` catalog keys, with `contact.error` as the
  fallback for any future unrecognized reason.

## Changed Files (full list, Phase 1.0 → 1.6)

| File | Change |
|---|---|
| `telegram/callback_router.py` | New — callback_query dispatch for `lang_*` |
| `telegram/command_router.py` | Keyboard language wiring |
| `telegram/handlers.py` | All USER-tier handlers + `/language` + `contact_handler` localized |
| `telegram/keyboards.py` | All USER-tier keyboards localized |
| `telegram/polling.py` | Callback router wiring |
| `translation/ui_catalog.py` | New — 77-key UZ/RU/EN catalog + `t()` |
| `tests/integration/test_telegram_flow.py` | Updated for UZ-default text |
| `tests/security/test_database_security.py` | Updated for UZ-default text |
| `tests/security/test_input_validation.py` | Updated for UZ-default + `/language` text |
| `tests/telegram/test_callback_router.py` | New |
| `tests/telegram/test_keyboards.py` | New |
| `tests/telegram/test_language_handler.py` | New/updated |
| `tests/telegram/test_phone_registration.py` | Updated for UZ-default + `contact_handler` failure tests |
| `tests/telegram/test_polling.py` | New |
| `tests/test_feedback.py` | Updated for UZ-default text |
| `tests/translation/test_ui_catalog.py` | New |

16 files, +1427/-226 lines across the full phase.

## Translation Catalog Summary

77 total keys in `translation/ui_catalog.py`, **every key has UZ, RU,
and EN** — verified programmatically (`tests/translation/
test_ui_catalog.py::test_every_catalog_entry_has_uz_ru_and_en`), zero
missing. Breakdown: 22 `keyboard.*` (Phase 1.5), 5 `language.*` + 5
`contact.*` (Phase 1.6), 45 other handler-text keys (Phase 1.3/1.4).

## Test Growth

4575 (pre-Phase-1 baseline, `1aebd48`) → **4622** (post-Phase-1,
`5c1f806`) — 47 net-new tests, 0 removed. Full suite passing at every
commit in the phase.

## Trading Core / OWNER-ADMIN Verification

Verified empty across the **entire** Phase 1 range (`1aebd48..5c1f806`,
every commit):
```
git diff --stat 1aebd48 5c1f806 -- core/ decision/ risk/ execution/ strategies/ signals/ context/ ai/
git diff --stat 1aebd48 5c1f806 -- telegram/owner/ telegram/admin_service.py
```
Both empty. Confirmed additionally at the `telegram/handlers.py`
diff-hunk level: every hunk across the phase falls within USER-tier
handler functions (`start_handler` → `feedback_handler`, plus
`contact_handler`); no hunk touches `admin_handler`,
`addadmin_handler`, `broadcast_handler`, `stats_handler`,
`users_handler`, `userinfo_handler`, `vipinfo_handler`,
`feedbacks_handler`, or any `ai_*`/`owner_*`/`runtime_*` handler.

## Production Verification

- GitHub Actions (GoldBot CI + GoldBot Production Deployment): green
  on all 5 Phase 1 commits (`31493da`, `cabed8c`, `c3f86f6`, `db7dffd`,
  `5c1f806`).
- Production Telegram Manual Test (Language): **PASS**, confirmed by
  the Director — `/language`, UZ/RU/EN selection via inline buttons,
  language persists across bot restart.

## Deferred Items (explicit, Director-approved)

| Item | Deferred to | Why |
|---|---|---|
| `telegram/signal_formatter.py` (`/signal`, `/history` content) | **V2.1** | Signal Product Layer — will be rebuilt alongside V2.1 Price Stream Foundation anyway; localizing now risks a second rewrite. |
| `telegram/signal_access_service.py` (`DENIED_MESSAGE_TEMPLATE`, the FREE-plan upgrade prompt) | **V2.1** | Same Signal Product Layer boundary as above. |
| `telegram/command_router.py`'s generic constants (`UNKNOWN_COMMAND_TEXT`, `SERVICE_UNAVAILABLE_TEXT`, `PERMISSION_DENIED_TEXT`) | **V2.2** | Belongs to a future Generic Error Catalog, done once as a system-wide UX refactor, not piecemeal per phase. |

OWNER/ADMIN-tier commands (`telegram/owner/*.py` and the operator
console) are **not** a deferred item — they are permanently
English-only by Director decision (internal operator tooling; a
future Operator Localization Phase would be a distinct, separately-
authorized effort, not implied by this freeze).

## Freeze Declaration

**Language Foundation is frozen as of commit `5c1f806`.** No further
changes to `translation/ui_catalog.py`, the localized USER-tier
handlers/keyboards, or the callback/command router language wiring
without explicit Director approval.

## Phase 1 Statistics

| Metric | Value |
|---|---|
| Duration | Phase 1.0 → Phase 1.6 |
| Commits | 5 (`31493da`, `cabed8c`, `c3f86f6`, `db7dffd`, `5c1f806`) |
| Files Changed | 16 |
| New Files | 6 (`telegram/callback_router.py`, `translation/ui_catalog.py`, `tests/telegram/test_callback_router.py`, `tests/telegram/test_keyboards.py`, `tests/telegram/test_language_handler.py`, `tests/translation/test_ui_catalog.py`) |
| Modified Files | 10 |
| Translation Keys | 77 |
| Languages | UZ, RU, EN |
| Tests | 4575 → 4622 (+47) |
| GitHub Actions | Passed (all 5 commits) |
| Production Deployment | Passed (all 5 commits) |
| Manual Telegram Test | Passed (Director-confirmed) |
| Trading Core | Zero Diff |
| Owner/Admin | Zero Diff |

## Lessons Learned

- **Translation Engine must exist before any handler is localized** —
  building `translation/ui_catalog.py` first (Phase 1.3) and only then
  wiring handlers (Phase 1.4 onward) avoided a second pass; doing it
  handler-by-handler with inline strings would have meant redoing
  every handler once the catalog pattern was chosen.
- **Callback architecture should precede keyboard localization** —
  `telegram/callback_router.py` (Phase 1.0/1.1) had to exist before
  Phase 1.5's keyboard `language` wiring made sense; building keyboards
  first would have meant retrofitting callback plumbing around
  already-shipped button labels.
- **Localization work should never touch Trading Core** — held for
  all 5 commits without exception; the zero-diff check on every commit
  (not just at the end) caught nothing, but running it every time
  cost nothing and kept the guarantee real, not assumed.
- **A "small, obvious" scope still needs its own explicit freeze gate**
  — the `/language` self-localization and `contact_handler` gaps
  found in the Phase 1 Final Audit were both easy to miss during
  Phase 1.3/1.4's handler sweep precisely because they looked done;
  a dedicated audit pass (not just "did I touch every file in
  `COMMANDS`") is what caught them.
- **Manual Production Test is mandatory before Freeze, CI is not a
  substitute** — GitHub Actions confirms the code builds/deploys;
  it says nothing about whether a real Telegram client renders the
  UZ/RU/EN text and inline buttons correctly. Both were required
  before this Freeze, not either/or.

## Phase 2 Checklist

- [x] Delete GitHub Owner Snapshot (Repository/Security cleanup —
      scope, rules, and deliverable format per the Director's Phase 2
      task brief; audit-first, no deletion until the Director confirms
      the audit). See `docs/PHASE_OWNER_SNAPSHOT_REMOVAL.md` for the
      removal record.
