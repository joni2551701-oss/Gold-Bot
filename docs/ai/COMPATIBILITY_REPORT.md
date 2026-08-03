# COMPATIBILITY_REPORT.md — TASK-AI-000A: Backward-Compatibility Impact

Status: **POST-IMPLEMENTATION**. This document states exactly what
moved or was renamed, and why it does not break the system. Success
criterion "Public API = Stable" and "Existing tests = 100% PASS" both
hold: all 4609 tests pass, and every in-repo consumer was updated in
the same change.

## 1. `EventBus` / `EventType` / `RuntimeEvent` — module relocated

- **Before:** `ai_layer.ai_engine.runtime.event_bus`
- **After:** `ai_layer.ai_service.event_bus`
- **Class-level API:** unchanged — same three public classes, same
  members, same behavior (byte-identical class bodies). Only the import
  path changed.
- **Consumers updated (14):** 7 source (`ai/runtime/ai_service.py`,
  `ai/runtime/runtime_manager.py`, `ai/runtime/self_check.py`,
  `ai/audit/provider_stats.py`, `ai/providers/circuit_breaker.py`,
  `platform_layer/telegram/owner/runtime_commands.py`,
  `platform_layer/telegram/owner/runtime_notifications.py`) + 7 tests.
- **Breaking risk:** an *external* caller doing
  `from ai.runtime.event_bus import EventBus` would need the new path.
  No such external caller exists (all consumers are in-repo and
  updated). No compatibility shim was left at the old path, on purpose:
  the whole point of a clean import graph (and Stage 4's "remove
  unnecessary re-exports") is to not accumulate them, and the pyflakes/
  test gates confirm nothing references the old path.

## 2. `ContentType` — enum relocated

- **Before:** `ai_layer.ai_service.content.content_types.ContentType`
- **After:** `ai_layer.ai_service.content.content_types.ContentType`
- **Enum API:** unchanged — same 9 members, same string values.
- **The `Capability`-based helpers stay put:** `CONTENT_CAPABILITIES`,
  `is_content_capability()`, `content_title()` remain importable from
  `ai_layer.ai_service.content.content_types` exactly as before (they are content-service
  internals, not shared vocabulary). Files that imported both a helper
  and `ContentType` from that one path now use two import lines.
- **Consumers updated (21 files):** 19 `ContentType`-only imports
  redirected by exact-line replacement; 2 mixed imports split by hand;
  5 docstring path references corrected.
- **`ExplanationOutput.content_type` field:** its public type
  annotation stays `Optional[ContentType]` and still accepts a
  `ContentType` member (the test
  `test_explanation_output_accepts_a_content_type` passes unchanged) —
  the field's contract is preserved exactly; only where `ContentType`
  is *imported from* changed.

## 3. `TradeJournalEntry` (Phase 55 record) — class renamed

- **Before:** `ai_layer.knowledge_ai.knowledge_base.journal.trade_journal.TradeJournalEntry`
- **After:** `ai_layer.knowledge_ai.knowledge_base.journal.trade_journal.TradeJournalRecord`
- **Unchanged:** all 15 fields, and the `create_journal_entry()`
  factory (same name, same signature, same behavior — it simply returns
  a `TradeJournalRecord` now).
- **The unrelated Phase 66.2 class keeps its name:**
  `ai_layer.knowledge_ai.knowledge_base.trade_journal.models.TradeJournalEntry` is **not** touched. After
  this change the name `TradeJournalEntry` resolves to exactly one
  class in the codebase.
- **Consumers updated (all in-repo):** `ai/context/context_builder.py`,
  `ai/context/context_snapshot.py`, the `ai_layer/knowledge_ai/knowledge_base/trade_journal.py`
  re-export shim, and a docstring in `ai/journal/failure_analysis.py`.
  The `create_journal_entry`/`TradeOutcome`/`DecisionType`/`SignalType`
  importers (e.g. `tests/ai/context/test_context_builder.py`) were
  unaffected — they never imported the class by name.
- **No backward-compat alias added:** an alias
  (`TradeJournalEntry = TradeJournalRecord`) would reintroduce the very
  duplicate name Stage 2 removes, so it was deliberately omitted.

## 4. Files moved (git-tracked renames, content unchanged)

- `ai/explanation/explanation_content_adapter.py` →
  `ai/content/explanation_content_adapter.py` (the adapter belongs on
  the downstream content side).
- `tests/ai/explanation/test_explanation_content_adapter.py` →
  `tests/ai/content/test_explanation_content_adapter.py` (test follows
  its subject; import path updated).

## Trading Core — zero regression

No file under `core/`, `decision/`, `risk/`, `execution/`,
`strategies/`, `signals/`, top-level `context/`, `data/`, `lifecycle/`,
or `database/` was modified (verified by `git diff --cached --stat` on
those paths: empty). The `ai/context/` edits above are the AI-layer
context builder, not the Trading-Core `context/` package.

## Net compatibility statement

Every change is a relocation or rename with all in-repo consumers
updated in the same commit; no public class/function signature, field,
or behavior changed. The only externally-observable delta is three
import *paths* (`ai_layer.ai_service.event_bus`, `ai_layer.ai_service.content.content_types`, and the
`TradeJournalRecord` name), each documented above.
