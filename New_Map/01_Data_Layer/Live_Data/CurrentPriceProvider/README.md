# Current Price Provider

Status: CANONICAL

---

# Purpose

CurrentPriceProvider — Live Data modulining real vaqt (Real-Time) narxini taqdim etuvchi komponentidir.

Uning asosiy vazifasi Live Provider'dan kelayotgan Tick ma'lumotlaridan GoldBot uchun yagona va ishonchli Current Price ni shakllantirish va PriceStreamService'ga uzatishdir.

CurrentPriceProvider narxni tahlil qilmaydi, Candle yaratmaydi va qaror qabul qilmaydi.

U faqat joriy narxni (Current Market Price) boshqaradi.

---

# Objective

CurrentPriceProvider quyidagi vazifalarni bajaradi:

• Current Price Management

• Tick Processing

• Bid / Ask Management

• Mid Price Calculation

• Price Synchronization

• Latest Price Cache

• Price Distribution

---

# Layer Position

```text
Live Provider

↓

PriceStreamService

↓

CurrentPriceProvider

↓

Stream Validator

↓

Candle Builder

↓

Market Memory

↓

GoldBot Core
```

---

# Responsibilities

CurrentPriceProvider:

✓ Live Tick qabul qilish

✓ Current Price yangilash

✓ Bid narxini boshqarish

✓ Ask narxini boshqarish

✓ Mid Price hisoblash (agar kerak bo'lsa)

✓ Latest Price saqlash

✓ PriceStreamService'ga Current Price uzatish

---

# Not Responsible

CurrentPriceProvider:

✗ Live Stream boshqarish

✗ Provider Connection

✗ Candle Building

✗ Stream Validation

✗ Market Calendar

✗ Historical Data

✗ Strategy

✗ Context

✗ Decision

✗ Risk

✗ Signal Generation

---

# Input

CurrentPriceProvider quyidagilarni qabul qiladi:

• Live Tick

• Bid

• Ask

• Timestamp

• Symbol

---

# Output

CurrentPriceProvider quyidagilarni yaratadi:

• Current Price

• Bid Price

• Ask Price

• Mid Price

• Latest Tick

• Price Update Event

---

# Managed Data

CurrentPriceProvider quyidagi ma'lumotlarni boshqaradi:

• Current Price

• Latest Tick

• Bid

• Ask

• Spread

• Timestamp

---

# Workflow

```text
Live Provider

↓

PriceStreamService

↓

CurrentPriceProvider

↓

Current Price Updated

↓

Stream Validator

↓

Candle Builder

↓

Market Memory
```

---

# Golden Rules

1. CurrentPriceProvider faqat Current Price bilan ishlaydi.

2. Har bir Tick Latest Price'ni yangilaydi.

3. CurrentPriceProvider Candle yaratmaydi.

4. Validation CurrentPriceProvider ichida bajarilmaydi.

5. CurrentPriceProvider History saqlamaydi.

6. CurrentPriceProvider faqat eng so'nggi narxni boshqaradi.

7. GoldBot Core Current Price'ni Market Memory orqali oladi.

8. CurrentPriceProvider Trading Logic'dan mustaqil bo'lishi shart.

---

# Related Documents

```text
CurrentPriceProvider/

├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```

---

# Summary

CurrentPriceProvider — Live Data modulining joriy bozor narxini boshqaruvchi komponentidir.

Uning vazifasi:

• Live Tick qabul qilish;

• Current Price'ni yangilash;

• Bid, Ask va kerak bo'lsa Mid Price'ni shakllantirish;

• PriceStreamService orqali keyingi modullarga uzatish.

CurrentPriceProvider Live Data Pipeline ichidagi yagona Canonical Current Price manbai hisoblanadi.
