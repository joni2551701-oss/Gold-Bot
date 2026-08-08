# REAL-DATA-007 — 12. Release Gate Verdict

## VERDIKT: **DIRECTOR REVIEW** (chinakam current-price stream uchun BLOCKED)

## Asos
GoldBot Price Stream = **candle-API polling** (TwelveData `/time_series`,
bitta candle, yangi candle yopilganda emit). Bu chinakam current-price /
real-time tick oqimi EMAS. Repoda current-price/quote kontrakti MAVJUD
EMAS. Price Stream'ni chinakam real-time oqimga aylantirish YANGI provayder
API arxitekturasini talab qiladi (TwelveDataClient `/price` yoki `/quote`
metodi + current-price PriceProvider). Bu — Direktor qarori, Worker
qarori emas (CLAUDE.md Trading Safety / section 16/18).

REAL-DATA-006 M1 xatosi (CI run 31251456946: 3 tick, 0 update,
`ValueError`) shu kontrakt bo'shlig'ining alomati. To'g'ri yechim M1→M5
EMAS.

## Direktor uchun variantlar (DRQ-001 format — amalga oshirilmagan)

### Variant A — Chinakam current-price kontraktini qurish
Amalga oshirish: `TwelveDataClient.get_price()` (`/price` yoki `/quote`) +
`CurrentPricePriceProvider` manbai qo'shish, XAUUSD'ni unga ro'yxatga
olish → chinakam real-time oqim.
- **Pros**: Price Stream nomiga mos chinakam current-price oqimi bo'ladi;
  tick-darajali yangilanish; current-price feature'lar to'g'ri ishlaydi.
- **Cons**: Yangi API arxitekturasi (yangi client metodi + yangi provider);
  yangi endpoint API kvotasini iste'mol qiladi; yangi test/validatsiya
  yuki; Trading Safety review talab qiladi.
- **Risk**: O'RTA-YUQORI — yangi tashqi API kontrakti, yangi failure
  yo'llari, Foundation Freeze'dan chiqish.

### Variant B — Candle-close polling ekanini tan olib, halol qayta nomlash
Amalga oshirish: manbani ochiqchasiga "CandleClosePollingSource" deb qayta
nomlash/hujjatlash; faqat interval'ni qo'llab-quvvatlanadigan candle TF'ga
(M5) tuzatish; bu tick-darajali emasligini halol qayd etish.
- **Pros**: Kichik o'zgarish; halol nomlash; M1 xatosi yo'qoladi;
  yangi API yo'q.
- **Cons**: Baribir current-price oqimi bo'lmaydi (5 daqiqalik candle
  yangilanishi); "Price Stream" nomidan voz kechish kerak; kutgan
  real-time consumer'lar qoniqmaydi.
- **Risk**: PAST-O'RTA — production wiring o'zgarishi (interval), lekin
  arxitektura yangiligi yo'q.

### Variant C — Kechiktirish (defer)
Amalga oshirish: hech narsa qo'shmaslik. Trading pipeline batch
MarketDataService (M15) yo'lidan foydalanadi (REAL-DATA-003/004'da
isbotlangan) va stream'ga muhtoj emas; stream'ni hujjatlashtirilgan-buzilgan
Foundation sifatida qoldirish — real-time consumer paydo bo'lguncha.
- **Pros**: Nol risk; pipeline allaqachon ishlaydi; Foundation Freeze
  saqlanadi; Direktor keyinroq A yoki B'ni tanlashi mumkin.
- **Cons**: Price Stream buzilgan/adashtiruvchi holatda qoladi; M1 xatosi
  va stale docstring saqlanadi (hujjatlangan bo'lsa ham).
- **Risk**: PAST — texnik qarz sifatida qayd etiladi.

## Worker tavsiyasi (qaror EMAS)
**Variant C (kechiktirish) + hujjat halolligini yaxshilash.** Sabab:
trading pipeline stream'ga muhtoj emas (batch M15 yo'li isbotlangan), real
current-price consumer hozircha yo'q, shuning uchun Variant A'ning API/risk
xarajati hozir oqlanmaydi. Agar real-time consumer paydo bo'lsa — Variant A.
Agar oraliq halol yechim kerak bo'lsa — Variant B. Yakuniy arxitektura
qarorini Direktor qiladi (section 16/18) — Worker amalga oshirmaydi.

## Yakuniy holat
- Current-price kontrakti: **MAVJUD EMAS**.
- Price Stream: **candle-API polling** (real-time emas).
- Verdikt: **DIRECTOR REVIEW**.
