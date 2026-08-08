# PROJECT_STATUS.md — GoldBot Boshqaruv Paneli

Status: Living Document (har muhim o'zgarishda yangilanadi)
Oxirgi yangilanish: 2026-08-05
Til: GLS-001 (proza O'zbek, texnik terminlar English)

> Bu hujjat GoldBot'ning yagona "boshqaruv paneli". Bitta faylni ochib,
> loyiha qaysi holatda ekanini darhol ko'rish mumkin. U yangi qaror
> yoki manba (SSOT) emas — mavjud hujjatlardagi holatni jamlaydi.

---

## 1. Phase holati

| Phase | Nomi | Status |
|---|---|---|
| PHASE-01 | Foundation Architecture | ✅ Approved (Foundation Frozen) |
| PHASE-02 | Flow-by-Flow Development | ✅ Completed (2026-08-07 — FLOW-016/017/018/019 barchasi CI bilan tasdiqlangan; batafsil `docs/PHASE_02_FLOW_BY_FLOW_DEVELOPMENT.md`) |
| PHASE-03 | Release Preparation | 🟡 In Progress (Branch Cleanup → release/v1.0.0-rc1 → Final Release Audit → Final Validation → main Promotion → VPS Deployment → Production Monitoring) |
| PHASE-04 | Evolution & Next Sprint | ⏳ Pending |

---

## 2. Joriy holat (snapshot)

| Maydon | Qiymat |
|---|---|
| Current Phase | PHASE-02 — Flow-by-Flow Development |
| Current Sprint | PHASE-02 Sprint 1 (standart o'rnatildi: `docs/PHASE_02_FLOW_BY_FLOW_DEVELOPMENT.md`) |
| Current Flow | FLOW-019 ✅ Completed (2026-08-07, PHASE-02 Final Sprint, Director scope korreksiyasi + DRQ-001 Option B). FLOW-019'ning haqiqiy nishoni — Application/Service Layer'ni Telegram orqali Production holatiga olib chiqish — allaqachon bajarilgan edi (`platform_layer/telegram/*_service.py`, 9 ta servis, jonli, test qilingan). `PlatformService`/`platform_service` (PlatformRegistry/MenuRegistry/NavigationCore) FLOW-019'ning nishoni emas edi — bu alohida, kelajakdagi ko'p-platformali (Mobile/Desktop/Web) abstraction, Foundation'da ataylab saqlanadi (`docs/FLOW_019_APPLICATION_SERVICES_FOUNDATION.md`). FLOW-018 ✅ Completed (2026-08-06, Backtesting Engine, `/backtest`). FLOW-017 ✅ Completed (Personal AI, `/ask`). Qolgan: FLOW-021-025 🟦 Blueprint. Reja: `docs/FLOW_017_025_PRODUCTION_REAUDIT.md`. |
| Production Readiness | GoldBot Core pipeline production-ready (V1.0 Freeze); non-Telegram Platform clients (Mini App/Android/iOS/Desktop/Web) Blueprint |
| Test Status | ✅ 5432 passed (0 fail) |
| Latest Director Decision | PHASE-02 Flow-by-Flow Development Initialization (2026-08-05) |
| Latest Stable Commit | goldbot-v1 — oxirgi push, GitHub Actions: SUCCESS |
| Branch | `goldbot-v1` (canonical, DD-002) |

---

## 3. Foundation Freeze (o'zgarmas asos)

Quyidagilar Foundation hisoblanadi va faqat RFC / ADR / Director
Decision / Architecture Migration orqali o'zgartiriladi (oddiy
Development jarayonida emas):

- GoldBot V3 Architecture (`docs/architecture/`)
- GDL-001 — Development Lifecycle (`docs/GDL-001_GOLDBOT_DEVELOPMENT_LIFECYCLE.md`)
- GFL-001 — Flow-First Standard (`docs/GFL-001_FLOW_FIRST_STANDARD.md` + oila)
- GEL-001 — Canonical Module = Package (`docs/GEL-001_CANONICAL_MODULE_STANDARD.md`)
- GLS-001 — Translation Standard (`docs/GLS-001_TRANSLATION_STANDARD.md`)
- Foundation Standards (`docs/standards/`, `docs/policies/`)
- Governance Standards (`docs/constitution/`, `docs/governance/`)

To'liq PHASE-01 hisoboti: `docs/PHASE_01_FOUNDATION_ARCHITECTURE.md`.

---

## 4. Development yo'nalishi

```
PHASE-01 Foundation Architecture   ✅ FROZEN
        ▼
PHASE-02 Flow-by-Flow Development   🟡 (Foundation ustiga quriladi)
        ▼
PHASE-03 Validation & Director Review   ⏳
        ▼
PHASE-04 Evolution & Next Sprint    ⏳
```

PHASE-02 qoidalari:
- Foundation o'zgarmaydi.
- Development faqat Foundation ustiga quriladi.
- Har qanday yangi modul Foundation qoidalariga (GEL-001, GFL-001,
  MIR-001, Module Reuse Principle) mos bo'lishi shart.

---

## 5b. Production Boundary (REAL-DATA-011 audited, 2026-08-08)

REAL-DATA-011 (production boundary completion audit,
`audits/REAL_DATA_VERIFICATION/REAL_DATA_011/`) tomonidan tasdiqlangan
haqiqiy holat — hech narsa jimgina o'zgartirilmadi:

- **data → risk spine = PASS** (real runtime). Current-price stream
  (008) `TwelveDataPriceSource` orqali; batch candle path
  `data_normalizer.get_candles()` orqali (`core_layer/pipeline/pipeline.py:325`);
  MarketMemory SSOT (REAL-DATA-003, regressiya yo'q); `RiskManager.evaluate()`
  (`pipeline.py:495`).
- **Risk'dan keyin ATAYLAB NOT WIRED / NOT VERIFIED:** Event Bus→Core
  (NOT WIRED), Risk→Execution (contract bor, production NOT WIRED),
  Execution→Monitoring (NOT WIRED), Risk→Service (NOT WIRED),
  Telegram→User (NOT VERIFIED — xavfsiz destination kerak).
- **Execution ataylab inert** — real order/trade yo'q, YOQILMAGAN.
- Wiring qarorlari — Director DRQ'lari (REAL_DATA_011/16_–19_).
- **VPS Clean gate: 🔴 BLOCKED** (bu audit uni ochmaydi).
- Daily/HTF parse bug = KNOWN NON-BLOCKING (context-only, non-binding).

## 5. Yangilash qoidasi

Bu faylni quyidagi holatlarda yangilang: Phase o'zgarganda, yangi
Director Decision qabul qilinganda, yangi stable commit CI SUCCESS
bo'lganda, yoki Current Flow/Sprint o'zgarganda. Faqat holat qayd
etiladi — hech qanday yangi qoida bu yerda o'rnatilmaydi.
