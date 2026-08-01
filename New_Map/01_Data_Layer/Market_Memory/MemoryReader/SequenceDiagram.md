# MemoryReader Sequence Diagram

Status: CANONICAL

---

# Purpose

Ushbu hujjat MemoryReader modulining Runtime Sequence (ishlash ketma-ketligi) ni tavsiflaydi.

MemoryReader MemoryStorage'dan Runtime Market Memory'ni o'qiydi va GoldBot Core hamda ruxsat etilgan modullarga taqdim etadi.

Bu implementatsiya emas.

Bu MemoryReader modulining Canonical Runtime Blueprint hisoblanadi.

---

# Complete Runtime Sequence

```text
GoldBot Core

        │
        ▼
MemoryReader

        │
        ▼
Read Request

        │
        ▼
MemoryStorage

        │
        ▼
Load Memory

        │
        ▼
Verify Version

        │
        ▼
Return Snapshot

        │
        ▼
GoldBot Core
```

---

# Current Market Read Sequence

```text
Read Request

↓

MemoryReader

↓

MemoryStorage

↓

Load Current Snapshot

↓

Return Current Market
```

---

# Candle Read Sequence

```text
Read Candle

↓

MemoryReader

↓

MemoryStorage

↓

Load Candle

↓

Return Candle
```

---

# Current Price Read Sequence

```text
Read Current Price

↓

MemoryReader

↓

MemoryStorage

↓

Load Current Price

↓

Return Price
```

---

# Snapshot Read Sequence

```text
Snapshot Request

↓

MemoryReader

↓

MemoryStorage

↓

Load Snapshot

↓

Verify Snapshot

↓

Return Snapshot
```

---

# Recovery Read Sequence

```text
Recovery Request

↓

MemoryReader

↓

MemoryStorage

↓

Load Recovery Snapshot

↓

Return Snapshot
```

---

# Error Sequence

```text
Read Failed

↓

Create Error Event

↓

Retry Read

↓

Retry Failed

↓

Return Error
```

---

# Runtime Rules

1. MemoryReader faqat MemoryStorage'dan o'qiydi.

2. Har bir Read Request Memory Version bilan tekshiriladi.

3. MemoryReader ma'lumotni o'zgartirmaydi.

4. Snapshot Read faqat Storage'dan olinadi.

5. GoldBot Core MemoryStorage bilan bevosita ishlamaydi.

6. MemoryReader Write Operation bajarmaydi.

7. Runtime Read izchil bo'lishi shart.

8. Circular Runtime Sequence qat'iyan taqiqlanadi.

---

# State Flow

```text
Idle

↓

Waiting Request

↓

Reading

↓

Loading

↓

Returning Data

↓

Ready

or

Failed
```

---

# Golden Rules

• MemoryReader yagona Canonical Read Interface hisoblanadi.

• MemoryStorage yagona Data Source hisoblanadi.

• Read Operation ma'lumotni o'zgartirmaydi.

• Snapshot doimo Storage'dan olinadi.

• Runtime Consistency saqlanishi shart.

• GoldBot Core faqat MemoryReader bilan ishlaydi.

• Circular Sequence taqiqlanadi.

---

# Summary

MemoryReader Sequence Diagram Runtime Memory o'qish ketma-ketligini belgilaydi.

Canonical Runtime Sequence:

GoldBot Core

↓

MemoryReader

↓

MemoryStorage

↓

Load Memory

↓

Verify Version

↓

Return Snapshot

↓

GoldBot Core

Ushbu ketma-ketlik MemoryReader moduli uchun yagona rasmiy Runtime Sequence hisoblanadi.
