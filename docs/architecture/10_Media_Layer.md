# GoldBot Ecosystem Architecture — Media Layer

Part of the Senior Trading AI Ecosystem architecture set. Governed by
`docs/constitution/CONSTITUTION.md` (supreme) and scoped under
`01_Ecosystem_Architecture.md` (the ecosystem's high-level map — see
its "Division of authority" section). This file is the Media Layer
detail split out of that document's own former Section (TASK-GOV-004,
Owner-directed restructure, Option A: ecosystem-level summary, not a
duplicate of the Trading-Core/AI/Telegram mechanical detail already
owned by `ARCHITECTURE_MASTER.md`/`LAYER_CONTRACT.md`/
`MODULE_DEPENDENCIES.md`/`DATA_FLOW.md` where this layer overlaps them
— this file cross-references those, it does not restate them).

**Status: contract-only foundation, no live channel.** Phase 63.0
already built `ai/persona/` (identity data), `broadcast/`
(`BroadcastRequest`/`ExplanationOutput` value objects, channel/media-
type/language intent flags), `media/` (`media_adapter.py`,
`media_manager.py`, `media_pipeline.py`, `media_registry.py`,
`media_types.py`), and `translation/` — all explicitly contract-first
per `docs/PHASE63_0_FREEZE.md`: they hold data, never call a prompt,
never call `AIService` or a provider, never call a YouTube/OBS/RTMP/
Twitch/Kick client, never synthesize voice/image/video. This is a real,
deliberate foundation for the diagram's Media Hub (YouTube, Telegram
Broadcast, TikTok, Shorts, Podcast, Weekly Market Review, AI Content
Studio, Live Streaming) — but no live channel integration exists yet.
This is the one layer in this section where "not built" would
understate the real, already-approved foundation work.

