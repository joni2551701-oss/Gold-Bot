# 12 — Unit Tests Catalogue

## Ijro natijasi (offline, real tarmoqsiz)

Buyruq: `python -m pytest tests/data/providers/ tests/data/stream/ -v`

**Natija: 211 passed** (0 failed, 0 skipped), 7.83 soniyada.

## Muhim ogohlantirish (Order o'zi talab qilgan)

**Ushbu pytest muvaffaqiyati REAL API funksionalligining dalili
EMAS.** Barcha testlar mock/fake provayder yoki oldindan tayyorlangan
test ma'lumotlari (fixture) bilan ishlaydi — hech biri
`api.twelvedata.com`ga haqiqiy tarmoq so'rovi yubormaydi (buni tasdiqlash
uchun `tests/data/stream/test_twelve_data_provider.py` sarlavhasidagi
`TwelveDataProvider` docstring'ining o'zi ochiq yozadi — canonical
manba, `data_layer/live_data/twelve_data_provider/twelve_data_provider.py:11-12`:
*"Not exercised by unit tests (needs a live key); the state machine is
tested against a fake provider."*).

## Klassifikatsiya (Order'ning Mock-vs-Real jadvaliga ko'ra)

| Toifa | Misollar | Turi |
|---|---|---|
| Unit (mock/test data) | `test_twelve_data_provider.py::test_read_converts_latest_candle_to_event`, `test_bitget_provider.py` (barchasi) | Mock — fake client/provider |
| Integration (contract, real tarmoqsiz) | `test_price_stream_service.py::test_tick_folds_into_market_memory_via_candle_builder`, `test_stream_integration.py::test_stream_builds_candles_into_memory` | Real ichki komponentlar orasidagi integratsiya, lekin tashqi tarmoq yo'q |
| Production Probe (real API talab qiladi) | **Repo'da topilmadi** | Yo'q — kutilganidek, chunki CI muhitida live kredensial/tarmoq yo'q |
| E2E (to'liq zanjir) | `test_stream_manager.py`, `test_price_stream.py` (lifecycle testlari) | Mocklangan provayder javoblari bilan, real emas |

## Xulosa

211 ta test o'tdi — bu kod mantig'ining (validatsiya, state machine,
retry, cache, event) ichki to'g'riligini tasdiqlaydi, lekin **hech
qanday real TwelveData/Bitget API javobini tekshirmaydi**. Bu farq
ushbu hujjatda va 17-hujjatdagi yakuniy xulosada aniq ta'kidlangan.
