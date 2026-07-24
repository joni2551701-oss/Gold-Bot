# GoldBot — Phase History

Governed by `docs/constitution/CONSTITUTION.md` Article 12. Every
major phase, in order. Phase number is the ordering key — this
repository does not track a per-phase calendar date, so none is
fabricated here; `git log` on each phase's own commit is the exact
timestamp record if one is needed.

| Phase | Name | What it built |
|---|---|---|
| v0.1–v0.3 | Core Trading Foundation | Data→Context→Strategy→Signal→Decision→Risk→Telegram pipeline, database layer, Telegram Owner panel foundation |
| 59–59.9 | AI & Platform Foundations | Provider foundation, market data providers, normalization, signal lifecycle, dataset collection, runtime feature control, Owner dashboard, Emergency system |
| 60.0 | Architecture Audit | Module dependency graph, dead code, duplicate logic, database, Owner, pipeline audits |
| 60.1–60.9 | Simulation & Intelligence Layers | Replay Engine, Backtesting Engine, Execution Simulator, Performance Validation, Fundamental Intelligence, Learning Loop (+ integration), Safe Integration hooks, Registry cleanup |
| 60.10 | Foundation Freeze v0.4 | Full module inventory, dependency/dead-code/duplicate audits, platform diagram, version roadmap |
| 61.0 | AI Foundation | `ai/capabilities/`, `ai/providers/`, `ai/router/`, `ai/context/`, `ai/access/`, `ai/session/`, `ai/tools/`, `ai/audit/` |
| 61.1 / 61.1.1 | AI Provider Reliability | Provider health/failover/capability matrix, prompt registry, tool permission matrix, `ai/cache/`, cache freshness correction |
| 61.2 | AI Runtime Foundation | Real Gemini provider, runtime error handling, `ai/validation/`, `ai/runtime/` service layer, cache integration |
| 61.3 | AI Intelligence Layer | `knowledge/` (new top-level), real tool calling, Conversation Engine, Memory Runtime, Explanation Engine, Runtime Trace, Provider Benchmark |
| 61.4 | AI Product Control Layer | AI Access Control integration, Telegram AI Owner commands, user registration, anti-abuse, usage accounting |
| 61.5 | AI Production Integration | Real OpenAI/Claude/Grok providers, Router Intelligence, live Telegram Owner AI dashboard, `ai/content/` foundation, Broadcast Preparation Interface |
| 61.6 | AI Runtime Foundation (Lifecycle) | `RuntimeManager`, `ProviderCircuitBreaker`, Runtime Event Bus, Runtime Dashboard, Notification Layer, Configuration Profiles |
| 61.7 | AI Runtime Integration | `RuntimeManager`/Circuit Breaker/Profile/Event Bus wired into `AIService.ask()`'s real control flow, `/runtime_status`, Runtime Self Check |
| 62.0 | Constitution & Architecture | `docs/constitution/CONSTITUTION.md` (Articles 1–7), full `docs/architecture/` set, `docs/roadmap/`, Owner/Telegram/AI architecture docs |
| 62.2 | AI Runtime Integration Completion | Runtime-unhealthy audit trail, exponential retry backoff, `/runtime_restart`/`/runtime_provider`, AI Cost Protection |
| 63.0 | Senior Trading AI Foundation | `ai/persona/`, `ContentType`, `ExplanationOutput`, `broadcast/`/`media/`/`translation/` (new top-level, foundation-only), 4 new `Capability` members |
| 62.1a | Governance System | Constitution Articles 8–12, `docs/policies/` (11 files) |
| 62.1b | Architecture & Standards | `docs/architecture/` flow/pattern/naming docs (7 files), `docs/standards/` (6 files), AI_EVOLUTION.md's roadmap-vision extension |
| 62.1c | AI + Telegram + Trading Docs | `docs/ai/` (6 files), `docs/telegram/` (3 files), new `docs/trading/` (5 files) |
| 62.1d | Roadmap + Changelog + Vision | `docs/VISION.md`, `docs/roadmap/VERSIONS.md`/`AI_EVOLUTION.md` restructure, `docs/changelog/` (this document + 2 siblings) |

## Related

- `docs/changelog/CHANGELOG.md` — per-version change/impact detail.
- `docs/changelog/DECISION_LOG.md` — the load-bearing decisions behind
  several of the phases above.
- `docs/roadmap/VERSIONS.md` — the same history, organized by version
  number instead of phase number.
