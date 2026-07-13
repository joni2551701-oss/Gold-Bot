# execution/

## Purpose
Scaffolding for a future MT5 order-execution layer. Currently inert.

## Responsibilities
`execution_engine.py`/`signal_lifecycle.py` unconditionally return
"not implemented" — no MT5 client, no order calls, no I/O. GoldBot
v0.2/v0.3 does not place trades automatically; execution is manual by
the trader.

## Input
None — not called from any runtime path.

## Output
None.

## Dependencies
None beyond stdlib. Not imported by `core/pipeline.py` or `main.py`
(confirmed by the Phase 48 audit).

## Future Roadmap
Real MT5 integration is the eventual purpose of this directory, but
no phase has scoped that work yet. Decide its fate (implement vs.
remove) before v0.4 rather than leaving it inert indefinitely — noted
as an open item in `docs/AUDIT_REPORT.md`.
