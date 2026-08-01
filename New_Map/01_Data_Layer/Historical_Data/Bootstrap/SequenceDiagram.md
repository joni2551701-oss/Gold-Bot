# Bootstrap Sequence Diagram

Status: CANONICAL

---

# Purpose

Ushbu hujjat Bootstrap moduli ishga tushganda modullar qanday ketma-ketlikda ishlashini ko'rsatadi.

Bu Runtime Sequence bo'lib, implementatsiya emas.

---

# Startup Sequence

```text
GoldBot Start
      │
      ▼
Configuration Layer
      │
      ▼
HistoricalDataService
      │
      ▼
Bootstrap
      │
      ▼
Provider Factory
      │
      ▼
Historical Provider
      │
      ▼
Download Historical Data
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
Bootstrap Completed
      │
      ▼
Start Live Data
```

---

# Detailed Runtime Sequence

```text
┌───────────────┐
│ GoldBot Start │
└───────┬───────┘
        │
        ▼
Load Configuration
        │
        ▼
Create HistoricalDataService
        │
        ▼
Initialize Bootstrap
        │
        ▼
Request Historical Data
        │
        ▼
Provider Factory
        │
        ▼
Historical Provider
        │
        ▼
Download Candles
        │
        ▼
Store Historical Database
        │
        ▼
Validate Data
        │
        ▼
Update Market Memory
        │
        ▼
Bootstrap Success
        │
        ▼
Enable Live Stream
```

---

# Module Interaction

```text
HistoricalDataService
        │
        ▼
Bootstrap
        │
        ▼
Provider Factory
        │
        ▼
Historical Provider
        │
        ▼
Historical Database
        │
        ▼
Data Validation
        │
        ▼
Market Memory
```

---

# Success Sequence

```text
Bootstrap Started

↓

Historical Data Downloaded

↓

Validation Passed

↓

Market Memory Initialized

↓

Bootstrap Finished

↓

Live Data Enabled
```

---

# Failure Sequence

```text
Bootstrap Started

↓

Historical Provider Error

↓

Retry Download

↓

Retry Failed

↓

Bootstrap Failed

↓

GoldBot Startup Aborted
```

---

# Recovery Sequence

```text
Bootstrap Failed

↓

Recovery Requested

↓

Historical Provider

↓

Missing Data Download

↓

Validation

↓

Market Memory Updated

↓

Bootstrap Completed
```

---

# Runtime Rules

1. Bootstrap Configuration yuklangandan keyin boshlanadi.

2. HistoricalDataService Bootstrap'ni ishga tushiradi.

3. Bootstrap Provider Factory orqali Historical Provider'ga ulanadi.

4. Provider'dan olingan ma'lumot avval Historical Database'ga yoziladi.

5. Har bir ma'lumot Validation'dan o'tishi shart.

6. Validation muvaffaqiyatli bo'lsa Market Memory yangilanadi.

7. Bootstrap tugamaguncha Live Data ishga tushmaydi.

8. Bootstrap muvaffaqiyatli tugagach tizim Live Data bosqichiga o'tadi.

---

# Summary

Bootstrap Sequence Diagram GoldBot ishga tushganda tarixiy ma'lumotlarning qanday yuklanishini va modullar orasidagi bajarilish ketma-ketligini belgilaydi.

Canonical Startup Sequence:

GoldBot Start

↓

Configuration

↓

HistoricalDataService

↓

Bootstrap

↓

Historical Provider

↓

Historical Database

↓

Data Validation

↓

Market Memory

↓

Bootstrap Completed

↓

Live Data Start
