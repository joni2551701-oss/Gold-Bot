# GoldBot — AI Content Foundation

Phase 63.0 (Senior Trading AI Foundation), TASK 2/3. Foundation only.

## Where the content contract lives

Not a new top-level `content/` package — extended in place inside the
already-existing `ai/content/` (Phase 61.5 TASK 5/6), per Module Reuse
Principle (see `docs/PHASE63_0_FOUNDATION_AUDIT.md`):

- `ai/content/content_schema.py` — `ContentRequest`/`ContentResult`
  (Phase 61.5).
- `ai/content/content_types.py` — `CONTENT_CAPABILITIES` (Phase 61.5)
  plus the new `ContentType` enum (Phase 63.0 TASK 2):
  `WEEKLY_OUTLOOK`, `DAILY_BRIEF`, `NEWS_ANALYSIS`, `MARKET_UPDATE`,
  `PERFORMANCE_REVIEW`, `EDUCATION`, `EXPLANATION`.
- `ai/content/content_adapter.py` — `ContentEngine` (Phase 61.5,
  unchanged this phase).
- `ai/content/broadcast_output.py` — `BroadcastReadyContent`/
  `prepare_broadcast()` (Phase 61.5, unchanged this phase).

`ContentType` is deliberately narrower than `Capability`: it names
*kinds* of content, not *who generates them*. Some values already
correspond to an existing `Capability` (`WEEKLY_OUTLOOK` ≈
`AI_WEEKLY_OUTLOOK`, `NEWS_ANALYSIS` ≈ `AI_NEWS_ANALYSIS`); others
(`DAILY_BRIEF`, `MARKET_UPDATE`, `PERFORMANCE_REVIEW`) have no
dedicated `Capability` yet — a future phase may generate any of them
through the new `Capability.AI_CONTENT` (TASK 8) plus a `ContentType`
parameter, rather than growing `Capability` one-for-one forever.

## Explanation Output Contract

`ai/explanation/explanation_output.py` (new file inside the existing
`ai/explanation/` package, Phase 63.0 TASK 3):

```
ExplanationOutput
  title: str
  summary: str
  body: str
  risk_note: str
  invalidation: str
  confidence: float
  language: str
  content_type: Optional[ContentType]
  metadata: Dict[str, Any]
```

Not read by `explanation_engine.py` this phase — a pure contract, the
same "shape now, wiring later" posture `ContentResult` established in
Phase 61.5.

## What this phase does not do (Rule 6)

- No AI generation of any content type.
- `explanation_engine.py`'s own three real methods
  (`explain_signal()`/`summarize_report()`/`explain_topic()`) are
  unchanged.

## Related

- `docs/ai/AI_ARCHITECTURE.md` — the full `ai/` package map.
- `docs/PHASE63_0_FOUNDATION_AUDIT.md` — the Reuse Principle audit
  behind this design.
