# FLOW-016 — Chart Service Production Foundation + Architecture Correction

Sana: 2026-08-05
Muallif: Worker (Director Decision FLOW-016 asosida)
Til: GLS-001 (proza O'zbek, texnik terminlar English)
Authority: Director Decision — "Architecture Correction" (oldindan
ruxsat berilgan; alohida tasdiq talab etilmaydi).

> Bu hujjat FLOW-016 Deliverables 1–5 ni qamrab oladi: Architecture
> Audit, topilgan xatolar, Architecture Correction Report, eski↔yangi
> struktura taqqoslash va o'zgargan diagramma. Deliverables 6–10
> (Production Code, Unit/Integration/E2E Test, Director Review) kod va
> `tests/chart_layer/` da hamda ushbu hujjat oxirida keltirilgan.

---

## 1. Architecture Audit — Chart subsystem hozirgi holati

Audit `chart_layer/` (Canonical `16_Chart_Layer`) ustida o'tkazildi.

**Mavjud canonical struktura (kod diskda):**
`chart_layer/` da 5 ta importable subpaket bor edi, barchasi Foundation
Freeze skeleton (13-qatorli generic `__init__.py`, biznes-logikasiz):

| Subpaket | Canonical vazifa (README bo'yicha) |
|---|---|
| `chart_core` | Chart Engine, Lifecycle, State, Camera, Coordinate System |
| `chart_api` | Yagona Public API + Event API + Plugin API Boundary Gateway |
| `chart_data` | Candle / Tick / OHLCV / Session / Symbol ma'lumotlari + keshlash |
| `chart_renderer` | Canvas/WebGL Rendering |
| `chart_interaction` | Mouse/Keyboard/Touch/Zoom/Pan/Selection |

`chart_layer/README.md` (Foundation BLUEPRINT) 20 ta numbered subpaketni
belgilaydi (`01_Chart_Core` … `20_Plugins`).

**Yetishmayotgan (FLOW-016 Core Infrastructure uchun):** ishlaydigan
Engine, Pipeline, Request/Response contract, Cache, Renderer va
Service/API — hech biri hali kod sifatida mavjud emas edi (faqat
skeleton).

**Ortiqcha modullar:** topilmadi.

**Noto'g'ri joylashgan modullar:** yo'q (skeleton bo'sh edi).

**Kelajakdagi kengayishga to'sqinlik:** Foundation faqat skeleton bo'lib
turibdi — Drawing Tools / Indicators / Replay / Elite View ustiga
quriladigan ishlaydigan Core Infrastructure yo'q edi. Bu FLOW-016 ning
aynan sababi.

---

## 2. Topilgan xato (Architecture Error)

Audit natijasida bitta jiddiy ziddiyat aniqlandi:

**Xato:** FLOW-016 topshirig'ining dastlabki (sessiya oldidan) talqinida
"10 ta alohida modul" — `chart_engine`, `chart_pipeline`,
`chart_service`, `chart_cache`, `chart_request`, `chart_response`,
`chart_models`, `chart_events` — har biri **alohida yangi top-level
paket** sifatida yaratilishi ko'zda tutilgan edi.

**Nega bu xato:**
1. Canonical blueprint (`chart_layer/README.md`) bu vazifalarni
   allaqachon mavjud subpaketlarga biriktirgan: Engine/Lifecycle →
   `Chart_Core`; Data/OHLCV/Cache → `Chart_Data`; Public+Event API →
   `Chart_API`; Rendering → `Chart_Renderer`.
2. 8 ta yangi parallel paket yaratish `Chart_Core`/`Chart_Data`/
   `Chart_API` bilan **qism-qism ustma-ust** tushar edi — ya'ni bir xil
   javobgarlik ikki joyda.
3. Bu GEL-001 (Canonical Module = Package), Module Reuse Principle va
   Foundation blueprint bilan ziddir. Foundation Freeze noto'g'ri
   qarorni saqlash uchun emas — to'g'ri arxitekturani himoya qilish
   uchun.

Director bu ziddiyatni ko'rib, "bu xato hisoblanadi" deb tasdiqladi va
Architecture Correction'ga oldindan ruxsat berdi.

---

## 3. Architecture Correction Report

**Qaror:** yangi ortiqcha paket YARATILMAYDI. FLOW-016 ning 10 mantiqiy
komponenti mavjud 5 canonical subpaketning to'g'ri egalariga
joylashtiriladi (Reuse-first).

**Nima o'zgardi:** yangi package yaratilmadi; package bo'linmadi yoki
birlashtirilmadi; package nomi o'zgarmadi. Faqat mavjud skeleton
subpaketlarga **production kod migratsiya** qilindi (MIR-001 bo'yicha
Director aynan chart subsystem uchun bunga ruxsat bergan).

**Dependency o'zgarishi:** yangi tashqi dependency qo'shilmadi (faqat
stdlib: `dataclasses`, `enum`, `hashlib`, `time`, `typing`). Ichki import
yo'nalishi bir tomonlama va layered:

```
chart_data  →  (hech kimga bog'liq emas; stdlib only)
chart_renderer  →  chart_data
chart_core  →  chart_data, chart_renderer
chart_api  →  chart_core, chart_data   (+ o'zining events moduli)
```

Sikl (cycle) yo'q. Yuqori layer pastga qaraydi, teskarisi emas.

---

## 4. Eski ↔ Yangi struktura taqqoslash

| # | Mantiqiy komponent | ESKI (noto'g'ri) joy | YANGI (canonical) joy |
|---|---|---|---|
| 1 | ChartType/OutputFormat/ChartStatus/Candle/ChartModel/ChartObject | `chart_models` (yangi paket) | `chart_data/models.py` |
| 2 | ChartRequest (+Error) | `chart_request` (yangi paket) | `chart_data/request.py` |
| 3 | ChartResponse | `chart_response` (yangi paket) | `chart_data/response.py` |
| 4 | ChartCache | `chart_cache` (yangi paket) | `chart_data/cache.py` |
| 5 | ChartRenderer | `chart_renderer` | `chart_renderer/renderer.py` |
| 6 | ChartPipeline (+ MarketDataSource port) | `chart_pipeline` (yangi paket) | `chart_core/pipeline.py` |
| 7 | ChartEngine | `chart_engine` (yangi paket) | `chart_core/engine.py` |
| 8 | ChartService | `chart_service` (yangi paket) | `chart_api/service.py` |
| 9 | ChartAPI | `chart_api` | `chart_api/api.py` |
| 10 | ChartEvent/Recorder + factories | `chart_events` (yangi paket) | `chart_api/events.py` |

Natija: **8 ta ortiqcha top-level paket → 0**. Barcha 10 komponent 5 ta
canonical subpaketga sig'di.

---

## 5. Diagramma — FLOW-016 Foundation Layer chain

Director belgilagan layer zanjiri (Market Memory → … → Platform)
canonical joylarga quyidagicha map bo'ladi:

```
                       ┌────────────────────────────────────────────┐
   Platform  ────────► │ chart_api.ChartAPI                         │  (yagona kirish nuqtasi)
                       │   create_chart / get_chart /               │
                       │   update_chart / clear_cache               │
                       └───────────────┬────────────────────────────┘
                                       │
                       ┌───────────────▼────────────────────────────┐
                       │ chart_api.ChartService                     │
                       │   Cache lifecycle + Event emit +           │
                       │   ChartResponse yig'ish                    │
                       └───────┬───────────────────┬────────────────┘
                               │                   │
             chart_api.events  │                   │  chart_data.ChartCache
             (ChartRequested/  │                   │  (request_hash → object, TTL)
              Created/Updated/ │                   │
              Failed)          │                   │
                       ┌───────▼───────────────────┴────────────────┐
                       │ chart_core.ChartEngine                     │
                       │   business logic; Pipeline'ni yuritadi     │
                       └───────────────┬────────────────────────────┘
                                       │
                       ┌───────────────▼────────────────────────────┐
                       │ chart_core.ChartPipeline                   │
                       │  Input Validation → Market Data Loading →  │
                       │  Chart Model Creation → Render             │
                       └───┬────────────────────────┬───────────────┘
                           │                        │
   Market Memory  ────────►│ MarketDataSource port  │  chart_renderer.ChartRenderer
   (kelajakda; hozir       │ (EmptyMarketDataSource) │  (faqat render; placeholder
    EmptyMarketDataSource) │                        │   ChartObject)
                           └────────────────────────┘
                                       │
                        chart_data: ChartRequest / ChartModel /
                        Candle / ChartObject / ChartResponse (contracts)
```

Muhim chegaralar (Director qoidalari bilan mos):
- **Renderer faqat render qiladi** — Market Memory/DB/Platform o'qimaydi.
- **Engine biznes-logikani ushlaydi**, render qilmaydi, cache egasi emas.
- **Chart API — yagona Platform kirish nuqtasi**; tashqaridan
  Engine/Pipeline/Renderer/Cache'ga to'g'ridan-to'g'ri kirilmaydi.
- **Events** — sof notification; Renderer/Cache/DB chaqirmaydi.

---

## 6. Production Code Summary (Deliverable 6)

Yaratilgan/kengaytirilgan production fayllar (barchasi ishlaydi va
importable):

- `chart_layer/chart_data/`: `models.py`, `request.py`, `response.py`,
  `cache.py`, `__init__.py` (export).
- `chart_layer/chart_renderer/`: `renderer.py`, `__init__.py` (export).
- `chart_layer/chart_core/`: `pipeline.py`, `engine.py`, `__init__.py`
  (export).
- `chart_layer/chart_api/`: `events.py`, `service.py`, `api.py`,
  `__init__.py` (export).

Har bir `__init__.py` canonical docstring header'ini saqlaydi va FLOW-016
export'larini qo'shadi (Foundation Freeze uslubi buzilmaydi).

---

## 7. Testlar (Deliverables 7–9)

`tests/chart_layer/` (31 test, barchasi PASS):
- `test_chart_data.py` — Unit: models, request validate/hash, response,
  cache TTL/invalidate.
- `test_chart_renderer.py` — Unit: placeholder render + type checks.
- `test_chart_core.py` — Unit + Integration: pipeline stages, injected
  MarketDataSource, engine.
- `test_chart_api.py` — Integration + E2E: events, service (cache/emit/
  update/failed), ChartAPI to'liq zanjiri, canonical subpaket import.

---

## 8. Success Criteria tekshiruvi

- ✅ Chart subsystem Production Foundation holatida (ishlaydigan Core
  Infrastructure, importable, testdan o'tgan).
- ✅ Arxitektura kod bilan mos — README endi haqiqatga mos keladi
  (kod README'ga emas, README kodga moslashtirildi).
- ✅ Kelajakdagi Chart funksiyalari (Drawing Tools, Indicators, Replay,
  Elite View) shu Foundation ustiga qayta arxitekturasiz quriladi:
  ular `chart_core` Engine/State, `chart_data` model/cache,
  `chart_renderer` va `chart_api` ustiga qo'shiladi.
- ✅ Silent Decision yo'q — ziddiyat Director'ga eskalatsiya qilindi,
  qaror hujjatlashtirildi.
