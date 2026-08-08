# 08 — Arxitektura verifikatsiyasi

## Qatlam chegaralari saqlangan

- Yangi `TwelveDataPriceSource` `data_layer/live_data/` ichida — mavjud
  `PriceProvider` ABC ni amalga oshiradi, `data/` dan yuqori qatlamni
  import qilmaydi.
- Yangi `get_price()` `data_layer/providers/` ichida — sof data fetching,
  tahlil mantiqi yo'q.
- Registratsiya `build_default_price_stream_service()` da — yagona
  sanksiyalangan wiring nuqtasi. Undan yuqori hech narsa o'zgarmaydi
  (DD-048 provider abstraksiyasi).

## Module Reuse Principle

- Mavjud qurilish bloklari qayta ishlatildi: `PriceProvider`, `PriceStream`,
  `PriceStreamService`, `_PriceTickSink`, `PriceCache`, `CandleBuilder`,
  `StreamValidator`, `EventBus`, `MarketMemory`. Yangi stream/provider
  freymvorki yaratilmadi.
- Yangi modul (`TwelveDataPriceSource`) faqat 1 va 2 qadamlar "yo'q"
  bo'lgani uchun yaratildi va docstringda asoslandi. `TwelveDataClient`
  yangi metod bilan kengaytirildi (kontrakt buzilmadi — `fetch_candles`
  o'zgarmagan).

## Trading Safety

- Signal/Risk/Decision/Execution mantig'iga tegilmadi.
- Batch/trading candle yo'li (`MarketDataService.get_candles`,
  `fetch_candles`) o'zgarmagan.
- Bitget inert qoladi (NOT VERIFIED).
- AI to'g'ridan-to'g'ri bajarish yo'q; Event Bus→Core ulanmadi.

## Taqiqlangan narsalar bajarilmadi
M1/M5 workaround yo'q; candle.close jonli narx sifatida yo'q; PriceStreamV2
yo'q; API kalit hech qachon logga chiqmaydi; mock real sifatida taqdim
etilmadi.
