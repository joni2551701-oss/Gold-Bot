# Live Providers

Status: CANONICAL

---

# Purpose

LiveProviders — Live Data modulining tashqi Real-Time Market Data Provider'lari bilan ishlovchi komponentidir.

Uning asosiy vazifasi bir yoki bir nechta Live Market Data Provider'lariga ulanish, ulardan Real-Time Tick ma'lumotlarini qabul qilish va ularni PriceStreamService'ga uzatishdir.

LiveProviders Trading Logic, Validation yoki Candle Generation bilan shug'ullanmaydi.

U faqat tashqi Live Market Data manbalari bilan integratsiya qiladi.

---

# Objective

LiveProviders quyidagi vazifalarni bajaradi:

• Live Provider Connection

• Provider Authentication

• Real-Time Tick Receiving

• Provider Health Monitoring

• Provider Switching

• Provider Failover

• Connection Recovery

• Provider Status Reporting

---

# Layer Position

```text
Configuration Layer

↓

PriceStreamService

↓

LiveProviders

↓

Exchange APIs

↓

Real-Time Market Data

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

LiveProviders:

✓ Live Provider bilan ulanish

✓ Authentication

✓ Real-Time Tick qabul qilish

✓ Connection Monitoring

✓ Provider Status kuzatish

✓ Provider almashtirish

✓ Failover boshqarish

✓ Tick'larni PriceStreamService'ga uzatish

---

# Not Responsible

LiveProviders:

✗ Current Price Management

✗ Tick Validation

✗ Candle Generation

✗ Market Calendar

✗ Historical Data

✗ Historical Storage

✗ Market Memory

✗ Context Analysis

✗ Strategy

✗ Decision

✗ Risk

✗ Signal Generation

✗ AI Analysis

---

# Input

LiveProviders quyidagilarni qabul qiladi:

• Provider Configuration

• Authentication Credentials

• Connection Request

• Subscription Request

• Symbol List

---

# Output

LiveProviders quyidagilarni yaratadi:

• Live Tick

• Provider Status

• Connection Status

• Provider Health

• Provider Event

---

# Supported Providers

Masalan:

• Bitget

• Binance

• Bybit

• Coinbase

• Kraken

• Future Providers

---

# Managed Data

LiveProviders quyidagi ma'lumotlarni boshqaradi:

• Provider Connection

• Authentication

• Live Subscription

• Provider Health

• Connection State

• Provider Metadata

---

# Workflow

```text
PriceStreamService

↓

LiveProviders

↓

Exchange API

↓

Receive Live Tick

↓

PriceStreamService

↓

CurrentPriceProvider
```

---

# Golden Rules

1. LiveProviders faqat tashqi Provider bilan ishlaydi.

2. LiveProviders Current Price yaratmaydi.

3. LiveProviders Validation bajarmaydi.

4. LiveProviders Candle yaratmaydi.

5. LiveProviders Trading Logic bajarmaydi.

6. Har bir Tick o'zgartirilmasdan PriceStreamService'ga uzatiladi.

7. Provider almashishi avtomatik bo'lishi mumkin.

8. LiveProviders GoldBot Core bilan bevosita ishlamaydi.

---

# Related Documents

```text
LiveProviders/

├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```

---

# Summary

LiveProviders — Live Data modulining tashqi Real-Time Market Data Provider'lari bilan integratsiya qiluvchi komponentidir.

Uning vazifasi:

• Live Provider'ga ulanish;

• Authentication bajarish;

• Real-Time Tick ma'lumotlarini qabul qilish;

• Connection holatini kuzatish;

• Tick'larni PriceStreamService'ga uzatish.

LiveProviders Live Data Pipeline ichidagi yagona Canonical External Live Provider Integration moduli hisoblanadi.
