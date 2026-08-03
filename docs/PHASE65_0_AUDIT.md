# Phase 65.0 — AI Voice Intelligence Foundation: Audit

TASK 0. Mandatory reading completed (`docs/constitution/CONSTITUTION.md`,
`docs/policies/DIRECTOR_POLICY.md`, `docs/architecture/*`,
`docs/roadmap/*`, `docs/ai/*`) before any code change, per this
phase's own Rule 1.

## Foundation Reuse Audit (Rule 1's own required table)

| Component | Brief's assumed location | Real state | Decision |
|---|---|---|---|
| Foundation | `voice/`, `ai/voice/` | ❌ Neither exists — confirmed by direct `Glob` search | Genuine new top-level package, per the reasoning below |
| Manager | — | ❌ No `VoiceManager`/equivalent anywhere | Genuine new work (TASK 4) |
| Registry | — | ❌ No voice-specific registry | Genuine new work (TASK 3) |
| Runtime | — | ❌ No voice-specific runtime | Genuine new work (TASK 8) |
| Model | — | ❌ No `VoiceProfile`/`VoiceProvider`/`VoiceRequest`/`VoiceResult`/`VoiceSettings` anywhere | Genuine new work (TASK 2) |
| Capability | `ai/capabilities/capability.py` | ✅ `Capability.VOICE` already exists (Phase 61.0), already routed in `ai/router/routing_rules.py`'s `_CAPABILITY_PROVIDER_PREFERENCE` (`openai`, `local_llm`) | Reused as-is, no new capability, no router change |
| Contract | — | ➖ Partial — `media/media_types.py`'s `MediaType.VOICE` (Phase 63.0) is an existing, adjacent vocabulary member ("Voice/TTS output (no synthesis this phase)", `media/media_registry.py`'s own descriptor text) | See relationship section below — not extended, not duplicated |
| Profile | `ai/persona/` | ➖ Partial — `ai/persona/persona.py`'s `Persona` has a free-text `tone` field (its own docstring example literally says "the intended *voice*") but no pitch/speed/language/provider fields a real Voice Profile needs | Not extended — a different, narrower contract (see Persona relationship section) |
| Provider | `ai/providers/`, `broadcast/provider_manager.py` | ➖ Pattern reused, concept not — `ai/providers/openai_provider.py`'s `OpenAIProvider` is a real, `AIService`-calling **LLM/chat** provider; `broadcast/provider_manager.py`'s `BroadcastProviderManager` manages **delivery-channel** intent (YouTube/Telegram/etc.) | Neither is a Voice-synthesis provider abstraction — genuine gap, but the *static catalog + Owner-set status* **pattern** both already establish is reused (Rule 8) |

## Why `voice/` is a genuine new top-level package (not `ai/voice/`)

