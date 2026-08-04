# GEL-001 Compatibility Exceptions — Reyestr

**Sanasi:** 2026-08-04
**Kelib chiqishi:** `DD-005 Compliance Audit — Result` (commit `d9e0a84`,
`DIRECTOR_DECISIONS.md`) va `DD005_COMPLIANCE_REPORT.md`'da ko'tarilgan
Director Review punkti — DD-005 "274 Canonical Packages / 11
Compatibility Exceptions / 0 Violations" deb tasdiqlagan, lekin o'sha 11
Exception'ning aniq modul nomlari hech bir hujjatda ro'yxatlanmagan edi.

## Maqsad

Ushbu reyestr DD-005'dagi Compatibility Exception sonini endi
**individual ravishda kuzatiladigan**, har biri haqiqiy empirik dalilga
ega yozuvlar to'plamiga aylantiradi — DD-003 Append-Only Discipline
talabiga muvofiq. Har bir yozuv nima uchun bu fayl paketlashtirishdan
(yoki paket ichida qayta joylashtirishdan) ozod qilinganini, qaysi
mexanizm (AST parser, MonkeyPatch, Public API) uni literal fayl yo'liga
bog'lab qo'yganini va Director tasdiqlash holatini ko'rsatadi.

**Metodologiya:** `tests/` katalogi butunlay Grep orqali skanerlandi —
(1) `mock.patch(`/`monkeypatch.setattr(` dotted-path nishonlari, (2)
`ast.parse(`/`ast.walk(`/`inspect.getsource(` chaqiruvlari, (3) repo
bo'yicha literal `"<layer>/.../<fayl>.py"` satrlari. Har bir topilma
qo'lda tekshirildi: faqat **bitta muayyan faylni** `pathlib.Path(...)`
orqali literal yo'l bilan qurib, so'ngra uni **`.read_text()` +
`ast.parse()` orqali diskdan o'qiydigan** testlar haqiqiy exception deb
hisoblandi. Quyidagilar **hisobga olinmadi** (haqiqiy exception emas,
False Positive):

- `mock.patch("a.b.c.func")` turidagi dotted-path nishonlar — bular
  Python import tizimi orqali ishlaydi, modul flat fayl bo'lsa ham,
  paket bo'lsa ham bir xil ishlaydi (`unittest.mock` OS fayl yo'liga
  bog'liq emas).
- `directory.rglob("*.py")` orqali butun katalogni AST bilan skanerlaydigan
  testlar (masalan `tests/ai/trade_journal/test_trade_journal_isolation.py`)
  — bular muayyan bitta faylni emas, butun paket katalogini nishonga
  oladi; katalog ichidagi fayllar qayta nomlansa/qo'shilsa ham test
  ishlayveradi, demak paket ichida hech qanday muayyan fayl yo'liga
  qattiq bog'lanish yo'q.

## Xulosa raqami

