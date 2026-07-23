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

Seven files, each independently reusable:

| File | What it is |
|---|---|
| `platform_model.py` | `PlatformName` enum (5 client platforms), `PlatformStatus` enum, `PlatformDefinition` dataclass |
| `platform_registry.py` | `PlatformRegistry` + `build_default_registry()`, seeded with the real current state (Telegram Bot `LIVE`, the other four `NOT_STARTED`) |
| `capability_model.py` | `SupportStatus` enum, `PlatformCapability` dataclass (platform/status/reason/future_plan) |
| `capability_registry.py` | `ModuleCapabilityRegistry` — one module name → its full 5-platform capability declaration |
| `cross_platform_checker.py` | `check_module_capabilities()` — validates a declaration covers all 5 platforms and every non-`SUPPORTED` entry has a `reason` |
| `navigation_model.py` | `NavigationNode` — a platform-agnostic navigation-tree contract, unrelated to any Telegram type |
| `menu_registry.py` | `MenuDefinition` + `MenuRegistry` — id/permission/platforms/version/dependencies, never hardcoded |

Every registry follows this repo's established shape
(`assets/asset_registry.py`): in-memory only, a `DuplicateXError` on a
repeated key, `register()`/`get()`/`list()`, no shared singleton.

## Testing

`tests/platforms/` — one `test_<module>.py` per file above (5 files,
covering all 7 modules since `capability_model.py`/`capability_registry.py`
and `platform_model.py`/`platform_registry.py` share test files with
their registry), 28 tests total, all passing. Mirrors
`tests/assets/test_asset_intelligence.py`'s convention: real objects,
no mocking, explicit immutability/duplicate/independence checks.

## Known Limitations

- **Not wired into any live command.** No `telegram/*.py` file imports
  `platforms/` in this phase — by design, this is a foundation phase.
- **`navigation_model.py`/`menu_registry.py` do not reflect the real
  live Telegram navigation tree yet** — they are contracts, not a
  populated registry of GoldBot's actual menu structure (that
  population is future work, likely part of TASK-002/Navigation).
- **`platform_registry.py`'s four non-Telegram platforms carry no
  real detail** beyond `NOT_STARTED` — honest, not filled in with
  speculative feature lists.

## Future Improvements

- Wire `MenuRegistry` to describe GoldBot's actual live menu tree
  (Main/Settings/Admin/Owner/Profile/Signals sections from
  `docs/PLATFORM_ARCHITECTURE.md` §5), as a read-only mirror first,
  before any live dispatch code depends on it.
- Populate `ModuleCapabilityRegistry` for each existing Telegram
  command/handler, run `cross_platform_checker` across all of them,
  and publish the result as a `docs/PLATFORM_CAPABILITY_MATRIX.md`
  snapshot — natural TASK-002+ candidate.
- Decide (a dedicated Director task, not a self-authorized change)
  whether `telegram/reply_keyboard_manager.py` should eventually
  adapt `NavigationNode` internally, keeping its own frozen Reply Menu
  layout (`docs/PHASE6_FREEZE.md` Stage 5) unchanged externally.

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
- `docs/PLATFORM_CHANGELOG.md` — this phase's commit-level record.
- `communication/task_queue/TASK-001.md` — the task this doc reports on.
