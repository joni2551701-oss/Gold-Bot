# GBA-001 — IMPORT GRAPH REPORT

## Qamrov haqida ochiq bayonot

**Bu bo'lim qisman ko'rib chiqildi, sababi:** to'liq 280+ modulli
import grafigini avtomatik vosita (masalan `pydeps`) bilan qurish va
vizualizatsiya qilish berilgan vaqt oynasida bajarilmadi. Buning
o'rniga maqsadli `grep`-asosli import tekshiruvlari (yuqoridagi
`02`/`07` fayllarda) va real ishga tushirish tasdiqlari (`main.py`,
`pytest`) orqali bilvosita dalil to'plandi.

## Qo'lda tekshirilgan asosiy import chetlari (edges)

- `core_layer/pipeline/pipeline.py` — barcha quyi qatlamlarni
  orkestratsiya qiladi (`main.py` smoke-run logida har bir stage nomi
  bilan tasdiqlangan: market_data, data_quality, htf_bias, context,
  market_phase, signal, signal_quality, explainability, features, ai,
  decision, risk, signal_history, telegram_format,
  telegram_delivery, database).
- `ai_layer` -> `media_layer.telegram_broadcast` (yuqorida
  hujjatlashtirilgan, minor topilma).
- `ai_layer` -> `database_layer`: import TOPILMADI (`grep -rln
  "^import database\|^from database" ai_layer/` bo'sh natija berdi).
- `platform_layer/telegram/handlers.py` -> service -> repository
  zanjiri CLAUDE.md talabi bo'yicha; bu audit doirasida
  `handlers.py`ning to'g'ridan-to'g'ri `database_layer`ni import
  qilmasligi maxsus tekshirilmadi (namunaviy sample sirtidan tashqarida
  qoldi) — **qisman ko'rib chiqilgan**, `09_SECURITY_REPORT.md`da
  qo'shimcha eslatma bilan.

## Circular import — bilvosita dalil

`python main.py` (exit=0) va `python -m pytest tests/` (5400 passed,
0 failed/error) — ikkalasi ham import vaqtida hech qanday
`ImportError`/`ModuleNotFoundError`/circular-import xatosi
bermadi. Bu strukturaviy circular dependency yo'qligining amaliy
dalili, biroq rasmiy grafik tahlil o'rnini bosmaydi.

## Tavsiya

Keyingi Sprint uchun backlog elementi sifatida: `pydeps` yoki
shunga o'xshash vositani CI'ga (yoki alohida audit skriptiga)
qo'shib, har Layer bo'yicha import grafigini avtomatik generatsiya
qilish va Layer Direction qoidasini avtomatik tekshirish (masalan,
"ai_layer papkasidan database_layer'ga hech qanday import chetlari
bo'lmasligi kerak" kabi assertlar bilan) — bu keyingi audit
sikllarida qo'lda `grep`ga tayanishni kamaytiradi.