**Ushbu tekshiruvda haqiqiy dalil bilan tasdiqlangan Compatibility
Exception soni: 9** — DD-005'da e'lon qilingan 11 tadan farqli
(pastdagi "Farq tushuntirishi" bo'limiga qarang).

## Jamlama jadvali

| Module | Layer | Status |
|---|---|---|
| `media_layer/telegram_broadcast/broadcast_adapter.py` | Media Layer | Active |
| `decision_layer/decision_logger/decision_logger.py` | Decision Layer | Active |
| `database_layer/audit_log/monitoring_repository.py` | Database Layer | Active |
| `ai_layer/ai_engine/intelligence_runtime.py` | AI Layer | Active |
| `platform_layer/telegram/owner/monitoring_commands.py` | Platform Layer | Active |
| `ai_layer/knowledge_ai/knowledge_base/knowledge_manager.py` | AI Layer | Active |
| `ai_layer/personal_ai/interaction_manager/conversation_adapters.py` | AI Layer | Active |
| `ai_layer/ai_service/content/content_adapters.py` | AI Layer | Active |
| `ai_layer/ai_engine/reasoning/reasoning_adapters.py` | AI Layer | Active |

---

### broadcast_adapter.py

- **Module:** `media_layer/telegram_broadcast/broadcast_adapter.py`
- **Layer:** Media Layer
- **Sabab:** `tests/broadcast/test_broadcast_adapter.py`'ning
  `test_broadcast_adapter_module_never_imports_decision_risk_execution`
  testi ushbu faylni literal `pathlib.Path(...) / "media_layer" /
  "telegram_broadcast" / "broadcast_adapter.py"` yo'li orqali qurib,
  `.read_text()` + `ast.parse()` bilan diskdan bevosita o'qiydi. Fayl
  nomi paket nomidan (`telegram_broadcast`) farqli, shu sababli uni
  o'z sub-paketiga aylantirish (`broadcast_adapter/broadcast_adapter.py`)
  ushbu literal yo'lni buzadi.
- **AST:** YES
- **MonkeyPatch:** NO
- **Public API:** NO
- **Risk:** Low
- **Director Decision:** Kutilmoqda — Director Review talab qilinadi
- **Status:** Active
- **Added Date:** 2026-08-04
- **Removed Date:**

### decision_logger.py

- **Module:** `decision_layer/decision_logger/decision_logger.py`
- **Layer:** Decision Layer
- **Sabab:** `tests/monitoring/test_monitoring_isolation.py`'ning
  `test_decision_logger_never_imports_signals_or_context` testi bu
  faylni `pathlib.Path(...) / "decision_layer" / "decision_logger" /
  "decision_logger.py"` literal yo'li orqali qurib, `ast.parse()` bilan
  o'qiydi (`_imported_names()` helper orqali). Fayl allaqachon
  `<stem>/<stem>.py` konvensiyasiga mos, ammo ichki joylashuvi yoki
  nomi o'zgarsa ushbu test literal yo'l bo'yicha buziladi.
- **AST:** YES
- **MonkeyPatch:** NO
- **Public API:** NO
- **Risk:** Low
- **Director Decision:** Kutilmoqda — Director Review talab qilinadi
- **Status:** Active
- **Added Date:** 2026-08-04
- **Removed Date:**

### monitoring_repository.py

- **Module:** `database_layer/audit_log/monitoring_repository.py`
- **Layer:** Database Layer
- **Sabab:** `tests/monitoring/test_monitoring_isolation.py`'ning
  `test_monitoring_repository_module_confined_to_database_and_stdlib`
  testi bu faylni `pathlib.Path(...) / "database_layer" / "audit_log" /
  "monitoring_repository.py"` literal yo'li orqali qurib, `ast.parse()`
  bilan o'qiydi. Fayl nomi paket nomidan (`audit_log`) farqli — sub-paket
  qilib qayta joylashtirish ushbu literal yo'lni buzadi.
- **AST:** YES
- **MonkeyPatch:** NO
- **Public API:** NO
- **Risk:** Low
- **Director Decision:** Kutilmoqda — Director Review talab qilinadi
- **Status:** Active
- **Added Date:** 2026-08-04
- **Removed Date:**

### intelligence_runtime.py

- **Module:** `ai_layer/ai_engine/intelligence_runtime.py`
- **Layer:** AI Layer
- **Sabab:** `tests/ai/test_intelligence_runtime_isolation.py`'ning
  `test_intelligence_runtime_never_imports_trading_layers` testi bu
  faylni `pathlib.Path(...) / "ai_layer" / "ai_engine" /
  "intelligence_runtime.py"` literal yo'li orqali qurib, `ast.parse()`
  bilan o'qiydi. Bu fayl — docstring'ida ta'kidlanganidek — "the one
  file... permitted to import every Intelligence layer at once (the
  composition root)", shu sababli uning aynan joylashuvi maxsus nazorat
  ostida.
- **AST:** YES
- **MonkeyPatch:** NO
- **Public API:** NO
- **Risk:** Medium
- **Director Decision:** Kutilmoqda — Director Review talab qilinadi
- **Status:** Active
- **Added Date:** 2026-08-04
- **Removed Date:**

### monitoring_commands.py

- **Module:** `platform_layer/telegram/owner/monitoring_commands.py`
- **Layer:** Platform Layer
- **Sabab:** `tests/monitoring/test_monitoring_isolation.py`'ning
  `_owner_commands_file()` helper funksiyasi bu faylni literal
  `pathlib.Path(...) / "platform_layer" / "telegram" / "owner" /
  "monitoring_commands.py"` yo'li orqali qurib,
  `test_monitoring_commands_never_imports_decision_risk_execution`
  testida `ast.parse()` bilan o'qiydi.
- **AST:** YES
- **MonkeyPatch:** NO
- **Public API:** NO
- **Risk:** Low
- **Director Decision:** Kutilmoqda — Director Review talab qilinadi
- **Status:** Active
- **Added Date:** 2026-08-04
- **Removed Date:**

### knowledge_manager.py

- **Module:** `ai_layer/knowledge_ai/knowledge_base/knowledge_manager.py`
- **Layer:** AI Layer
- **Sabab:** `tests/knowledge/test_knowledge_manager.py`'ning
  `test_knowledge_manager_never_imports_trading_layers` testi bu
  faylni `pathlib.Path(...) / "ai_layer" / "knowledge_ai" /
  "knowledge_base" / "knowledge_manager.py"` literal yo'li orqali
  qurib, `ast.parse()` bilan o'qiydi.
- **AST:** YES
- **MonkeyPatch:** NO
- **Public API:** NO
- **Risk:** Low
- **Director Decision:** Kutilmoqda — Director Review talab qilinadi
- **Status:** Active
- **Added Date:** 2026-08-04
- **Removed Date:**

### conversation_adapters.py

- **Module:** `ai_layer/personal_ai/interaction_manager/conversation_adapters.py`
- **Layer:** AI Layer
- **Sabab:** `tests/ai/conversation/test_conversation_adapters.py`'ning
  `test_conversation_adapters_module_never_imports_ai_explanation` testi
  bu faylni `pathlib.Path(...) / "ai_layer" / "personal_ai" /
  "interaction_manager" / "conversation_adapters.py"` literal yo'li
  orqali qurib, `ast.parse()` bilan o'qiydi — "Intelligence Dependency
  Principle"ning eng muhim nazorat nuqtasi sifatida ta'kidlangan.
- **AST:** YES
- **MonkeyPatch:** NO
- **Public API:** NO
- **Risk:** Low
- **Director Decision:** Kutilmoqda — Director Review talab qilinadi
- **Status:** Active
- **Added Date:** 2026-08-04
- **Removed Date:**

### content_adapters.py

- **Module:** `ai_layer/ai_service/content/content_adapters.py`
- **Layer:** AI Layer
- **Sabab:** `tests/ai/content/test_content_adapters.py`'ning
  `test_content_adapters_module_never_imports_translation_media_or_broadcast`
  testi bu faylni `pathlib.Path(...) / "ai_layer" / "ai_service" /
  "content" / "content_adapters.py"` literal yo'li orqali qurib,
  `ast.parse()` bilan o'qiydi.
- **AST:** YES
- **MonkeyPatch:** NO
- **Public API:** NO
- **Risk:** Low
- **Director Decision:** Kutilmoqda — Director Review talab qilinadi
- **Status:** Active
- **Added Date:** 2026-08-04
- **Removed Date:**

### reasoning_adapters.py

- **Module:** `ai_layer/ai_engine/reasoning/reasoning_adapters.py`
- **Layer:** AI Layer
- **Sabab:** `tests/ai/reasoning/test_reasoning_adapters.py`'ning
  `test_reasoning_adapters_module_never_imports_ai_explanation` testi bu
  faylni `pathlib.Path(...) / "ai_layer" / "ai_engine" / "reasoning" /
  "reasoning_adapters.py"` literal yo'li orqali qurib, `ast.parse()`
  bilan o'qiydi.
- **AST:** YES
- **MonkeyPatch:** NO
- **Public API:** NO
- **Risk:** Low
- **Director Decision:** Kutilmoqda — Director Review talab qilinadi
- **Status:** Active
- **Added Date:** 2026-08-04
- **Removed Date:**

---

## Farq tushuntirishi (Discrepancy)

Ushbu tekshiruv **9 ta** haqiqiy, empirik dalilga ega Compatibility
Exception'ni tasdiqladi — DD-005'da e'lon qilingan **11** ta emas.

**Tekshirilgan, lekin exception EMAS deb topilgan holatlar:**

- `mock.patch("platform_layer.telegram.owner.monitoring_commands...")`
  turidagi dotted-path nishonlar (`tests/telegram/owner/
  test_owner_commands.py`, `test_monitoring_commands_phase_b0.py`,
  `tests/monitoring/test_phase_b0_extra_coverage_2.py`) — bular Python
  import mexanizmi orqali ishlaydi, literal OS fayl yo'liga bog'liq
  emas (`DD005_COMPLIANCE_REPORT.md` §5'da ham False Positive deb
  qayd etilgan).
- 33 ta `ast.parse`/`ast.walk` ishlatuvchi isolation testining
  aksariyati (`tests/ai/*/test_*_isolation.py`, `tests/monitoring/
  test_monitoring_isolation.py`ning `rglob("*.py")` chaqiruvlari kabi)
  — bular **butun katalogni** skanerlaydi, muayyan bitta faylga literal
  yo'l bilan bog'lanmagan; katalog ichida fayllar qayta tashkil
  etilganda ham test ishlayveradi.
- Repo bo'yicha faqat 2 ta literal `"<layer>/<fayl>.py"` satri topildi
  (`ai_layer/knowledge_ai/knowledge_base/models.py` va
  `platform_layer/telegram/owner/provider_commands.py:32`) — ikkisi ham
  faqat izoh/docstring matni, ijro etiladigan mantiqqa ta'sir qilmaydi.
- `database_layer/database_manager/database.py` mavjudligini tekshiruvchi
  `tests/deploy/test_deploy_scripts_shape.py:326`dagi `.exists()`
  assert'i ham ko'rib chiqildi — bu literal `.py` satr, lekin faylni
  diskdan o'qib AST/mock bilan tahlil qilmaydi, shunchaki mavjudligini
  tasdiqlaydi; `scripts/deploy/release_deploy.sh`da esa umuman
  hardcoded fayl nomi yo'q (rsync exclude-pattern asosida ishlaydi).
  Shuning uchun bu **kuchsiz bog'lanish** deb baholandi va reyestrga
  9 ta asosiy ro'yxatga qo'shilmadi — past ishonch darajasi bilan
  qayd etilishi mumkin bo'lgan qo'shimcha nomzod sifatida qoldirildi.

**Xulosa:** Tasdiqlangan 9 ta va DD-005'ning 11 tasi orasidagi **2
birlik farq hal qilinmagan holda qoladi.** Bu farqni bartaraf etish
uchun ikki yo'l bor: (a) DD-005'dagi 11 raqami tuzatilishi (agar
haqiqiy son 9 yoki 10 bo'lsa — `database.py`ning `.exists()` holatini
hisobga olgan holda), yoki (b) boshqa metodologiya bilan qo'shimcha 1-2
ta haqiqiy exception topish uchun ikkinchi tekshiruv o'tkazilishi kerak
(masalan, `docs/`, `scripts/`, yoki konfiguratsiya fayllaridagi literal
yo'l bog'lanishlarini alohida chuqur skanerlash). **Ushbu farq Director
Review talab qiladi** — DD-003 Append-Only Discipline tamoyiliga ko'ra,
soni o'zgarishi kerak bo'lsa, bu alohida DD sifatida qayd etilishi
kerak, mavjud DD-005 matnini tahrirlash orqali emas.

Ushbu reyestrda **hech qanday xayoliy (fabricated) yozuv yo'q** — har
bir yuqoridagi 9 ta yozuv aniq test fayli, aniq qator raqami va aniq
kod parchasi bilan tasdiqlangan (Grep/Read orqali bevosita o'qilgan).
11 taga to'ldirish uchun qo'shimcha nomzodlar **ataylab kiritilmadi**.
