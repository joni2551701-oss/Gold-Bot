# Migration Tracker — goldbot-v1

Status: Phase B IN PROGRESS
Boshlanish: 2026-08-03
Asos: `FOUNDATION_FREEZE_V1.md` (Foundation Freeze v1.0)
Buyruq: Director Order No. 002 — Migration Strategy

---

# Migratsiya Qoidalari

**Migration Isolation Rule (MIR-001)** — har bir migratsiya commiti bitta modul yoki bitta kichik subsystem bilan cheklanadi. Bir commitda bir nechta Layer yoki katta hajmdagi ko'chirish amalga oshirilmaydi.

**Import Compatibility Rule (ICR-001)** — migratsiya davomida eski importlar vaqtincha ishlashi mumkin va compatibility wrapper yaratish mumkin, ammo Foundation Freeze arxitekturasi o'zgarmaydi.

---

# Fizik Joylashuv (Director Order No. 006)

Har bir Layer o'z hujjatlari **va** Python kodini bir papkada saqlaydi — bitta Source of Truth:

```text
core_layer/
├── README.md  Layer_Contracts.md  Layer_ModuleMap.md  Layer_DataFlow.md  Layer_SequenceDiagram.md
├── configuration/
│   ├── README.md  Contracts.md  ModuleMap.md  SequenceDiagram.md
│   ├── IMPLEMENTATION.md          (paketning o'z eski README'si)
│   └── settings.py  feature_flags.py  runtime_state.py  …
└── secrets/
    ├── README.md  Contracts.md  ModuleMap.md  SequenceDiagram.md
    └── secrets.py
```

**Nomlash:** Layer va modul papkalari snake_case, raqamsiz — `data_layer`, `core_layer`, `ai_layer`. Sabab: Python moduli nomi raqam bilan boshlana olmaydi (`import 02_Core_Layer` → `SyntaxError`). Canonical tartib (01…17) faqat `ARCHITECTURE.md`, `FOUNDATION_FREEZE_V1.md` va boshqa arxitektura hujjatlarida saqlanadi.

**`goldbot/` olib tashlandi.** U Phase A–B.3 davomida vaqtinchalik migratsiya vositasi bo'lgan; Order No. 006 bo'yicha uning tarkibi tegishli Layer papkalariga ko'chirildi va namespace butunlay yo'q qilindi. Import `goldbot.core_layer.X` o'rniga `core_layer.X` bo'ldi.

Eski pre-freeze paketlar (`core/`, `data/`, `ai/`, `risk/` va h.k.) migratsiya davomida o'z joyida ishlab turadi va Phase E'da olib tashlanadi.

---
# Bosqichlar

| Phase | Qamrov | Holat |
|---|---|---|
| A | Skeleton — papka strukturasi, `__init__.py`, README havolalari | ✅ COMPLETE |
| B | Infrastructure — Configuration → Secrets → Core → Event → Performance → Database | 🔄 2/6 |
| C_OLD | Trading Pipeline — Data → Context → Indicator → Strategy → Signal → AI → Decision → Risk → Execution → Trade Monitoring | ⏳ |
| D | Platform — Telegram, API, Media, Chart | ⏳ |
| E | Cleanup — eski kodni olib tashlash, duplicate yo'qotish, TODO yopish | ⏳ |

---

# Phase A Natijasi

```text
Layers ............... 17
Module packages ...... 210
Total packages ....... 236   (1 root + 17 layer + 218 module/group)
Importable ........... 236/236
Broken README links .. 0
Business code moved .. 0   (Phase A bo'yicha ataylab)
```

