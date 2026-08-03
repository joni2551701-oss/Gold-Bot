# LiveProviders Sequence Diagram

Status: CANONICAL

---

# Purpose

Ushbu hujjat LiveProviders modulining Runtime Sequence (ishlash ketma-ketligi) ni tavsiflaydi.

LiveProviders tashqi Exchange yoki Market Data Provider'lari bilan ulanishni boshqaradi, Real-Time Tick ma'lumotlarini qabul qiladi va ularni PriceStreamService'ga uzatadi.

Bu implementatsiya emas.

Bu LiveProviders modulining Canonical Runtime Blueprint hisoblanadi.

---

# Complete Runtime Sequence

```text
Configuration

        │
        ▼
PriceStreamService

        │
        ▼
LiveProviders

        │
        ▼
Connect Provider

        │
        ▼
Authenticate

        │
        ▼
Subscribe Symbols

        │
        ▼
Receive Live Tick

        │
        ▼
Publish Tick

        │
        ▼
PriceStreamService

        │
        ▼
CurrentPriceProvider
```

---

# Provider Connection Sequence

```text
PriceStreamService

↓

LiveProviders

↓

Load Provider Configuration

↓

Open Connection

↓

Authenticate

↓

Connection Established
```

---

# Symbol Subscription Sequence

```text
Connection Ready

↓

Subscribe Symbols

↓

Provider Accepted

↓

Streaming Enabled
```

---

# Live Tick Sequence

```text
Exchange API

↓

LiveProviders

↓

Receive Tick

↓

Create Provider Event

↓

Publish Tick

↓

PriceStreamService
```

---

# Provider Health Monitoring Sequence

```text
LiveProviders

↓

Check Connection

↓

Measure Latency

↓

Verify Stream

↓

Update Health Status

↓

Publish Health Event
```

---

# Provider Failover Sequence

```text
Primary Provider Failed

↓

Detect Failure

↓

Select Backup Provider

↓

Reconnect

↓

Authenticate

↓

Resume Streaming
```

---

# Reconnect Sequence

```text
Connection Lost

↓

Retry Connection

↓

Reconnect Provider

↓

Restore Subscription

↓

Continue Streaming
```

---

# Shutdown Sequence

```text
PriceStreamService

↓

Stop Streaming

↓

Unsubscribe Symbols

↓

Disconnect Provider

↓

Release Resources
```

---

# Error Sequence

```text
Provider Error

↓

LiveProviders

↓

Create Error Event

↓

Retry Connection

↓

Retry Failed

↓

Notify PriceStreamService
```

---

# Runtime Rules

1. LiveProviders faqat PriceStreamService tomonidan boshqariladi.

2. Har bir Provider ulanishdan oldin autentifikatsiyadan o'tishi shart.

3. Streaming faqat Symbol Subscription muvaffaqiyatli tugagandan keyin boshlanadi.

4. Har bir Tick o'zgartirilmasdan PriceStreamService'ga uzatiladi.

5. Provider uzilganda Reconnect yoki Failover ishga tushadi.

6. Connection Health doim monitoring qilinadi.

7. LiveProviders Tick Validation bajarmaydi.

8. LiveProviders GoldBot Core bilan bevosita ishlamaydi.

---

# State Flow

```text
Idle

↓

Loading Configuration

↓

Connecting

↓

Authenticating

↓

Subscribing

↓

Streaming

↓

Reconnecting

↓

Disconnected

or

Failed
```

---

# Golden Rules

• LiveProviders tashqi Provider bilan ishlovchi yagona modul hisoblanadi.

• Provider Connection doim monitoring qilinadi.

• Tick ma'lumotlari o'zgartirilmaydi.

• Validation keyingi modul tomonidan bajariladi.

• Provider almashtirish avtomatik amalga oshirilishi mumkin.

• Streaming uzilganda Recovery ishga tushadi.

• PriceStreamService yagona Consumer hisoblanadi.

• Circular Sequence taqiqlanadi.

---

# Summary

LiveProviders Sequence Diagram tashqi Market Data Provider bilan ulanish va Live Tick oqimining Runtime ketma-ketligini belgilaydi.

Canonical Runtime Sequence:

Configuration

↓

PriceStreamService

↓

LiveProviders

↓

Connect Provider

↓

Authenticate

↓

Subscribe Symbols

↓

Receive Live Tick

↓

Publish Tick

↓

PriceStreamService

↓

CurrentPriceProvider

Ushbu ketma-ketlik LiveProviders moduli uchun yagona rasmiy Runtime Sequence hisoblanadi.
