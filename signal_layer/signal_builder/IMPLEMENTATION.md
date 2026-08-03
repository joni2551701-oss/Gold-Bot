# IMPLEMENTATION.md -- signal_layer/signal_builder

## `adapter.py`

Signal Layer — backward-compatibility adapter (Phase A15; wired into

Top-level functions: `from_signal_candidate()`

## `enricher.py`

Signals — Canonical Signal enricher (TASK-CORE-008 / STEP-08).

Classes: `SignalEnrichment`

Top-level functions: `enrich()`

## `models.py`

Classes: `SignalType`, `SignalCandidate`

## `schema.py`

Signal Layer — Signal Schema Standard (Phase A15).

Classes: `SignalSchema`, `ValidationResult`

Top-level functions: `generate_signal_id()`, `validate_signal()`

## Runtime / Algorithms / Pipeline / Event Flow / Sequence / Design Decisions / Performance Notes

Not authored at rollout time -- this section requires domain understanding beyond what can be mechanically derived from code, and is left for a future Development Phase to fill in (per Director Order No. 012/013, this rollout is documentation standardization only, not new authorship of technical narrative).

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013).*
