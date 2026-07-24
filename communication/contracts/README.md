# contracts/

An agreed data/API shape crossing the Core↔Platform boundary — e.g. a
future "Signal History API" Platform needs from Core. Recorded once
both sides agree, so the shape doesn't drift between what was asked
for (`requests/REQ-XXXX.md`) and what was actually built.

Not the same as `docs/constitution/` Article-level contracts (those
govern the whole codebase's dependency rules) or
`docs/PLATFORM_DEPENDENCY_MAP.md` (which states existing import
boundaries) — this folder is for a specific, new cross-role data/API
agreement, one per file.

## Naming

`CONTRACT-XXXX.md`, sequential, zero-padded to 4 digits.

## Template

See `TEMPLATE.md` in this folder.

## Related

- `communication/requests/README.md` — the request that usually
  precedes a new contract.
- `docs/PLATFORM_DEPENDENCY_MAP.md` — existing import boundaries a new
  contract must respect.
