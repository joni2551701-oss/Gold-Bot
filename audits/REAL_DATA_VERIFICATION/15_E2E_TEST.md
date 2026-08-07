# 15 — E2E Test

## Repo'dagi mavjud E2E-ga yaqin testlar

`tests/data/stream/test_stream_manager.py`, `test_price_stream.py`,
`test_price_stream_service.py` — Provider (fake) -> Stream -> Cache/Memory/Event
to'liq zanjirini sinaydi, lekin provayder qatlami har doim fake/mock
(masalan `test_price_stream.py::test_provider_agnostic_swap` — turli
fake provayderlarni almashtirib sinash uchun maxsus yozilgan).

`python main.py` darajasidagi haqiqiy end-to-end (Data -> Context ->
Strategy -> Signal -> AI -> Decision -> Risk -> Telegram) test
`tests/`ichida repo bo'ylab boshqa joyларда (masalan
`tests/integration/`) mavjud bo'lishi mumkin, ammo bular ham real
TwelveData tarmog'iga ulanmaydi — pipeline testlari odatda
`MarketDataService`/`MarketDataNormalizer.get_candles`ni monkeypatch
qiladi (`core_layer/pipeline/pipeline.py:214-215` dagi sharh buni
tasdiqlaydi: *"existing tests monkeypatch
pipeline.data_normalizer.get_candles/.get_snapshot directly"*).

## Ushbu sessiyada bajarilgan

`python -m pytest tests/data/providers/ tests/data/stream/ -v` — 211
passed (12-hujjatga qarang). Bu buyurtma tomonidan berilgan aniq
ko'rsatma, va u E2E emas, balki unit+integration darajasi.

To'liq `tests/` to'plami (5490+ test, CLAUDE.md commit protokoliga
ko'ra) commit bosqichida ishga tushiriladi (18-band, quyidagi commit
protokoli bo'limiga qarang).

## Xulosa

Repo'da real tarmoq bilan ishlaydigan E2E test **yo'q** — bu
kutilgan holat, chunki CI muhitida live kredensial mavjud emas. E2E
testlar mocklangan provayder javoblari bilan to'liq zanjirni
tekshiradi, real ma'lumot bilan emas.
