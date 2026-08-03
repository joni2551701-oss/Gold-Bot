# telegram/

## Purpose
The Telegram product layer: registration, settings, subscriptions,
signal access control, admin panel, feedback. Built entirely on top
of the pipeline's output, without modifying pipeline/strategy/AI/risk
logic.

## Flow
```
Telegram Update
      |
      v
Command Router -> Permission Check -> Handler -> Service -> Database
```

## Responsibilities
Routing (`command_router.py`), permissions (`permissions.py`),
handlers (`handlers.py`, Handler → Service only), services
(`*_service.py`, business logic), outbound delivery (`bot.py`,
`notifier.py`), inbound polling (`polling.py`).

## Input
Telegram updates (commands), or a formatted signal string (from
`core/pipeline.py` via `Notifier`).

## Output
Telegram messages (text + optional keyboard hint).

## Dependencies
`database/` (via services, never directly from handlers — see
`CLAUDE.md`), `goldbot/core_layer/secrets/secrets.py`. No dependency on `context/`,
`strategies/`, `signals/`, `ai/`, `decision/`, or `risk/` — this layer
only ever sees their already-computed output via
`telegram/signal_formatter.py`'s typed parameters.

## Future Roadmap
See `docs/telegram_layer.md` for the full service/permission map and
`docs/commands_reference.md` for every command's detail — this README
is intentionally short; those documents are the real reference.
