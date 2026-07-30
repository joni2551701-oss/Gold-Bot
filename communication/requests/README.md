# requests/

Platform → Core: "I need X to finish Y." Used when the Platform Worker
needs something from Core (an API, a data shape, a confirmation) that
it cannot build itself, per the Director's own worked example in
PLATFORM-001's brief.

## When to use this

Only when the Platform role is genuinely blocked by something only
Core can provide — not for questions Platform can answer by reading
`docs/PLATFORM_ARCHITECTURE.md`/`docs/PLATFORM_MODULE_MAP.md`/
`docs/PLATFORM_DEPENDENCY_MAP.md` first.

## Naming

`REQ-XXXX.md`, sequential, zero-padded to 4 digits, never reused.

## Template

See `TEMPLATE.md` in this folder. Copy it, fill in the next `REQ-XXXX`
number, and answer is expected in `../responses/RESP-XXXX.md` with the
matching number.

## Related

- `communication/README.md` — the full request/response loop.
- `communication/responses/README.md` — where the answer lands.
