# HistoricalDataService Sequence Diagram

Status: CANONICAL

---

# Purpose

Ushbu hujjat HistoricalDataService modulining Runtime Sequence (ishlash ketma-ketligi) ni tavsiflaydi.

HistoricalDataService Historical Data modulining markaziy Orchestrator'i bo'lib, Bootstrap, Recovery, Historical Providers, Historical Database, Data Validation va Market Memory o'rtasidagi barcha jarayonlarni boshqaradi.

Bu implementatsiya emas.

Bu HistoricalDataService modulining Canonical Runtime Blueprint hisoblanadi.

---

# Complete Runtime Sequence

```text
Historical Request

        │
        ▼
HistoricalDataService

        │
        ├──────────────┐
        ▼              ▼
   Bootstrap       Recovery
        │              │
        └──────┬───────┘
               ▼
      Historical Providers
               │
               ▼
     Historical Database
               │
               ▼
       Data Validation
               │
               ▼
        Market Memory
               │
               ▼
        GoldBot Core
```

---

# Bootstrap Sequence

```text
GoldBot Start

↓

HistoricalDataService

↓

Bootstrap

↓

Historical Providers

↓

Historical Database

↓

Data Validation

↓

Market Memory

↓

Bootstrap Completed
```

---

# Recovery Sequence

```text
Gap Detected

↓

HistoricalDataService

↓

Recovery

↓

Historical Providers

↓

Historical Database

↓

Data Validation

↓

Market Memory

↓

Recovery Completed
```

---

# Historical Download Sequence

```text
HistoricalDataService

↓

Historical Providers

↓

Download Historical Data

↓

Normalize Data

↓

Historical Database
```

---

# Database Write Sequence

```text
HistoricalDataService

↓

Historical Database

↓

Store Historical Data

↓

Storage Success
```

---

# Validation Sequence

```text
HistoricalDataService

↓

Data Validation

↓

Validate Historical Data

↓

Validation Passed

↓

Market Memory
```

---

# Market Memory Update Sequence

```text
HistoricalDataService

↓

Market Memory

↓

Update Historical Cache

↓

Memory Updated
```

---

# Read Sequence

```text
GoldBot Core

↓

Memory Reader

↓

Market Memory

↓

HistoricalDataService

↓

Historical Database

↓

Return Historical Data
```

---

# Error Recovery Sequence

```text
HistoricalDataService

↓

Historical Providers

↓

Provider Error

↓

Retry

↓

Retry Failed

↓

Recovery

↓

Recovery Failed
```

---

# Startup Sequence

```text
GoldBot Start

↓

Configuration Loaded

↓

HistoricalDataService Initialized

↓

Bootstrap Started

↓

Historical Data Ready

↓

GoldBot Core Ready
```

---

# Runtime Rules

1. HistoricalDataService Historical Data modulining yagona Orchestrator'i hisoblanadi.

2. Bootstrap faqat tizim ishga tushganda bajariladi.

3. Recovery faqat Gap aniqlanganda ishga tushadi.

4. Historical Providers faqat HistoricalDataService tomonidan chaqiriladi.

5. Historical Database bilan barcha operatsiyalar HistoricalDataService orqali amalga oshiriladi.

6. Validation har doim Database'dan keyin bajariladi.

7. Market Memory faqat Validation muvaffaqiyatli tugagandan keyin yangilanadi.

8. GoldBot Core HistoricalDataService bilan bevosita ishlamaydi.

---

# State Flow

```text
Idle

↓

Initialized

↓

Bootstrap

↓

Ready

↓

Processing Request

↓

Updating Database

↓

Validating

↓

Updating Memory

↓

Completed

or

Failed
```

---

# Golden Rules

• HistoricalDataService Historical Data modulining markaziy boshqaruvchisidir.

• Barcha Historical Data oqimi HistoricalDataService orqali o'tadi.

• Bootstrap va Recovery yagona boshqaruv nuqtasiga ega.

• Historical Providers mustaqil ishlamaydi.

• Validation majburiy bosqich.

• Market Memory faqat tasdiqlangan ma'lumotni qabul qiladi.

• GoldBot Core faqat Market Memory orqali ma'lumot oladi.

• Circular Sequence taqiqlanadi.

---

# Summary

HistoricalDataService Sequence Diagram Historical Data modulidagi barcha Runtime jarayonlarning bajarilish ketma-ketligini belgilaydi.

Canonical Runtime Sequence:

Historical Request

↓

HistoricalDataService

↓

Bootstrap / Recovery

↓

Historical Providers

↓

Historical Database

↓

Data Validation

↓

Market Memory

↓

GoldBot Core

Ushbu ketma-ketlik HistoricalDataService moduli uchun yagona rasmiy Runtime Sequence hisoblanadi.