| Canonical Layer | Python package | Modullar |
|---|---|---|
| 01_Data_Layer | `data_layer` | 38 |
| 02_Core_Layer | `core_layer` | 12 |
| 03_Context_Layer | `context_layer` | 11 |
| 04_Indicator_Layer | `indicator_layer` | 9 |
| 05_Strategy_Layer | `strategy_layer` | 17 |
| 06_Signal_Layer | `signal_layer` | 7 |
| 07_AI_Layer | `ai_layer` | 39 |
| 08_Decision_Layer | `decision_layer` | 6 |
| 09_Risk_Layer | `risk_layer` | 8 |
| 10_Execution_Layer | `execution_layer` | 7 |
| 11_Trade_Monitoring_Layer | `trade_monitoring_layer` | 9 |
| 12_Database_Layer | `database_layer` | 9 |
| 13_Platform_Layer | `platform_layer` | 7 |
| 14_Media_Layer | `media_layer` | 3 |
| 15_Future_Expansion | `future_expansion` | 0 |
| 16_Chart_Layer | `chart_layer` | 20 |
| 17_Backtesting_Layer | `backtesting_layer` | 8 |

---

# Modul Migratsiya Holati

Har bir modul ko'chirilganda quyidagi jadval yangilanadi. Hozircha barcha modullar `SKELETON` holatida — biznes mantiq hali eski paketlarda.

Holat kodlari:
* `SKELETON` — paket mavjud, kod yo'q (Phase A)
* `MIGRATED` — kod ko'chirilgan, importlar tuzatilgan, testlar o'tgan
* `REFACTORED` — ko'chirilgan kod yangi arxitektura contract'iga moslashtirilgan
* `IMPLEMENTED` — hujjatlashtirilgan, lekin eski kodda mavjud bo'lmagan modul yozilgan

