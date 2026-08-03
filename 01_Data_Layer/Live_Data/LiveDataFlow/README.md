# Live Data Flow

Status: CANONICAL

---

# Purpose

LiveDataFlow — Live Data modulining Real-Time Data Pipeline oqimini tavsiflovchi komponentidir.

Uning asosiy vazifasi Live Market Data qanday ketma-ketlikda harakatlanishini, qaysi moduldan qaysi modulga o'tishini va Pipeline qoidalarini belgilashdir.

LiveDataFlow hech qanday ma'lumot yaratmaydi yoki qayta ishlamaydi.

U faqat Live Data oqimining Canonical Flow modelini belgilaydi.

---

# Objective

LiveDataFlow quyidagi vazifalarni bajaradi:

• Live Data Pipeline Definition

• Runtime Flow Definition

• Module Communication Order

• Data Movement Definition

• Pipeline Standardization

• Flow Integrity

• Runtime Consistency

---

# Layer Position

```text
Configuration Layer

↓

MarketCalendar

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

# Responsibilities

LiveDataFlow:

✓ Live Data oqimini belgilash

✓ Modul ketma-ketligini belgilash

✓ Pipeline qoidalarini belgilash

✓ Runtime Data Flow'ni standartlashtirish

✓ Modul chegaralarini saqlash

✓ Pipeline yaxlitligini ta'minlash

---

# Not Responsible

LiveDataFlow:

✗ Provider Connection

✗ Current Price

✗ Tick Validation

✗ Candle Generation

✗ Market Calendar

✗ Historical Data

✗ Market Memory

✗ Context Analysis

✗ Strategy

✗ Decision

✗ Risk

✗ Signal Generation

✗ AI Analysis

---

# Input

LiveDataFlow quyidagilarni qabul qiladi:

• Live Tick

• Market Status

• Provider Events

• Pipeline Events

---

# Output

LiveDataFlow quyidagilarni belgilaydi:

• Runtime Flow

• Module Order

• Pipeline Sequence

• Data Route

• Flow Status

---

# Flow Stages

LiveDataFlow quyidagi bosqichlardan iborat:

• Market Status

• Stream Start

• Provider Connection

• Tick Receiving

• Current Price Update

• Tick Validation

• Candle Generation

• Market Memory Update

• GoldBot Core Access

---

# Workflow

```text
MarketCalendar

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

1. Live Data faqat bitta Canonical Pipeline orqali harakatlanadi.

2. Har bir Tick barcha bosqichlardan o'tishi shart.

3. Hech bir modul Pipeline bosqichini chetlab o'tolmaydi.

4. Validation har doim CandleBuilder'dan oldin bajariladi.

5. Market Memory faqat tayyor Candle qabul qiladi.

6. GoldBot Core faqat Market Memory orqali ma'lumot oladi.

7. Pipeline tartibi o'zgartirilmaydi.

8. Circular Data Flow taqiqlanadi.

---

# Related Documents

```text
LiveDataFlow/

├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```

---

# Summary

LiveDataFlow — Live Data modulining Canonical Runtime Pipeline hujjati hisoblanadi.

U Live Market Data oqimining to'liq marshrutini, modul ketma-ketligini va Pipeline qoidalarini belgilaydi.

LiveDataFlow GoldBot arxitekturasida Live Market ma'lumotlari uchun yagona Canonical Data Flow hisoblanadi.
