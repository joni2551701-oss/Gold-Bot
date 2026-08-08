# 13 — Dead / Duplicate Classification (REAL-DATA-011, Item M)

Repo-wide tasnif — real import grafi + consumer trace orqali (nom
bo'yicha EMAS).

## Metodologiya

Har nomzod uchun 5 shartli airtight-proof qo'llandi: (1) production
consumer yo'q (grep butun repo, main.py, polling.py, workflows),
(2) test reference yo'q, (3) migration/compat ehtiyoji yo'q,
(4) Foundation Freeze contract'ini buzmaydi, (5) o'chirilgach
pytest+compileall+main.py yashil qoladi. Bitta shubha bo'lsa —
O'CHIRILMAYDI, classify-and-defer.

## Topilmalar

| Nomzod | Tasnif | Airtight-orphanmi? | Qaror |
|---|---|---|---|
| `live_data/twelve_data_provider` `TwelveDataProvider` (eski M1 stream) | TEST-ONLY | YO'Q (test bor — shart 2 buziladi) | CLASSIFY-AND-DEFER, tavsiya (03_) |
| Bitget provider'lar | FOUNDATION | YO'Q (registry, Director inert qarori) | KEEP |
| `execution_layer/` skeletonlari | FOUNDATION | YO'Q (Foundation Freeze) | KEEP |
| `binance_provider` | FOUNDATION | YO'Q (registry) | KEEP |
| `keynorq_provider` | FOUNDATION | YO'Q (registry) | KEEP |

## Xulosa

**O'chirish uchun airtight-orphan item TOPILMADI.** Har bir "o'lik
ko'rinishli" modulning yo test reference'i, yo registry ro'yxati, yo
Foundation Freeze contract'i bor. Shuning uchun **bu passda hech
qanday kod o'chirilmaydi.** Eski M1 stream sinfi keyingi ko'rib
chiqilgan pass uchun removal-tavsiya sifatida qayd etildi.

Bu **RC1 oldidan xavfsizlikni** ta'minlaydi (guardrail: "Deleting
code right before RC1 is high-risk").
