# GLS-001 — Translation / Language Standard

Status: Canonical
Version: 1.0
Trigger: PHASE-01 Foundation Completion Task (Director qarori —
PHASE-01 SHARTLI APPROVED). Bu master hujjat ilgari faqat komponent
sifatida mavjud bo'lgan tarjima qoidasiga (`docs/TERMINOLOGY.md`)
yagona canonical anchor beradi. Reuse First: yangi qoida yaratilmadi —
mavjud, amalda qo'llanilayotgan qoida bir joyga to'plandi.

---

## 1. Maqsad

GoldBot hujjatlari va hisobotlarida qaysi til ishlatilishini yagona
manba (SSOT) sifatida belgilash. Bu hujjat butun sessiya davomida
amalda bo'lgan "docs va reports O'zbek tilida" qoidasining rasmiy
canonical shaklidir.

## 2. Asosiy qoida

**Prozaik matn O'zbek tilida, texnik terminlar inglizcha.**

- `.md` hujjatlarning matni, izohlar, tavsiflar, hisobotlar, auditlar,
  xulosalar, WORK_LOG yozuvlari — O'zbek tilida yoziladi.
- Texnik terminlar (`Layer`, `Module`, `Package`, `Pipeline`,
  `Dependency`, `Contract`, `Validation`, `Rollback`, `Blueprint`,
  h.k.) har doim asl inglizcha shaklida qoladi — O'zbekcha muqobil
  qidirilmaydi.
- Identifikatorlar (RFC, ADR, DD, GDS, GEL, GLS, FLOW-XXX), `.py` fayl/
  Package/Module/Class/Function/Variable nomlari, API/Framework/
  kutubxona nomlari, kod bloklari, diagramma identifikatorlari, Git
  commit va Branch nomlari — hech qachon tarjima qilinmaydi.

## 3. Komponentlar (Reuse First)

Bu standart yangi lug'at ixtiro qilmaydi — u mavjud komponentga
tayanadi:

- **`docs/TERMINOLOGY.md`** — GLS-001 ning yagona texnik lug'ati
  (append-only): "Tarjima qilinadi" va "Tarjima qilinmaydi" jadvallari.
  Yangi prozaik so'z topilganda shu faylga qo'shiladi, mavjud tarjima
  o'zgartirilmaydi.

## 4. Boshqa standartlar bilan munosabat

- **Engineering Language Policy**
  (`docs/governance/policies/Engineering_Language_Policy.md`) — kod,
  kod izohlari, identifikatorlar va muhandislik artefaktlari uchun
  ingliz tilini belgilaydi. GLS-001 bunga zid emas, balki
  to'ldiruvchi: Engineering Language Policy = kod tili (English),
  GLS-001 = hujjat/report prozasi tili (O'zbek, texnik terminlar
  inglizcha). Ikkalasi birga butun repo til rejimini tashkil qiladi.
- **`docs/GFL-001_FLOW_FIRST_STANDARD.md`** — "Relationship with other
  standards" bo'limida GLS-001 ni "Docs va reports O'zbek tilida" deb
  canonical havola qiladi.

## 5. Doiradan tashqari (o'zgartirmaydi)

Bu hujjat arxitekturani, kodni yoki dependency'ni o'zgartirmaydi —
faqat mavjud til qoidasining canonical anchori. PHASE-01 qayta
ochilmaydi (Director qarori: Foundation Completion Task).

---

## Xulosa

GLS-001 — GoldBot hujjat va hisobotlari tilining SSOT'i: prozaik matn
O'zbek tilida, texnik terminlar va identifikatorlar inglizcha, lug'at
esa `docs/TERMINOLOGY.md` da append-only saqlanadi.
