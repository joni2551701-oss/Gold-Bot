# Recovery

Status: CANONICAL

---

# Purpose

Recovery — Historical Data modulining ma'lumotlarni tiklash (Recovery) komponentidir.

Uning asosiy vazifasi tizim uzilganda, provider ishlamay qolganda yoki tarixiy ma'lumotlarda bo'shliqlar (Data Gaps) paydo bo'lganda yetishmayotgan ma'lumotlarni aniqlash va tiklashdir.

Recovery faqat kerakli ma'lumotlarni tiklaydi.

Recovery hech qachon to'liq Bootstrap vazifasini bajarmaydi.

---

# Objective

Recovery quyidagi vazifalarni bajaradi:

• Missing Data Detection

• Historical Gap Recovery

• Partial Synchronization

• Data Integrity Recovery

• Provider Reconnection Recovery

• Market Memory Recovery

---

# Layer Position

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

---

# Responsibilities

Recovery:

✓ Missing Candle aniqlash

✓ Missing Candle yuklash

✓ Historical Gap tiklash

✓ Provider uzilgandan keyin sinxronlash

✓ Historical Database yangilash

✓ Market Memory tiklash

✓ Recovery natijasini qaytarish

---

# Not Responsible

Recovery:

✗ Initial Bootstrap

✗ Live Streaming

✗ Current Price

✗ Candle Building

✗ Strategy

✗ Context

✗ Decision

✗ Risk

✗ Signal Generation

---

# Input

Recovery quyidagilarni qabul qiladi:

• Recovery Request

• Symbols

• Timeframes

• Missing Range

• Historical Provider

---

# Output

Recovery quyidagilarni yaratadi:

• Missing Historical Data

• Recovered Candles

• Recovery Status

• Updated Historical Database

• Updated Market Memory

---

# Recovery Flow

Recovery Requested

↓

HistoricalDataService

↓

Recovery

↓

Gap Detection

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

---

# Recovery Triggers

Recovery quyidagi holatlarda ishga tushadi:

• Provider Reconnected

• Missing Candle Detected

• Missing Timeframe

• Missing Symbol

• Startup Integrity Check

• Manual Recovery Request

---

# Recovery Types

## Gap Recovery

Faqat yetishmayotgan Candle'larni yuklaydi.

---

## Partial Recovery

Ma'lum vaqt oralig'ini tiklaydi.

---

## Full Recovery

Kerak bo'lganda to'liq tarixni qayta tiklaydi.

(Faqat HistoricalDataService ruxsati bilan.)

---

# Golden Rules

1. Recovery faqat yetishmayotgan ma'lumotlarni tiklaydi.

2. Recovery Bootstrap o'rnini bosmaydi.

3. Har bir yuklangan ma'lumot Validation'dan o'tishi shart.

4. Recovery mavjud ma'lumotlarni qayta yuklamaydi.

5. Recovery Market Memory'ni faqat Validation'dan keyin yangilaydi.

6. Recovery Provider orqali ishlaydi.

7. Recovery GoldBot Core bilan to'g'ridan-to'g'ri ishlamaydi.

8. Recovery yakunlangandan keyin HistoricalDataService natijani tekshiradi.

---

# Related Documents

Recovery/

├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md

---

# Summary

Recovery — Historical Data modulining ma'lumotlarni tiklash komponentidir.

Uning vazifasi:

• yetishmayotgan tarixiy ma'lumotlarni aniqlash;

• providerdan kerakli ma'lumotlarni qayta yuklash;

• Historical Database va Market Memory'ni tiklash;

• Data Layer yaxlitligini saqlash.

Recovery faqat zarur bo'lgan ma'lumotlarni tiklaydi va hech qachon Bootstrap jarayonining o'rnini bosmaydi.