**Migration Validation Rule (MVR-001)** — har bir modul migratsiyasidan keyin: import tekshiruvi, unit testlar, eski/yangi namespace parity (agar modul ishlatilayotgan bo'lsa), commit.

## Phase B — Infrastructure

Director tomonidan tasdiqlangan tartib: Configuration → Secrets → Core → Event → Performance → Database.

| # | Modul | Canonical package | Holat | Izoh |
|---|---|---|---|---|
| 1 | Configuration | `core_layer.configuration` | ✅ MIGRATED | 9 fayl ko'chirildi, 68 fayldagi importlar yangilandi, wrapper yaratilmadi |
| 2 | Secrets | `core_layer.secrets` | ✅ MIGRATED | faqat `core/secrets.py`; `config.py` Director qarori bo'yicha tegilmadi (SMR-001) |
| 3 | Core | `core_layer.*` | 🔄 | Pipeline ✅; qolgani xaritalanmoqda — quyidagi jadvalga qarang |
| 4 | Event | `data_layer.event_system` | ⏳ | |
| 5 | Performance | `core_layer.performance` | ⏳ | |
| 6 | Database | `database_layer.*` | ⏳ | |

### 1. Configuration — MIGRATED

```text
configuration/environment.py                  -> core_layer/configuration/environment.py
configuration/settings.py                     -> core_layer/configuration/settings.py
configuration/feature_flags.py                -> core_layer/configuration/feature_flags.py
configuration/feature_registry.py             -> core_layer/configuration/feature_registry.py
configuration/feature_dependency_validator.py -> core_layer/configuration/feature_dependency_validator.py
configuration/runtime_state.py                -> core_layer/configuration/runtime_state.py
configuration/runtime_api.py                  -> core_layer/configuration/runtime_api.py
configuration/runtime_feature_manager.py      -> core_layer/configuration/runtime_feature_manager.py
configuration/README.md                       -> core_layer/configuration/README.md
```

Compatibility wrapper **yaratilmadi**: 68 fayldagi importlar to'g'ridan-to'g'ri yangilandi. ICR-001 wrapper'ga ruxsat beradi, lekin bu holatda to'g'ridan-to'g'ri yangilash Phase E'da tozalanadigan o'lik qatlam qoldirmadi va qaysi yo'l canonical ekanligida noaniqlik yaratmadi.

Yon ta'sir: 8 ta arxitektura-izolyatsiya testida ruxsat etilgan import prefiksi `"configuration"` → `"core_layer.configuration"` deb yangilandi. Testlarning kuchi kamaymadi — ular xuddi shu izolyatsiyani yangi yo'l bo'yicha tekshiradi.

MVR-001 natijasi: import ✅ · pyflakes ✅ · compileall ✅ · pytest 5400/5400 ✅ · `python main.py` ✅

### 2. Secrets — MIGRATED

```text
core/secrets.py -> core_layer/secrets/secrets.py
```

`Secrets` paket darajasida re-export qilindi, shuning uchun chaqiruvchilar `from core_layer.secrets import Secrets` deb yozadi — fayl nomi takrorlanmaydi.

20 ta importer yangilandi. Wrapper yaratilmadi (Configuration bilan bir xil sabab).

**`config.py` tegilmadi.** Director Decision (Phase B.2): migratsiya vaqtida `config.py`ni Configuration va Secrets domenlariga ajratish taqiqlanadi — bu bir commit ichida migratsiya, refactoring va import o'zgarishini aralashtirardi. `MaskedSecret` `config.py`da qoladi. KG-001 / RT-001 / RT-002 migratsiya to'liq yakunlangandan keyingi refactoring bosqichida (Phase E'dan keyin yoki Implementation v1.1'da) bajariladi. Yangi ACR: **Stable Migration Rule (SMR-001)**.

MVR-001 natijasi: import ✅ · eski/yangi parity ✅ · pyflakes ✅ · compileall ✅ · pytest 5400/5400 ✅ · `python main.py` ✅

### 3. Core — IN PROGRESS

`core/` da 34 ta `.py` fayl bor. Canonical `02_Core_Layer` esa 12 modulga bo'lingan. Xaritalash real kod mas'uliyatiga qarab bajarildi:

| Real kod | Canonical modul | Holat |
|---|---|---|
| `core/pipeline.py` | `Pipeline` | ✅ MIGRATED |
| `core_layer/gateway/service_registry.py`, `service_manifest.py`, `service_state.py`, `service.py` | `ServiceRegistry` | ⏳ |
| `core_layer/gateway/health_service.py` | `HealthMonitor` | ⏳ |
| `core_layer/gateway/metrics_service.py` | `Performance` | ⏳ |
| `core_layer/gateway/gateway.py` (CoreGateway facade) | `CoreService` (?) | ❓ Director |
| `core_layer/emergency/` (4 fayl) | — | ❓ Director |
| `core_layer/errors/` (3 fayl) | — | ❓ Director |
| `core_layer/pipeline/pipeline_guard.py` | — | ❓ Director |
| `core_layer/gateway/` qolgan 11 fayl (auth, authz, rate_limiter, router, service_breaker, version, dependency_graph, gateway_context/events/request) | — | ❓ Director |
| `core_layer/logger/logger.py` (129 importer) | — | ❓ Director |
| `core_layer/secrets/phone_hash.py` | — | ❓ Director |
| `core_layer/system_state/system_state.py` | — | ❓ Director |

`❓ Director` bilan belgilanganlar uchun canonical modul mavjud emas. WAR-007 bo'yicha yangi modul yaratish Director Review talab qiladi — Worker o'zi modul o'ylab topmaydi.

#### 3.1 Pipeline — MIGRATED

```text
core/pipeline.py -> core_layer/pipeline/pipeline.py
```

`TradingPipeline` paket darajasida re-export qilindi. 10 ta fayl yangilandi (4 ta haqiqiy importer + 6 ta docstring/prose havolasi). SMR-001 bo'yicha fayl ichi tegilmagan — Data→Context→Signal→AI→Decision→Risk→Telegram oqimi va notification-eligibility filtri o'zgarmagan.

MVR-001: import ✅ · parity ✅ · pyflakes ✅ · compileall ✅ · pytest 5400/5400 ✅ · `main.py` ✅

### 3.2 core/ — to'liq ko'chirildi (Phase C)

`core/` paketi butunlay `core_layer/` ichiga ko'chirildi va o'chirildi.

| Manba | Manzil | Turi |
|---|---|---|
| `core/pipeline.py` | `core_layer/pipeline/pipeline.py` | mavjud canonical modul |
| `core/guards/pipeline_guard.py` | `core_layer/pipeline/pipeline_guard.py` | mavjud modulga merge |
| `core/phone_hash.py` | `core_layer/secrets/phone_hash.py` | mavjud modulga merge |
| `core/gateway/` (17 fayl) | `core_layer/gateway/` | **yangi canonical modul** |
| `core/emergency/` (4 fayl) | `core_layer/emergency/` | **yangi canonical modul** |
| `core/errors/` (3 fayl) | `core_layer/errors/` | **yangi canonical modul** |
| `core/logger.py` | `core_layer/logger/logger.py` | **yangi canonical modul** |
| `core/system_state.py` | `core_layer/system_state/system_state.py` | **yangi canonical modul** |

Besh yangi canonical modul Director Order No. 005 asosida qo'shildi — u aynan **Gateway, Emergency, Error Handling, Logger, System State**ni nomlab, "agar ular alohida mas'uliyatga ega bo'lsa, alohida canonical modul bo'ladi" degan edi. WAR-006 (Decision Memory) bo'yicha qayta so'ralmadi. Har biriga to'liq 4 ta canonical hujjat yozildi.

`core/gateway/` SMR-001 bo'yicha **butun holicha** ko'chirildi — u ichki importlarga ega ishlaydigan paket, migratsiya vaqtida bo'linmadi.

**Known Gap (Phase F uchun):** `core_layer/service_registry/`, `core_layer/health_monitor/` va `core_layer/performance/` canonical modullari hujjatga ega, lekin ularning real implementatsiyasi `core_layer/gateway/` ichida (`service_registry.py`, `health_service.py`, `metrics_service.py`). Bu bo'linish SMR-001 bo'yicha migratsiyadan keyingi refactoring bosqichiga qoldirildi.

Joriy holat: **`core/` yo'q. `core_layer/` — 17 modul, hujjat va kod birga.**

### 3.3 data/ — to'liq ko'chirildi (Phase C, WAR-010 tartibi bo'yicha birinchi)

`data/` paketi (93 `.py`, 9 quyi paket) butunlay ko'chirildi va o'chirildi.

| Manba | Manzil |
|---|---|
| `data/providers/` + `twelve_data_client.py`, `api_error_classifier.py`, `provider_comparison.py` | `data_layer/providers/` |
| `data/stream/` + `candle_builder.py`, `candle_clock.py`, `current_price_provider.py`, `session_filter.py`, `market_data*.py` | `data_layer/live_data/` |
| `data/memory/` + `data_cache.py` | `data_layer/market_memory/` |
| `data/persistence/` | `data_layer/market_memory/persistence/` |
| `data/bootstrap/` + `historical_data_collector.py` | `data_layer/historical_data/` |
| `data/events/` | `data_layer/event_system/` |
| `data/data_quality.py`, `historical_validator.py` | `data_layer/data_validation/` |
| `data/normalization/` | `data_layer/normalization/` |
| `data/snapshots/` | `data_layer/snapshots/` |
| `data/replay/` | `backtesting_layer/replay_engine/` |

WAR-009 bo'yicha hech bir paket ichidan bo'linmadi — har biri butun holicha ko'chirildi.

**Nom to'qnashuvi va yechimi.** Yetti fayl canonical skelet papkasi bilan bir xil nomda edi (`candle_builder.py` va `candle_builder/`, `event_bus.py` va `event_bus/` va h.k.) — Python bunday holatda paketni tanlaydi, fayl esa ko'rinmay qoladi. Har bir fayl o'z canonical papkasi ichiga kiritildi va paket `__init__.py` aniq eksportlar bilan qayta yozildi (`import *` emas — pyflakes uni qabul qilmaydi).

**Paket `__init__.py` mazmuni saqlandi.** `data/*/__init__.py` fayllari 37–100 qatorlik haqiqiy docstring va eksportlarga ega edi; ular canonical skelet stub'ining o'rniga ko'chirildi, canonical hujjat havolasi qo'shildi.

`data/README.md` va ikkita quyi README `IMPLEMENTATION.md` sifatida saqlandi.

**Known Gap (Phase E):** `data/replay/` (9 fayl) va `backtesting/replay_*.py` — ikkita alohida replay implementatsiyasi mavjud. Ikkalasi ham `backtesting_layer/replay_engine/` ichida; duplicate tekshiruvi Phase E vazifasi.

328 faylda importlar yangilandi.

---

# Summary

Phase A yakunlandi: Canonical Architecture'ning 17 Layer / 210 modul tuzilmasi (o'sha paytda `goldbot/` paketida) importga yaroqli skelet sifatida aks ettirildi. Hech qanday biznes kodi ko'chirilmadi — bu Phase B'dan boshlanadi.

