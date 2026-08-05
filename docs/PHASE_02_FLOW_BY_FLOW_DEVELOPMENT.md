# PHASE-02 — Flow-by-Flow Development

Status: Canonical (Development Standard)
Version: 1.0
Authority: Director Order (PHASE-02 Flow-by-Flow Development Initialization)
Sana: 2026-08-05
Til: GLS-001 (proza O'zbek, texnik terminlar English)

> Bu hujjat PHASE-02 uchun **yagona boshqaruv hujjati**. U Production
> kod emas va yangi qoida ixtiro qilmaydi — Foundation'da (PHASE-01,
> Frozen) allaqachon belgilangan qoidalarni PHASE-02 kontekstida bir
> joyga jamlaydi va ularga havola qiladi (Single Source of Truth).
> Foundation hujjatlari (V3 Architecture, GDL-001, GFL-001, GEL-001,
> GLS-001) o'zgartirilmaydi.

---

## 1. Purpose

PHASE-02 maqsadi — GoldBot'ni GFL-001 Flow-First metodologiyasi
bo'yicha, Foundation ustiga, Flow-by-Flow ishlab chiqish. Har bir Flow
boshidan oxirigacha ishlaydigan holatga kelgandan keyingina keyingisi
boshlanadi. Foundation o'zgarmaydi; barcha ish uning ustiga quriladi.

Bu hujjat PHASE-02'ning rasmiy Development standarti: undan keyingi
barcha Development ishlari shu hujjatga tayangan holda olib boriladi.

## 2. Scope

PHASE-02 GFL-001 katalogidagi barcha 25 Flow'ni qamrab oladi
(canonical V3 raqamlash, GFL-002):

```
FLOW-001  (System Bootstrap / Configuration)
   ↓
  ...  (FLOW-002 .. FLOW-024)
   ↓
FLOW-025  (Web)
   ↓
End User
```

To'liq katalog va bog'liqliklar Foundation'da (o'zgarmaydi):
- `docs/GFL-001_FLOW_CATALOG.md` — har bir Flow'ning
  Producer/Input/Processing/Output/Consumer kontrakti.
- `docs/GFL-001_FLOW_DEPENDENCY.md` — Flow bog'liqlik grafigi.
- `docs/GFL-001_FLOW_PROGRESS.md` — joriy holat (🟩/🟦).

Izoh: Flow'lar qayta raqamlanmaydi (Forbidden). Katalog Foundation
Freeze'da — Flow raqamlari va kontraktlari o'zgarmas.

## 3. Development Lifecycle (per Flow)

Har bir Flow uchun yagona tartib — bu GDL-001 "Flow Lifecycle"ning
aynan o'zi (`docs/GDL-001_GOLDBOT_DEVELOPMENT_LIFECYCLE.md`, §3):

```
Short Audit
   ↓
Reuse Analysis
   ↓
Production Code
   ↓
Documentation
   ↓
WORK_LOG
   ↓
Commit
```

Bu GFL-004 Lightweight Loop bilan mos: Flow'ning natijasi "allaqachon
amalga oshirilgan" (docs-only) yoki "hali qurilmagan = Blueprint"
(xolis) bo'lishi mumkin — ikkalasi ham qonuniy natija. Soxta
"Completed" belgilash taqiqlanadi (butun sessiya audit naqshi).

## 4. Sequential Flow Rule

GFL-003 Sequential Flow Rule (`docs/GFL-001_FLOW_FIRST_STANDARD.md`,
§GFL-003) amal qiladi, o'zgarmasdan:

