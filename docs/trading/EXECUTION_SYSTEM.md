# GoldBot — Execution System

Governed by `docs/constitution/CONSTITUTION.md` Article 2. Verified
directly against `execution/` and `lifecycle/`'s real file listings.

## Real structure

```
execution/
  execution_engine.py     intentionally inert — no live MT5 order
                           calls exist yet; wiring it up requires
                           explicit Director approval, not a routine
                           addition (CLAUDE.md Trading Safety rule)
  signal_lifecycle.py       signal lifecycle bookkeeping

lifecycle/
  paper_trade.py             PaperTrade model
  paper_trade_monitor.py       the real, running monitor (Phase 59.4)
  signal_state.py                signal lifecycle state
  trade_state.py                  trade lifecycle state
```

## Why `execution/` is separate from `lifecycle/`

`execution/` is the designated future home for real order placement —
today it validates a `RiskResult` shape without sending anything
anywhere. `lifecycle/` is what actually runs today: `paper_trade_monitor.py`
tracks an approved/paper trade after delivery, independent of whether
a real order was ever placed. The same reasoning that keeps
`broadcast/` separate from `ai/content/` (Phase 63.0) applies here in
reverse chronological order — `lifecycle/` predates `execution/`
becoming a real concern, and neither absorbed the other.

## What Execution can and cannot do

- **CAN**: exist as the designated future home for order placement.
- **CANNOT**: place a real order today.
- **Depends on**: `risk/`.

## What Trade Monitor can and cannot do

- **CAN**: track the lifecycle of an approved/paper trade after
  delivery.
- **CANNOT**: originate a new signal, alter a risk decision already
  made.
- **Depends on**: `decision/`, `risk/`.

## Related

- `docs/trading/RISK_SYSTEM.md` — what `execution/` receives as input.
- `docs/EXECUTION_SIMULATOR.md` — the paper-trading simulation layer
  built on top of `lifecycle/`.
- `docs/architecture/ARCHITECTURE_MASTER.md` — the same CAN/CANNOT
  table in the full system context.
