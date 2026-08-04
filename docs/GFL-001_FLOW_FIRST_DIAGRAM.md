# GFL-001 — Flow-First Development Diagram

## Maqsad

Ushbu diagramma GoldBot'ning yagona rasmiy Data Flow (Flow-First) arxitekturasini ko'rsatadi.

Har bir modul o'zidan oldingi modulning Output'ini qabul qiladi va keyingi modul uchun Input yaratadi.

Development har doim ushbu oqim bo'yicha amalga oshiriladi.

**V3 qayta ko'rib chiqish (GFL-002, Director Order):** ushbu diagramma
endi GoldBot V3 Architecture asosida quriladi -- oltita gorizontal
Layer (Foundation -> Data -> GoldBot -> Application Services ->
Platform -> End User), GoldBot esa ichida to'rtta parallel subsystem
(GoldBot Core / Chart Service / Personal AI Core / Backtesting
Engine) sifatida ko'rsatiladi. Ilgari GoldBot Core zanjiri (Market
Engine ... GoldBot Core API) yagona chiziq sifatida chizilgan edi --
u endi shu to'rtta subsystemdan biri, GoldBot Core, sifatida
joylashtirilgan.

---

# V3 ARCHITECTURE (top-level)

══════════════════════════════════════════════════════════════════════════════
                         GOLDBOT V3 ARCHITECTURE
══════════════════════════════════════════════════════════════════════════════

                              Foundation Layer
                          (core/, secrets, config)
                                     │
                                     ▼
                                Data Layer
                    (Provider Factory, Price/Historical Data,
                       Data Validation, Market Memory SSOT)
                                     │
                                     ▼
                 ┌───────────────────────────────────────────┐
                 │                  GoldBot                   │
                 │                                             │
                 │   GoldBot Core   Chart Service               │
                 │       │              │                       │
                 │   Personal AI Core   Backtesting Engine       │
                 │                                             │
                 └───────────────────────────────────────────┘
                                     │
                                     ▼
                          Application Services
                                     │
                                     ▼
                              Platform Layer
      ┌──────────────┬──────────────┬──────────────┬──────────────┐
      ▼              ▼              ▼              ▼              ▼
 Telegram       Mini App        Android         iOS          Desktop / Web
      │              │              │              │              │
      └──────────────┴──────────────┴──────────────┴──────────────┘
                                     │
                                     ▼
                                 End User

══════════════════════════════════════════════════════════════════════════════

Har bir Consumer bir xil GoldBot -> Application Services zanjiri
orqali ishlaydi.

Telegram / Mini App / Android / iOS / Desktop / Web hech qachon
GoldBot yoki Data Layer moduliga to'g'ridan-to'g'ri ulanmaydi --
faqat Application Services orqali.

══════════════════════════════════════════════════════════════════════════════

# GoldBot ICHKI TUZILISHI (4 Subsystem)

GoldBot bloki to'rtta parallel subsystemdan iborat. Ular bir-biriga
bog'liq emas (har biri mustaqil Flow zanjiriga ega), lekin barchasi
Data Layer'dan input oladi va Application Services'ga output beradi.

## GoldBot Core (savdo pipeline)

Market Memory (Data Layer)
      │
      ▼
 Market Engine
      │
      ▼
 Context Engine
      │
      ▼
 Analysis Engine
      │
      ▼
 Indicator Engine
      │
      ▼
 Strategy Engine
      │
      ▼
 Confluence Engine
      │
      ▼
 Decision Engine
      │
      ▼
 Risk Engine
      │
      ▼
 Signal Engine
      │
      ▼
 Execution Engine
      │
      ▼
 Trade Monitoring
      │
      ▼
 GoldBot Core API
      │
      ▼
 (Application Services)

Real modul: `core_layer/`, `context_layer/`, `strategy_layer/`,
`signal_layer/`, `decision_layer/`, `risk_layer/`, `execution_layer/`,
`trade_monitoring_layer/`, `indicator_layer/`.

## Chart Service

Market Memory (Data Layer)
      │
      ▼
 Chart Service (`chart_layer/`)
      │
      ▼
 (Application Services)

Hozircha GFL Flow sifatida rasmiylashtirilmagan -- Blueprint (bo'sh
joy band qilingan, ichi hali aniqlanmagan). Ko'ring: FLOW_CATALOG.md
FLOW-016.

## Personal AI Core

GoldBot Core / Data Layer (advisory input, hech qachon boshqaruvchi emas)
      │
      ▼
 Personal AI Core (`ai_layer/`)
      │
      ▼
 (Application Services)

Constitution Article 1/3: AI Layer faqat maslahat beradi, hech qachon
savdo qarorini o'zi qabul qilmaydi, Risk Manager'ni chaqirmaydi va
Telegram'ga to'g'ridan-to'g'ri yubormaydi. Hozircha GFL Flow sifatida
rasmiylashtirilmagan -- Blueprint. Ko'ring: FLOW_CATALOG.md FLOW-017.

## Backtesting Engine

Data Layer (tarixiy ma'lumot) / GoldBot Core (strategiya qoidalari)
      │
      ▼
 Backtesting Engine (`backtesting_layer/`)
      │
      ▼
 (Application Services)

Hozircha GFL Flow sifatida rasmiylashtirilmagan -- Blueprint. Ko'ring:
FLOW_CATALOG.md FLOW-018.

══════════════════════════════════════════════════════════════════════════════

## Development Rule

Development har doim quyidagi tartibda amalga oshiriladi.

Producer
↓
Input
↓
Processing
↓
Output
↓
Consumer
↓
Validation
↓
End-to-End Test
↓
Documentation
↓
WORK_LOG
↓
Next Flow

Har bir Flow to'liq yakunlanmaguncha keyingi Flow boshlanmaydi.

══════════════════════════════════════════════════════════════════════════════

## Flow Completion

Flow Completed hisoblanadi agar:

✓ Producer ishlaydi

✓ Input qabul qilinadi

✓ Processing ishlaydi

✓ Output hosil bo'ladi

✓ Consumer ishlaydi

✓ Barcha Consumer'lar PASS (Fan-Out Rule)

✓ End-to-End Test PASS

✓ Producer→Consumer latency o'lchangan va yozilgan (Latency Rule)

✓ Documentation yangilangan

✓ WORK_LOG yozilgan

══════════════════════════════════════════════════════════════════════════════

## Forbidden

Taqiqlanadi:

• Producer'siz Consumer yaratish

• Input'siz modul yaratish

• Output ishlatilmasligi

• Flow uzilgan holda Development davom ettirish

• Batch Coding

• Layer bo'yicha tasodifiy Development

• End-to-End test o'tmasdan Completed deb belgilash

• V3 Architecture'dan tashqari yangi Layer/Subsystem qo'shish (Director tasdig'isiz)

══════════════════════════════════════════════════════════════════════════════

## Final Principle

GoldBot Layer-first emas.

GoldBot File-first emas.

GoldBot Flow-first arxitektura asosida, V3 Architecture (Foundation ->
Data -> GoldBot[Core/Chart/AI/Backtesting] -> Application Services ->
Platform -> End User) doirasida ishlab chiqiladi.

Har bir Data Flow boshidan oxirigacha ishlaydigan holatga kelgandan
keyingina keyingi Flow boshlanadi.
