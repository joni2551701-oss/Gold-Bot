# CandleBuilder Sequence Diagram

Status: CANONICAL

---

# Purpose

Ushbu hujjat CandleBuilder modulining Runtime Sequence (ishlash ketma-ketligi) ni tavsiflaydi.

CandleBuilder Live Data Pipeline ichida Validation'dan o'tgan Tick ma'lumotlarini qabul qiladi, ularni OHLC Candle'ga aylantiradi va tayyor Candle'ni Market Memory'ga uzatadi.

Bu implementatsiya emas.

Bu CandleBuilder modulining Canonical Runtime Blueprint hisoblanadi.

---

# Complete Runtime Sequence

```text
Live Provider

        │
        ▼
PriceStreamService

        │
        ▼
CurrentPriceProvider

        │
        ▼
Stream Validator

        │
        ▼
CandleBuilder

        │
        ▼
Update Current Candle

        │
        ▼
Close Candle (if needed)

        │
        ▼
Open New Candle

        │
        ▼
Market Memory

        │
        ▼
GoldBot Core
```

---

# Tick Processing Sequence

```text
Validated Tick

↓

CandleBuilder

↓

Find Active Candle

↓

Update OHLC

↓

Update Timestamp

↓

Return Current Candle
```

---

# New Candle Sequence

```text
Timeframe Completed

↓

Close Current Candle

↓

Store Closed Candle

↓

Create New Candle

↓

Set Open Price

↓

Start New Timeframe
```

---

# Candle Update Sequence

```text
Receive Tick

↓

Current Candle

↓

Update High

↓

Update Low

↓

Update Close

↓

Update Volume

↓

Publish Candle
```

---

# Multi-Timeframe Sequence

```text
Validated Tick

↓

M1 Candle

↓

M5 Candle

↓

M15 Candle

↓

H1 Candle

↓

H4 Candle

↓

Daily Candle
```

Har bir Timeframe mustaqil ravishda yangilanadi.

---

# Market Memory Sequence

```text
CandleBuilder

↓

Completed Candle

↓

Market Memory

↓

Memory Updated

↓

Memory Reader

↓

GoldBot Core
```

---

# Error Sequence

```text
Validated Tick

↓

CandleBuilder

↓

Build Failed

↓

Report Error

↓

Notify PriceStreamService
```

---

# Restart Sequence

```text
System Restart

↓

Load Active Candle

↓

Resume Candle

↓

Continue Updates
```

---

# Runtime Rules

1. CandleBuilder faqat Validation'dan o'tgan Tick bilan ishlaydi.

2. Har bir Tick faqat bitta faol Candle'ni yangilaydi.

3. Har bir Candle faqat bitta Timeframe'ga tegishli bo'ladi.

4. Candle yopilgandan keyin qayta o'zgartirilmaydi.

5. Yangi Candle faqat oldingi Candle yopilgandan keyin yaratiladi.

6. Multi-Timeframe Candle'lar mustaqil ravishda yangilanadi.

7. CandleBuilder Market Memory'ga faqat tayyor Candle uzatadi.

8. GoldBot Core CandleBuilder bilan bevosita ishlamaydi.

---

# State Flow

```text
Idle

↓

Waiting Tick

↓

Updating Candle

↓

Closing Candle

↓

Opening New Candle

↓

Publishing

↓

Completed

or

Failed
```

---

# Golden Rules

• CandleBuilder faqat tasdiqlangan Tick bilan ishlaydi.

• Har bir Candle bitta Timeframe uchun yaratiladi.

• Open narxi Candle boshida bir marta belgilanadi.

• High va Low faqat kengayishi mumkin.

• Close har bir Tick bilan yangilanadi.

• Yopilgan Candle qayta o'zgartirilmaydi.

• Market Memory faqat yakuniy Candle'ni qabul qiladi.

• Circular Sequence taqiqlanadi.

---

# Summary

CandleBuilder Sequence Diagram Live Data Pipeline ichidagi OHLC Candle yaratish va yangilash ketma-ketligini belgilaydi.

Canonical Runtime Sequence:

Live Provider

↓

PriceStreamService

↓

CurrentPriceProvider

↓

Stream Validator

↓

CandleBuilder

↓

Update Current Candle

↓

Close Candle

↓

Open New Candle

↓

Market Memory

↓

Memory Reader

↓

GoldBot Core

Ushbu ketma-ketlik CandleBuilder moduli uchun yagona rasmiy Runtime Sequence hisoblanadi.