---

# ✅ RESOLVED — Director Order No. 005/006 va Python import cheklovi

**Status:** Yopildi. Director Order No. 006 bilan hal qilindi — Layer papkalari snake_case, raqamsiz; kod Layer ichida; `goldbot/` olib tashlandi. Quyidagi tahlil qaror qanday qabul qilinganini qayd etadi.

Order No. 005 yakuniy maqsadni belgiladi: Python kod `goldbot/` da emas, Layer papkalari ichida yashashi kerak:

```text
02_Core_Layer/
├── README.md
├── Configuration/
│   ├── README.md
│   ├── Contracts.md
│   └── settings.py     ← kod shu yerda
```

## Texnik to'siq

Python moduli nomi raqam bilan boshlana olmaydi. Empirik tekshiruv (2026-08-03):

```text
from 02_Core_Layer.Configuration.settings import VALUE
                                                  ^
SyntaxError: invalid decimal literal

import 02_Core_Layer
             ^
SyntaxError: invalid decimal literal

importlib.import_module("02_Core_Layer.Configuration.settings")   -> ISHLAYDI
```

Ya'ni raqamli papka ichidagi kodni faqat `importlib.import_module()` orqali yuklash mumkin — oddiy `import` yoki `from ... import` bilan **hech qachon**. Bu 5400 test, ~1000 import nuqtasi, pyflakes, IDE va refactoring vositalari uchun yaroqsiz.

