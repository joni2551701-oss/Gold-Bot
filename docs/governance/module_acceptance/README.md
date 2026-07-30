# Module Acceptance Registry (MA)

The controlled registry of **Module Acceptance Records** for GoldBot
development. Established by **DD-053**.

An MA record (`MA-XXX.md`) is the durable, audit-traceable statement that
a specific implementation module passed CI + Director Final Review and is
accepted into `main`. Module acceptances are **not** Director Decisions —
`DD-xxx` is reserved for architecture and governance decisions; `MA-xxx`
holds acceptances, so the two numbering streams never collide (DD-053).

## Registry

| ID | Module | PR | CI | Status |
|----|--------|----|----|--------|
| [MA-001](MA-001.md) | MarketMemory Core (v1.1 Phase 1, module 1) | #5 | ✅ | Accepted |
| [MA-002](MA-002.md) | MemoryReader (module 2) | #6 | ✅ | Accepted |
| [MA-003](MA-003.md) | Candle Builder + candle_clock (module 3) | #7 | ✅ | Accepted |
| [MA-004](MA-004.md) | Price Stream (module 4) | #8 | ✅ | Accepted |
| [MA-005](MA-005.md) | Historical Bootstrap (module 5) | #11 | ✅ | Accepted |

Batch cadence (ORDER-049): acceptances are recorded in a batch governance
PR roughly every 3–5 accepted modules.

## Related

- `docs/governance/director/DD-053.md` — the decision establishing this
  registry.
- `docs/architecture/MARKET_DATA_FOUNDATION.md` — the canonical
  architecture these modules realize.
- `docs/governance/director/` — the DD registry (architecture / governance
  decisions only).
