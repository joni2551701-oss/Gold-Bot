# Architecture Backlog

Deferred, Director-approved architecture improvements that are intentionally
**not** done now (to avoid churn on a frozen layer) and are scheduled for a
future major version or architecture refresh. Each item records why it is
deferred and what triggers picking it up.

This is a backlog of *deferred refactors*, distinct from `docs/ROADMAP.md`
(phase roadmap) and `docs/roadmap/VERSIONS.md` (version status).

---

## ARCH-RENAME-001 — Rename `CanonicalSignalResult` → `SignalEnvelope`

- **Status:** Deferred
- **Layer:** `signals/` (STEP-08 / TASK-CORE-008)
- **Raised by:** Director review of STEP-08 (post-approval).
- **Decision:** Do **not** rename now — STEP-08 is officially FROZEN, CI #411
  passed, tests pass, docs written. A rename-only commit at this point is
  churn with little benefit.

### The change (when picked up)
```
signals.manager.CanonicalSignalResult  →  SignalEnvelope
```
Update the class name, its `__all__`/`signals.__init__` export, all
`tests/signals/` references, and `docs/PHASE_SIGNALS.md` / `signals/README.md`.

### Why `SignalEnvelope` is the better name
`SignalSchema` **is** the signal itself (the canonical model). The result
object is a wrapper that carries everything *around* the signal —
lifecycle, routing, metadata, consumer list, enrichment, strength. In
enterprise-messaging terminology that wrapper is an **envelope**:

```
SignalEnvelope
  ├─ signal        (SignalSchema — the canonical signal itself)
  ├─ strength      (SignalStrength)
  ├─ enrichment    (SignalEnrichment / metadata)
  ├─ presentation  (SignalPresentation)
  ├─ routes        (SignalConsumer list)
  ├─ lifecycle     (CanonicalSignalStatus)
  └─ validation    (ValidationResult)
```
`SignalSchema` + `SignalEnvelope` reads more clearly than `SignalSchema` +
`CanonicalSignalResult`, which can be confused (both sound "canonical").

### Trigger to pick up
Next major version bump or a dedicated `signals/` architecture refresh —
whichever comes first — so the rename ships alongside other intentional
`signals/` changes rather than as a standalone churn commit. It is a
mechanical, non-behavioral rename (no contract or logic change).
