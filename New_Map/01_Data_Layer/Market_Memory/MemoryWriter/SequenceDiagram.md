# MemoryWriter Sequence Diagram

Status: CANONICAL

---

# Purpose

Ushbu hujjat MemoryWriter modulining Runtime Sequence (ishlash ketma-ketligi) ni tavsiflaydi.

MemoryWriter Live Data Layer'dan kelgan tasdiqlangan (Validated) market ma'lumotlarini qabul qiladi va ularni MemoryStorage'ga yozadi.

Bu implementatsiya emas.

Bu MemoryWriter modulining Canonical Runtime Blueprint hisoblanadi.

---

# Complete Runtime Sequence

```text
Live Data Layer

        │
        ▼
MemoryWriter

        │
        ▼
Receive Write Request

        │
        ▼
Validate Request

        │
        ▼
MemoryStorage

        │
        ▼
Persist Memory

        │
        ▼
Update Version

        │
        ▼
Publish Write Event

        │
        ▼
MemoryReader

        │
        ▼
GoldBot Core
```

---

# Candle Write Sequence

```text
Validated Candle

↓

MemoryWriter

↓

Validate Request

↓

MemoryStorage

↓

Persist Candle

↓

Update Version

↓

Write Complete
```

---

# Current Price Write Sequence

```text
Current Price

↓

MemoryWriter

↓

MemoryStorage

↓

Update Runtime State

↓

Write Complete
```

---

# Snapshot Write Sequence

```text
Snapshot Request

↓

MemoryWriter

↓

MemoryStorage

↓

Persist Snapshot

↓

Snapshot Ready
```

---

# Recovery Write Sequence

```text
Recovery Request

↓

MemoryWriter

↓

MemoryStorage

↓

Restore Runtime State

↓

Recovery Complete
```

---

# Error Sequence

```text
Write Failed

↓

Create Error Event

↓

Retry Write

↓

Retry Failed

↓

Recovery Mode

or

Write Failed
```

---

# Runtime Rules

1. MemoryWriter faqat Live Data Layer'dan yozuv qabul qiladi.

2. Har bir Write Request tekshirilishi shart.

3. MemoryWriter faqat MemoryStorage'ga yozadi.

4. Version faqat muvaffaqiyatli yozuvdan keyin yangilanadi.

5. MemoryReader yozuv tugagandan keyin yangi ma'lumotni o'qiydi.

6. GoldBot Core MemoryWriter bilan bevosita ishlamaydi.

7. Runtime Sequence qat'iy saqlanadi.

8. Circular Runtime Sequence qat'iyan taqiqlanadi.

---

# State Flow

```text
Idle

↓

Waiting Request

↓

Validating

↓

Writing

↓

Persisting

↓

Completed

↓

Ready

or

Failed
```

---

# Golden Rules

• MemoryWriter yagona Canonical Write Interface hisoblanadi.

• MemoryStorage yagona Storage hisoblanadi.

• Har bir Write Request tekshiriladi.

• Memory faqat muvaffaqiyatli yoziladi.

• Version avtomatik yangilanadi.

• GoldBot Core MemoryWriter bilan ishlamaydi.

• Circular Sequence taqiqlanadi.

---

# Summary

MemoryWriter Sequence Diagram Runtime Write jarayonining bajarilish ketma-ketligini belgilaydi.

Canonical Runtime Sequence:

Live Data Layer

↓

MemoryWriter

↓

Validate Request

↓

MemoryStorage

↓

Persist Memory

↓

Update Version

↓

Publish Write Event

↓

MemoryReader

↓

GoldBot Core

Ushbu ketma-ketlik MemoryWriter moduli uchun yagona rasmiy Runtime Sequence hisoblanadi.
