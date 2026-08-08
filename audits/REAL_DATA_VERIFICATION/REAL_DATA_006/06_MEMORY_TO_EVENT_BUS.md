# REAL-DATA-006 — 06. Event Bus publish (PRICE_UPDATED)

## Transition

- **Input:** validated `StreamEvent` → `PriceTick`
  (`price_stream_service.py:86-92`).
- **Processing:** `_PriceTickSink.on_event()` `price_stream_service.py:94-102`
  — `self._event_bus.publish(Event(...))` (agar `_event_bus` mavjud bo'lsa).
- **Output:** `data_layer.event_system.event_bus.EventBus` ga
  `EventType.PRICE_UPDATED` event.
- **NextConsumer:** hech kim (07 ga qarang — NOT WIRED).

## Event payload (file:line)

`price_stream_service.py:95-102`:

```
Event(
    type=EventType.PRICE_UPDATED,          # "PRICE.UPDATED", event_model.py:50
    payload=tick,                          # PriceTick
    asset=tick.symbol,
    event_id=f"price-{tick.symbol}-{tick.timestamp.timestamp()}",
    timestamp=datetime.now(timezone.utc),
    source="PriceStreamService",
)
```

`PriceTick` (`price_stream_service.py:86-92`) maydonlari: `symbol`,
`price`, `timestamp`, `provider`, `volume` — ya'ni payload symbol +
price + timestamp'ga ega (order talabi tasdiqlandi).

## EventBus mexanikasi

- `EventBus` klassi: `data_layer/event_system/event_bus/event_bus.py:56`.
- `publish()`: `:115`. `subscribe()`: `:78`.

Publish real va production-wired (sink har validated tick'da chaqiradi,
tick esa `polling.py:308` orqali haydaladi).

## Status: **PASS (publish REAL va production-wired)**

`PRICE_UPDATED` event real chiqariladi — payload to'liq (symbol/price/
timestamp). Bu Foundation emas: sink production kod, tick production
driver. **Ammo** event iste'molchisi yo'q (07). Va 03-fayldagi M1
mismatch tufayli XAUUSD uchun amalda hech qanday event chiqmaydi
(publish faqat validated tick bo'lganda; tick esa tushmaydi). Kod
PASS, runtime dalil CI probe'ga bog'liq.
