# GoldBot — Decision Log

Governed by `docs/constitution/CONSTITUTION.md` Article 8. The
load-bearing architectural and governance decisions behind this
repository, in the Director's requested format: Decision / Reason /
Date. "Date" here is the phase the decision was made or formalized in
— this repository does not track a per-decision calendar date, so none
is fabricated.

---

**Decision**: Trading Core must remain isolated from the AI layer —
`ai/` never imports `decision/`, `risk/`, or `execution/`.

**Reason**: Risk reduction. A deterministic, rule-based Decision Engine
is auditable in a way an AI-influenced one is not; Constitution
Article 1 makes this permanent, not a temporary limitation.

**Date**: Phase 61.0's isolation audit; formalized as Constitution
Article 1/3, Phase 62.0.

---

**Decision**: A LOCKed Foundation module's name, path, import path,
and public API cannot change without explicit Director approval.

**Reason**: Architecture stability — a rename or move silently breaks
every existing import path across the codebase; explicit approval
keeps that blast radius visible before it happens.

**Date**: Director Policy following Phase 63.0's freeze; formalized as
Constitution Article 9, Phase 62.1a.

---

**Decision**: Before writing a new module, search for an existing
Foundation/Manager/Contract/Model/Capability/Registry first.

**Reason**: Prevents duplicate logic at scale — `ai/audit/provider_stats.py`
being extended three separate times (61.1/61.3/61.6) rather than
replaced is the worked proof this discipline holds.

**Date**: Phase 59's Architecture Freeze; Constitution Article 7,
Phase 62.0; the explicit six-item checklist, Constitution Article 11,
Phase 62.1a.

---

**Decision**: Content-type contracts extend the existing `ai/content/`
package; they do not get a new top-level `content/` package.

**Reason**: `ai/content/` already existed from Phase 61.5 — a Reuse
Audit found it before Phase 63.0's brief assumed it needed building
from scratch.

**Date**: Phase 63.0 TASK 2.

---

**Decision**: `broadcast/`, `media/`, `translation/` are new top-level
packages, not `ai/broadcast/` etc.

**Reason**: Channel/media-type/language *management* is a genuinely
different responsibility from AI content *generation* — the same
reasoning that keeps `execution/` (Layer 3) separate from `decision/`
(Layer 2).

**Date**: Phase 63.0 TASK 4/5/6.

---

**Decision**: `ai/router/router.py`'s selection logic is never touched
when adding a new `Capability` — only `routing_rules.py`'s declarative
data table gains an entry.

**Reason**: Keeps the Router's tested selection behavior stable across
every capability addition; a routing rule is data, not a code change
to the router itself.

**Date**: Established Phase 62.2, reused Phase 63.0 TASK 8.

---

**Decision**: `AI_EVOLUTION.md` holds Future Vision only;
`docs/roadmap/VERSIONS.md` plus each phase's Freeze document hold
Actual Development Status. The two never mix.

**Reason**: A Worker's own audit flagged `AI_EVOLUTION.md`'s stage
table as possibly stale relative to real Phase 61.3 work. Rather than
silently rewriting a vision document to match code status, the
Director ruled the two document types stay role-separated —
`AI_EVOLUTION.md` was later restructured (Phase 62.1d) on its own
terms, not to "catch up" to code.

**Date**: Phase 62.1c.

---

**Decision**: Version numbers `v0.5`–`v0.9` are never renumbered or
reassigned, even when a new roadmap vision (`docs/VISION.md`'s
"Senior Trading AI Platform") groups their themes differently.

**Reason**: Multiple existing documents
(`docs/PHASE61_7_FREEZE.md`, `docs/owner/OWNER_PANEL.md`,
`docs/telegram/OWNER_SYSTEM.md`) already reference these exact version
numbers; renumbering would silently break every one of those
cross-references.

**Date**: Phase 62.1d TASK 2.

---

**Decision** (ADR-001): GoldBot Platform is architected around a
Shared Platform Layer serving five equal clients — Telegram Bot,
Telegram Mini App, Android, iOS, Desktop — not around Telegram Bot
with other clients bolted on afterward. Concretely: `Platform Core →
Shared Platform Layer → {Telegram Bot, Mini App, Android, iOS,
Desktop}`, and no Platform component may be written as `Telegram
Callback → Business Logic` directly — it is always `Platform UI →
Navigation Layer → Application Layer → Business Logic` (the Universal
UI Abstraction rule).

**Reason**: A Navigation (or any Platform component) designed
Telegram-first would have to be rewritten for Android, iOS, and
Desktop once they exist — the exact rework this decision exists to
avoid, at the cost of designing for four platforms with zero code
today.

**Date**: TASK-002A review (Navigation Analysis approved); formalized
as Constitution Article 13 (Future First Principle) in the same
review. Full record: `communication/decisions/ADR-001.md`.

## Related

- `docs/changelog/CHANGELOG.md` — what shipped alongside each decision.
- `docs/changelog/PHASE_HISTORY.md` — the full phase list.
- `docs/constitution/AMENDMENTS.md` — the subset of these decisions
  that became Constitution Articles.
