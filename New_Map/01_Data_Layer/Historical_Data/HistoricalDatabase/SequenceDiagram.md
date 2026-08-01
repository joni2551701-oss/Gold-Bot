# Historical Database Sequence Diagram

Status: CANONICAL

---

# Purpose

Ushbu hujjat Historical Database modulining Runtime Sequence (ishlash ketma-ketligi) ni tavsiflaydi.

Bu hujjat Historical Database qanday ma'lumot qabul qilishi, qanday saqlashi va qanday qilib boshqa modullarga ma'lumot taqdim etishini belgilaydi.

Bu implementatsiya emas.

Bu Historical Database modulining Canonical Runtime Blueprint hisoblanadi.

---

# Database Write Sequence

Historical Data bazaga yozilganda.

```text
Historical Provider

        │
        ▼
HistoricalDataService

        │
        ▼
Historical Database

        │
        ▼
Duplicate Check

        │
        ▼
Store Candle

        │
        ▼
Write Success
```

---

# Bootstrap Read Sequence

Bootstrap tarixiy ma'lumotni o'qiganda.

```text
Bootstrap

        │
        ▼
HistoricalDataService

        │
        ▼
Historical Database

        │
        ▼
Read Historical Data

        │
        ▼
Return Candles

        │
        ▼
Bootstrap
```

---

# Recovery Read Sequence

Recovery Missing Data tekshirayotganda.

```text
Recovery

        │
        ▼
HistoricalDataService

        │
        ▼
Historical Database

        │
        ▼
Read Existing Data

        │
        ▼
Compare History

        │
        ▼
Gap Detected
```

---

# Validation Sequence

Yozilgan ma'lumot Validation'ga uzatilganda.

```text
Historical Database

        │
        ▼
Data Validation

        │
        ▼
Validation Passed

        │
        ▼
Market Memory
```

---

# Query Sequence

Historical ma'lumot so'ralganda.

```text
HistoricalDataService

        │
        ▼
Historical Database

        │
        ▼
Execute Query

        │
        ▼
Load Candles

        │
        ▼
Return Result
```

---

# Duplicate Sequence

Duplicate Candle kelganda.

```text
Store Request

↓

Historical Database

↓

Duplicate Check

↓

Duplicate Found

↓

Ignore Write

↓

Return Status
```

---

# Failure Sequence

Bazaga yozishda xatolik yuz bersa.

```text
HistoricalDataService

↓

Historical Database

↓

Write Failed

↓

Database Error

↓

Return Error

↓

HistoricalDataService
```

---

# Startup Sequence

GoldBot ishga tushganda.

```text
GoldBot Start

↓

Bootstrap

↓

HistoricalDataService

↓

Historical Database

↓

Load Historical Data

↓

Return History

↓

Bootstrap Continue
```

---

# Runtime Rules

1. Historical Database faqat HistoricalDataService orqali ishlaydi.

2. Har bir yozishdan oldin Duplicate Check bajariladi.

3. Timestamp tartibi saqlanishi shart.

4. Historical Database ma'lumotni o'zgartirmaydi.

5. Historical Database Validation bajarmaydi.

6. Historical Database Market Memory'ni to'g'ridan-to'g'ri yangilamaydi.

7. Historical Database faqat tarixiy ma'lumotlarni boshqaradi.

8. Har qanday yozish natijasi HistoricalDataService'ga qaytariladi.

---

# State Flow

```text
Idle

↓

Reading

↓

Writing

↓

Checking Duplicate

↓

Completed

or

Failed
```

---

# Golden Rules

• Historical Database faqat Storage modulidir.

• Historical Database hisob-kitob qilmaydi.

• Historical Database Validation bajarmaydi.

• Duplicate Candle saqlanmaydi.

• Timestamp tartibi buzilmaydi.

• Database faqat HistoricalDataService bilan ishlaydi.

• Database Market Memory bilan bevosita ishlamaydi.

• Database GoldBot Core bilan ishlamaydi.

---

# Summary

Historical Database Sequence Diagram Historical Database modulining bajarilish ketma-ketligini belgilaydi.

Canonical Runtime Sequence:

HistoricalDataService

↓

Historical Database

↓

Duplicate Check

↓

Store Historical Data

↓

Return Result

↓

Data Validation

↓

Market Memory

Ushbu ketma-ketlik Historical Database moduli uchun yagona rasmiy Runtime Sequence hisoblanadi.
