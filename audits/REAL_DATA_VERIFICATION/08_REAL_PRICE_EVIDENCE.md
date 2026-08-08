# 08 — Real Price Evidence

## STATUS: ✅ PRESENT (REAL) — GitHub Actions'da olindi (REAL-DATA-002)

**Yangilash (2026-08-08, REAL-DATA-002):** quyidagi BLOCKED holati
GitHub Actions muhitida real API bilan **hal qilindi**. Real dalil
`ci.yml`'ning `real_data_probe` job'i orqali, real GitHub Secrets va
ochiq tarmoq egress bilan olingan.

- **Workflow run:** `31229724552`, job `real_data_probe` (`93031001954`),
  branch `goldbot-v1`, commit `e4d18f6`.
- **Skript:** `scripts/verification/real_market_data_probe.py`.

```
Provider:    TwelveData
Instrument:  XAU/USD
HTTP Status: 200 (SUCCESS)
Price:       4342.34099
Timestamp:   2026-08-08T10:15:00+00:00
Manba:       real TwelveDataClient (production hot-path class)
Probe:       SUCCESS (REAL)
```

```
Provider:    Bitget (public spot ticker, diagnostic)
Instrument:  BTC/USDT
HTTP Status: 200
Price:       64870.01
Timestamp:   1786148320401 (ms epoch)
Manba:       https://api.bitget.com/api/v2/spot/market/tickers (auth yo'q)
Probe:       SUCCESS (REAL, diagnostic-only)
```

**Muhim ajratish (Order section 7):** Bitget diagnostic PASS =
Bitget API real BTC/USDT narx qaytaradi. Bu Bitget'ning GoldBot
production pipeline'da ishlatilishini **isbotlamaydi** —
`BitgetProvider` ataylab inert stub (`NotImplementedError`), shuning
uchun Bitget **production-path = NOT_VERIFIED** (03-hujjatga qarang).
GoldBot faqat XAUUSD savdo qiladi; Bitget/crypto arxitektura jihatidan
signal yo'lida ishlatilmaydi.

Narxlar hardcode qilinmadi, mock ishlatilmadi — barchasi real API
response'idan. API key hech qayerda ko'rsatilmadi (GitHub secret
masking `***`; skript faqat narx/timestamp/status chiqaradi).

---

## Tarixiy yozuv — oldingi sandbox BLOCKED holati (saqlanadi)

## STATUS: BLOCKED (sandbox, superseded above)

Sabab (aniq, ikki qism):

1. **Tarmoq siyosati bloki** — `curl -sS -m 8
   https://api.twelvedata.com/time_series` -> `curl: (56) CONNECT
   tunnel failed, response 403`. Proxy status
   (`$HTTPS_PROXY/__agentproxy/status`) `recentRelayFailures`
   ro'yxatida aniq qayd etilgan: `"kind": "connect_rejected", "detail":
   "gateway answered 403 to CONNECT (policy denial or upstream
   failure)", "host": "api.twelvedata.com:443"`. Bu — tashkilot
   siyosati taqig'i, avtorizatsiya xatosi emas.
2. **Kredensial yo'qligi** — bu sessiyada `TWELVE_DATA_API_KEY` na
   `os.environ`da, na `core_layer.secrets.Secrets` orqali mavjud emas
   (loyiha topshirig'ida tasdiqlangan holat).

## Nima qilinmadi (va nima uchun)

Hech qanday narx, timestamp yoki bid/ask qiymati **o'ylab
topilmadi, taxmin qilinmadi yoki simulyatsiya qilinmadi**. Buyurtma
buni aniq taqiqlaydi ("Mock response'ni real response deb ko'rsatish"
— bu yerda mock ham yaratilmadi, chunki hatto mock ham "real" deb
noto'g'ri taqdim etilishi mumkin edi). Buning o'rniga ushbu hujjat
faqat blok sababini hujjatlashtiradi.

## Tavsiya

Ushbu tekshiruv real muhitda — **VPS'ning o'zida**, real
`TWELVE_DATA_API_KEY` va ochiq tarmoq egress bilan — Final Release
Audit / RC1 gate bosqichining majburiy qadami sifatida qayta
o'tkazilishi kerak, VPS Deployment'dan OLDIN. 14-hujjat
("Production Probe") shu tavsiyani batafsil beradi.
