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

# Fizik Joylashuv

Yangi arxitektura `goldbot/` namespace paketida joylashadi. Eski top-level paketlar (`core/`, `data/`, `ai/`, `risk/` va h.k.) migratsiya davomida o'z joyida ishlab turadi va Phase E'da olib tashlanadi.

Sabab: `goldbot/` yagona chegara beradi — eski va yangi kod aralashmaydi, rollback bitta papkani o'chirish bilan amalga oshadi, va 29 ta mavjud top-level paket bilan nom to'qnashuvi bo'lmaydi.

Nom konversiyasi: `01_Data_Layer` → `data_layer`, `HistoricalDataService` → `historical_data_service` (CamelCase → snake_case, raqamli prefiks olib tashlanadi).

---

# Bosqichlar

| Phase | Qamrov | Holat |
|---|---|---|
| A | Skeleton — papka strukturasi, `__init__.py`, README havolalari | ✅ COMPLETE |
| B | Infrastructure — Configuration → Secrets → Core → Event → Performance → Database | 🔄 2/6 |
| C | Trading Pipeline — Data → Context → Indicator → Strategy → Signal → AI → Decision → Risk → Execution → Trade Monitoring | ⏳ |
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
| 01_Data_Layer | `goldbot.data_layer` | 38 |
| 02_Core_Layer | `goldbot.core_layer` | 12 |
| 03_Context_Layer | `goldbot.context_layer` | 11 |
| 04_Indicator_Layer | `goldbot.indicator_layer` | 9 |
| 05_Strategy_Layer | `goldbot.strategy_layer` | 17 |
| 06_Signal_Layer | `goldbot.signal_layer` | 7 |
| 07_AI_Layer | `goldbot.ai_layer` | 39 |
| 08_Decision_Layer | `goldbot.decision_layer` | 6 |
| 09_Risk_Layer | `goldbot.risk_layer` | 8 |
| 10_Execution_Layer | `goldbot.execution_layer` | 7 |
| 11_Trade_Monitoring_Layer | `goldbot.trade_monitoring_layer` | 9 |
| 12_Database_Layer | `goldbot.database_layer` | 9 |
| 13_Platform_Layer | `goldbot.platform_layer` | 7 |
| 14_Media_Layer | `goldbot.media_layer` | 3 |
| 15_Future_Expansion | `goldbot.future_expansion` | 0 |
| 16_Chart_Layer | `goldbot.chart_layer` | 20 |
| 17_Backtesting_Layer | `goldbot.backtesting_layer` | 8 |

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
| 1 | Configuration | `goldbot.core_layer.configuration` | ✅ MIGRATED | 9 fayl ko'chirildi, 68 fayldagi importlar yangilandi, wrapper yaratilmadi |
| 2 | Secrets | `goldbot.core_layer.secrets` | ✅ MIGRATED | faqat `core/secrets.py`; `config.py` Director qarori bo'yicha tegilmadi (SMR-001) |
| 3 | Core | `goldbot.core_layer.*` | ⏳ | |
| 4 | Event | `goldbot.data_layer.event_system` | ⏳ | |
| 5 | Performance | `goldbot.core_layer.performance` | ⏳ | |
| 6 | Database | `goldbot.database_layer.*` | ⏳ | |

### 1. Configuration — MIGRATED

```text
configuration/environment.py                  -> goldbot/core_layer/configuration/environment.py
configuration/settings.py                     -> goldbot/core_layer/configuration/settings.py
configuration/feature_flags.py                -> goldbot/core_layer/configuration/feature_flags.py
configuration/feature_registry.py             -> goldbot/core_layer/configuration/feature_registry.py
configuration/feature_dependency_validator.py -> goldbot/core_layer/configuration/feature_dependency_validator.py
configuration/runtime_state.py                -> goldbot/core_layer/configuration/runtime_state.py
configuration/runtime_api.py                  -> goldbot/core_layer/configuration/runtime_api.py
configuration/runtime_feature_manager.py      -> goldbot/core_layer/configuration/runtime_feature_manager.py
configuration/README.md                       -> goldbot/core_layer/configuration/README.md
```

Compatibility wrapper **yaratilmadi**: 68 fayldagi importlar to'g'ridan-to'g'ri yangilandi. ICR-001 wrapper'ga ruxsat beradi, lekin bu holatda to'g'ridan-to'g'ri yangilash Phase E'da tozalanadigan o'lik qatlam qoldirmadi va qaysi yo'l canonical ekanligida noaniqlik yaratmadi.

Yon ta'sir: 8 ta arxitektura-izolyatsiya testida ruxsat etilgan import prefiksi `"configuration"` → `"goldbot.core_layer.configuration"` deb yangilandi. Testlarning kuchi kamaymadi — ular xuddi shu izolyatsiyani yangi yo'l bo'yicha tekshiradi.

MVR-001 natijasi: import ✅ · pyflakes ✅ · compileall ✅ · pytest 5400/5400 ✅ · `python main.py` ✅

### 2. Secrets — MIGRATED

```text
core/secrets.py -> goldbot/core_layer/secrets/secrets.py
```

`Secrets` paket darajasida re-export qilindi, shuning uchun chaqiruvchilar `from goldbot.core_layer.secrets import Secrets` deb yozadi — fayl nomi takrorlanmaydi.

20 ta importer yangilandi. Wrapper yaratilmadi (Configuration bilan bir xil sabab).

**`config.py` tegilmadi.** Director Decision (Phase B.2): migratsiya vaqtida `config.py`ni Configuration va Secrets domenlariga ajratish taqiqlanadi — bu bir commit ichida migratsiya, refactoring va import o'zgarishini aralashtirardi. `MaskedSecret` `config.py`da qoladi. KG-001 / RT-001 / RT-002 migratsiya to'liq yakunlangandan keyingi refactoring bosqichida (Phase E'dan keyin yoki Implementation v1.1'da) bajariladi. Yangi ACR: **Stable Migration Rule (SMR-001)**.

MVR-001 natijasi: import ✅ · eski/yangi parity ✅ · pyflakes ✅ · compileall ✅ · pytest 5400/5400 ✅ · `python main.py` ✅

Joriy holat: **210 moduldan 2 tasi MIGRATED, 208 tasi SKELETON**.

---

# Summary

Phase A yakunlandi: Canonical Architecture'ning 17 Layer / 210 modul tuzilmasi `goldbot/` paketida importga yaroqli skelet sifatida aks ettirildi. Hech qanday biznes kodi ko'chirilmadi — bu Phase B'dan boshlanadi.
