# Security Policy

## Never logged, never committed

- API keys and provider tokens (`TWELVE_DATA_API_KEY`,
  `TELEGRAM_BOT_TOKEN`, AI provider keys).
- User phone numbers.
- Passwords or any credential.
- Any secret value read via `os.getenv`/`os.environ`.

A grep sweep for `os.getenv`/`os.environ` under any new package is run
at the close of every phase that touches secrets-adjacent code (the
practice already followed at the close of Phase 63.0, confirming zero
matches under `ai/persona/`, `broadcast/`, `media/`, `translation/`).
A secret that reaches a log line, an exception message, or an Owner
Telegram message is a security defect, not a style issue.

## Provider isolation (Article 5)

A vendor name (`Gemini`, `OpenAI`, `Claude`, `Grok`) never appears
above `ai/providers/` and `ai/runtime/ai_service.py`. This keeps a key
rotation, a vendor swap, or a vendor outage from ever needing a change
outside those two locations.

## Database boundary (Article 4)

No raw SQL, no direct `sqlite3`/ORM call from a handler or service.
Only a `database/*_repository.py` module touches the database. This
is also a security boundary, not only a layering one: it is the one
place injection-style defects are checked for.

## Existing reference

`docs/SECURITY.md` predates this policy and documents the concrete
security posture (input validation, the pre-existing repository-layer
exceptions Article 4 references) in more detail. This policy does not
replace it — it states the standing rule this policy layer now also
governs going forward.

## Related

- `docs/constitution/CONSTITUTION.md` Articles 4, 5.
- `docs/SECURITY.md` — the detailed, pre-existing security audit.
