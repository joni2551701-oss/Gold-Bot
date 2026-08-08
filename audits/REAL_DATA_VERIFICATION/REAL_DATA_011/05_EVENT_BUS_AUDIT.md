# 05 — Event Bus Audit (REAL-DATA-011, Items D/G)

## Publish tomoni — REAL

`PriceStreamService` har tick landida real `PRICE_UPDATED` event
publish qiladi:
`data_layer/live_data/price_stream_service/price_stream_service.py:95-96`
(`self._event_bus.publish(Event(type=EventType.PRICE_UPDATED, ...))`).
EventType: `data_layer/event_system/event_model/event_model.py:50`.

## Consumer tomoni — Core NOT WIRED

`PRICE_UPDATED` ga **production subscriber YO'Q**. Grep butun repo
(test'siz):
- `provider_stats.py:198-202` — CACHE_HIT/MISS, VALIDATION_FAILED,
  PROVIDER_FAILED/CHANGED ga subscribe qiladi, **PRICE_UPDATED'ga
  emas**.
- `runtime_notifications.py:96-99` — PROVIDER_FAILED/RECOVERED,
  RUNTIME_* ga subscribe, **PRICE_UPDATED'ga emas**.
- Yagona PRICE_UPDATED subscriber — **verification probe**:
  `scripts/verification/real_price_stream_probe.py:145` (izoh:37-39
  aniq aytadi — "the TradingPipeline does NOT subscribe to
  PRICE_UPDATED — it reads via MemoryReader").

**Xulosa: Event Bus → Core = NOT WIRED.** Core MarketMemory SSOT'dan
o'qiydi, event'dan emas. Bu dizayn.

## Consumer contract / schema / lifecycle audit

- **Schema:** `Event(type, payload=PriceTick, ...)` mavjud va barqaror
  (`price_tick.py`). Contract publish tomonida to'liq.
- **Lifecycle:** EventBus subscribe/publish
  (`data_layer/event_system/event_bus/event_bus.py`) ishlaydi va
  boshqa event turlarida faol ishlatiladi — infratuzilma REUSE-mumkin.
- **Bo'shliq:** Core tomonida PRICE_UPDATED consumer va uni Pipeline
  triggeriga bog'lash mantig'i YO'Q. Buni qurish — Pipeline'ni
  event-driven qilish = **yangi arxitektura/wiring qarori**.

## Determinatsiya: REUSE-mumkinmi yoki DRQ?

Infratuzilma (EventBus) REUSE-mumkin, ammo **Core'ni event consumeriga
aylantirish yangi wiring** — Trading-Safety'ga tegadi (pipeline trigger
mexanizmi o'zgaradi). → **DRQ** (16_ — Event Bus → Core). Bu passda
WIRE QILINMAYDI.
