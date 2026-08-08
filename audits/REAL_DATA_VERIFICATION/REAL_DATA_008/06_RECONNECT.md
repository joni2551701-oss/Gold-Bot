# 06 — Qayta ulanish / fail-safe

`TwelveDataPriceSource` stateless HTTP polling: ochiladigan doimiy ulanish
yo'q. `connect()` statusni optimistik UP qiladi; muvaffaqiyatsiz `read()`
xatoni ko'taradi va statusni DOWN qiladi.

Xatolar ikki qatlamda izolyatsiya qilinadi:

1. **Klient qatlami** (`get_price`) — 429/tarmoq xatolarida `fetch_candles()`
   bilan bir xil eksponensial backoff (3 urinish), keyin `ConnectionError`.
2. **Stream qatlami** — `PriceStream` provider xatosini DD-051 bo'yicha
   standart provider-error holatiga izolyatsiya qiladi; bitta manba
   yiqilsa boshqa manbalarga (BTCUSDT) ta'sir qilmaydi.

Lokal probe buni ko'rsatadi: kalit yo'qligida XAUUSD manba
`ValueError: TWELVE_DATA_API_KEY not configured.` bilan izolyatsiya
qilinadi, probe crash bo'lmaydi, BLOCKED (real sabab) qaytaradi.

Keyingi tick avvalgi xatodan mustaqil qayta uriniladi (har `read()`
yangi HTTP so'rov) — de-facto qayta ulanish.
