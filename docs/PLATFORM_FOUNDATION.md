# Platform Foundation (`platforms/`)

Written under `docs/PLATFORM_DOCUMENTATION_POLICY.md` — the first
module documented with its seven required sections, dogfooding the
policy on real content from the same phase that introduced it
(PLATFORM-001).

## Architecture

`platforms/` sits alongside `telegram/` as a second Platform-layer
package — not beneath it, not above it. It holds cross-platform
metadata and validation only; it is never imported by `core/pipeline.py`
or any Trading Core module, and (in this phase) is not yet imported by
`telegram/` either — it is a parallel foundation, the same
relationship `assets/`/`configuration/`/`strategies/lifecycle/` had to
the live pipeline when each was first introduced. A future,
separately-authorized task decides whether/how `telegram/`'s existing
Telegram-specific implementations (`reply_keyboard_manager.py`,
`commands.py`) come to consume this package's platform-agnostic
contracts.

## Implementation

Ten files (seven from PLATFORM-001, `navigation_events.py` added
TASK-002C, `navigation_core.py`/`platform_adapter.py` added TASK-002D),
each independently reusable:

| File | What it is |
|---|---|
| `platform_model.py` | `PlatformName` enum (5 client platforms), `PlatformStatus` enum, `PlatformDefinition` dataclass |
| `platform_registry.py` | `PlatformRegistry` + `build_default_registry()`, seeded with the real current state (Telegram Bot `LIVE`, the other four `NOT_STARTED`) |
| `capability_model.py` | `SupportStatus` enum, `PlatformCapability` dataclass (platform/status/reason/future_plan) |
| `capability_registry.py` | `ModuleCapabilityRegistry` — one module name → its full 5-platform capability declaration |
| `cross_platform_checker.py` | `check_module_capabilities()` — validates a declaration covers all 5 platforms and every non-`SUPPORTED` entry has a `reason` |
| `navigation_model.py` | `NavigationNode` (now with `category`/`content_type`, TASK-002C) — a platform-agnostic navigation-tree contract; `is_valid_screen_id()` (TASK-002C, ADR-002) — the Universal Screen Identity validator |
| `menu_registry.py` | `MenuDefinition` (now with `target_bindings`, TASK-002C — the Route Registry concept) + `MenuRegistry`; `DEFAULT_MENUS`/`build_default_menu_registry()` (TASK-002C) — a read-only mirror of GoldBot's 25 real, live Telegram screens |
| `navigation_events.py` | `NavigationEventType` enum + `NavigationEvent` dataclass — the Navigation Event Bus vocabulary (ADR-004), interface only, no dispatcher |
| `navigation_core.py` | **New, TASK-002D.** `NavigationCore` — Registry lookup + Permission Flow (`Request → Permission → Navigation → Screen`) + per-session Navigation State (a real stack, no Telegram exception) + Event Interface (`navigate()`/`go_back()` return a `NavigationResult` carrying a real `NavigationEvent`). `has_sufficient_permission()` — platform-agnostic tier comparison. |
| `platform_adapter.py` | **New, TASK-002D.** `PlatformAdapterBase` — abstract interface only (`render_screen()`/`render_permission_denied()`/`render_navigation_failed()`); no concrete per-platform subclass exists. |

Every registry follows this repo's established shape
(`assets/asset_registry.py`): in-memory only, a `DuplicateXError` on a
repeated key, `register()`/`get()`/`list()`, no shared singleton.
`NavigationCore` follows the same "real objects, no hidden state"
posture — its only state is the per-session stack, never persisted,
never read by anything outside this class.

## Testing

`tests/platforms/` — one `test_<module>.py` per file above (8 files),
plus `test_navigation_validation.py` (TASK-002E, deeper coverage
against the same frozen contracts, not a per-module file) — 80 tests
total, all passing (28 from PLATFORM-001 + 11 from TASK-002C + 12 from
TASK-002D + 29 from TASK-002E: stack consistency, multi-session
isolation under interleaving, the full permission-rank matrix,
recovery after repeated failures, a stress test, and an integration
test composing `NavigationCore` + `build_default_menu_registry()` + a
test-only `PlatformAdapterBase` subclass end-to-end). TASK-002E also
surfaced and documented one validation finding without changing frozen
code: `has_sufficient_permission()` ranks an unrecognized *required*
tier at -1, making it permissive rather than restrictive for that one
malformed-data direction — not exploitable today since every
`DEFAULT_MENUS` entry's `permission` is independently validated to be
exactly USER/ADMIN/OWNER; left to a future authorized fix, per the
Freeze Checklist. Mirrors `tests/assets/test_asset_intelligence.py`'s
convention: real objects, no mocking, explicit immutability/duplicate/independence
checks.

