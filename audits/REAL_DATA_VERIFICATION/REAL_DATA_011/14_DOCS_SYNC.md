# 14 — Docs Sync (REAL-DATA-011, Item N)

Hujjatlarni haqiqiy audit qilingan holatga moslash — aniqlik bilan,
ortiqcha da'vosiz.

## Amalga oshirilgan o'zgarish

- **`docs/PROJECT_STATUS.md`** — yangi "5b. Production Boundary
  (REAL-DATA-011 audited)" bo'limi qo'shildi: data→risk spine PASS,
  Risk'dan keyin NOT WIRED/NOT VERIFIED, execution inert, VPS BLOCKED,
  Daily/HTF non-blocking. Ortiqcha da'vo yo'q.

## Aniqlik uchun qayd etilgan nomuvofiqliklar (kelajakdagi pass uchun)

- **`ARCHITECTURE.md` / CLAUDE.md path'lari** — ba'zi hujjatlar
  `core/pipeline.py`, `risk/`, `signals/`, `strategies/` kabi eski/
  aspirational path'larni ishlatadi; haqiqiy fayllar
  `core_layer/pipeline/pipeline.py`, `risk_layer/risk_engine/…`,
  `platform_layer/telegram/…`. Bu faqat qayd etildi — RC1 oldidan
  keng path-refactor qilinmaydi (minimal-change qoidasi).
- **`docs/GFL-001_FLOW_PROGRESS.md`** — flow holatlari joriy; REAL-DATA
  spine holati REAL_DATA_011 auditida to'liq qamrab olingan, u yerga
  ko'rsatgich yetarli (dublikat status yozilmadi).
- **Test soni** — PROJECT_STATUS.md'da "5432 passed" deb yozilgan;
  joriy baza **5503 passed**. Bu farq keyingi status-yangilashda
  to'g'rilanishi tavsiya etiladi (bu passda faqat qayd etildi, chunki
  u REAL-DATA-011 doirasidan tashqari status-maydon).

## Xulosa

Docs = production boundary bo'yicha SYNC qilindi (PROJECT_STATUS.md).
Qolgan kichik nomuvofiqliklar (path'lar, test soni) qayd etildi,
ortiqcha da'vosiz.
