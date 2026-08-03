# Recovery Sequence Diagram

Status: CANONICAL

---

# Purpose

Ushbu hujjat Recovery modulining Runtime Sequence (ishlash ketma-ketligi) ni tavsiflaydi.

Recovery qachon ishga tushishi, qanday modullar bilan ishlashi va ma'lumotlar qanday oqim bo'yicha harakatlanishini belgilaydi.

Bu implementatsiya emas.

Bu Recovery modulining Canonical Runtime Blueprint hisoblanadi.

---

# Recovery Trigger Sequence

Recovery quyidagi holatlardan biri sodir bo'lganda ishga tushadi.

```text
Market Open

or

Provider Reconnected

or

Gap Detected

or

Manual Recovery Request

        │
        ▼
HistoricalDataService

        │
        ▼
Recovery
```

---

# Complete Recovery Sequence

```text
HistoricalDataService

        │
        ▼
Recovery

        │
        ▼
Gap Detection

        │
        ▼
Provider Factory

        │
        ▼
Historical Provider

        │
        ▼
Download Missing Data

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
Event Bus

        │
        ▼
Recovery Completed
```

---

# Missing Candle Recovery

Agar Candle yetishmasa.

```text
Missing Candle

↓

Recovery

↓

Historical Provider

↓

Download Candle

↓

Historical Database

↓

Data Validation

↓

Market Memory

↓

Recovery Success
```

---

# Missing Timeframe Recovery

Agar timeframe ma'lumotlari yetishmasa.

```text
Missing Timeframe

↓

Recovery

↓

Historical Provider

↓

Download Timeframe

↓

Historical Database

↓

Data Validation

↓

Market Memory
```

---

# Provider Reconnect Recovery

Provider qayta ulanganda.

```text
Provider Reconnected

↓

Recovery

↓

Compare Database

↓

Find Missing Range

↓

Historical Provider

↓

Download Missing Data

↓

Validation

↓

Market Memory

↓

Recovery Completed
```

---

# Validation Failed Sequence

Validation muvaffaqiyatsiz bo'lsa.

```text
Recovery

↓

Historical Provider

↓

Downloaded Data

↓

Data Validation

↓

Validation Failed

↓

Reject Data

↓

Retry Recovery
```

---

# Provider Failure Sequence

Provider javob bermasa.

```text
Recovery

↓

Historical Provider

↓

Connection Failed

↓

Retry

↓

Retry Failed

↓

Recovery Failed

↓

Notify HistoricalDataService
```

---

# Successful Recovery Sequence

```text
Recovery Started

↓

Gap Detected

↓

Download Missing Data

↓

Validation Passed

↓

Database Updated

↓

Market Memory Updated

↓

Recovery Completed
```

---

# Runtime Rules

1. Recovery faqat HistoricalDataService tomonidan ishga tushiriladi.

2. Recovery Bootstrap tugagandan keyin ishlashi mumkin.

3. Recovery faqat yetishmayotgan ma'lumotlarni yuklaydi.

4. Har bir yuklangan ma'lumot Validation'dan o'tishi shart.

5. Validation muvaffaqiyatsiz bo'lsa ma'lumot bekor qilinadi.

6. Recovery Market Memory'ni faqat Validation'dan keyin yangilaydi.

7. Recovery tugagandan keyin Event Bus RecoveryCompleted hodisasini yuboradi.

8. Recovery hech qachon Live Data oqimini to'xtatmaydi (zarur holatlar bundan mustasno).

---

# Recovery State Flow

```text
Idle

↓

Requested

↓

Running

↓

Downloading

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

• Recovery Bootstrap o'rnini bosmaydi.

• Recovery faqat Gap yoki Missing Data uchun ishlaydi.

• Validation majburiy.

• Provider orqali ma'lumot olinadi.

• Market Memory faqat tasdiqlangan ma'lumotni qabul qiladi.

• Recovery yakunida Event Bus xabar yuboradi.

• Recovery GoldBot Core bilan to'g'ridan-to'g'ri ishlamaydi.

---

# Summary

Recovery Sequence Diagram Recovery modulining bajarilish tartibini belgilaydi.

Canonical Runtime Sequence:

Recovery Request

↓

Gap Detection

↓

Historical Provider

↓

Download Missing Data

↓

Historical Database

↓

Data Validation

↓

Market Memory

↓

Event Bus

↓

Recovery Completed

Ushbu ketma-ketlik Recovery moduli uchun yagona rasmiy Runtime Sequence hisoblanadi.
