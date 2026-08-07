# 13 — Integration Tests

## Ko'rib chiqilgan fayllar

- `tests/data/stream/test_price_stream_service.py` — Provider ->
  PriceStream -> MarketMemory zanjirini sinaydi
  (`test_tick_folds_into_market_memory_via_candle_builder`,
  `test_memory_write_is_fail_safe_for_cache_and_events`,
  `test_shared_registry_is_single_source_of_truth_for_both_services`)
  — PASSED, lekin provayder qismi **fake/test double**.
- `tests/data/stream/test_stream_integration.py::test_stream_builds_candles_into_memory`
  — stream'dan candle qurish va Memory'ga yozishni sinaydi, real
  tarmoqsiz. PASSED.
- `tests/data/providers/test_data_provider_manager.py`,
  `tests/data/providers/test_registry.py` — `ProviderManager`/`ProviderRegistry`
  tanlash mantig'ini sinaydi, real provayder chaqiruvisiz (fake/stub
  provayderlar bilan). Bu fayllar `pytest tests/data/providers/
  tests/data/stream/` to'plamiga kiradi (12-hujjatdagi 211 natijaga
  qo'shilgan).

## Kontrakt darajasi

Bu testlar **provider integration contract**ni tekshiradi — ya'ni
"agar provayder shunday `Candle`/`MarketCandle` qaytarsa, yuqori
qatlam to'g'ri ishlaydi"mi — lekin hech biri haqiqiy HTTP javobi bilan
ishlamaydi. Bu — Order'ning o'z ta'rifiga mos "Integration (provider
integration contract, still no real network call)" toifasi.

## Xulosa

Integratsiya darajasidagi testlar mavjud va o'tadi, lekin ular ham
real tarmoq bilan bog'liq emas — 12-hujjatdagi bir xil ogohlantirish
shu yerga ham tegishli.
