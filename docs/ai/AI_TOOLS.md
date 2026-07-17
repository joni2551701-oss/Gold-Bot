# GoldBot — AI Tools

Governed by `docs/constitution/CONSTITUTION.md` Article 1 — every tool
here is advisory/read-only, never a trigger for a pipeline action.
`ai/tools/` foundation shipped Phase 61.0 TASK 8; Phase 61.3 TASK 4
gave all five real, read-only logic over already-built input objects
(an explicit architecture correction from that phase's initial plan,
which would have read `database/` directly — documented in
`docs/AI_INTELLIGENCE_LAYER.md`).

## The five tools

```
ai/tools/
  market_tool.py       reads already-computed market/context data
  analytics_tool.py     reads already-computed analytics/performance data
  education_tool.py      reads knowledge/ entries
  learning_tool.py         reads learning/ records
  news_tool.py               reads fundamental/economic context
  tool_registry.py             the lookup surface every caller uses
```

## The rule every tool follows

A tool reads an **already-built object** another layer produced — it
never queries `database/` directly (Constitution Article 4 applies
here too: a tool is not a repository), never calls a live external
API, and never triggers `decision/`, `risk/`, or `execution/`.
`tool_registry.py` is the single place a caller looks a tool up by
name; no second registry exists.

## Related

- `docs/PHASE61_3_INTELLIGENCE_FREEZE.md` — TASK 4, the read-only
  correction.
- `docs/AI_INTELLIGENCE_LAYER.md` — the original TASK 4 architecture
  note.
- `docs/architecture/DESIGN_PATTERNS.md` — the Registry pattern
  `tool_registry.py` follows.