## Known Limitations

- **Not wired into any live command.** No `telegram/*.py` file imports
  `platforms/` in this phase — by design, this is a foundation phase.
- **`is_valid_screen_id()` is not enforced at construction time** in
  either `NavigationNode` or `MenuDefinition` — TASK-001's
  already-approved, frozen registrations predate ADR-002 and are not
  retroactively required to match it (enforcing it now would be a
  breaking contract change under the No Silent Decisions Policy). New
  registrations (`DEFAULT_MENUS`) are checked explicitly by test, not
  by the dataclass itself.
- **`navigation_events.py` has no dispatcher** — events can be
  constructed but nothing publishes, queues, or delivers one. Deferred
  to a future task per ADR-004.
- **`DEFAULT_MENUS` mirrors only today's real Telegram screens** (25
  entries) — no AI/Education/Marketplace/Trading screens are
  pre-registered, since none of those modules exist yet (honest, not
  speculative).
- **`platform_registry.py`'s four non-Telegram platforms carry no
  real detail** beyond `NOT_STARTED` — honest, not filled in with
  speculative feature lists.
- **`PlatformAdapterBase` has no concrete subclass.** No
  Telegram/Android/iOS/Desktop/Mini-App adapter exists — building one
  (especially a Telegram one, which would need to import `telegram/`
  types) is a future, separately-authorized task, per ADR-003's own
  framing.
- **`NavigationCore` is not called by anything.** No `telegram/*.py`
  file constructs or invokes it — it exists, is tested, and is unwired,
  same posture as every other module in this package.

## Future Improvements

- Build a concrete Platform Adapter (Telegram first, per
  `docs/NAVIGATION_ARCHITECTURE.md` §8) that reads `MenuRegistry`/
  `DEFAULT_MENUS` through `NavigationCore`, keeping
  `platform_layer/telegram/reply_keyboard_manager.py`'s own frozen behavior unchanged
  externally — a dedicated future task, not self-authorized here.
- Implement the Navigation Event Bus's actual dispatch mechanism
  (`navigation_events.py` is interface-only today) once a real
  consumer (Analytics, AI) is scoped.
- Populate `ModuleCapabilityRegistry` for each existing Telegram
  command/handler, run `cross_platform_checker` across all of them,
  and publish the result as a `docs/PLATFORM_CAPABILITY_MATRIX.md`
  snapshot.
- Extend `DEFAULT_MENUS` with non-Telegram target bindings once a
  second platform (Telegram Mini App, per the roadmap) has real code
  to bind to.

## Platform Impact

| Platform | Impact |
|---|---|
| Telegram Bot | Registered as `LIVE` in `platform_registry.py`; no behavior change — this phase adds metadata about it, not new Telegram behavior. |
| Telegram Mini App | Registered as `NOT_STARTED`; this foundation is what a future Mini App client would eventually register itself into. |
| Android | Registered as `NOT_STARTED`; same. |
| iOS | Registered as `NOT_STARTED`; same. |
| Desktop | Registered as `NOT_STARTED`; same. |

## Dependencies

`platforms/` imports only the Python standard library
(`dataclasses`, `enum`, `typing`) and its own sibling modules within
`platforms/`. It imports nothing from `telegram/`, `database/`, or any
Trading Core package (`context/`, `strategies/`, `signals/`, `decision/`,
`risk/`, `ai/`, `core/pipeline.py`) — confirmed by
`python -m pyflakes platforms/` reporting no unresolved/unused
cross-package import, and by direct review of every file's import
block.

## Related

- `docs/PLATFORM_DOCUMENTATION_POLICY.md` — the policy this doc follows.
- `docs/PLATFORM_ARCHITECTURE.md`, `docs/PLATFORM_MODULE_MAP.md`,
  `docs/PLATFORM_DEPENDENCY_MAP.md` — the existing Telegram-specific
  Platform Layer docs this foundation sits alongside.
- `docs/NAVIGATION_ARCHITECTURE.md`, `communication/decisions/ADR-002.md`
  through `ADR-004.md` — the approved design TASK-002C's additions
  implement.
- `docs/PLATFORM_CHANGELOG.md` — this phase's commit-level record.
- `communication/task_queue/TASK-001.md`, `TASK-002C.md`, `TASK-002D.md`
  — the tasks this doc reports on.
