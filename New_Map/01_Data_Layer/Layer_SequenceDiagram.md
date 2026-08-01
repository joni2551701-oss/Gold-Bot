# Layer Sequence Diagram

Status: CANONICAL

---

# Purpose

Layer Sequence Diagram hujjati Data Layer ichidagi modullar ishga tushganda ma'lumotlarning ketma-ket qanday harakatlanishini (Runtime Execution Sequence) tavsiflaydi.

Bu hujjat Data Layer uchun rasmiy Runtime Blueprint hisoblanadi.

Bu yerda implementatsiya emas, balki modullar orasidagi ishlash tartibi ko'rsatiladi.

---

# Startup Sequence

Tizim ishga tushganda Data Layer quyidagi tartibda ishga tushadi.

```text
GoldBot Start
      │
      ▼
Configuration Layer
      │
      ▼
Provider Factory
      │
      ├──────────────┐
      ▼              ▼
Historical       Live
Providers      Providers
      │              │
      ▼              ▼
Historical     Price Stream
Data Service     Service
      │              │
      ▼              ▼
Bootstrap     Connection
      │              │
      └──────┬───────┘
             ▼
     Data Validation
             │
             ▼
      Market Memory
             │
             ▼
         Event Bus
             │
             ▼
       GoldBot Core
```

---

# Historical Data Sequence

Repository ishga tushganda tarixiy ma'lumot yuklanishi.

```text
Historical Provider

↓

HistoricalDataService

↓

Bootstrap

↓

Recovery (agar kerak bo'lsa)

↓

Historical Database

↓

Data Validation

↓

Market Memory

↓

Event Bus

↓

GoldBot Core
```

---

# Live Data Sequence

Realtime ma'lumot kelganda.

```text
Live Provider

↓

PriceStreamService

↓

StreamValidator

↓

CurrentPriceProvider

↓

CandleBuilder

↓

Data Validation

↓

Market Memory

↓

Event Bus

↓

GoldBot Core
```

---

# Memory Read Sequence

GoldBot Core ma'lumot so'raganda.

```text
GoldBot Core

↓

MemoryReader

↓

Market Memory

↓

Response

↓

GoldBot Core
```

GoldBot Core hech qachon Market Memory'ga yozmaydi.

---

# Event Sequence

Market Memory yangilanganda.

```text
Market Memory

↓

Event Bus

↓

Subscribers

↓

GoldBot Core

↓

Monitoring

↓

Application Services
```

---

# Candle Close Sequence

Yangi Candle yopilganda.

```text
Live Provider

↓

Price Stream

↓

Stream Validator

↓

Candle Builder

↓

Candle Validation

↓

Market Memory

↓

Event Bus

↓

GoldBot Core
```

---

# Current Price Sequence

Har bir yangi Tick kelganda.

```text
Live Provider

↓

Price Stream

↓

Stream Validator

↓

CurrentPriceProvider

↓

Market Memory

↓

MemoryReader

↓

GoldBot Core
```

---

# Recovery Sequence

Provider uzilib qayta ulanganda.

```text
Provider Reconnect

↓

Recovery

↓

Historical Provider

↓

Missing Data

↓

Data Validation

↓

Market Memory

↓

Resume Streaming
```

---

# Shutdown Sequence

Tizim to'xtaganda.

```text
GoldBot Stop

↓

Stop Providers

↓

Close Streams

↓

Flush Memory

↓

Save State

↓

Shutdown
```

---

# Runtime Rules

1. Historical Data har doim Live Data'dan oldin ishga tushadi.

2. Provider Factory barcha providerlarni boshqaradi.

3. Live Stream faqat Bootstrap tugagandan keyin boshlanadi.

4. Validation har bir ma'lumot uchun majburiy.

5. Market Memory faqat Validation'dan o'tgan ma'lumotni qabul qiladi.

6. Event Bus faqat Memory yangilangandan keyin Event yuboradi.

7. GoldBot Core faqat MemoryReader orqali ma'lumot oladi.

8. Circular Sequence taqiqlanadi.

---

# Golden Rules

• Startup yuqoridan pastga ishlaydi.

• Historical Data birinchi yuklanadi.

• Live Data keyin boshlanadi.

• Validation har doim majburiy.

• Market Memory yagona saqlash markazi.

• Event Bus barcha hodisalarni tarqatadi.

• GoldBot Core faqat o'qiydi.

• Data Layer hech qachon Decision chiqarmaydi.

---

# Summary

Layer Sequence Diagram Data Layer modullarining ishga tushish va ishlash ketma-ketligini rasmiy ravishda belgilaydi.

Har qanday ma'lumot quyidagi standart yo'l bo'yicha harakat qiladi:

External Provider

↓

Historical Data yoki Live Data

↓

Data Validation

↓

Market Memory

↓

Event Bus

↓

GoldBot Core

Bu ketma-ketlik Data Layer uchun yagona Canonical Runtime Sequence hisoblanadi.
