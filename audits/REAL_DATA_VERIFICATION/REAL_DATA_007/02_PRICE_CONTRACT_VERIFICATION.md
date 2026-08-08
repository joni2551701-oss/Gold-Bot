# REAL-DATA-007 — 02. Price Contract Verification (Markaziy javob)

## Markaziy savol
"GoldBot Price Stream chinakam current real-time narx oqimimi, yoki
candle-API polling'ni Price Stream deb qayta nomlangan holimi?"

## Javob: **CANDLE-API POLLING** (current-price oqimi EMAS)

## Kontrakt farqi: PriceUpdate (tick/quote) vs Candle (OHLC)

| Xususiyat | Chinakam current-price oqimi | GoldBot'da amalda bor narsa |
|---|---|---|
| Manba endpoint | `/price` yoki `/quote` (real-time) | `/time_series` (candle) — `twelve_data_client.py:28` |
| Yangilanish birligi | har bir kotirovka (tick/quote) | yopilgan candle close — `twelve_data_provider.py:83` |
| Yangilanish chastotasi | uzluksiz (soniyalar/tiklar) | candle TF bo'yicha (M5=5 daqiqa) |
| Emit sharti | yangi narx keldi | yangi candle YOPILDI — dedupe `:77-78` |
| Kechikish (latency) | ~real-time | candle TF gacha eskirgan |
| Model | `PriceUpdate`/quote | `Candle.close` `StreamEvent`ga o'ralgan |

## Kod dalili
- `TwelveDataProvider.read()` (`twelve_data_provider.py:67-88`):
  `fetch_candles(..., outputsize=1)` → `StreamEvent(price=candle.close)`.
- `CurrentPrice` docstring (`current_price_provider.py:41-43`) ochiq
  tan oladi: *"price is the last **closed** candle's close; timestamp is
  when that candle closed — the same value a signal for that candle would
  have used."* Ya'ni current-price emas, oxirgi yopilgan candle.
- `PriceStreamService` docstring (`price_stream_service.py`) — service
  `get_price()` "single-tick, read-only cache lookup" — bu ham candle
  close'ni qaytaradi, tick emas.

## Nima UCHUN bu current-price emas
1. Candle faqat TF oxirida yopiladi → narx TF davomida "muzlagan" bo'lib
   ko'rinadi (M5'da 5 daqiqa bir xil narx).
2. Dedupe (`:77-78`) yangi candle bo'lmaguncha hech narsa emit qilmaydi —
   real-time narxda bunday to'siq bo'lmaydi.
3. Chinakam current-price uchun `/price`/`/quote` kontrakti kerak — repoda
   YO'Q (`03_TWELVEDATA_STREAM_VERIFICATION.md`).

## Current-price kontrakti holati: **MAVJUD EMAS (DOES NOT EXIST)**
Reponing TwelveData amalga oshirilishida current-price/quote metodi yo'q.
Uni qo'shish yangi provayder API arxitekturasi — Direktor qarori
(`12_RELEASE_GATE_VERDICT.md`).
