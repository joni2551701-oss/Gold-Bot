# REAL-DATA-006 — 10. Reconnect / Recovery

## Status: **IMPLEMENTED (PriceStream state-machine darajasida)**

Order "agar mavjud bo'lmasa NOT IMPLEMENTED yoz" deydi — bu yerda
reconnect/recovery MAVJUD, shuning uchun mavjud xulq qayd etiladi
(yangi reconnect arxitektura O'YLAB TOPILMADI).

## Dalil (`data_layer/live_data/price_stream/price_stream.py`)

State machine: `STREAMING → {WAITING_FOR_MARKET | RECONNECTING} →
SHUTDOWN` (docstring `:8`).

| Mexanizm | file:line |
|---|---|
| Max reconnect attempts | `:64` `max_reconnect_attempts: int = 5` |
| Exponential backoff base/cap | `:65-66` `backoff_base_seconds=1.0`, `backoff_cap_seconds=60.0` |
| Reconnect counter | `:90` `self._reconnect_attempts = 0` |
| Keyingi retry vaqti | `:91` `self._next_retry_at` |
| RECONNECTING tick | `:140,175-182` `_tick_reconnecting()` |
| Backoff hisobi | `:225-228` `_schedule_retry()` — `min(base*2**attempts, cap)` |
| Attempts tugashi | `:181-182` `reconnect attempts exhausted` |
| Muvaffaqiyatli ulanishda reset | `:154` `self._reconnect_attempts = 0` |

Shuningdek WAITING_FOR_MARKET (weekend/market-closed) rejimi
(`:214-223`, `_enter_waiting`, `_market_open`) — DD-047 bo'yicha yopiq
bozorda polling to'xtatiladi.

## Provider isolation (DD-051)

`_safe_connect`/`_safe_disconnect`/`_safe_read` (`:266+`) provider
xatolarini ushlaydi — xato stream'dan tashqariga chiqmaydi. Bu
recovery posture'ning bir qismi (xato → RECONNECTING → backoff → retry).

## Status: **IMPLEMENTED (real, mavjud state-machine)**

Reconnect/recovery real va mavjud. Auditda o'zgartirilmadi. Real oqim
orqali empirik tasdiq (masalan provider tushib qayta ulanishi) M1
mismatch tuzatilib real oqim ishga tushgandagina kuzatiladi.