Per Module Reuse Principle step 2 ("can an existing module be
extended?"): the two closest candidates are `media/` (already owns
one `MediaType.VOICE` vocabulary member) and `ai/persona/` (already
owns a `tone` field). Neither can absorb this phase's actual scope —
a `VoiceProfile`/`VoiceProvider`/`VoiceRequest`/`VoiceResult`/
`VoiceSettings` model set, a profile registry, a provider catalog, a
Manager, an Adapter, and a Runtime — without turning a narrow
single-enum-member or single-string-field concern into a full
subsystem, the same reasoning `docs/PHASE63_0_FOUNDATION_AUDIT.md`
used to justify `broadcast/` as a new top-level package rather than
extending `ai/content/broadcast_output.py`. **Decision: `voice/`, a
new top-level package, a sibling of `ai/` — never `ai/voice/`** —
matching the `media/`/`broadcast/` precedent (both are "production/
delivery-shaping" Foundations, top-level siblings of `ai/`, distinct
from `ai/`'s pure-reasoning subpackages). No Constitution conflict:
this is the same category of decision Phase 63.0's own audit already
made twice for this exact shape of module.

## Relationship to `media/media_types.py`'s `MediaType.VOICE` (not duplicated)

`MediaType.VOICE` stays exactly what it already is — "this asset is
shaped for voice/TTS delivery," a flag at the Media layer, reused
as-is, untouched this phase. `voice/`'s new models answer a different,
more granular question this phase's brief itself asks: *who* is
speaking (`VoiceProfile`: Senior/Seniorita/Narrator) and *through
which backend* (`VoiceProvider`: OpenAI/ElevenLabs/local/custom) and
*with what settings* (`VoiceSettings`: language/speed/pitch). These
are complementary, not competing — a future integration phase would
have `media/`'s `MediaAsset.media_type == MediaType.VOICE` reference a
`voice/` `VoiceRequest`/`VoiceResult` by primitive key, never the
reverse and never an embedded object either way. Not resolved this
phase — foundation only.

## Relationship to `ai/persona/`'s `Persona` (not extended, not duplicated)

`Persona` (`name`, `role`, `tone`, `language_style`, `disclaimer`,
`system_identity`) is a *textual identity/prompt* contract — Rule 5 of
its own governing phase (63.0) is explicit: "Persona prompt yozmaydi.
AI chaqirmaydi. Faqat identity." `VoiceProfile` (this phase) is a
*voice-delivery capability* contract (`supported_languages`,
`supported_modes`, `default_provider`) — a different shape for a
different purpose. **Critical resolution, carried forward from
`docs/PHASE63_8_AUDIT.md`'s own Persona finding:** `ai/persona/persona_registry.py`
registers exactly one real `Persona`, `SENIOR_TRADING_AI` — no
"Seniorita" `Persona` exists, and Phase 63.8's brief explicitly forbade
creating one this program. This phase's `VoiceProfile` named
`"Seniorita"` is **not** an `ai.persona.Persona` and does not create
one — it is a self-contained voice-delivery metadata record inside the
new `voice/` package, referencing the *name* `"Seniorita"` as a
free-text string only (the same "never carry another package's object
graph" convention `MediaAsset.content_id`/`BroadcastAsset.persona_name`
already established). A future, separately-approved `ai/persona/`
Worker Brief would be the only place a real `Persona` named
"Seniorita" could be created — untouched, unaffected by this phase.

## TASK 5/6's file-layout resolution (Rule 8 — reuse the pattern, not the literal layout)

The brief names `profiles/senior.py`/`seniorita.py`/`narrator.py` and
`providers/openai.py`/`elevenlabs.py`/`local.py`/`custom.py` — one
file per named item. No existing static-catalog module in this
codebase uses that shape: `ai/persona/persona_registry.py` (one
`Persona` per module-level constant, one file), `media/media_registry.py`
(one `MediaDescriptor` per list entry, one file), and
`broadcast/provider_manager.py` (one `BroadcastProviderDescriptor` per
list entry, one file) are the three closest precedents, and all three
use a single file with a `build_*_registry()` function. **Decision:
`voice/profiles.py`** (module-level `VoiceProfile` constants —
`SENIOR_VOICE`, `SENIORITA_VOICE`, `NARRATOR_VOICE` — plus
`build_voice_profile_registry()`) **and `voice/providers.py`**
(`build_voice_provider_registry()`, four `VoiceProvider` descriptors)
— matching the established pattern exactly, not the brief's literal
one-file-per-item suggestion. Rule 8 ("mavjud pattern'dan foydalanish")
is itself the brief's own instruction to make this resolution.

## TASK 3/4/8's three-tier resolution (no duplicate logic)

The brief asks for a Registry (TASK 3: `register`/`get`/`exists`/
`list_all`/`default`), a Manager (TASK 4: `register_profile`/
`register_provider`/`get_profile`/`get_provider`/`validate`/`prepare`),
and a Runtime (TASK 8: `prepare_voice`/`resolve_profile`/
`resolve_provider`/`validate`/`build_request`/`build_result`) as three
separate files with overlapping-sounding responsibilities. Per
CLAUDE.md's "No duplicate logic" restriction, these are composed, not
reimplemented three times:

- `voice/registry.py`'s `VoiceProfileRegistry` owns the actual
  profile store (register/get/exists/list_all/default) — the same
  "class wrapping a dict, pre-seeded from the static catalog" shape
  `broadcast/trigger_manager.py`'s `BroadcastTriggerManager` already
  established (the one existing Phase 63.0 class with a real,
  runtime-mutable `register()`).
- `voice/manager.py`'s `VoiceManager` owns provider status
  (ENABLED/DISABLED intent, the same shape
  `MediaManager`/`BroadcastProviderManager` already established) and
  *delegates* `register_profile()`/`get_profile()` to an injected
  `VoiceProfileRegistry` rather than re-implementing profile storage.
  `validate()`/`prepare()` are the one real deterministic-logic home.
- `voice/runtime.py`'s `VoiceRuntime` is a thin façade: every one of
  its six methods delegates directly to `VoiceManager` (or, for
  `build_request()`/`build_result()`, assembles a `VoiceRequest`/
  `VoiceResult` from already-validated primitive values) — it computes
  nothing `VoiceManager` doesn't already compute.

## `voice/adapter.py`'s scope (TASK 7)

Mirrors `media/media_adapter.py`'s `content_result_to_media_asset()`
shape exactly: one pure function reading an upstream `ai.content.content_schema.ContentResult`'s
own already-public fields (never `ContentEngine`'s internal state)
into a `VoiceRequest` via `VoiceManager`. `voice/` may read `ai/content/`
(type-only, upstream) but never `media/`/`broadcast/` (this phase adds
no Voice→Media/Voice→Broadcast code — a future integration phase
would own that, per this brief's own TASK 9 "Yakuniy Architecture"
diagram, which is a target-state illustration, not something this
phase implements).

## Dependency Compliance

`voice/*.py` imports only `ai.content.content_schema` (type-only,
TASK 7's adapter) and `core_layer.logger.logger` (the same logging convention
`MediaManager`/`BroadcastProviderManager` already use) — zero
dependency on `decision/`, `risk/`, `execution/`, `strategies/`,
`signals/`, `database/`, `telegram/`, `media/`, or `broadcast/`.
TASK 10's isolation test enforces this permanently.

## Trading Core Isolation

`git diff --stat -- core/ decision/ risk/ execution/ strategies/
signals/` — zero output before any change this phase.

## Conclusion

No Constitution Article conflict. `voice/` is a genuine new top-level
Foundation — every one of TASK 1–8's deliverables is new work, with
two deliberate structural resolutions (file layout per Rule 8; the
three-tier Registry/Manager/Runtime composition per "no duplicate
logic") documented above. No `Persona` is created, no `MediaType`
member is added or duplicated, no `Capability` is added, no LLM call
exists anywhere in the new package. Requesting no Director Decision.
