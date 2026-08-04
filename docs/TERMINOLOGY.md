# TERMINOLOGY.md — GoldBot yagona texnik lug'ati

Bu fayl GLS-001 Translation Standard doirasida ishlatiladigan yagona
lug'at. Qoida oddiy: **faqat `.md` hujjat matni tarjima qilinadi —
gap O'zbek tilida yoziladi, lekin texnik terminlar asl inglizcha
ko'rinishida qoladi.** Texnik terminlarni alohida tarjima qilish
shart emas — ular har doim ingliz tilida qoladi, hech qanday O'zbek
muqobili qidirilmaydi.

## Tarjima qilinadi (faqat bular)

Hujjat matni, izohlar, tavsiflar, hisobotlar, auditlar, xulosalar,
kod bo'lmagan misollar — oddiy prozaik so'zlar/gaplar. Masalan:

| English | O'zbek |
|---|---|
| Problem | Muammo |
| Cause / Root Cause | Sabab / Ildiz sabab |
| Solution | Yechim |
| Recommendation | Tavsiya |
| Impact | Ta'sir |
| Lessons Learned | O'rganilgan saboqlar |

Bu jadval ham to'liq emas — yangi prozaik so'z topilganda shu yerga
qo'shiladi, mavjud tarjima o'zgartirilmaydi.

## Tarjima qilinmaydi (har doim ingliz tilida qoladi)

- `.py` fayl nomlari, Package nomlari, Module nomlari, Class nomlari,
  Function nomlari, Variable nomlari
- API nomlari, Framework nomlari, Kutubxona nomlari
- Kod bloklari, diagrammadagi identifikatorlar
- Git commit va Branch nomlari
- RFC, ADR, DD, GDS, GEL, GLS identifikatorlari
- **Texnik terminlar** — bularning O'zbekcha muqobili yozilmaydi,
  gap ichida original inglizcha shaklida qoladi: `Layer`, `Module`,
  `Package`, `Pipeline`, `Event Bus`, `Compatibility`, `Exception`,
  `Violation`, `Dependency`, `Contract`, `Validation`, `Rollback`,
  `Refactor`, `Regression`, `Unit Test`, `Integration Test`, `Mock`,
  `Fixture`, `Documentation`, `Implementation`, `Roadmap`,
  `Changelog`, `Work Log`, `Architecture`, `Ownership`,
  `Foundation Rule`, `Compliance`, `Investigation`, `Release`,
  `Sprint`, `Backlog`, `Technical Debt`, `Deprecated`, `Active`,
  `Resolved`, `Stable`, `Blueprint`, `Health Score`,
  `Maintainability`, `Performance`, `Security`, `Status`, `Evidence`,
  `Confidence`, `Risk`, `Audit`, `Report`, `Registry`, `Lifecycle`,
  `Workflow`, `Empirical Verification` — ro'yxat to'liq emas, har
  qanday texnik/dasturlash termini shu qoidaga tushadi.

## Misol

❌ Noto'g'ri: `Layer → Qatlam`, `Package → Paket`, `Pipeline → Quvur`

✅ To'g'ri:

```
Muammo

Module ichidagi Package noto'g'ri Dependency ishlatyapti.

Sabab

Pipeline Contract buzilgan.

Yechim

Compatibility tekshirildi va Validation muvaffaqiyatli yakunlandi.
```

Gap O'zbek tilida, texnik terminlar original inglizcha shaklida.
