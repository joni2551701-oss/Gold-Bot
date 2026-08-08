# REAL-DATA-007 — 08. Event Bus Verification

## Publish yo'li: REAL
`data_layer/live_data/price_stream_service/price_stream_service.py`:
- `from data_layer.event_system.event_bus import EventBus` (:58).
- `_PriceTickSink` `event_bus` ni ushlaydi (:79-82).
- Yangi tick'da: `self._event_bus.publish(Event(...))` (:94-95) —
  `PRICE.UPDATED` / `PRICE_UPDATED` payload=`PriceTick`
  (symbol/price/timestamp). Publish REAL.

## Event Bus → Core: **NOT WIRED**
REAL-DATA-006 07 (`07_EVENT_BUS_TO_CORE.md`) tasdiqlagan:
- `EventType.PRICE_UPDATED`ga **birorta ham `.subscribe()` YO'Q** (data
  layer event bus'ida subscriber mavjud emas).
- Core (`TradingPipeline`) data-layer event bus'iga subscribe QILMAYDI —
  u Market Memory'ni jadval bo'yicha (batch) o'qiydi.
- AI layer'dagi subscribe'lar butunlay boshqa bus va boshqa event turlari.

## Xulosa
Publish tomoni real va ishlaydi, lekin **Event Bus → Core simlanmagan
(NOT WIRED)**: PRICE_UPDATED event'ini hech kim iste'mol qilmaydi. Bu
Foundation holati — REAL-DATA-006 bilan mos. (Core'ni Event Bus'ga
simlash — REAL-DATA-007 doirasidan tashqari, TAQIQLANGAN.)
