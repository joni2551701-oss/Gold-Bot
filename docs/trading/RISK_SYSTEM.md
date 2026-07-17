# GoldBot — Risk System

Governed by `docs/constitution/CONSTITUTION.md` Article 1 ("Never
bypass Risk Manager" — `CLAUDE.md`'s own Trading Safety hard rule).
Verified directly against `risk/risk_manager.py`.

## What `RiskManager.evaluate()` does

```
RiskManager.evaluate(signal, account_balance, risk_percent)
    │
    ├── validate_stop_loss_distance()   invalid → RiskResult(lot_size=0.0, rejected)
    ├── calculate_risk_reward()          reward:risk ratio
    ├── calculate_position_size()
    │       risk_amount = account_balance * risk_percent
    │       lot_size = risk_amount / stop_loss_distance
    └── RiskResult(lot_size, ...)
```

`lot_size` is a **suggested** sizing output — the Risk Manager
computes it, it does not itself place an order (that boundary belongs
to `execution/`, and `execution/` is intentionally inert today).

## Risk rules

- **risk %** — `risk_percent` per trade, applied against
  `account_balance` to get a dollar `risk_amount`.
- **lot calculation** — `risk_amount / stop_loss_distance`, never a
  fixed lot size regardless of account size or stop distance.
- **drawdown** — `RiskConfig.max_drawdown` (default 0.10) is the
  configured ceiling; enforcement beyond the config value itself is
  the same "config, not hardcoded" convention `decision/` uses.
- **emergency stop** — not `risk/`'s own concern; the Emergency Kill
  Switch lives in `core/emergency/` (`docs/EMERGENCY_SYSTEM.md`) as an
  independent, higher-priority override that can halt the pipeline
  before `risk/` is ever reached.

## What Risk can and cannot do

- **CAN**: evaluate a signal's geometry/stop-loss validity, size a
  position, reject on risk-limit violation via `evaluate()`.
- **CANNOT**: be skipped for any signal reaching a user; consult the
  AI layer (`risk/` imports nothing from `ai/` today and has no
  sanctioned reason to — `docs/architecture/IMPORT_RULES.md`).
- **Depends on**: `decision/` only.

## Related

- `docs/trading/DECISION_ENGINE.md` — what `risk/` receives as input.
- `docs/trading/EXECUTION_SYSTEM.md` — what happens to `RiskResult`
  next.
- `docs/EMERGENCY_SYSTEM.md` — the separate, higher-priority halt
  mechanism.
