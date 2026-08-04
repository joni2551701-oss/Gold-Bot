# GEL-001 Compatibility Exceptions — Reyestr

**Sanasi:** 2026-08-04 (DD-005 Exception Registry Verification — keng metodologiyali qayta tekshirish)
**Kelib chiqishi:** Director Order "DD-005 Exception Registry Verification" —
avvalgi reyestr (commit `72135eb`) faqat `Path(...).read_text()` +
`ast.parse()` kombinatsiyasini qidiruvchi tor metodologiya bilan
tuzilgan edi va 9 ta topgan edi. Ushbu qayta tekshiruv **kengaytirilgan
metodologiya** bilan (`ast.parse`, `inspect.getsource`/`getfile`,
`.exists()`/`.is_file()`, `importlib.resources`, `pkgutil`,
`monkeypatch.setattr`/`mock.patch` literal-yo'l nishonlari, va boshqa
literal fayl-yo'l satrlari) butun repozitoriyni (barcha 17 Layer) qayta
skanerladi.

## Metodologiya

Grep orqali quyidagi patternlar butun repo bo'yicha (barcha 17 Layer:
`data_layer`, `context_layer`, `core_layer`, `indicator_layer`,
`strategy_layer`, `signal_layer`, `ai_layer`, `decision_layer`,
`risk_layer`, `execution_layer`, `trade_monitoring_layer`,
`database_layer`, `platform_layer`, `media_layer`, `chart_layer`,
`backtesting_layer`, `future_expansion`) qidirildi: `ast.parse`,
`.read_text()`, `.exists()`/`.is_file()` (literal modul-fayl yo'llari
ustida), `inspect.getsource`/`inspect.getfile`, `importlib.resources`,
`pkgutil`, `monkeypatch.setattr(`/`mock.patch(` (literal dotted-path
yoki fayl-yo'l nishonlari), va boshqa literal `"<layer>/.../<fayl>.py"`
satrlari.

**Haqiqiy exception mezoni (o'zgarishsiz, DD-005'dan):** kod (odatda
test) (a) **bitta muayyan modulning** joriy joylashuvidagi fayliga
literal yo'l quradi, VA (b) shu aniq faylni o'qiydi/tahlil qiladi
(`.read_text()` + `ast.parse()`, yoki teng kuchli), shundayki modulning
fizik fayl yo'li o'zgarsa (masalan `foo.py` dan `foo/foo.py` ga),
mazkur kod buziladi.

**False Positive deb hisoblangan (exception EMAS) toifalar:**
- `mock.patch("dotted.module.path...")` / `monkeypatch.setattr(module,
  "attr", ...)` — dotted-path nishon paket ham, flat fayl ham bo'lsa
  bir xil ishlaydi (Python import tizimi orqali, OS fayl yo'liga
  bog'liq emas). Repo bo'yicha 110 ta shunday chaqiruv (24 faylda)
  topildi — barchasi shu toifaga kiradi, birortasi ham
  `sys.modules["flat.exact.name"]`ga qattiq bog'lanmagan.
- `directory.rglob("*.py")` / katalog bo'yicha AST skaneri — butun
  paketni qamrab oladi, muayyan bitta faylga bog'lanmagan.
- `inspect.getsource(imported_module)` / `inspect.getsource(Class.method)`
  — bu **import qilingan modul obyekti** orqali ishlaydi (`module.__file__`
  avtomatik aniqlanadi), literal yo'l qurilmaydi; modul flat fayldan
  paketga o'tsa ham import yo'li o'zgarmasa, bu chaqiruv buzilmaydi.
  Topilgan holatlar: `tests/ai/test_context_memory.py:69`,
  `tests/ai/test_user_profile.py:48`, `tests/ai/test_intelligence_runtime.py:82`,
  `tests/ai/router/test_provider_score.py:87`, `tests/ai/test_prompt_manager.py:60`,
  `tests/platforms/test_navigation_model.py:58` — barchasi False Positive.
- `.exists()`/`.is_file()` — deploy skript/systemd/contracts fayllarini
  tekshiruvchi holatlar (`tests/deploy/*.py`, `tests/contracts/test_contracts_exist.py`)
  va "modul MAVJUD EMAS" tasdiqlovchi salbiy testlar (`tests/ai/learning/
  test_ai_learning_compatibility.py`, `tests/ai/coaching/
  test_ai_coaching_compatibility.py`) — bular faylni o'qib/tahlil
  qilmaydi, faqat mavjudligini/yo'qligini tekshiradi; modul-fayl
  tarkibiga bog'lanish yo'q.
- `database_layer/database_manager/database.py`ning `tests/deploy/
  test_deploy_scripts_shape.py:326`dagi `.exists()` assert'i — avvalgi
  audit tomonidan ham ko'rib chiqilgan, kuchsiz bog'lanish (faylni
  o'qimaydi), reyestrga qo'shilmadi.
- Repo bo'yicha izoh/docstring ichidagi literal `"<layer>/<fayl>.py"`
  satrlari (`ai_layer/knowledge_ai/knowledge_base/models.py`,
  `platform_layer/telegram/owner/provider_commands.py:32`) — ijro
  etiladigan mantiqqa ta'sir qilmaydi.
- `importlib.resources` va `pkgutil` — repo bo'yicha birorta chaqiruv
  topilmadi.

## Xulosa raqami

**Ushbu kengaytirilgan tekshiruvda haqiqiy dalil bilan tasdiqlangan
Compatibility Exception soni: 20** — bu DD-005'da e'lon qilingan **11**
tadan ham, avvalgi tor-metodologiyali audit topgan **9** tadan ham
farq qiladi. Farqning sababi: avvalgi ikkala audit ham faqat "bitta
faylga bitta literal Path qurish" naqshini qidirgan, lekin repoda **bir
nechta faylni for-loop ichida ketma-ket literal yo'l bilan qurib
o'qiydigan** testlar ham mavjud edi (`for filename in (...): py_file =
_dir() / filename; ast.parse(py_file.read_text())`) — bu naqsh ham xuddi
shu mezonga to'liq mos keladi (har bir alohida fayl uchun alohida
literal yo'l va alohida o'qish), ammo ikkala oldingi audit metodologiyasi
buni "bitta fayl" qidiruvi bilan cheklangani sababli qamrab olmagan edi.

Bu son DD-005'ning 11 raqamidan **9 birlik ko'p** — **Director Review
talab qilinadi**, DD-003 Append-Only Discipline tamoyiliga ko'ra son
o'zgarishi mavjud DD-005 matnini tahrirlash orqali emas, alohida yozuv
orqali qayd etiladi (pastga qarang).

## Jamlama jadvali

| # | Module | Layer | Manba (loop yoki yakka) | Status |
|---|---|---|---|---|
| 1 | `media_layer/telegram_broadcast/broadcast_adapter.py` | Media Layer | Yakka | Active |
| 2 | `decision_layer/decision_logger/decision_logger.py` | Decision Layer | Yakka | Active |
| 3 | `database_layer/audit_log/monitoring_repository.py` | Database Layer | Yakka | Active |
| 4 | `ai_layer/ai_engine/intelligence_runtime.py` | AI Layer | Yakka | Active |
| 5 | `platform_layer/telegram/owner/monitoring_commands.py` | Platform Layer | Yakka | Active |
| 6 | `ai_layer/knowledge_ai/knowledge_base/knowledge_manager.py` | AI Layer | Yakka | Active |
| 7 | `ai_layer/personal_ai/interaction_manager/conversation_adapters.py` | AI Layer | Yakka | Active |
| 8 | `ai_layer/ai_service/content/content_adapters.py` | AI Layer | Yakka | Active |
| 9 | `ai_layer/ai_engine/reasoning/reasoning_adapters.py` | AI Layer | Yakka | Active |
| 10 | `media_layer/content_manager/media_adapter.py` | Media Layer | For-loop | Active |
| 11 | `media_layer/content_manager/media_pipeline.py` | Media Layer | For-loop | Active |
| 12 | `core_layer/health_monitor/system_monitor.py` | Core Layer | For-loop | Active |
| 13 | `core_layer/health_monitor/market_monitor.py` | Core Layer | For-loop | Active |
| 14 | `core_layer/health_monitor/signal_monitor.py` | Core Layer | For-loop | Active |
| 15 | `core_layer/health_monitor/error_monitor.py` | Core Layer | For-loop | Active |
| 16 | `core_layer/health_monitor/models.py` | Core Layer | For-loop | Active |
| 17 | `core_layer/health_monitor/resource_monitor.py` | Core Layer | For-loop | Active |
| 18 | `core_layer/health_monitor/health_monitor.py` | Core Layer | For-loop | Active |
| 19 | `core_layer/health_monitor/performance_collector.py` | Core Layer | For-loop | Active |
| 20 | `core_layer/health_monitor/access.py` | Core Layer | For-loop | Active |

---

## 1–9: Avvalgi tor-metodologiyali audit (commit `72135eb`) — qayta tasdiqlangan

Quyidagi 9 yozuv avvalgi reyestrdan qayta tekshirildi (fayl mavjudligi,
test satri, `ast.parse` chaqiruvi — barchasi hozirgi kod holatiga mos
keldi, o'zgarishsiz qayta tasdiqlanadi).

### 1. broadcast_adapter.py
- **Module:** `media_layer/telegram_broadcast/broadcast_adapter.py`
- **Layer:** Media Layer
- **Sabab:** Fayl nomi (`broadcast_adapter`) paket nomidan
  (`telegram_broadcast`) farqli, shu sababli uni sub-paketga aylantirish
  quyidagi literal yo'lni buzadi.
- **Evidence:** `tests/broadcast/test_broadcast_adapter.py:93` —
  `adapter_file = pathlib.Path(__file__).resolve().parents[2] / "media_layer" / "telegram_broadcast" / "broadcast_adapter.py"`,
  shu o'zgaruvchi keyinroq `.read_text()` + `ast.parse()` bilan o'qiladi.
- **Confidence:** Yuqori
- **Status:** Active

### 2. decision_logger.py
- **Module:** `decision_layer/decision_logger/decision_logger.py`
- **Layer:** Decision Layer
- **Sabab:** Fayl allaqachon `<stem>/<stem>.py` konvensiyasiga mos, ammo
  literal yo'l bilan qattiq bog'langan — joylashuvi o'zgarsa test buziladi.
- **Evidence:** `tests/monitoring/test_monitoring_isolation.py:72` —
  `decision_logger_file = pathlib.Path(__file__).resolve().parents[2] / "decision_layer" / "decision_logger" / "decision_logger.py"`,
  74-qatorda `_imported_names(decision_logger_file)` orqali `ast.parse(py_file.read_text())`.
- **Confidence:** Yuqori
- **Status:** Active

### 3. monitoring_repository.py
- **Module:** `database_layer/audit_log/monitoring_repository.py`
- **Layer:** Database Layer
- **Sabab:** Fayl nomi paket nomidan (`audit_log`) farqli.
- **Evidence:** `tests/monitoring/test_monitoring_isolation.py:104` —
  `repo_file = pathlib.Path(__file__).resolve().parents[2] / "database_layer" / "audit_log" / "monitoring_repository.py"`,
  106-qatorda `_imported_names(repo_file)`.
- **Confidence:** Yuqori
- **Status:** Active

### 4. intelligence_runtime.py
- **Module:** `ai_layer/ai_engine/intelligence_runtime.py`
- **Layer:** AI Layer
- **Sabab:** Composition root — "the one file... permitted to import
  every Intelligence layer at once" (fayl docstring'i).
- **Evidence:** `tests/ai/test_intelligence_runtime_isolation.py:10` —
  `module_file = pathlib.Path(__file__).resolve().parents[2] / "ai_layer" / "ai_engine" / "intelligence_runtime.py"`, keyin `ast.parse(module_file.read_text())`.
- **Confidence:** Yuqori
- **Status:** Active

### 5. monitoring_commands.py
- **Module:** `platform_layer/telegram/owner/monitoring_commands.py`
- **Layer:** Platform Layer
- **Sabab:** `_owner_commands_file()` helper orqali literal yo'l qurilib
  `ast.parse()` bilan o'qiladi.
- **Evidence:** `tests/monitoring/test_monitoring_isolation.py:23` —
  `return pathlib.Path(__file__).resolve().parents[2] / "platform_layer" / "telegram" / "owner" / "monitoring_commands.py"`,
  66-qatorda `_imported_names(_owner_commands_file())`.
- **Confidence:** Yuqori
- **Status:** Active

### 6. knowledge_manager.py
- **Module:** `ai_layer/knowledge_ai/knowledge_base/knowledge_manager.py`
- **Layer:** AI Layer
- **Sabab:** Literal yo'l bilan qattiq bog'langan izolyatsiya testi.
- **Evidence:** `tests/knowledge/test_knowledge_manager.py:77` —
  `manager_file = pathlib.Path(__file__).resolve().parents[2] / "ai_layer" / "knowledge_ai" / "knowledge_base" / "knowledge_manager.py"`, keyin `ast.parse(manager_file.read_text())`.
- **Confidence:** Yuqori
- **Status:** Active

### 7. conversation_adapters.py
- **Module:** `ai_layer/personal_ai/interaction_manager/conversation_adapters.py`
- **Layer:** AI Layer
- **Sabab:** "Intelligence Dependency Principle"ning nazorat nuqtasi.
- **Evidence:** `tests/ai/conversation/test_conversation_adapters.py:60` —
  `adapters_file = pathlib.Path(__file__).resolve().parents[3] / "ai_layer" / "personal_ai" / "interaction_manager" / "conversation_adapters.py"`.
- **Confidence:** Yuqori
- **Status:** Active

### 8. content_adapters.py
- **Module:** `ai_layer/ai_service/content/content_adapters.py`
- **Layer:** AI Layer
- **Sabab:** Literal yo'l bilan qattiq bog'langan izolyatsiya testi.
- **Evidence:** `tests/ai/content/test_content_adapters.py:80` —
  `adapters_file = pathlib.Path(__file__).resolve().parents[3] / "ai_layer" / "ai_service" / "content" / "content_adapters.py"`.
- **Confidence:** Yuqori
- **Status:** Active

### 9. reasoning_adapters.py
- **Module:** `ai_layer/ai_engine/reasoning/reasoning_adapters.py`
- **Layer:** AI Layer
- **Sabab:** Literal yo'l bilan qattiq bog'langan izolyatsiya testi.
- **Evidence:** `tests/ai/reasoning/test_reasoning_adapters.py:54` —
  `adapters_file = pathlib.Path(__file__).resolve().parents[3] / "ai_layer" / "ai_engine" / "reasoning" / "reasoning_adapters.py"`.
- **Confidence:** Yuqori
- **Status:** Active

---

## 10–11: Kengaytirilgan qidiruvda topilgan yangi holatlar — Media Layer (for-loop naqshi)

Ikkalasi ham bitta testda, `for filename in (...)` sikli ichida
**har bir fayl uchun alohida** literal yo'l qurib, `.read_text()` +
`ast.parse()` bilan o'qiladi — mezonning (a) va (b) shartlariga to'liq
mos keladi, faqat bir nechta modul bitta test funksiyasida qamrab
olingan, xolos (bu holat avvalgi ikkala audit metodologiyasida ham
qidirilmagan edi).

### 10. media_adapter.py
- **Module:** `media_layer/content_manager/media_adapter.py`
- **Layer:** Media Layer
- **Sabab:** "Intelligence Dependency Principle" bo'yicha media/
  translation/broadcast'ni import qilmasligini tekshiruvchi test bu
  faylni nomi bo'yicha literal ravishda qurib, `ast.parse()` bilan
  diskdan o'qiydi.
- **Evidence:** `tests/media/test_media_adapter.py:90-92` —
  `for filename in ("media_adapter.py", "media_pipeline.py"): module_file = pathlib.Path(__file__).resolve().parents[2] / "media_layer" / "content_manager" / filename; tree = ast.parse(module_file.read_text(), filename=str(module_file))`.
- **Confidence:** Yuqori
- **Status:** Active

### 11. media_pipeline.py
- **Module:** `media_layer/content_manager/media_pipeline.py`
- **Layer:** Media Layer
- **Sabab:** Xuddi shu test funksiyasi, xuddi shu siklda — filename
  ro'yxatidagi ikkinchi fayl.
- **Evidence:** `tests/media/test_media_adapter.py:90-92` (yuqoridagi bilan bir xil qator, `filename` o'zgaruvchisi "media_pipeline.py" bo'lganida).
- **Confidence:** Yuqori
- **Status:** Active

---

## 12–20: Kengaytirilgan qidiruvda topilgan yangi holatlar — core_layer/health_monitor (for-loop naqshi)

`core_layer/health_monitor/` paketi ichidagi 9 ta flat modul uchtа
alohida testda `for filename in (...)` sikli orqali (yoki `NEW_FILES`
konstantasi orqali) individual ravishda literal yo'l qurilib
`_imported_names()` helper (= `ast.parse(py_file.read_text())`) orqali
o'qiladi. Bu 9 fayl — `system_monitor.py`, `market_monitor.py`,
`signal_monitor.py`, `error_monitor.py`, `models.py`, `resource_monitor.py`,
`health_monitor.py`, `performance_collector.py`, `access.py` — hammasi
`core_layer/health_monitor/` paketining o'zi ichidagi flat fayllar
(paket allaqachon mavjud, lekin ichidagi individual fayllar GEL-001'ning
"bitta canonical modul = bitta paket" qoidasi nuqtai nazaridan alohida
kandidat modullar hisoblanadi, chunki `<stem>/<stem>.py`
konvensiyasiga mos emas).

### 12. system_monitor.py
- **Module:** `core_layer/health_monitor/system_monitor.py`
- **Evidence:** `tests/monitoring/test_monitoring_isolation.py:96-98` —
  `for filename in ("system_monitor.py", "market_monitor.py", "signal_monitor.py", "error_monitor.py", "models.py"): py_file = _monitoring_dir() / filename; for name in _imported_names(py_file): ...` (`_imported_names` 27-qatorda `ast.parse(py_file.read_text(), ...)`).
- **Layer:** Core Layer
- **Sabab:** `strategy_layer`/`signal_layer` import qilmasligini
  tasdiqlaydigan test bu faylni nomi bo'yicha literal qurib o'qiydi.
- **Confidence:** Yuqori
- **Status:** Active

### 13. market_monitor.py
- **Module:** `core_layer/health_monitor/market_monitor.py`
- **Layer:** Core Layer
- **Sabab:** Xuddi shu sikl, ro'yxatdagi ikkinchi fayl.
- **Evidence:** `tests/monitoring/test_monitoring_isolation.py:96` (yuqoridagi bilan bir xil qator).
- **Confidence:** Yuqori
- **Status:** Active

### 14. signal_monitor.py
- **Module:** `core_layer/health_monitor/signal_monitor.py`
- **Layer:** Core Layer
- **Sabab:** Xuddi shu sikl, ro'yxatdagi uchinchi fayl.
- **Evidence:** `tests/monitoring/test_monitoring_isolation.py:96`.
- **Confidence:** Yuqori
- **Status:** Active

### 15. error_monitor.py
- **Module:** `core_layer/health_monitor/error_monitor.py`
- **Layer:** Core Layer
- **Sabab:** Xuddi shu sikl, ro'yxatdagi to'rtinchi fayl.
- **Evidence:** `tests/monitoring/test_monitoring_isolation.py:96`.
- **Confidence:** Yuqori
- **Status:** Active

### 16. models.py (core_layer/health_monitor)
- **Module:** `core_layer/health_monitor/models.py`
- **Layer:** Core Layer
- **Sabab:** Ikki testda ishlatiladi: (i) yuqoridagi sikldagi beshinchi
  fayl, (ii) `test_monitoring_models_are_primitive_only` alohida
  literal yo'l bilan.
- **Evidence:** `tests/monitoring/test_monitoring_isolation.py:96` (sikl)
  va `tests/monitoring/test_monitoring_isolation.py:80` —
  `models_file = _monitoring_dir() / "models.py"`, keyin `_imported_names(models_file)`.
- **Confidence:** Yuqori
- **Status:** Active

### 17. resource_monitor.py
- **Module:** `core_layer/health_monitor/resource_monitor.py`
- **Layer:** Core Layer
- **Sabab:** Phase B.0 fayllari uchun uch alohida testda (`NEW_FILES`
  konstantasi orqali) va yana bir alohida "confined to" testida literal
  yo'l bilan o'qiladi.
- **Evidence:** `tests/monitoring/test_phase_b0_isolation.py:11,31,54` —
  `NEW_FILES = ("resource_monitor.py", ...)`, `py_file = _monitoring_dir() / filename` va `py_file = _monitoring_dir() / "resource_monitor.py"`; shuningdek `tests/monitoring/test_phase_b0_compatibility.py:35-37`.
- **Confidence:** Yuqori
- **Status:** Active

### 18. health_monitor.py
- **Module:** `core_layer/health_monitor/health_monitor.py`
- **Layer:** Core Layer
- **Evidence:** `tests/monitoring/test_phase_b0_isolation.py:61,83` —
  `py_file = _monitoring_dir() / "health_monitor.py"`; shuningdek `tests/monitoring/test_phase_b0_compatibility.py:35-37`.
- **Sabab:** Xuddi shu Phase B.0 for-loop va alohida "confined"/"never
  imports database" testlari.
- **Confidence:** Yuqori
- **Status:** Active

### 19. performance_collector.py
- **Module:** `core_layer/health_monitor/performance_collector.py`
- **Layer:** Core Layer
- **Evidence:** `tests/monitoring/test_phase_b0_isolation.py:68,90` —
  `py_file = _monitoring_dir() / "performance_collector.py"`; shuningdek `tests/monitoring/test_phase_b0_compatibility.py:35-37`.
- **Sabab:** Xuddi shu Phase B.0 for-loop va alohida testlar.
- **Confidence:** Yuqori
- **Status:** Active

### 20. access.py (core_layer/health_monitor)
- **Module:** `core_layer/health_monitor/access.py`
- **Layer:** Core Layer
- **Evidence:** `tests/monitoring/test_phase_b0_isolation.py:75` —
  `py_file = _monitoring_dir() / "access.py"`; shuningdek `tests/monitoring/test_phase_b0_compatibility.py:35-37`.
- **Sabab:** Xuddi shu Phase B.0 for-loop va "confined to configuration
  feature flags" testi.
- **Confidence:** Yuqori
- **Status:** Active

---

## Ko'rib chiqilgan, lekin exception EMAS deb topilgan qo'shimcha holatlar

- 110 ta `mock.patch(`/`monkeypatch.setattr(` chaqiruvi (24 faylda) —
  barchasi dotted-path nishonlar, OS fayl yo'liga bog'liq emas.
- 6 ta `inspect.getsource(imported_module)` chaqiruvi (`tests/ai/
  test_context_memory.py`, `test_user_profile.py`,
  `test_intelligence_runtime.py`, `test_prompt_manager.py`,
  `tests/ai/router/test_provider_score.py`,
  `tests/platforms/test_navigation_model.py`) — import qilingan modul
  obyekti orqali ishlaydi, literal yo'l qurilmaydi.
- `database_layer/database_manager/database.py`ning
  `.exists()`-only tekshiruvi (`tests/deploy/test_deploy_scripts_shape.py:326`) —
  faylni o'qimaydi/tahlil qilmaydi.
- Deploy/systemd/contracts fayllarini tekshiruvchi barcha `.exists()`/
  `.is_file()` chaqiruvlari (`tests/deploy/*.py`,
  `tests/contracts/test_contracts_exist.py`) — bular shell-skript,
  systemd unit, yoki hujjat fayllarini tekshiradi, Python modul emas.
- `_learning_dir()`/`_coaching_dir()` ichidagi "modul MAVJUD EMAS"
  salbiy `.exists()` testlari — o'chirilgan modullarni tasdiqlaydi,
  literal o'qish/tahlil yo'q.
- `importlib.resources`, `pkgutil` — repo bo'yicha birorta ishlatilishi
  topilmadi.
- 33 dan ortiq `rglob("*.py")` asosidagi izolyatsiya testlari — butun
  katalogni skanerlaydi, muayyan bitta faylga bog'lanmagan.

## Yakuniy xulosa

**Tasdiqlangan Compatibility Exception soni: 20.** DD-005'ning asl 11
raqami ham, avvalgi tor audit topgan 9 raqami ham **empirik jihatdan
tasdiqlanmadi** — haqiqiy son ikkalasidan ham katta. Farqning yagona
sababi — metodologiya torligi: ikkala oldingi audit ham faqat "bitta
test = bitta literal Path" naqshini qidirgan, ammo bir nechta modulni
bitta `for`-siklida ketma-ket literal yo'l bilan o'qiydigan testlar
mavjud edi va ular e'tibordan chetda qolgan edi.

**Ushbu farq Director Review talab qiladi.** Ushbu reyestrda hech qanday
xayoliy (fabricated) yozuv yo'q — barcha 20 yozuv aniq test fayli, aniq
qator raqami va aniq kod parchasi bilan tasdiqlangan.
