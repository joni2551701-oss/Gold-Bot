# 14 — Production Probe

## STATUS: BLOCKED

## Aniq sabab

1. **Tashkilot siyosati taqig'i** — bu sessiyaning tarmoq chiqishi
   (`$HTTPS_PROXY`) orqali `api.twelvedata.com:443`ga `CONNECT`
   urinishi `403` bilan rad etildi (dalil: proxy status
   `recentRelayFailures` yozuvi, timestamp `2026-08-07T23:16:04.493Z`,
   `"detail": "gateway answered 403 to CONNECT (policy denial or
   upstream failure)"`; qo'shimcha to'g'ridan-to'g'ri `curl`
   tasdig'i: `curl: (56) CONNECT tunnel failed, response 403`). Bu
   sessiyaning o'zi tomonidan chetlab o'tilishi mumkin bo'lmagan,
   muhit darajasidagi bloklashdir (`/root/.ccr/README.md`ning o'zi:
   "do not retry organization policy denials").
2. **Kredensial yo'qligi** — `TWELVE_DATA_API_KEY` na
   `os.environ`da, na `core_layer.secrets.Secrets` orqali ushbu
   sessiyada mavjud.

Ikkala sabab birgalikda: hatto tarmoq ochiq bo'lganda ham, kalit
yo'qligi sababli chaqiruv `ValueError("TWELVE_DATA_API_KEY not
configured.")` bilan tugagan bo'lardi (`twelve_data_client.py:75-76`).

## Nima qilinmadi

Hech qanday real yoki simulyatsiya qilingan API javobi ishlab
chiqarilmadi/ko'rsatilmadi. `python main.py`ni to'liq ishga tushirish
ham amalga oshirilmadi, chunki u xuddi shu tarmoq/kredensial
yo'qligiga urinib, ishlab chiqarish holatini noto'g'ri aks ettirgan
bo'lardi (real natija emas — istisno bilan tugaydi va bu "ishlamayapti"
degan noto'g'ri taassurot qoldirishi mumkin, aslida sabab faqat muhit
cheklovi).

## Aniq, amaliy tavsiya

Ushbu tekshiruv **VPS'ning o'zida** (yoki boshqa real kredensial +
ochiq egress'li muhitda) quyidagi qadamlar bilan qayta o'tkazilishi
kerak:

1. Production `.env`dagi haqiqiy `TWELVE_DATA_API_KEY` bilan
   `python -c "from data_layer.providers.twelve_data_client import
   TwelveDataClient; print(TwelveDataClient().fetch_candles('XAUUSD',
   'M15', 5))"` ishga tushirish — real 5ta M15 candle qaytishini
   tasdiqlash.
2. `python main.py`ni bitta sikl uchun ishga tushirish, log
   chiqishida haqiqiy narx/signal ko'rinishini kuzatish.
3. Natijani (real candle qiymatlari, timestamp, HTTP status) Final
   Release Audit hujjatiga biriktirish.

Bu tekshiruv **doimiy Final Release Audit / RC1 gate checklist
bandi** sifatida rasmiylashtirilishi tavsiya etiladi — har safar
provider kodiga tegilganda yoki har yangi release oldidan qayta
o'tkaziladigan qadam sifatida.


---

## ⚡ REAL RUN NATIJASI (REAL-DATA-002, 2026-08-08, run 31229724552)

✅ **PASS (REAL, GitHub Actions).** Oldingi BLOCKED (sandbox: egress 403 + key yo'q) hal qilindi. Probe `ci.yml`'ning workflow_dispatch-gated `real_data_probe` job'i orqali ishga tushirildi (run 31229724552, commit e4d18f6). Real credentials + real network + real provider bilan: TwelveData XAU/USD PASS, Bitget BTC/USDT diagnostic PASS, Validation PASS, Market Memory PASS. Skript `scripts/verification/real_market_data_probe.py`.
