# REAL-DATA-006 — 04. Stream Validation (StreamValidator behavior)

## Qaysi validator production'da ishlaydi

Production PriceStream (`data_layer/live_data/price_stream/price_stream.py`)
canonical `StreamValidator`ni ishlatadi
(`data_layer/live_data/stream_validator/stream_validator.py`), uni
`build_default_price_stream_service()` (`price_stream_service.py:236,241,245`)
har ikkala source'ga inject qiladi.

## Validation chaqiruv nuqtasi (file:line)

- `price_stream.py:240` — `_forward_ordered` ichida: agar validator
  mavjud bo'lsa va `not self._is_valid(e)` bo'lsa, event **DROP**
  qilinadi (`_stats["dropped_invalid"] += 1`), `_last_ts`/`_last_event`
  yangilanmaydi.
- `price_stream.py:248-255` — `_is_valid()`: `self._validator.validate(
  event, previous=self._last_event)`. Validator xatosi fail-safe —
  `except` bo'lsa `True` qaytaradi (validator hech qachon stream'ni
  bloklamaydi).

## StreamValidator tekshiruvlari (`stream_validator.py:65-112`)

| Tekshiruv | file:line | Kod (invalid) | Xulq |
|---|---|---|---|
| empty (None event) | `:73-74` | `code="empty"` | DROP |
| empty (asset yoki timestamp yo'q) | `:75-76` | `code="empty"` | DROP |
| symbol mismatch | `:79-82` | `code="asset"` | DROP — **lekin production'da `expected_asset` UZATILMAYDI** (pastga qarang) |
| price None/non-finite | `:86-87` | `code="price"` | DROP |
| price ≤ 0 (invalid price<=0) | `:88-89` | `code="price"` | DROP ✓ |
| negative volume | `:90-91` | `code="price"` | DROP |
| future timestamp (>5 min skew) | `:94-99` | `code="timestamp"` | DROP ✓ |
| duplicate (bir xil timestamp) | `:107-108` | `code="duplicate"` | DROP ✓ |
| out-of-sequence (eski timestamp) | `:109-110` | `code="sequence"` | DROP ✓ |

`_FUTURE_TOLERANCE = 5 min` (`:57`).

## Topilma: symbol-mismatch production'da faol emas

`price_stream.py:250` `validate(event, previous=self._last_event)`ni
`expected_asset` argumentisiz chaqiradi. Validator symbol-mismatch
tekshiruvini qo'llab-quvvatlaydi (`:79-82`), lekin production stream uni
uzatmagani uchun bu tekshiruv **production'da faol emas**. Bu
mavjud xulq (existing behavior) — yangi validation QO'SHILMADI, faqat
qayd etiladi.

Qo'shimcha: `TwelveDataProvider.read()` o'zi ham `_last_ts` bo'yicha
dedupe qiladi (`twelve_data_provider.py:76-79`) — faqat yangiroq candle
close chiqqanda emit qiladi; `PriceStream._forward_ordered` esa
strictly-older event'larni tashlaydi (`price_stream.py:232-234`,
`dropped_out_of_order`). Demak duplicate/stale ikki qatlamda ushlanadi.

## Status: **PASS (existing validator, real drop-on-invalid)**

Validation kodi real va production PriceStream'ga wire qilingan.
Invalid price ≤ 0, future timestamp, duplicate, out-of-sequence
hammasi dropga olib keladi. Real oqim orqali empirik tasdiq CI
probe'dan keladi (M1 mismatch tuzatilmaguncha 0 real event — 03/08 ga
qarang).
