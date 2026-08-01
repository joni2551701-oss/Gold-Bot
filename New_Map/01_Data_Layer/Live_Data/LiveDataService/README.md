# LiveDataService

Status: CANONICAL

---

# Purpose

LiveDataService — Live Data modulining markaziy boshqaruv (Orchestrator) komponentidir.

Uning asosiy vazifasi Live Data modulidagi barcha komponentlarni yagona Runtime Pipeline ichida boshqarish va koordinatsiya qilishdir.

LiveDataService barcha Live Market Data jarayonlarini nazorat qiladi, ammo narx yaratmaydi, Candle yaratmaydi va Validation bajarmaydi.

U faqat jarayonlarni boshqaradi.

---

# Objective

LiveDataService quyidagi vazifalarni bajaradi:

• Live Data Orchestration

• Live Stream Lifecycle Management

• Provider Coordination

• Current Price Coordination

• Validation Coordination

• Candle Building Coordination

• Market Calendar Coordination

• Market Memory Coordination

• Runtime Flow Management

---

# Layer Position

```text
Configuration Layer

↓

LiveDataService

├── MarketCalendar
├── PriceStreamService
├── LiveProviders
├── CurrentPriceProvider
├── StreamValidator
├── CandleBuilder
└── LiveDataFlow

↓

Market Memory

↓

GoldBot Core
```

---

# Responsibilities

LiveDataService:

✓ Live Data Pipeline boshqarish

✓ Live Stream Lifecycle boshqarish

✓ MarketCalendar koordinatsiyasi

✓ PriceStreamService koordinatsiyasi

✓ LiveProviders koordinatsiyasi

✓ CurrentPriceProvider koordinatsiyasi

✓ StreamValidator koordinatsiyasi

✓ CandleBuilder koordinatsiyasi

✓ LiveDataFlow koordinatsiyasi

✓ Market Memory yangilanishini boshqarish

---

# Not Responsible

LiveDataService:

✗ Provider Connection

✗ Tick Generation

✗ Current Price Calculation

✗ Tick Validation

✗ Candle Generation

✗ Market Memory Storage

✗ Historical Data

✗ Context Analysis

✗ Strategy

✗ Decision

✗ Risk

✗ Signal Generation

✗ AI Analysis

---

# Input

LiveDataService quyidagilarni qabul qiladi:

• Market Status

• Live Stream Request

• Provider Events

• Live Tick Events

• Runtime Events

• Configuration

---

# Output

LiveDataService quyidagilarni yaratadi:

• Live Pipeline Control

• Module Commands

• Runtime Status

• Pipeline Events

• Memory Update Request

---

# Controlled Modules

LiveDataService quyidagi modullarni boshqaradi:

• MarketCalendar

• PriceStreamService

• LiveProviders

• CurrentPriceProvider

• StreamValidator

• CandleBuilder

• LiveDataFlow

---

# Workflow

```text
Market Status

↓

LiveDataService

↓

PriceStreamService

↓

LiveProviders

↓

CurrentPriceProvider

↓

StreamValidator

↓

CandleBuilder

↓

Market Memory

↓

GoldBot Core
```

---

# Golden Rules

1. LiveDataService Live Data modulining yagona Orchestrator'i hisoblanadi.

2. Live Data Pipeline faqat LiveDataService tomonidan boshqariladi.

3. Har bir Live Tick belgilangan Pipeline orqali o'tishi shart.

4. Validation bosqichi hech qachon chetlab o'tilmaydi.

5. CandleBuilder faqat Validation'dan o'tgan Tick bilan ishlaydi.

6. Market Memory faqat tayyor Candle bilan yangilanadi.

7. GoldBot Core LiveDataService bilan bevosita ishlamaydi.

8. LiveDataService biznes logikasini bajarmaydi, faqat koordinatsiya qiladi.

---

# Related Documents

```text
LiveDataService/

├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```

---

# Summary

LiveDataService — Live Data modulining markaziy boshqaruv (Orchestrator) komponentidir.

U MarketCalendar, PriceStreamService, LiveProviders, CurrentPriceProvider, StreamValidator, CandleBuilder va LiveDataFlow modullarini yagona Runtime Pipeline ichida boshqaradi.

LiveDataService Live Data Layer ichidagi barcha Runtime jarayonlarini koordinatsiya qiluvchi yagona Canonical Orchestrator hisoblanadi.
