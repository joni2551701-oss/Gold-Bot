# GoldBot — Version Roadmap

Governed by `docs/constitution/CONSTITUTION.md`. This roadmap
reflects the real, completed phase history in this repository plus
the Director's own stated "what comes next" direction
(`docs/PHASE61_7_FREEZE.md`), not a speculative plan invented for
this document.

| Version | Scope | Status |
|---|---|---|
| v0.1 | Core trading pipeline: Data → Context → Strategy → Signal → Decision → Risk → Telegram delivery | Done |
| v0.2 | Database layer, repositories, user/subscription models | Done |
| v0.3 | Telegram Owner panel foundation (`telegram/owner/*`), permissions, admin tooling | Done |
| v0.4 | AI Foundation: providers, router, capabilities, runtime foundation (Phases 59–61.6) | Done |
| v0.4.7 | AI Platform Stabilization & Integration — `AIService` as the single real orchestration point over `RuntimeManager`/`ProviderCircuitBreaker`/`RuntimeProfile`/`EventBus` (Phase 61.7) | Done |
| v0.5 | Business Layer — subscription/billing/monetization | Not started |
| v0.6 | Owner Control Center — unified Owner Telegram dashboard beyond today's per-domain commands (see `docs/owner/OWNER_PANEL.md`) | Not started |
| v0.7 | Broadcast Foundation (Owner-only) — periodic delivery of queued Runtime/Provider alerts via a live process loop (the gap `docs/PHASE61_7_FREEZE.md` names explicitly: `deliver_alerts()` is not yet called from any running loop) | Not started |
| v0.8 | Web Dashboard | Not started |
| v0.9 | Academy / Education Platform | Not started |
| v1.0 | Full production release across Trading Core + AI Layer + Business Layer + Owner Control Center | Not started |

## Notes

- This table intentionally does not promise dates — only scope and
  status, matching this codebase's own convention of never reporting
  a phase "Complete" without GitHub Actions confirmation (`CLAUDE.md`
  Reporting language rule).
- v0.4.7 (Phase 61.7) explicitly did not grow AI Core's capability
  surface — it made existing foundation pieces real and load-bearing.
  See `docs/PHASE61_7_FREEZE.md` for the full freeze declaration.
- Phase 62.0 (this document's own phase) is a documentation-only
  Foundation Lock and does not correspond to a version bump — no code
  changed.

## Related documents

- `docs/roadmap/AI_EVOLUTION.md` — the AI-specific timeline within
  this same roadmap (v0.4 / v0.4.7 and beyond).
- `docs/PHASE61_7_FREEZE.md` — the most recent phase freeze this
  table's "Done" rows are backed by.
