# 08 — Real Price Evidence

## STATUS: BLOCKED

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
