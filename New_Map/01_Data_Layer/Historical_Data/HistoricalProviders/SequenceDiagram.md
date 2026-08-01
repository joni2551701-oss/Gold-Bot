# Historical Providers Sequence Diagram

Status: CANONICAL

---

# Purpose

Ushbu hujjat Historical Providers modulining Runtime Sequence (ishlash ketma-ketligi) ni tavsiflaydi.

Bu hujjat Historical Provider qanday ishga tushishi, HistoricalDataService bilan qanday ishlashi va tarixiy market ma'lumotlarini qanday uzatishini belgilaydi.

Bu implementatsiya emas.

Bu Historical Providers modulining Canonical Runtime Blueprint hisoblanadi.

---

# Startup Sequence

HistoricalDataService Bootstrap yoki Recovery jarayonida Historical Provider'ni chaqiradi.

```text
HistoricalDataService

        │
        ▼
Provider Factory

        │
        ▼
Historical Provider

        │
        ▼
Authentication

        │
        ▼
Provider Ready
```

---

# Historical Download Sequence

```text
HistoricalDataService

        │
        ▼
Provider Factory

        │
        ▼
Historical Provider

        │
        ▼
Build Request

        │
        ▼
Provider API

        │
        ▼
Receive Response

        │
        ▼
Normalize Data

        │
        ▼
HistoricalDataService
```

---

# Bootstrap Sequence

```text
Bootstrap

↓

HistoricalDataService

↓

Provider Factory

↓

Historical Provider

↓

Download Historical Data

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

# Recovery Sequence

```text
Recovery

↓

HistoricalDataService

↓

Provider Factory

↓

Historical Provider

↓

Download Missing Data

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

# Authentication Sequence

```text
Historical Provider

↓

Load Credentials

↓

Authenticate

↓

Provider Connected
```

---

# Error Sequence

```text
Historical Provider

↓

API Request

↓

Provider Error

↓

Retry

↓

Retry Failed

↓

Return Error

↓

HistoricalDataService
```

---

# Timeout Sequence

```text
Historical Provider

↓

API Request

↓

Timeout

↓

Retry

↓

Timeout

↓

Provider Failed
```

---

# Successful Response Sequence

```text
Historical Provider

↓

API Request

↓

Receive Data

↓

Normalize Response

↓

Validate Response Format

↓

HistoricalDataService
```

---

# Runtime Rules

1. Historical Provider faqat HistoricalDataService tomonidan chaqiriladi.

2. Har bir so'rov Provider Factory orqali yaratiladi.

3. Authentication muvaffaqiyatli bo'lishi shart.

4. Provider javobi standart formatga o'tkaziladi (Normalization).

5. Provider ma'lumotni Validation'siz Market Memory'ga yubormaydi.

6. Provider faqat HistoricalDataService bilan ishlaydi.

7. Provider GoldBot Core bilan to'g'ridan-to'g'ri ishlamaydi.

8. Provider xatolari HistoricalDataService tomonidan boshqariladi.

---

# State Flow

```text
Idle

↓

Connecting

↓

Authenticated

↓

Downloading

↓

Normalizing

↓

Completed

or

Failed
```

---

# Golden Rules

• Provider faqat tarixiy ma'lumotlarni yuklaydi.

• Provider faqat Provider Factory orqali yaratiladi.

• Authentication majburiy.

• Response Normalize qilinishi shart.

• HistoricalDataService Provider natijasini boshqaradi.

• Provider Validation bajarmaydi.

• Provider Database bilan ishlamaydi.

• Provider Market Memory bilan ishlamaydi.

---

# Summary

Historical Providers Sequence Diagram Historical Provider modulining bajarilish tartibini belgilaydi.

Canonical Runtime Sequence:

HistoricalDataService

↓

Provider Factory

↓

Historical Provider

↓

Authentication

↓

API Request

↓

Receive Response

↓

Normalize Data

↓

HistoricalDataService

↓

Historical Database

↓

Data Validation

↓

Market Memory

Ushbu ketma-ketlik Historical Providers moduli uchun yagona rasmiy Runtime Sequence hisoblanadi.
