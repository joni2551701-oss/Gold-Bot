# Test Standard

The concrete, file-level companion to `docs/policies/TESTING_POLICY.md`
(which states *why* and *when*; this states *how the files look*).

## Layout

Tests live under `tests/`, mirroring the source tree:
`ai/persona/persona_manager.py` → `tests/ai/persona/test_persona.py`.
No `__init__.py` inside a `tests/<package>/` directory — the
established convention (confirmed by `find tests -name __init__.py`
returning nothing under any subpackage) that Phase 63.0 corrected
itself back to after briefly deviating from it.

## What a test file covers

- **Unit** — the module's own logic, every collaborator injected via
  the optional-constructor-argument convention
  (`docs/standards/CODE_STANDARD.md`), no real network/database/API
  call.
- **Isolation** (for anything under `ai/`) — an import-sweep test
  confirming no `decision`/`risk`/`execution` import was introduced.
  `tests/ai/` already carries several of these; a new `ai/` subpackage
  adds its own or is covered by the existing repository-wide sweep.
- **Dispatch** (for a new Telegram command) — a `route_command()`-level
  test proving the handler is actually reachable by name, not just
  that the handler function works in isolation
  (`tests/telegram/test_runtime_owner_dispatch.py` is the model, built
  specifically to catch the Phase 61.7 handler-naming bug again).

## What "done" looks like

`pytest tests/` passes, full suite, before and after the new test file
is added — a new test that only passes in isolation but breaks the
full run is not done.

## Related

- `docs/policies/TESTING_POLICY.md`.
- `docs/constitution/CONSTITUTION.md` Article 6.
