# GoldBot — Changelog

Governed by `docs/constitution/CONSTITUTION.md` Article 12. One entry
per version-relevant phase, in the Director's requested format:
Version / Changes / Architecture Impact. No calendar date is recorded
per entry — this repository does not track one per phase; `git log`
against the phase's own commit is the exact record when needed.
`docs/changelog/PHASE_HISTORY.md` is the flat phase-by-phase list this
document adds Architecture Impact detail to for the phases most worth
elaborating on.

## v0.4.7 / Phase 61.7 — AI Runtime Integration

**Changes**: `RuntimeManager`, `ProviderCircuitBreaker`, `RuntimeProfile`,
`EventBus` wired into `AIService.ask()`'s real control flow.
`/runtime_status`, Runtime Self Check.

**Architecture Impact**: `AIService` became the single real
orchestration point for every AI request — no code path calls a
provider directly anymore.

## Phase 62.0 — Constitution & Architecture

**Changes**: `docs/constitution/CONSTITUTION.md` (Articles 1–7), full
`docs/architecture/` set (`ARCHITECTURE_MASTER.md`,
`MODULE_DEPENDENCIES.md`, `IMPORT_RULES.md`, `EXTENSION_GUIDE.md`),
`docs/roadmap/`, Owner/Telegram/AI architecture docs.

**Architecture Impact**: GoldBot gained a written, supreme governance
document for the first time. Every subsequent phase reads it first.

## Phase 62.2 — AI Runtime Integration Completion

**Changes**: Runtime-unhealthy audit trail, exponential retry backoff,
structured `error_type` on `PROVIDER_FAILED`, `/runtime_restart`/
`/runtime_provider`, AI Cost Protection (daily cost/token ceiling →
`DEGRADED` + Owner alert).

**Architecture Impact**: Closed the last 5 gaps between "AI Runtime
exists" and "AI Runtime is production-wired." No new architecture —
unification of what Phase 61.7 already built.

## Phase 63.0 — Senior Trading AI Foundation

**Changes**: `ai/persona/` (new), `ai/content/content_types.py`'s
`ContentType` (extended, not duplicated), `ai/explanation/explanation_output.py`
(new), `broadcast/`/`media/`/`translation/` (three genuinely new
top-level packages, foundation-only), four new `Capability` members.

**Architecture Impact**: AI Media Platform foundation created. Trading
pipeline zero diff. No real broadcast/media/translation API call
anywhere — contract-first, exactly as `docs/PHASE63_0_FREEZE.md`
declares.

## Phase 62.1 (a–d) — Governance System

**Changes**: Constitution Articles 8–12; `docs/policies/` (11 files);
`docs/architecture/` flow/pattern/naming docs (7 files) +
`docs/standards/` (6 files); `docs/ai/`/`docs/telegram/`/`docs/trading/`
documentation (14 files); `docs/VISION.md`, roadmap restructure,
`docs/changelog/` (this document + 2 siblings).

**Architecture Impact**: Zero code changed across all four sub-phases.
GoldBot gained a five-layer governance system (Constitution →
Architecture → Roadmap → Director Policy → Operational Standards) and
a full technical documentation base for `ai/`, `telegram/`, and
`trading/` — the "architecture memory" this phase's own closing note
names as its purpose.

## Related

- `docs/changelog/PHASE_HISTORY.md` — the flat, complete phase list.
- `docs/changelog/DECISION_LOG.md` — the reasoning behind the
  load-bearing decisions in the phases above.
