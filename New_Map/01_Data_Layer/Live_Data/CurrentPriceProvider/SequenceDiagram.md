# CurrentPriceProvider Sequence Diagram

Status: CANONICAL

---

# Purpose

Ushbu hujjat CurrentPriceProvider modulining Runtime Sequence (ishlash ketma-ketligi) ni tavsiflaydi.

CurrentPriceProvider Live Data Pipeline ichida Live Provider'dan kelgan Tick ma'lumotlarini qabul qiladi, Current Price'ni yangilaydi va keyingi modullarga uzatadi.

Bu implementatsiya emas.

Bu CurrentPriceProvider modulining Canonical Runtime Blueprint hisoblanadi.

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
Receive Tick

        │
        ▼
Update Current Price

        │
        ▼
Publish Price Update

        │
        ▼
Stream Validator

        │
        ▼
Candle Builder

        │
        ▼
Market Memory

        │
        ▼
GoldBot Core
```

---

# Tick Receive Sequence

```text
Live Provider

↓

New Tick

↓

PriceStreamService

↓

CurrentPriceProvider

↓

Receive Tick

↓

Update Current Price
```

---

# Price Update Sequence

```text
CurrentPriceProvider

↓

Extract Bid

↓

Extract Ask

↓

Calculate Mid Price (Optional)

↓

Update Current Price

↓

Publish Update
```

---

# Validation Sequence

```text
CurrentPriceProvider

↓

Price Update

↓

Stream Validator

↓

Validation Passed

↓

Candle Builder
```

CurrentPriceProvider Validation bajarmaydi.

Faqat Stream Validator'ga uzatadi.

---

# Candle Update Sequence

```text
CurrentPriceProvider

↓

Validated Price

↓

Candle Builder

↓

Current Candle Updated

↓

Market Memory
```

---

# Market Memory Sequence

```text
CurrentPriceProvider

↓

Latest Price

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

# Provider Reconnect Sequence

```text
Provider Disconnected

↓

Reconnect

↓

Receive First Tick

↓

Update Current Price

↓

Resume Streaming
```

---

# Error Sequence

```text
Live Provider

↓

Invalid Tick

↓

CurrentPriceProvider

↓

Reject Tick

↓

Notify PriceStreamService
```

---

# Runtime Rules

1. CurrentPriceProvider faqat PriceStreamService tomonidan boshqariladi.

2. Har bir Tick ketma-ket qayta ishlanadi.

3. Har bir Tick Current Price'ni yangilaydi.

4. CurrentPriceProvider Validation bajarmaydi.

5. Validation Stream Validator tomonidan bajariladi.

6. Candle Builder faqat Validation'dan o'tgan narxni qabul qiladi.

7. Market Memory faqat tasdiqlangan ma'lumot bilan yangilanadi.

8. GoldBot Core CurrentPriceProvider bilan bevosita ishlamaydi.

---

# State Flow

```text
Idle

↓

Waiting Tick

↓

Receiving Tick

↓

Updating Price

↓

Publishing

↓

Completed

or

Failed
```

---

# Golden Rules

• CurrentPriceProvider yagona Current Price manbai hisoblanadi.

• Har bir Tick Current Price'ni yangilaydi.

• Tick tartibi saqlanishi shart.

• Validation alohida modul tomonidan bajariladi.

• Candle Builder faqat tasdiqlangan narxni qabul qiladi.

• Market Memory faqat yakuniy narxni qabul qiladi.

• CurrentPriceProvider History saqlamaydi.

• Circular Sequence taqiqlanadi.

---

# Summary

CurrentPriceProvider Sequence Diagram Live Data Pipeline ichidagi joriy narxni boshqarish ketma-ketligini belgilaydi.

Canonical Runtime Sequence:

Live Provider

↓

PriceStreamService

↓

CurrentPriceProvider

↓

Update Current Price

↓

Stream Validator

↓

Candle Builder

↓

Market Memory

↓

Memory Reader

↓

GoldBot Core

Ushbu ketma-ketlik CurrentPriceProvider moduli uchun yagona rasmiy Runtime Sequence hisoblanadi.
