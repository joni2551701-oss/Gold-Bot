# Historical Data Flow Sequence Diagram

Status: CANONICAL

---

# Purpose

Ushbu hujjat Historical Data Flow modulining Runtime Sequence (ishlash ketma-ketligi) ni tavsiflaydi.

Bu hujjat Historical Data ichidagi barcha modullar o'rtasida ma'lumot qanday harakatlanishini bosqichma-bosqich ko'rsatadi.

Bu implementatsiya emas.

Bu Historical Data Flow modulining Canonical Runtime Blueprint hisoblanadi.

---

# Complete Historical Data Flow

```text
External Historical Provider

          │
          ▼
Provider Factory

          │
          ▼
Historical Provider

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
      Historical Database

                 │
                 ▼
         Data Validation

                 │
                 ▼
          Market Memory

                 │
                 ▼
          MemoryReader

                 │
                 ▼
           GoldBot Core
```

---

# Bootstrap Flow

```text
GoldBot Start

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
```

Bootstrap faqat tizim ishga tushganda bajariladi.

---

# Recovery Flow

```text
Gap Detected

↓

HistoricalDataService

↓

Recovery

↓

Historical Provider

↓

Historical Database

↓

Data Validation

↓

Market Memory

↓

Recovery Completed
```

Recovery faqat yetishmayotgan tarixiy ma'lumotlarni tiklaydi.

---

# Historical Download Flow

```text
HistoricalDataService

↓

Provider Factory

↓

Historical Provider

↓

Build Request

↓

Download Historical Data

↓

Normalize Response

↓

Historical Database
```

---

# Validation Flow

```text
Historical Database

↓

Data Validation

↓

Structure Validation

↓

Integrity Check

↓

Validation Passed

↓

Market Memory
```

---

# Memory Update Flow

```text
Market Memory

↓

Memory Updated

↓

MemoryReader

↓

GoldBot Core
```

---

# Read Flow

```text
GoldBot Core

↓

MemoryReader

↓

Market Memory

↓

Historical Data

↓

Return Result
```

---

# Error Flow

```text
Historical Provider

↓

Request Failed

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

# Runtime Rules

1. Historical Data oqimi doimo Provider Factory'dan boshlanadi.

2. HistoricalDataService barcha oqimni boshqaradi.

3. Bootstrap va Recovery parallel ishlamaydi.

4. Historical Database Validation'dan oldingi oxirgi bosqich hisoblanadi.

5. Validation muvaffaqiyatli tugamaguncha Market Memory yangilanmaydi.

6. MemoryReader faqat Market Memory'dan o'qiydi.

7. GoldBot Core Historical Data bilan bevosita ishlamaydi.

8. Historical Data Flow Live Data Flow'dan mustaqil ishlaydi.

---

# State Flow

```text
Idle

↓

Request Created

↓

Downloading

↓

Normalizing

↓

Database Updated

↓

Validating

↓

Memory Updated

↓

Completed

or

Failed
```

---

# Golden Rules

• Historical Data oqimi har doim bir xil ketma-ketlikda ishlaydi.

• Provider → Database → Validation → Memory tartibi buzilmaydi.

• Bootstrap va Recovery bir xil Data Flow'dan foydalanadi.

• Validation majburiy.

• Market Memory faqat tasdiqlangan ma'lumotni qabul qiladi.

• GoldBot Core faqat MemoryReader orqali ma'lumot oladi.

• Circular Flow taqiqlanadi.

---

# Summary

Historical Data Flow Sequence Diagram Historical Data modulidagi barcha Runtime Data Flow ketma-ketligini belgilaydi.

Canonical Runtime Sequence:

External Historical Provider

↓

Provider Factory

↓

Historical Provider

↓

HistoricalDataService

↓

Bootstrap / Recovery

↓

Historical Database

↓

Data Validation

↓

Market Memory

↓

MemoryReader

↓

GoldBot Core

Ushbu ketma-ketlik Historical Data Flow moduli uchun yagona rasmiy Runtime Sequence hisoblanadi.
