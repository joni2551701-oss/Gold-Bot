# MemoryStorage Sequence Diagram

Status: CANONICAL

---

# Purpose

Ushbu hujjat MemoryStorage modulining Runtime Sequence (ishlash ketma-ketligi) ni tavsiflaydi.

MemoryStorage Live Data Layer'dan kelayotgan tasdiqlangan (Validated) market ma'lumotlarini qabul qiladi, ularni xavfsiz saqlaydi va MemoryReader orqali GoldBot Core foydalanishi uchun tayyor holatda ushlab turadi.

Bu implementatsiya emas.

Bu MemoryStorage modulining Canonical Runtime Blueprint hisoblanadi.

---

# Complete Runtime Sequence

```text
Live Data Layer

        │
        ▼
MemoryWriter

        │
        ▼
MemoryStorage

        │
        ▼
Integrity Check

        │
        ▼
Persist Memory

        │
        ▼
Update Cache

        │
        ▼
Create Snapshot

        │
        ▼
MemoryReader

        │
        ▼
GoldBot Core
```

---

# Memory Write Sequence

```text
Validated Candle

↓

MemoryWriter

↓

MemoryStorage

↓

Integrity Check

↓

Persist Memory

↓

Update Version

↓

Storage Complete
```

---

# Current Price Update Sequence

```text
Current Price

↓

MemoryWriter

↓

MemoryStorage

↓

Update Runtime State

↓

Update Cache

↓

Ready
```

---

# Memory Read Sequence

```text
GoldBot Core

↓

MemoryReader

↓

MemoryStorage

↓

Load Memory

↓

Return Snapshot

↓

MemoryReader
```

---

# Cache Synchronization Sequence

```text
Memory Updated

↓

MemoryStorage

↓

Update Cache

↓

Verify Cache

↓

Cache Ready
```

---

# Recovery Sequence

```text
Recovery Request

↓

MemoryStorage

↓

Load Snapshot

↓

Restore Runtime State

↓

Verify Integrity

↓

Recovery Complete
```

---

# Restart Sequence

```text
System Restart

↓

Initialize MemoryStorage

↓

Load Latest Snapshot

↓

Restore Memory

↓

Ready
```

---

# Shutdown Sequence

```text
Shutdown Request

↓

Flush Pending Writes

↓

Persist Final State

↓

Close Storage

↓

Shutdown Complete
```

---

# Error Sequence

```text
Storage Error

↓

Create Error Event

↓

Retry Write

↓

Retry Failed

↓

Recovery Mode

or

Storage Failed
```

---

# Runtime Rules

1. MemoryStorage faqat MemoryWriter orqali yozuv qabul qiladi.

2. Har bir yozuv Integrity Check'dan o'tishi shart.

3. Memory faqat muvaffaqiyatli saqlangandan keyin Version yangilanadi.

4. Cache har doim Storage bilan sinxron bo'lishi kerak.

5. Recovery faqat Snapshot asosida amalga oshiriladi.

6. MemoryReader yagona o'qish interfeysi hisoblanadi.

7. GoldBot Core MemoryStorage bilan bevosita ishlamaydi.

8. Circular Runtime Sequence qat'iyan taqiqlanadi.

---

# State Flow

```text
Idle

↓

Initializing

↓

Ready

↓

Writing

↓

Persisting

↓

Updating Cache

↓

Available

↓

Recovering

↓

Stopping

↓

Stopped

or

Failed
```

---

# Golden Rules

• MemoryStorage yagona Canonical Storage komponentidir.

• Har bir yozuv Integrity Check'dan o'tadi.

• Storage va Cache doimo sinxron bo'ladi.

• Snapshot Recovery uchun asosiy manba hisoblanadi.

• MemoryReader yagona o'qish interfeysi hisoblanadi.

• GoldBot Core Storage bilan bevosita ishlamaydi.

• Runtime Sequence qat'iy saqlanadi.

• Circular Sequence taqiqlanadi.

---

# Summary

MemoryStorage Sequence Diagram MemoryStorage modulining Runtime ishlash ketma-ketligini belgilaydi.

Canonical Runtime Sequence:

Live Data Layer

↓

MemoryWriter

↓

MemoryStorage

↓

Integrity Check

↓

Persist Memory

↓

Update Cache

↓

Create Snapshot

↓

MemoryReader

↓

GoldBot Core

Ushbu ketma-ketlik MemoryStorage moduli uchun yagona rasmiy Runtime Sequence hisoblanadi.
