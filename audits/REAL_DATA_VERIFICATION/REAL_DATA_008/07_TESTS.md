# 07 — Testlar

Baseline: **5493** test. Yangi jami: **5503** (5493 + 10).

## Qo'shilgan testlar (10 ta)

### `tests/data/providers/test_twelve_data_client_get_price.py` (5)
- `test_get_price_success_returns_float` — `/price` (PRICE_URL, BASE_URL emas)
  chaqiriladi, `XAUUSD`→`XAU/USD`, `{"price":"2412.34"}` → `2412.34` float,
  candle params yo'q.
- `test_get_price_api_error_body_raises` — `{"status":"error"}` → `ValueError`.
- `test_get_price_missing_key_raises` — kalit yo'q → `ValueError(...not
  configured)`.
- `test_get_price_none_price_returns_none` — `price` maydoni yo'q → `None`.
- `test_get_price_network_error_raises_connection_error` — tarmoq xatosi →
  `ConnectionError` (backoff sleep mock qilingan).

### `tests/data/stream/test_twelve_data_price_source.py` (5)
- `test_capabilities_declared_polling_not_streaming` — polling=True,
  streaming=False.
- `test_connect_disconnect_status` — DOWN→UP→DOWN.
- `test_read_returns_current_price_event_with_observation_timestamp` —
  `read()` real joriy narxli `StreamEvent`, kuzatuv timestampi (before≤ts≤after),
  `source=STREAM`, `get_price` chaqiriladi.
- `test_read_empty_when_no_price` — narx `None` → `[]`.
- `test_read_does_not_dedupe_repeated_price` — takror narx ham yaroqli tick.

## Natija
`python -m pytest tests/` → **5503 passed**. Hech bir mavjud test buzilmadi
(hech qaysi test eski candle STREAM manbasining XAUUSD turini qat'iy
tekshirmagan edi — swap xavfsiz).
