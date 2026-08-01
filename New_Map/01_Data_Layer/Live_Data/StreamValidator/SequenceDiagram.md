# StreamValidator Sequence Diagram

Status: CANONICAL

---

# Purpose

Ushbu hujjat StreamValidator modulining Runtime Sequence (ishlash ketma-ketligi) ni tavsiflaydi.

StreamValidator Live Data Pipeline ichida CurrentPriceProvider tomonidan uzatilgan Tick ma'lumotlarini tekshiradi, noto'g'ri ma'lumotlarni filtrlaydi va faqat tasdiqlangan Tick'larni CandleBuilder moduliga uzatadi.

Bu implementatsiya emas.

Bu StreamValidator modulining Canonical Runtime Blueprint hisoblanadi.

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
StreamValidator

        │
        ▼
Receive Tick

        │
        ▼
Validate Tick

        │
        ▼
Validation Passed

        │
        ▼
CandleBuilder

        │
        ▼
Market Memory

        │
        ▼
GoldBot Core
```

---

# Tick Validation Sequence

```text
CurrentPriceProvider

↓

Receive Tick

↓

StreamValidator

↓

Timestamp Validation

↓

Symbol Validation

↓

Price Validation

↓

Duplicate Check

↓

Integrity Check

↓

Validation Passed
```

---

# Duplicate Tick Sequence

```text
Receive Tick

↓

StreamValidator

↓

Duplicate Check

↓

Duplicate Found

↓

Reject Tick

↓

Notify PriceStreamService
```

---

# Invalid Tick Sequence

```text
Receive Tick

↓

StreamValidator

↓

Validation Failed

↓

Reject Tick

↓

Log Validation Error

↓

Notify PriceStreamService
```

---

# Missing Tick Sequence

```text
Receive Tick

↓

Gap Detection

↓

Missing Tick Found

↓

Generate Warning

↓

Notify PriceStreamService
```

---

# Successful Validation Sequence

```text
Receive Tick

↓

Validation Passed

↓

Publish Validated Tick

↓

CandleBuilder

↓

Update Candle
```

---

# Stream Quality Monitoring Sequence

```text
Receive Tick

↓

Measure Stream Quality

↓

Update Stream Statistics

↓

Check Health Status

↓

Report Stream Status
```

---

# Error Sequence

```text
Validation Error

↓

StreamValidator

↓

Create Error Report

↓

Publish Error Event

↓

Notify PriceStreamService
```

---

# Runtime Rules

1. Har bir Tick StreamValidator orqali o'tishi shart.

2. Validation'dan o'tmagan Tick keyingi modulga uzatilmaydi.

3. Duplicate Tick rad etiladi.

4. Timestamp tekshiruvi majburiy.

5. Symbol tekshiruvi majburiy.

6. Price tekshiruvi majburiy.

7. Validation muvaffaqiyatli tugagandan keyingina CandleBuilder ishlaydi.

8. StreamValidator Market Memory bilan bevosita ishlamaydi.

---

# State Flow

```text
Idle

↓

Waiting Tick

↓

Validating

↓

Integrity Check

↓

Publishing

↓

Completed

or

Rejected

or

Failed
```

---

# Golden Rules

• Har bir Tick tekshirilishi shart.

• Validation Pipeline chetlab o'tilmaydi.

• Duplicate Tick qabul qilinmaydi.

• Invalid Tick qabul qilinmaydi.

• Stream sifati doim kuzatiladi.

• CandleBuilder faqat Validated Tick oladi.

• Market Memory faqat Validated Candle oladi.

• Circular Sequence taqiqlanadi.

---

# Summary

StreamValidator Sequence Diagram Live Data Pipeline ichidagi Tick Validation ketma-ketligini belgilaydi.

Canonical Runtime Sequence:

Live Provider

↓

PriceStreamService

↓

CurrentPriceProvider

↓

StreamValidator

↓

Tick Validation

↓

Validation Passed

↓

CandleBuilder

↓

Market Memory

↓

Memory Reader

↓

GoldBot Core

Ushbu ketma-ketlik StreamValidator moduli uchun yagona rasmiy Runtime Sequence hisoblanadi.
