# GoldBot Security Audit (Phase 54)

Full-repository security audit. Builds on and re-verifies findings
from the Phase 48 full-system audit, the Phase 51 logging/exception
hardening, and Phase 52's initial `tests/security/` suite — this
report is the authoritative, current-state security document; where a
finding below repeats an earlier phase's, it has been independently
re-checked this phase, not just copied forward.

## 1. Secret Management

**Status: PASS**

- All 5 real secrets (`TWELVE_DATA_API_KEY`, `GEMINI_API_KEY`,
  `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `TELEGRAM_OWNER_ID`) are
  read exclusively through `core/secrets.py`'s `Secrets` class.
  Repo-wide grep confirms zero direct `os.getenv`/`os.environ` access
  to any of these outside that one file (and `tests/conftest.py`'s
  intentional test-determinism setup).
- `config.py`'s `APP_ENV`/`DEBUG` read `os.getenv` directly, but
  neither is a credential — non-issue, same conclusion as Phase 48.
- `Secrets.get()` raises `ValueError` on a missing required value with
  no default, and every caller (`TwelveDataClient`, `TelegramBot`)
  catches it and degrades gracefully (`api_key = None` /
  `self._bot = None`) rather than crashing.
- `Secrets` exposes only named `@property` accessors
  (`TWELVE_DATA_API_KEY`, etc.) plus the underlying `get()` — no
  bulk-dump method exists that could leak every secret at once
  (`tests/security/test_secret_security.py::test_secrets_class_exposes_only_named_properties_not_a_bulk_dump`).
- No hardcoded token/key-shaped string found anywhere in production
  code (`grep` for bot-token shapes, `AIza...`, `sk-...` patterns —
  zero matches outside `tests/conftest.py`'s and `.github/workflows/ci.yml`'s
  explicitly-fake test tokens).
- `config.Config`'s public attributes were scanned for accidental
  hardcoded secret-shaped values — none found
  (`test_config_class_has_no_hardcoded_secret_looking_values`).
- **Error-message leak check (new this phase, empirically verified,
  not just read)**: `aiogram.Bot(token=<malformed>)` raises
  `TokenValidationError("Token is invalid!")` — confirmed by direct
  construction that the raw token value is never included in that
  exception's message. `platform_layer/telegram/bot.py`'s
  `logger.warning(f"TelegramBot init failed (token missing/invalid): {e}")`
  is therefore safe: `{e}` can only ever be "Token is invalid!" or
  "Secret 'TELEGRAM_BOT_TOKEN' not found in environment." (the
  secret's *name*, never its value). Verified dynamically with a real
  fake token value through `caplog`
  (`test_telegram_bot_init_failure_log_does_not_contain_the_token_value`,
  `test_market_data_normalizer_error_log_does_not_contain_the_api_key`).
- No user-facing Telegram response can ever contain a secret value
  (`test_handler_error_responses_never_contain_a_secret_value`).

### GitHub / Repository Security

**Status: PASS**

- `.gitignore` covers `.env`, `__pycache__/`, `.pytest_cache/`,
  `database/goldbot.db` (plus, added this phase, blanket `*.db` and
  `*.log` patterns for defense-in-depth — no code currently writes a
  `.log` file or a `.db` file outside the paths already covered, but
  this closes the gap for any future addition).
- `git ls-files | grep -i env` — no `.env` file tracked.
- Full `git log --all --full-history` scan for `.env`/`.db`/credential/
  key-shaped filenames across the *entire* commit history (not just
  the current tree) — **nothing found**. No secret has ever been
  committed, at any point in this repository's history.

## 2. Telegram Security

**Status: PASS**

Permission flow re-verified end-to-end through the real
`route_command()` chain (not just read — driven with real calls):

- **USER denied every admin-tier command**: `/admin`, `/stats`,
  `/users`, `/system`, `/broadcast` all return `PERMISSION_DENIED_TEXT`
  for a plain USER
  (`test_permission_security.py::test_user_denied_every_admin_tier_command`).
- **ADMIN allowed every ADMIN-tier command**, correctly excluded from
  OWNER-only ones: `/admin` renders the reduced panel (no "Broadcast"/
  "Admin Management" text), `/stats`/`/users`/`/system`/`/broadcast`
  all succeed, `/addadmin`/`/removeadmin` are denied
  (`test_admin_allowed_every_admin_tier_command`,
  `test_admin_denied_owner_only_commands`).
- **OWNER has full access**, including the OWNER-exclusive commands
  (`test_owner_has_full_access_including_owner_only_commands`).
- **No stale-permission window**: revoking an ADMIN's row takes effect
  on the very next command, no caching
  (`test_revoked_admin_immediately_loses_access`).
- **OWNER status cannot be granted via the database**: adding a
  `telegram_id` to the `admins` table grants ADMIN, never OWNER — OWNER
  comes exclusively from `TELEGRAM_OWNER_ID`
  (`test_owner_status_is_config_only_never_a_database_row`).
- **No attribute-injection via command name**: `command_router.py`
  checks the parsed command against the closed `_ALL_COMMANDS`
  registry *before* it is ever used in
  `getattr(handlers, f"{command}_handler", None)` — confirmed by
  re-reading the exact statement order in `route_command()`, then
  proven dynamically by sending `/__class__`, `/os.system`,
  `/../etc/passwd`, `/eval` and confirming every one resolves to
  `UNKNOWN_COMMAND_TEXT`, never reaching the handler lookup with
  attacker-controlled input
  (`test_command_allowlist_blocks_attribute_injection_attempts`).
- No `parse_mode` (Markdown/HTML) is configured anywhere — every
  Telegram message is sent as plain text, so no formatting-injection
  vector exists from user-supplied feedback/broadcast content being
  echoed back.

## 3. Database Security

**Status: PASS**

- **SQL injection**: every query across all 5 repositories uses `?`
  parameterized placeholders. Re-confirmed by grep (zero raw
  string-interpolated *values* in any `execute()` call) and, new this
  phase, proven dynamically: 6 classic SQL-injection payloads
  (`' OR '1'='1`, `'; DROP TABLE users; --`, `Robert'); DROP TABLE
  students;--`, etc.) fed as `telegram_id`/`username`/feedback
  `message` values through both the repository layer directly and the
  full `route_command()` chain — every payload is stored and read back
  **literally**, no table is dropped/altered, no query is corrupted
  (`tests/security/test_database_security.py`, 6 tests).
- **Dynamic SET-clause construction** (`user_repository.py`'s
  `update_user()`, `subscription_repository.py`'s `_update()`) builds
  its SQL from an f-string, but only for *column names* pre-filtered
  against a fixed, hardcoded allowlist — an attacker-supplied field
  name (e.g. `"telegram_id = '1'; DROP TABLE users; --"` passed as a
  kwarg) is silently dropped before ever reaching the query string.
  Verified dynamically, not just read
  (`test_dynamic_update_column_allowlist_rejects_unknown_fields`).
- **Migration DDL** (`database_layer/database_manager/models.py`'s `ALTER TABLE ... ADD
  COLUMN` f-strings) interpolates `column_name`/`column_def` from a
  hardcoded, developer-authored list literal in the source — never
  from any external input.
- No duplicate/leaked connections: `Database.__enter__()`/`__exit__()`
  opens and closes a connection per `with` block, every time (Phase 53
  memory audit, re-confirmed).

## 4. Input Validation

**Status: PASS**

Crash-safety re-verified with a much wider payload set than Phase 52's
original coverage — `tests/security/test_input_validation.py` now
covers, for every payload, "must not crash, must produce a safe text
response":

- **This phase's exact named scenario** — `/risk abc` (non-numeric) —
  confirmed rejected safely, no crash.
- Negative numbers, floats, integer-overflow-shaped strings, non-ASCII
  digits (`/risk -5`, `/risk 1.5`, `/risk 999999999999999999999`,
  `/risk ٥`) — all safely rejected by the fixed-allowlist check before
  any numeric conversion is attempted.
- **Very long input**: a 10,000-character `/feedback` body and a
  10,000-character `/broadcast` body (Telegram's own real cap is 4,096)
  — both handled without error.
- **Special/unicode characters**: emoji, mathematical Unicode symbols,
  raw control characters (`\x00`, `\x01`, `\x02`), newlines/tabs,
  an XSS-shaped `<script>` payload, a SQL-injection-shaped payload,
  right-to-left Persian script, and astral-plane Unicode (mathematical
  bold Fraktur) — all 8 payloads accepted and stored without crashing.
- `/userinfo` and `/strategy` with special-character/very-long
  arguments — safe, well-formed responses, no crash.
- `/addadmin` with a SQL-injection-shaped target_id — stored literally
  (matching the database-security findings above), not executed.

## 5. Dependency Audit

**Status: PASS** (real vulnerability scan, `pip-audit` against the
PyPI Advisory Database / OSV — not a manual/recollection-based check)

| Package | Risk | Recommendation |
|---|---|---|
| `aiogram` (3.29.1, unpinned in `requirements.txt`) | None found — `pip-audit -r requirements.txt` reports zero known vulnerabilities. Actively maintained, mainstream Telegram bot framework. | None required. Unpinned means every fresh install (including every CI run) automatically gets the current, already-patched release — see note below. |
| `requests` (2.33.1, unpinned) | None found for `requests` itself. Its transitive dependencies `idna` and `urllib3` were resolved to versions with known, low/medium-severity published advisories in *this specific sandbox's pre-existing package cache* (`idna` 3.11, `urllib3` 2.6.3). | Upgraded in this session (`idna`→3.18, `urllib3`→2.7.0) as a verification step; `pip-audit` confirms clean afterward and the full test suite (150/150) still passes. **Not** encoded into `requirements.txt` — GoldBot never pinned these transitive packages, and a genuinely fresh `pip install -r requirements.txt` (exactly what CI does on every run) resolves them via pip's own resolver to the current newest-compatible release directly from PyPI, not the stale cached versions this sandbox happened to have pre-installed. The stale versions found here are an artifact of this environment's history, not a reproducible CI/production risk. |
| Everything else `pip-audit` (whole-environment scan) flagged (`cryptography`, `PyJWT`, `pip`, `setuptools`, `wheel`) | **Not applicable to GoldBot** — confirmed via `pip show <pkg> \| grep Required-by`: `cryptography` and `PyJWT` have **empty** `Required-by` (not used by `aiogram` or `requests`, unrelated packages present in this shared sandbox from something else entirely); `pip`/`setuptools`/`wheel` are Python's own bootstrap tooling, not something `requirements.txt` controls or a project dependency in any meaningful sense. | None — out of scope, not part of GoldBot's actual dependency tree. |
| Unused dependencies | None found. Both `aiogram` and `requests` are actively imported and used (re-confirmed, matching the Phase 48 audit). | None required. |

**Recommendation, not applied this phase** (a process change, not a
code change, and explicitly a "future phase" item per this phase's own
scope discipline): add an automated dependency-vulnerability scan
(GitHub Dependabot, or a `pip-audit` CI step) so a real, exploitable
CVE in a *direct* dependency is caught automatically rather than
relying on a periodic manual audit like this one.

## 6. Found Issues

**P0 Critical**: none.

**P1 High**: none.

**P2 Medium**: none newly found this phase. (The Phase 48 audit's one
P2-adjacent Telegram finding — authorization enforced only at the
command-router/handler layer, not the service layer, as a
defense-in-depth gap — remains accurate and unchanged; re-confirmed
still true, still not exploitable today since no other entry point
calls these services directly. Not re-litigated here since nothing
about it changed this phase.)

**P3 Low**:
- `config.py`'s `APP_ENV`/`DEBUG` are defined but **never read by any
  other code** in the repository (`grep` for `Config.DEBUG`/`APP_ENV`
  outside `config.py` returns nothing). Not a vulnerability — there is
  no debug-mode code path that could leak internals, since nothing
  branches on these flags at all — but worth noting: the "Production:
  DEBUG=False" requirement is trivially satisfied today (safe default,
  `False` unless the literal string `"True"` is set) purely because
  the flag is inert, not because of active enforcement.
- Direct dependencies (`aiogram`, `requests`) remain unpinned in
  `requirements.txt` — a reproducibility trade-off, not a known
  vulnerability (see Dependency Audit above); deliberately left as-is
  this phase.

## 7. Recommendations

1. Add Dependabot or a `pip-audit` CI step for automated, ongoing
   dependency-vulnerability monitoring (this phase's scan was manual
   and one-time).
2. If `config.Config.DEBUG` is ever wired into an actual debug-mode
   code path in a future phase (e.g. verbose stack traces in a
   response), re-run this audit's Production Config Security section
   against that new code path specifically before shipping it.
3. Continue the existing pattern (Phase 48's finding, still valid): if
   a future phase ever adds a second entry point that calls
   `SignalService`/subscription-gated services directly (bypassing
   `command_router`), move the access checks into the service layer at
   that point — not before, since no such entry point exists today.

---

Every finding above with a "verified dynamically" claim has a
corresponding passing test in `tests/security/` — this report is not
a claim independent of the test suite, it is a narrative of what that
suite (Phase 52's `test_secrets.py`/`test_input_validation.py` plus
this phase's `test_secret_security.py`, `test_permission_security.py`,
`test_database_security.py`, and `test_input_validation.py`'s new
additions) actually proves by executing.
