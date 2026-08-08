# 05 — Event Bus

## Publish — HAQIQIY

Har tick `PriceCache` ga tushgach `_PriceTickSink.on_event`
`EventBus.publish(Event(type=EventType.PRICE_UPDATED, payload=PriceTick, ...))`
ni chaqiradi. Bu o'zgarmagan, ishlaydigan yo'l; REAL-DATA-008 uni
o'zgartirmaydi — endi payload haqiqiy joriy narxni olib yuradi.

Probe `PRICE_UPDATED` ga probe-tomon hisoblagich obuna bo'lib, har
yangilanishda event chiqqanini (`event_published=YES`) qayd etadi. Bu
FAQAT verifikatsiya instrumenti — production consumer emas.

## Event Bus → Core — WIRED EMAS (doiradan tashqari)

Core (TradingPipeline) `PRICE_UPDATED` ga obuna BO'LMAYDI — u Market
Memory ni jadval bo'yicha o'qiydi (REAL-DATA-003). REAL-DATA-008
`PRICE_UPDATED` consumer ni Core'ga ulamaydi — bu ataylab doiradan
tashqarida. Holat: **NOT WIRED (out of scope)**.