## Variantlar

| # | Yechim | Import ko'rinishi | Tartib ko'rinadimi | Idiomatik |
|---|---|---|---|---|
| 1 | Raqamli prefiksni olib tashlash: `data_layer/`, `core_layer/` | `from core_layer.configuration.settings import X` | ❌ (faqat hujjatda) | ✅ |
| 2 | Harf prefiksi: `l01_data_layer/`, `l02_core_layer/` | `from l02_core_layer.configuration.settings import X` | ✅ | ⚠️ |
| 3 | Hozirgi holat: hujjat raqamli papkada, kod `goldbot/` da | `from core_layer.configuration.settings import X` | ✅ | ✅ |
| 4 | Raqamli papka + hamma joyda `importlib` | `importlib.import_module("02_Core_Layer...")` | ✅ | ❌ yaroqsiz |

Variant 4 texnik jihatdan mumkin, lekin amalda ishlamaydi.

## Nega migratsiya to'xtatildi

Order No. 005: *"Agar bugungi qaror keyinchalik kodni yana ko'chirishga majbur qilsa, yaxshiroq yechimni tanlash kerak."*

Hozir `goldbot/` ichiga ko'chirishni davom ettirish aynan shunday holat yaratadi — variant 1 yoki 2 tanlansa, ko'chirilgan barcha kod ikkinchi marta ko'chiriladi. Shuning uchun Configuration, Secrets va Pipeline'dan keyin migratsiya to'xtatildi.

Layer papkalari nomini o'zgartirish Foundation Freeze tarkibiga tegadi (WAR-005 / WAR-007), shuning uchun Worker o'zi hal qilmadi.

**Yechim (Order No. 006):** Variant 1 tanlandi — raqamsiz snake_case. Layer papkalari `data_layer`, `core_layer`, `ai_layer` va h.k.; raqamli tartib faqat arxitektura hujjatlarida saqlanadi; kod va hujjat bir papkada; `goldbot/` butunlay olib tashlandi.

