# Price Stream Service

Status: CANONICAL

---

# Purpose

PriceStreamService — Live Data modulining markaziy boshqaruv (Orchestrator) komponentidir.

Uning asosiy vazifasi real vaqt (Live Market) narx oqimini boshqarish, Live Provider'lar bilan ishlash, oqimni nazorat qilish va GoldBot Core foydalanishi uchun ishonchli Live Market Data tayyorlashdir.

PriceStreamService narxlarni o'zi yaratmaydi, o'zgartirmaydi yoki tahlil qilmaydi.

U faqat Live Data oqimini boshqaradi.

---

# Objective

PriceStreamService quyidagi vazifalarni bajaradi:

• Live Price Streaming

• Live Provider Coordination

• Stream Lifecycle Management

• Stream Validation Coordination

• Candle Builder Coordination

• Market Calendar Coordination

• Live Data Flow Management

• Market Memory Update Coordination

---

# Layer Position

```text
Configuration Layer

↓

PriceStreamService

├── Live Providers
├── Current Price Provider
├── Candle Builder
├── Stream Validator
├── Market Calendar
└── Live Data Flow

↓

Market Memory

↓

GoldBot Core
```

---

# Responsibilities

PriceStreamService:

✓ Live Price Stream boshqarish

✓ Live Provider'larni boshqarish

✓ Stream ulanishini nazorat qilish

✓ Candle Builder bilan ishlash

✓ Stream Validation jarayonini boshqarish

✓ Market Calendar holatini tekshirish

✓ Live Data Flow'ni koordinatsiya qilish

✓ Market Memory yangilanishini boshqarish

---

# Not Responsible

PriceStreamService:

✗ Historical Data

✗ Historical Download

✗ Historical Database

✗ Data Validation Logic

✗ Market Memory Storage

✗ Context Analysis

✗ Strategy

✗ Decision

✗ Risk

✗ Signal Generation

✗ AI Analysis

---

# Input

PriceStreamService quyidagilarni qabul qiladi:

• Live Stream Request

• Provider Response

• Current Price Update

• Market Status

• Configuration

---

# Output

PriceStreamService quyidagilarni yaratadi:

• Live Price Stream

• Current Price

• Candle Update

• Validation Request

• Memory Update Request

• Live Stream Status

---

# Controlled Modules

PriceStreamService quyidagi modullarni boshqaradi:

• Live Providers

• Current Price Provider

• Candle Builder

• Stream Validator

• Market Calendar

• Live Data Flow

---

# Workflow

```text
Live Provider

↓

PriceStreamService

↓

Current Price Provider

↓

Candle Builder

↓

Stream Validator

↓

Market Memory

↓

GoldBot Core
```

---

# Golden Rules

1. PriceStreamService Live Data modulining yagona Orchestrator'i hisoblanadi.

2. Live Stream faqat PriceStreamService orqali boshqariladi.

3. Live Provider'lar faqat PriceStreamService tomonidan chaqiriladi.

4. Har bir Price Update Stream Validator orqali tekshiriladi.

5. Candle Builder faqat tasdiqlangan narxlar bilan ishlaydi.

6. Market Memory faqat tekshirilgan Live Data bilan yangilanadi.

7. GoldBot Core Live Provider bilan bevosita ishlamaydi.

8. PriceStreamService savdo qarorini qabul qilmaydi.

---

# Related Documents

```text
PriceStreamService/

├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```

---

# Summary

PriceStreamService — Live Data modulining markaziy boshqaruv (Orchestrator) komponentidir.

U Live Provider, Current Price Provider, Candle Builder, Stream Validator, Market Calendar va Live Data Flow modullarini yagona Live Pipeline ichida boshqaradi.

PriceStreamService real vaqt narx oqimini koordinatsiya qiladi va tekshirilgan ma'lumotlarni Market Memory orqali GoldBot Core foydalanishi uchun tayyorlaydi.
