# Market Memory Layer Data Flow

Status: CANONICAL

---

# Purpose

Ushbu hujjat Market Memory Layer ichidagi barcha Runtime Data Flow'ni tavsiflaydi.

Market Memory Layer Live Data Layer'dan kelgan tayyor market ma'lumotlarini qabul qiladi, ularni Runtime Memory'da boshqaradi va GoldBot Core uchun taqdim etadi.

Bu implementatsiya emas.

Bu Market Memory Layer'ning Canonical Runtime Data Flow hujjati hisoblanadi.

---

# Layer Position

```text
Live Data Layer

↓

Market Memory Layer

↓

GoldBot Core
```

---

# Complete Data Flow

```text
Live Data Layer

↓

MemoryWriter

↓

MemoryStorage

↓

MemoryCache

↓

MemoryReader

↓

GoldBot Core
```

---

# Runtime Flow

```text
Validated Candle

↓

MemoryWriter

↓

MemoryStorage

↓

Update Cache

↓

MemoryCache

↓

MemoryReader

↓

GoldBot Core
```

---

# Recovery Flow

```text
Recovery Request

↓

MemoryLifecycle

↓

Restore Storage

↓

Restore Cache

↓

Ready
```

---

# Data Objects Flow

```text
Validated Candle

↓

Current Price

↓

Runtime Snapshot

↓

Memory Storage

↓

Memory Cache

↓

Market Snapshot

↓

GoldBot Core
```

---

# Layer Rules

1. MemoryWriter yagona Write Interface hisoblanadi.

2. MemoryStorage yagona Persistent Storage hisoblanadi.

3. MemoryCache faqat Runtime Cache hisoblanadi.

4. MemoryReader yagona Read Interface hisoblanadi.

5. GoldBot Core faqat MemoryReader orqali ma'lumot oladi.

6. Circular Data Flow taqiqlanadi.

---

# Summary

Canonical Layer Flow:

Live Data Layer

↓

MemoryWriter

↓

MemoryStorage

↓

MemoryCache

↓

MemoryReader

↓

GoldBot Core
