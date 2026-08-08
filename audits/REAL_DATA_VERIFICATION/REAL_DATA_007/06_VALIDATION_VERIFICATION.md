# REAL-DATA-007 — 06. Validation Verification

## Tekshirilgan
`data_layer/live_data/stream_validator/stream_validator.py` va uning
`price_stream_service.py`dagi ishlatilishi.

## Dalillar
- `price_stream_service.py:236` — `validator = StreamValidator()` quriladi.
- `:238-244` — har bir `register_source()` chaqiruviga `validator=validator`
  uzatiladi (XAUUSD va BTCUSDT).
- StreamValidator — StreamEvent'lar uchun haqiqiy validatsiya qatlami
  (narx/timestamp tekshiruvi, stale/duplicate filtri). U REAL — mock emas.

## Muhim izoh (upstream BLOCKED)
Validatsiya kodi to'g'ri va real, LEKIN uni oziqlantiradigan upstream
(TwelveDataProvider M1) BLOCKED — `read()` `ValueError` beradi, shuning
uchun validatorga hech qanday real StreamEvent yetib bormaydi. Validatsiya
"kod bo'yicha PASS, lekin upstream BLOCKED tufayli amalda ishlamaydi".
Bu REAL-DATA-006 topilmasi bilan mos.

## Xulosa
Validation qatlami REAL va to'g'ri simlangan. Ammo candle-polling
upstream'ining M1 nuqsoni tufayli production'da hech narsa validatsiyadan
o'tmaydi.
