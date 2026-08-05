# GEL-001 — Canonical Module = Package Standard

Status: Canonical
Version: 1.0
Trigger: PHASE-01 Foundation Completion Task (Director qarori —
PHASE-01 SHARTLI APPROVED). Bu master hujjat ilgari faqat inline
qoida sifatida (`GFL-001_FLOW_FIRST_STANDARD.md` va
`GFL-001_FLOW_CATALOG.md` da "GEL-001 Strict") havola qilingan
tamoyilga yagona canonical anchor beradi. Reuse First: yangi qoida
yaratilmadi — mavjud, amalda qo'llanilayotgan qoida bir joyga
to'plandi.

---

## 1. Maqsad

GoldBot arxitekturasida "canonical Module" nima ekanligini yagona
manba (SSOT) sifatida belgilash. Bu tamoyil butun loyiha strukturasi
zamirida yotadi va Module Reuse Principle bilan birga ishlaydi.

## 2. Asosiy qoida

**Canonical Module = Package.**

- Har bir canonical Module — bu Python Package (papka +
  `__init__.py`), alohida bo'sh `.py` fayl emas.
- Layer'lar (`data_layer/`, `context_layer/`, `core_layer/`,
  `ai/`, `risk_layer/`, `decision_layer/`, `execution_layer/`,
  `platform_layer/`, `database/`, `monitoring/`, ...) canonical
  Package'lar sifatida tashkil etiladi.
- Module nomi Package nomi bilan aynan bir xil bo'ladi — ikki xil
  nom ostida bir xil mas'uliyat takrorlanmaydi (Single Source of
  Truth).

## 3. GEL-001 Strict

"GEL-001 Strict" — yangi funksionallik qo'shishda quyidagi tartib:

1. Yangi top-level Package yaratish o'rniga, mavjud Package ichida
   yangi sub-modul qo'shiladi (masalan `core_layer/features/atr/`,
   `core_layer/features/` paketi ichida — yangi top-level `indicator/`
   emas).
2. Bu CLAUDE.md **Module Reuse Principle** ("1) mavjudmi? 2)
   kengaytirish mumkinmi? 3) faqat ikkalasi ham yo'q bo'lsa — yangi
   modul") bilan bir xil natijaga olib keladi: yangi top-level Package
   eng yuqori narxli variant va kamdan-kam ishlatiladi.
3. Real misol: FLOW-007 (Indicator Engine) auditida ATR sub-moduli
   `core_layer/features/atr/` sifatida, yangi top-level `indicator_layer/`
   ochmasdan qo'shildi (`GFL-001_FLOW_CATALOG.md`, Director Decision:
   Approve).

## 4. Boshqa standartlar bilan munosabat

- **CLAUDE.md — Module Reuse Principle**: GEL-001 uning strukturaviy
  asosidir — "canonical Module = Package" bo'lgani uchun "mavjudini
  kengaytir" har doim "yangi Package yarat"dan arzonroq.
- **MIR-001 / Foundation Freeze** (`docs/policies/FOUNDATION_POLICY.md`):
  skeleton Package'lar (13-qatorli generik `__init__.py`-only) ham
  GEL-001 bo'yicha to'g'ri Package shaklida, ammo ularga yangi business
  logic yozilmaydi.
- **`docs/GFL-001_FLOW_FIRST_STANDARD.md`** — "Relationship with other
  standards" bo'limida GEL-001 ni "Canonical Module = Package" deb
  canonical havola qiladi.

## 5. Doiradan tashqari (o'zgartirmaydi)

Bu hujjat arxitekturani, kodni yoki dependency'ni o'zgartirmaydi —
faqat mavjud strukturaviy tamoyilning canonical anchori. PHASE-01
qayta ochilmaydi (Director qarori: Foundation Completion Task).

---

## Xulosa

GEL-001 — GoldBot strukturasining SSOT'i: canonical Module har doim
Package, kengaytirish yangi top-level Package'dan ustun (GEL-001
Strict), va bu Module Reuse Principle bilan birga arxitektura
barqarorligini ta'minlaydi.
