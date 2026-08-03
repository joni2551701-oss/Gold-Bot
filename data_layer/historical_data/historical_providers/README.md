# Historical Providers

Status: CANONICAL

---

# Purpose

Historical Providers — Historical Data modulining tashqi tarixiy ma'lumot manbalari bilan ishlovchi bo'limidir.

Uning asosiy vazifasi tashqi providerlardan ishonchli tarixiy market ma'lumotlarini olish va ularni Historical Data moduliga uzatishdir.

Historical Providers faqat ma'lumotlarni yuklaydi.

Ular ma'lumotlarni tahlil qilmaydi, o'zgartirmaydi yoki saqlamaydi.

---

# Objective

Historical Providers quyidagi vazifalarni bajaradi:

• Historical Market Data Download

• Multi Provider Support

• Provider Selection

• Provider Authentication

• Provider Health Monitoring

• Historical Data Synchronization

• Standardized Data Delivery

---

# Layer Position

```text
Configuration Layer

↓

Provider Factory

↓

Historical Providers

↓

HistoricalDataService

↓

Historical Database

↓

Data Validation

↓

Market Memory
```

---

# Responsibilities

Historical Providers:

✓ Historical market ma'lumotlarini yuklash

✓ Provider API bilan ishlash

✓ Authentication

✓ Symbol Mapping

✓ Timeframe Mapping

✓ Rate Limit boshqaruvi

✓ Provider Status kuzatish

✓ Standard formatdagi ma'lumotni qaytarish

---

# Not Responsible

Historical Providers:

✗ Historical Database

✗ Data Validation

✗ Market Memory

✗ Bootstrap

✗ Recovery

✗ Live Data

✗ Current Price

✗ Strategy

✗ Analysis

✗ Decision

✗ Risk

✗ Signal Generation

---

# Supported Providers

Loyiha quyidagi providerlarni qo'llab-quvvatlashi mumkin.

• Twelve Data

• Polygon

• Alpha Vantage

• Finnhub

• Yahoo Finance

• CSV Import

• Local Historical Storage

• Future Providers

Providerlar Provider Factory orqali boshqariladi.

---

# Input

Historical Providers quyidagilarni qabul qiladi:

• Provider Configuration

• Symbol

• Timeframe

• Start Time

• End Time

• Candle Limit

---

# Output

Historical Providers quyidagilarni qaytaradi:

• Historical Candles

• OHLC Data

• Volume

• Timestamp

• Provider Status

---

# Data Flow

```text
Configuration

↓

Provider Factory

↓

Historical Provider

↓

HistoricalDataService

↓

Historical Database
```

---

# Provider Responsibilities

Har bir provider quyidagilarni bajarishi shart:

✓ API Connection

✓ Authentication

✓ Historical Download

✓ Request Validation

✓ Response Validation

✓ Error Reporting

✓ Timeout Handling

✓ Retry Support

---

# Provider Requirements

Har bir provider quyidagi interfeysni qo'llab-quvvatlashi kerak:

• Connect

• Authenticate

• Request Historical Data

• Receive Response

• Disconnect

---

# Golden Rules

1. Provider faqat ma'lumotlarni yuklaydi.

2. Provider marketni tahlil qilmaydi.

3. Provider signal yaratmaydi.

4. Provider Decision Engine bilan ishlamaydi.

5. Provider Data Validation'ni chetlab o'tmaydi.

6. Provider barcha ma'lumotni standart formatda qaytaradi.

7. Provider almashishi GoldBot Core'ga ta'sir qilmasligi kerak.

8. Provider implementatsiyasi Provider Factory orqali boshqariladi.

---

# Related Documents

```text
HistoricalProviders/

├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```

---

# Summary

Historical Providers — Historical Data modulining tashqi market ma'lumot manbalari bilan ishlovchi komponentidir.

Uning vazifasi:

• tashqi providerlarga ulanish;

• tarixiy market ma'lumotlarini yuklash;

• standartlashtirilgan formatda HistoricalDataService'ga uzatish.

Historical Providers Data Layer uchun yagona tarixiy ma'lumot manbai hisoblanadi.
