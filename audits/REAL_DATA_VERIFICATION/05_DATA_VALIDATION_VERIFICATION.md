# 05 — Data Validation Verification

Validator: `MarketDataNormalizer._validate_and_clean()`
(`data_layer/live_data/market_data/market_data.py:41-56`), production
yo'lida `get_candles()` (satr 106-111) tomonidan **har bir** chaqiruvda
avtomatik ishga tushiriladi — tashqi provayder javobi to'g'ridan-to'g'ri
chaqiruvchiga qaytmaydi.

## CONFIRMED tekshiruvlar (kod, `market_data.py:41-56`)

1. **Manfiy/nol narx** — `c.open <= 0 or c.high <= 0 or c.low <= 0 or
   c.close <= 0` bo'lsa candle **tashlab yuboriladi** (satr 47-48).
2. **OHLC geometrik nomuvofiqlik** — `(c.high < c.low) or (c.high <
   max(c.open, c.close)) or (c.low > min(c.open, c.close))` bo'lsa
   tashlab yuboriladi (satr 49-50).
3. **Dublikat timestamp** — `seen_timestamps` set orqali, takroriy
   `c.timestamp` tashlab yuboriladi (satr 51-54).
4. **Majburiy maydonlar** — dataclass darajasida (`Candle`,
   `twelve_data_client.py:11-19`) `timestamp/open/high/low/close`
   majburiy; ular yo'q bo'lsa parsing bosqichidayoq (`float(v["open"])`
   va h.k., `twelve_data_client.py:112-116`) `KeyError`/`ValueError`
   chiqadi — bu holat `TwelveDataClient.fetch_candles()`ning try/except
   zanjiriga tushmaydi (faqat `requests.exceptions.RequestException`
   ushlanadi), shuning uchun bunday xato **pastga tarqaladi** (aniq
   qayd etilishi kerak bo'lgan gap — quyidagi "Topilmalar" bo'limiga
   qarang).
5. **Simvol/timeframe** — validatsiya darajasida alohida tekshirilmaydi
   (chaqiruvchi tomonidan allaqachon belgilangan parametr sifatida
   qabul qilinadi); ammo `_verify_timeframe_alignment()` (satr 86-104)
   turli timeframe'lar orasidagi **desync**ni tekshiradi (masalan H4
   snapshot boshqalardan 4 soatdan ortiq orqada qolsa, `logger.warning`
   — filtermaydi, faqat ogohlantiradi).
6. **Eskirgan (stale) ma'lumot / yetishmayotgan candle** —
   `_detect_missing_candles()` (satr 59-83): kutilgan interval bilan
   solishtirib, kun ichidagi (`< 1 kun`) kutilmagan gapni aniqlaydi,
   `logger.warning` chiqaradi — **filtrламайди**, faqat log yozadi
   (return qiymati `bool`, chaqiruvchi tomonidan hozircha
   ishlatilmaydi — `get_candles()` uni chaqirmaydi, faqat
   `get_snapshot()` docstring darajasida eslatiladi; amalda
   `get_candles()` bu funksiyani chaqirmaydi — quyida aniqlashtirilgan).

## Topilma: `_detect_missing_candles()` va `_verify_timeframe_alignment()` chaqirilishi

`get_candles()` (`market_data.py:106-121`) faqat `_validate_and_clean()`ni
chaqiradi; `_detect_missing_candles()` chaqirilmaydi. `get_snapshot()`
(satr 123+, fayl davomida) — ehtimol ikkalasini ham chaqiradi (bu
hujjat doirasida to'liq satr raqami bilan tasdiqlash uchun qo'shimcha
o'qish talab etiladi — hozirgi audit faqat `get_candles()`ning asosiy
yo'lini sinchiklab tekshirdi, chunki bu `TradingPipeline.run()` har
sikl chaqiradigan aniq yo'l). Bu — kelgusi chuqurroq audit uchun ochiq
band sifatida qayd etiladi, yangi kod yozilmadi.

## Market Memory'ga yozilishdan oldin validatsiya bormi?

Ha — `MarketDataService.get_candles()` (`market_data_service.py:76-81`)
`self._normalizer.get_candles()`ni chaqiradi (validatsiyadan o'tgan
natija), so'ng shu **tozalangan** ro'yxatni `_hydrate_memory()`ga
uzatadi (satr 80, `06`-hujjatga qarang). Xom (raw) provayder javobi
Market Memory'ga bevosita yozilmaydi.

## BLOCKED

Real provayder javobidagi haqiqiy anomaliya (masalan real API'dan
kelgan noto'g'ri narx)ni amalda ko'rish — tarmoq bloklangani sababli
mumkin emas. Yuqoridagi barcha tekshiruvlar sintetik/kod darajasida
tasdiqlangan, real ma'lumot bilan sinalmagan.
