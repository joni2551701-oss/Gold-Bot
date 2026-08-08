# 16 — DRQ — Event Bus → Core (REAL-DATA-011)

**DRQ turi:** Director Review Question / wiring decision.
**Holat:** NOT WIRED. Bu passda WIRE QILINMADI.

## Bir jumlalik so'rov

Director ruxsat beradimi — `TradingPipeline`ni `PRICE_UPDATED`
event'iga subscribe qilib, price stream'dan event-driven trigger
qilishga (hozir Pipeline MarketMemory SSOT'dan batch o'qiydi)?

## Kontekst

- Publish REAL: `price_stream_service.py:95-96` real `PRICE_UPDATED`
  event chiqaradi.
- Consumer: Core subscribe QILMAYDI. Yagona subscriber — verification
  probe (`real_price_stream_probe.py:145`).
- EventBus infratuzilmasi REUSE-mumkin
  (`data_layer/event_system/event_bus/event_bus.py`), boshqa event
  turlarida faol ishlatiladi.

## Nega DRQ (nega Worker wire qilmaydi)

Core'ni event-driven qilish pipeline trigger mexanizmini o'zgartiradi
— bu Trading-Safety va Pipeline contract'iga tegadi
(`CLAUDE.md`: Pipeline flow "must keep working exactly as
documented"). Yangi wiring = Director qarori.

## Tavsiya

Agar kerak bo'lsa — RFC (`RFC_STANDARD.md`) + ADR
(`ADR_STANDARD.md`) orqali "Event-Driven Pipeline Trigger" sifatida
rasmiylashtirish. Aks holda joriy SSOT-pull yo'li WORKING, KEEP.
