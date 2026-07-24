# GoldBot Documentation Audit (Phase A1, Task 6)

Consistency check across README, ARCHITECTURE, `CLAUDE.md`,
Development Rules, Database docs, and Deployment docs — every finding
below was verified by reading the actual files this phase, not
assumed. No documentation was edited to produce this audit (findings
only, per the phase's design-only scope).

## Missing

| Module | Finding |
|---|---|
| `core/` | **No `core/README.md`.** The orchestration package — arguably the single most important module (it's what wires every layer together) — has no Purpose/Flow/Input/Output/Dependencies/Future README, unlike every other module with runtime code. |
| `strategies/` | **No `strategies/README.md`.** The layer v0.3.5's Wyckoff work would add a fourth strategy to has zero documented contract today. |
| `monitoring/` | **No `monitoring/README.md`.** Compounds a real finding from `docs/ARCHITECTURE_AUDIT.md`: `monitoring/signal_monitor.py`'s docstring claims a package-wide "no database.*" isolation contract that `monitoring/performance.py` (same package) already violates — with no README to state the real, per-file posture, a future reader has only the (partially wrong) docstring to go on. |

Both `CLAUDE.md`'s "Before Code Changes" checklist and
`docs/DEVELOPMENT_RULES.md`'s "Review Process" section list module
READMEs to read before a change — **neither list includes `core/`,
`strategies/`, or `monitoring/`**, meaning this gap isn't just
"nobody wrote it yet," it isn't even on the checklist that's supposed
to catch it. See "Conflicting" below for the two lists' further
divergence from each other.

## Outdated

- **Root `README.md` is the most significant finding in this audit.**
  Its "Architecture" section header literally reads "GoldBot v0.2 is
  two separate processes..." — unchanged since v0.2, despite v0.3
  (Phases 48-58) having since added `docs/ARCHITECTURE.md`,
  `docs/DATABASE.md`, `docs/SECURITY.md`, `docs/TESTING.md`,
  `docs/LOGGING.md`, `docs/PERFORMANCE.md`, `docs/AI_ARCHITECTURE.md`,
  `docs/DEPLOYMENT.md`, `docs/production_setup.md`, and
  `docs/v0.3_RELEASE_NOTES.md`. The root README's own doc-pointer list
  still names only `docs/telegram_layer.md`, `docs/database_schema.md`,
  `docs/commands_reference.md`, and `docs/v0.2_release_notes.md` —
  every one of them real and still accurate in its own content, but
  the README gives a new reader zero indication that nine more current
  docs exist. This is the repository's front door and it describes a
  version two major hardening cycles behind where the code actually
  is.
- `docs/telegram_layer.md`, `docs/commands_reference.md`, and
  `docs/database_schema.md` each carry a literal "(v0.2)" in their H1
  title. Their *content* was re-checked this phase and found still
  accurate — no Telegram command or database schema changed during any
  v0.3 phase (`CLAUDE.md`'s Trading Safety / "no Telegram feature
  expansion" boundaries held throughout Phases 48-58) — so this is a
  **cosmetic** staleness (a version label), not a content-accuracy
  problem. Still worth flagging: a "(v0.2)" title on a doc still being
  actively cross-referenced by current, v0.3-era docs
  (`docs/ARCHITECTURE.md` links to `docs/telegram_layer.md` by name)
  reads as more stale than it is.
- `docs/DEVELOPMENT_RULES.md`'s "Review Process" section references
  "`docs/*_report.md`/`docs/*_architecture.md`" as a generic pattern
  to check before a change. After Phase 56's doc consolidation, no
  current file matches either literal suffix (`testing_report.md`,
  `security_report.md`, `performance_report.md`,
  `database_architecture.md` were all renamed to `TESTING.md`,
  `SECURITY.md`, `PERFORMANCE.md`, `DATABASE.md`; only
  `docs/AI_ARCHITECTURE.md` still resembles the pattern, and only if
  case-insensitive). The sentence still communicates the right idea
  (check the relevant topic doc) but its literal glob no longer
  matches anything.

## Duplicate

**None found that are actually problematic.** Two pairs looked like
candidates on first read and were checked in full this phase; both
turned out to be deliberately complementary, not duplicated:

- `docs/DATABASE.md` (architecture/relationships, Phase 50 audit
  findings) explicitly states "For the full column-by-column schema,
  see `docs/database_schema.md`" in its own opening paragraph — the
  two are cross-referenced by design, covering different levels of
  detail on the same subject. Not a duplicate.
- `docs/code_structure.md` states in its own opening paragraph that it
  is "the index, not a replacement for" the deeper per-layer docs it
  links to, and `docs/ARCHITECTURE.md` in turn says it is "the entry
  point that ties them together." A three-level index → overview →
  detail structure, not duplication.
- `docs/DEPLOYMENT.md` (Phase 56, general install/run/backup) and
  `docs/production_setup.md` (Phase 58, VPS-specific systemd/
  monitoring/env) are cross-referenced in both directions
  (`docs/DEPLOYMENT.md` points to `docs/production_setup.md` for VPS
  specifics; `docs/production_setup.md`'s own intro states it covers
  "what `docs/DEPLOYMENT.md` does not"). Deliberately layered, not
  duplicated.

## Conflicting

- **`CLAUDE.md`'s "Before Code Changes" module-README list and
  `docs/DEVELOPMENT_RULES.md`'s "Review Process" module-README list
  do not match.** `CLAUDE.md` lists: `data/`, `context/`, `signals/`,
  `decision/`, `risk/`, `execution/`, `database/`, `telegram/`, `ai/`
  (9 modules). `docs/DEVELOPMENT_RULES.md` lists: `data/`, `context/`,
  `signals/`, `risk/`, `execution/`, `telegram/`, `ai/` (7 modules) —
  **missing `database/README.md` and `decision/README.md`**, both of
  which exist (added in Phase 56) and both of which `CLAUDE.md`
  correctly includes. Two governance documents that are supposed to
  tell a contributor the same thing ("read these before you touch
  this area") currently tell them slightly different things. Given
  `docs/DEVELOPMENT_RULES.md`'s own stated purpose ("See `CLAUDE.md`
  for the higher-level... rules this document's conventions support"),
  the two should be kept in lockstep, and currently aren't.

No other conflicting factual claims were found between
`docs/ARCHITECTURE.md`, `CLAUDE.md`, `docs/DEVELOPMENT_RULES.md`,
`docs/DATABASE.md`, `docs/DEPLOYMENT.md`, and `docs/production_setup.md`
— dependency rules, thresholds, and deployment instructions were
cross-checked against each other and against the real code this phase
and were found internally consistent, aside from the README-list
mismatch above.

## Recommendation (documentation-only, not implemented this phase)

1. Update root `README.md`'s Architecture section and doc-pointer list
   to reflect v0.3 (this is the single highest-value documentation fix
   found in this entire audit — it's the first thing any new reader
   sees).
2. Add `core/README.md`, `strategies/README.md`, `monitoring/README.md`
   following the same Purpose/Flow/Responsibilities/Input/Output/
   Dependencies/Future format Phase 56 established for the other nine.
3. Reconcile `CLAUDE.md`'s and `docs/DEVELOPMENT_RULES.md`'s module-
   README lists to the same 12-module set (once item 2 above exists).
4. Either drop the "(v0.2)" labels from `docs/telegram_layer.md`/
   `docs/commands_reference.md`/`docs/database_schema.md`'s titles, or
   replace them with an explicit "content verified current as of
   Phase A1" note — the content is fine, the label is what's
   misleading.
5. Fix `docs/DEVELOPMENT_RULES.md`'s `docs/*_report.md`/
   `docs/*_architecture.md` reference to name the actual current doc
   set.

None of the above was implemented in this phase — recommendations
only, per the Phase A1 brief's design/documentation-only scope.
