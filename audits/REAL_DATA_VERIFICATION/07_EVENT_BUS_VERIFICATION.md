# 07 — Event Bus Verification

## CONFIRMED: real EventBus mavjud

`data_layer/event_system/event_bus/event_bus.py:EventBus` — real,
ishlaydigan `publish`/`publish_async`/`subscribe`/`unsubscribe` amalga
oshirilgan (sync + bounded priority queue asinxron, satr 56-185
atrofida), test bilan qoplangan (`tests/data/events/test_event_bus_async.py`).

## CONFIRMED: kim publish qiladi

`data_layer/event_system/` ichida foydalanuvchilar: `data_layer/snapshots/manager/manager.py`,
`data_layer/live_data/candle_builder/candle_builder.py`,
`data_layer/live_data/price_stream_service/price_stream_service.py`
(`test_publishes_price_updated_event` PASSED — 12-hujjat), va
`data_layer/event_system/producer_bridges/producer_bridges.py`
(provayder hodisalarini EventBus formatiga ko'prik qiladigan modul).

## MUHIM TOPILMA: Core buni iste'mol qilmaydi

`core_layer/pipeline/pipeline.py`ning to'liq import ro'yxati (fayl
boshi, 1-28 qatorlar) `data_layer.event_system`ga hech qanday
importni o'z ichiga olmaydi. `TradingPipeline` EventBus'ga obuna
bo'lmaydi, undan hech narsa o'qimaydi. Demak Event Bus — **Foundation
darajasida real, lekin Core tomonidan iste'mol qilinmaydigan**
komponent, xuddi order o'zi taxmin qilganidek ("matches this repo's
established pattern of some Foundation pieces existing but not live").

## Xulosa

Event Bus diagrammasi arxitektura hujjatlarida ko'rsatilgan bo'lishi
mumkin, ammo amalda u faqat `data_layer` ichidagi ikkinchi darajali
oqim (`PriceStreamService`/`candle_builder`) uchun ishlaydi — asosiy
signal generatsiya yo'lining (`TradingPipeline.run()`) bir qismi emas.
