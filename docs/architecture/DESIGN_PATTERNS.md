# GoldBot — Design Patterns

Governed by `docs/constitution/CONSTITUTION.md` Article 7 (Reuse
Principle) and Article 11 (Foundation Reuse Law). These are the eight
patterns this codebase actually uses, repeatedly, across many phases —
not a generic design-patterns primer. Recognizing which pattern a new
piece of work fits is the fastest way to answer Article 11's own
checklist ("does a Manager/Registry/Contract for this already exist?").

## Manager Pattern

A class that owns runtime state and read/write operations over a
domain, always with every constructor argument optional and
fake-able. Examples: `RuntimeManager` (`ai/runtime/`), `PersonaManager`
(`ai/persona/`), `BroadcastManager`/`BroadcastProviderManager`/
`BroadcastTriggerManager` (`broadcast/`), `MediaManager` (`media/`),
`TranslationManager` (`translation/`), `EmergencyManager`
(`core_layer/emergency/`).

## Registry Pattern

A static catalog, usually built by a `build_*_registry()` function,
that a Manager looks up against. Examples: `provider_registry.py`
(`ai/providers/`), `persona_registry.py` (`ai/persona/`),
`media_registry.py` (`media/`), `language_registry.py` (`translation/`),
`ai/router/routing_rules.py`'s `ROUTING_RULES` dict (a registry of
`Capability → candidate provider order`, declarative data, never
selection logic).

## Provider Pattern

A single abstract contract (`BaseAIProvider`, `data_layer/providers/base_provider.py`)
implemented by every concrete vendor/source (`gemini_provider.py`,
`openai_provider.py`, `claude_provider.py`, `grok_provider.py`;
`twelve_data_client.py`, the MT5 stub). Constitution Article 5: no code
outside the provider's own package ever names the vendor.

## Adapter Pattern

A narrow function or class that reshapes one module's data into
another's expected type without either module depending on the other
directly. Examples: the `MarketCandle` → `RawCandle` adapter (Phase 59
Validation), `ai/content/broadcast_output.py`'s `prepare_broadcast()`
(reshapes a `ContentResult` into `BroadcastReadyContent`), the
`ai/analyzer/ai_analyzer.py` / `ai/journal/trade_journal.py` Phase-55
compat shims that re-export the canonical top-level files.

## Repository Pattern

The only layer allowed to touch the database (Constitution Article 4).
19 real repositories under `database/*_repository.py`, each owning SQL
for exactly one domain, no business logic.

## Factory Pattern

A `build_*()` function that constructs a fully-formed registry or
default configuration in one call rather than requiring the caller to
assemble it piece by piece. Examples: `build_persona_registry()`,
`build_broadcast_provider_registry()`, `build_media_registry()`,
`build_language_registry()`, `build_cache_key_from_context()`.

## Event Bus Pattern

A single publish/subscribe channel (`ai/runtime/event_bus.py`'s
`EventBus`) that decouples an event's producer (`AIService`) from its
consumers (`platform_layer/telegram/owner/runtime_notifications.py`, audit logging)
via a typed `EventType`/`RuntimeEvent` payload, rather than each
producer calling each consumer directly.

## Capability Pattern

A single enum (`ai/capabilities/capability.py`'s `Capability`) that
names *what a request is asking for*, decoupled from *which provider
answers it* (`ai/router/routing_rules.py`) and *who may ask*
(`ai/access/`'s permission matrix). Adding a new capability is always
Article 11's checklist item 5 — check before adding a new mechanism to
express the same idea.

## Related

- `docs/constitution/CONSTITUTION.md` Article 7, Article 11.
- `docs/architecture/NAMING_CONVENTIONS.md` — the file-naming
  convention that signals which pattern a new file follows.
- `docs/architecture/EXTENSION_GUIDE.md` — applying these patterns
  when adding a capability or command.
