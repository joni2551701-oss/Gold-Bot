# REAL-DATA-007 — 09. Reconnect / Recovery

## Tekshirilgan
`data_layer/live_data/price_stream/price_stream.py` — `PriceStream` holat
mashinasi (state machine).

## Dalillar (file:line)
- `PriceStream` — "per-asset market lifecycle state machine" (:2, :58-59).
- DD-046 lifecycle holatlari (:7-8):
  `INITIALIZING → CONNECTING → STREAMING → {WAITING_FOR_MARKET |
  RECONNECTING} → SHUTDOWN`.
- `max_reconnect_attempts: int = 5` (:64), `self._max_attempts` (:78),
  `self._reconnect_attempts = 0` (:90).
- `tick()` (:125) holat mashinasini bir qadam oldinga suradi;
  `StreamState.RECONNECTING` bo'lsa `_tick_reconnecting(now)` (:139-140).
- `stats` reconnects hisoblagichi (:96), `health()` `reconnect_attempts`
  ni chiqaradi (:118).
- Provider xatolari (`NotImplementedError`, `ValueError`, tarmoq)
  PriceStream ichida ushlanadi va standart holat/health'ga aylantiriladi
  (:17, DD-051 isolation).

## Xulosa
Reconnect / recovery **IMPLEMENTED** — chinakam lifecycle state machine
(RECONNECTING holati, urinishlar chegarasi, izolyatsiya). Bu qatlam real
va ishlaydi. (E'tibor: reconnect real bo'lsa-da, u candle-polling
upstream ustida ishlaydi — reconnect current-price kontraktini yaratmaydi.)
