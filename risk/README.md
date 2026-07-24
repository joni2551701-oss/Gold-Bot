# risk/

## Purpose
Validates a decision's trade geometry and computes a sizing
suggestion. The last gate before a signal can reach Telegram.

## Flow
```
Decision Engine
      |
      v
Risk Manager   -- geometry + stop-loss validation
      |
      v
Telegram Notification Filter (core/pipeline.py)
```

## Responsibilities
- SL/TP geometry validation (BUY: `stop_loss < entry < take_profit`;
  SELL: mirrored).
- Stop-loss distance validation.
- Risk/reward and position-size calculation (sizing suggestion only —
  no broker/MT5 connection, never an order instruction).

## Input
`TradeDecision` (from `decision/`), optional `account_balance`.

## Output
`RiskResult` (`approved`, `lot_size`, `risk_amount`, `risk_reward`,
`reason`).

## Dependencies
`decision/` and `signals/` (for their model types). No dependency on
`database/`, `telegram/`, or `ai/`.

## Future Roadmap
None planned. This is the layer `CLAUDE.md`'s Trading Safety rules
name explicitly: never bypassed, never modified without approval.