- Flow'lar ketma-ket bajariladi.
- Flow o'tkazib yuborilmaydi.
- Oldingi Flow tugamasdan (uning CI SUCCESS bo'lmasdan) keyingisi
  boshlanmaydi.
- Navbatdagi Flow — eng kichik raqamli hali bajarilmagan Flow.

## 5. Reuse Rule

CLAUDE.md **Module Reuse Principle** + GEL-001 Canonical Module =
Package (`docs/GEL-001_CANONICAL_MODULE_STANDARD.md`) amal qiladi. Har
bir Flow boshlanishidan oldin Reuse Analysis **majburiy**, quyidagi
tartibda (birinchi "ha"da to'xta):

1. Bu allaqachon repo'da mavjudmi?
2. Mavjud modulni kengaytirish mumkinmi (yangi method / optional field
   / mavjud faylga yangi funksiya) — kontraktni buzmasdan?
3. Faqat ikkalasi ham "yo'q" bo'lsa — yangi modul yaratiladi va uning
   docstring'ida 1 va 2 nima uchun "yo'q" bo'lgani hujjatlashtiriladi.

Yangi top-level Package eng yuqori narxli, eng oxirgi variant. Reuse —
standart natija.

## 6. Documentation Rule

Har bir Flow yakunida quyidagilar yangilanadi (mavjud, o'zgarmas
hujjatlar):

- `platform_layer/WORK_LOG.md` (yoki tegishli layer'ning
  `WORK_LOG.md`'i) — append-only `Issue ID` yozuvi.
- `docs/changelog/CHANGELOG.md` — o'zgarish qaydi.
- `docs/GFL-001_FLOW_PROGRESS.md` — Flow status/foiz.
- `docs/GFL-001_FLOW_CATALOG.md` — kerak bo'lsa audit izohi.

Documentation Standard va GLS-001 til qoidasi amal qiladi
(`docs/standards/DOCUMENTATION_STANDARD.md`,
`docs/GLS-001_TRANSLATION_STANDARD.md`). Append-only tamoyil: eski
yozuvlar o'chirilmaydi.

## 7. Commit Policy

Har bir Commit:

- **kichik** — bitta Flow yoki bitta aniq qadam.
- **aniq** — commit message nima va nima uchun o'zgarganini aytadi.
- **bitta maqsadli** — bir commit'da bir maqsad (Commit Standard,
  `docs/standards/COMMIT_STANDARD.md`).

Har bir commit CLAUDE.md majburiy Commit Protocol zanjiridan o'tadi
(§8).

## 8. CI Policy

PHASE-02 CI siyosati (mavjud pipeline'ni o'zgartirmaydi — faqat
siyosatni belgilaydi):

- **Lokal tekshiruv har bir Commit'dan oldin majburiy**, CLAUDE.md
  "After Code Changes — Commit Protocol" tartibida: `git add -A` →
  `pyflakes` → (agar o'zgarsa qayta `git add -A`) → `compileall` →
  `pytest tests/` → `python main.py` smoke → `git status` clean →
  `git diff --cached` review → commit → push.
- **GitHub Actions majburiy tekshiruv** sifatida ishlatiladi: pushed
  commit uchun CI `success` qaytarmaguncha Flow "Completed" deb
  hisoblanmaydi (GFL-003 bilan mos — Sequential Flow Rule keyingi
  Flow'ni CI SUCCESS'dan keyin ochadi).
- **CI ishlatish strategiyasi** GDL-001/GFL-001 bilan mos va Director
  qarori bilan boshqariladi. CI trigger usuli, batching (har Flow'dan
  keyin CI yoki bir nechta Flow'dan keyin bitta CI) — Director
  Decision doirasida; Worker o'zboshimchalik bilan o'zgartirmaydi (No
  Silent Decisions).
- **Reporting language** (CLAUDE.md majburiy): CI `success`
  kelmaguncha "Local validation passed. Waiting for GitHub Actions
  confirmation."; keyin "GitHub Actions: SUCCESS. Phase complete."
- Bu hujjat mavjud `.github/workflows/ci.yml`'ni yoki pipeline'ni
  o'zgartirmaydi.

## 9. Completion Criteria

PHASE-02 tugashi uchun GFL-001 katalogidagi ketma-ketlik to'liq
yakunlangan bo'lishi kerak:

```
FLOW-001 ... FLOW-025  →  End User   (barchasi Completed yoki xolis
                                       Blueprint audit natijasi bilan)
```

Har bir Flow'ning yakuniy holati `docs/GFL-001_FLOW_PROGRESS.md`da
qayd etiladi. "Completed" faqat real, test qilingan implementatsiya
uchun; qurilmagan subsystem xolis "Blueprint"da qoladi.

## 10. Director Review Criteria

PHASE-02 yakunida Director quyidagilarni tekshiradi (GDL-001 §6 Director
Review bilan mos):

- Architecture
- Code Quality
- Reuse (Module Reuse Principle qo'llanilganmi)
- Performance
- Security
- Documentation
- Technical Debt
- Production Readiness

---

## Constraints (majburiy)

- Foundation o'zgarmaydi.
- V3 Architecture o'zgarmaydi.
- GDL-001 / GFL-001 / GEL-001 / GLS-001 o'zgarmaydi.
- PHASE-01 qayta ochilmaydi.

## Forbidden (taqiqlanadi)

- Bu hujjat doirasida Production kod yozish.
- Flow'larni qayta raqamlash.
- Architecture'ni o'zgartirish.
- Foundation hujjatlarini tahrirlash.
- Yangi Development Rule ixtiro qilish (faqat mavjud qoidalarga
  havola).
- Silent Decision.

## Trading Safety (o'zgarmas)

PHASE-02 davomida ham CLAUDE.md Trading Safety hard rules amal qiladi:
`decision_layer/`, `risk_layer/`, `execution_layer/` faqat aniq
Director approval bilan o'zgartiriladi; AI to'g'ridan-to'g'ri
execution qila olmaydi; har bir signal Risk Manager'dan o'tadi.

---

## Xulosa

Bu hujjat PHASE-02 Flow-by-Flow Development'ning yagona boshqaruv
standarti. U Foundation qoidalarini (GDL-001 lifecycle, GFL-003
Sequential, GFL-004 Lightweight Loop, GEL-001 Reuse, CLAUDE.md Commit
Protocol) PHASE-02 uchun jamlaydi va ularga havola qiladi — yangi
qoida yaratmaydi. Shu hujjat tasdiqlangach, PHASE-02 rasmiy ravishda
boshlanadi va keyingi barcha Development ishlari unga tayanadi.
