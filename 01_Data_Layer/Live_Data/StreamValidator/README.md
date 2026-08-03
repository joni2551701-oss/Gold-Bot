# Stream Validator

Status: CANONICAL

---

# Purpose

StreamValidator — Live Data modulining Live Stream sifati va yaxlitligini (Integrity) tekshiruvchi komponentidir.

Uning asosiy vazifasi Live Provider'dan kelayotgan barcha Tick ma'lumotlarini tekshirish, noto'g'ri yoki buzilgan ma'lumotlarni filtrlash va faqat ishonchli ma'lumotlarni CandleBuilder moduliga uzatishdir.

StreamValidator hech qachon Tick yaratmaydi, Candle yaratmaydi yoki Trading Decision qabul qilmaydi.

U faqat Live Data sifatini nazorat qiladi.

---

# Objective

StreamValidator quyidagi vazifalarni bajaradi:

• Tick Validation

• Timestamp Validation

• Price Validation

• Symbol Validation

• Stream Integrity Check

• Duplicate Tick Detection

• Missing Tick Detection

• Invalid Tick Filtering

• Stream Quality Monitoring

---

# Layer Position

```text
Live Provider

↓

PriceStreamService

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

StreamValidator:

✓ Live Tick tekshirish

✓ Timestamp tekshirish

✓ Price tekshirish

✓ Symbol tekshirish

✓ Duplicate Tick aniqlash

✓ Missing Tick aniqlash

✓ Invalid Tick filtrlash

✓ Stream sifati monitoringi

✓ Tasdiqlangan Tick'ni CandleBuilder'ga uzatish

---

# Not Responsible

StreamValidator:

✗ Live Stream Management

✗ Provider Connection

✗ Current Price Management

✗ Candle Building

✗ Historical Data

✗ Historical Database

✗ Market Memory Storage

✗ Context Analysis

✗ Strategy

✗ Decision

✗ Risk

✗ Signal Generation

✗ AI Analysis

---

# Input

StreamValidator quyidagilarni qabul qiladi:

• Current Price

• Live Tick

• Bid

• Ask

• Timestamp

• Symbol

• Provider Metadata

---

# Output

StreamValidator quyidagilarni yaratadi:

• Validated Tick

• Validation Result

• Validation Status

• Validation Error

• Stream Quality Status

---

# Validation Types

StreamValidator quyidagi tekshiruvlarni bajaradi:

• Tick Validation

• Timestamp Validation

• Symbol Validation

• Bid / Ask Validation

• Price Range Validation

• Duplicate Detection

• Missing Tick Detection

• Stream Integrity Validation

---

# Workflow

```text
Live Provider

↓

PriceStreamService

↓

CurrentPriceProvider

↓

StreamValidator

↓

Validated Tick

↓

CandleBuilder

↓

Market Memory
```

---

# Golden Rules

1. Har bir Tick Validation'dan o'tishi shart.

2. Validation'dan o'tmagan Tick Pipeline bo'ylab uzatilmaydi.

3. Duplicate Tick rad etiladi.

4. Noto'g'ri Timestamp rad etiladi.

5. Noto'g'ri Symbol rad etiladi.

6. StreamValidator Candle yaratmaydi.

7. StreamValidator Current Price yaratmaydi.

8. StreamValidator Trading Logic'dan mustaqil bo'lishi shart.

---

# Related Documents

```text
StreamValidator/

├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```

---

# Summary

StreamValidator — Live Data modulining Live Stream sifati va yaxlitligini nazorat qiluvchi komponentidir.

Uning vazifasi:

• Live Tick tekshirish;

• Duplicate va Invalid Tick'larni filtrlash;

• Stream sifati monitoringini olib borish;

• Faqat tasdiqlangan Tick'larni CandleBuilder moduliga uzatish.

StreamValidator Live Data Pipeline ichidagi yagona Canonical Validation moduli hisoblanadi.
