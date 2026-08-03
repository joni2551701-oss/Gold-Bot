# Memory Cache

Status: CANONICAL

---

# Purpose

MemoryCache — Market Memory modulining yuqori tezlikdagi (High-Speed Runtime Cache) komponentidir.

Uning asosiy vazifasi MemoryStorage'da saqlanayotgan eng so'nggi Runtime Market Data'ni RAM ichida ushlab turish va MemoryReader uchun maksimal tezlikda taqdim etishdir.

MemoryCache doimiy saqlash (Persistent Storage) emas.

U faqat Runtime Cache hisoblanadi.

---

# Objective

MemoryCache quyidagi vazifalarni bajaradi:

• Runtime Cache

• Current Market Cache

• Current Price Cache

• Latest Candle Cache

• Snapshot Cache

• Read Optimization

• Cache Synchronization

• Cache Recovery

---

# Layer Position

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

# Responsibilities

MemoryCache:

✓ Latest Candle Cache

✓ Current Price Cache

✓ Runtime Snapshot Cache

✓ Fast Read Access

✓ Cache Synchronization

✓ Cache Refresh

✓ Cache Consistency

---

# Not Responsible

MemoryCache:

✗ Persistent Storage

✗ Memory Writing

✗ Tick Validation

✗ Candle Generation

✗ Market Analysis

✗ Strategy

✗ Decision

✗ AI Analysis

---

# Input

MemoryCache qabul qiladi:

• Storage Update

• Runtime Snapshot

• Cache Refresh Request

• Recovery Request

---

# Output

MemoryCache yaratadi:

• Cached Snapshot

• Cached Current Price

• Cached Candle

• Cache Status

• Cache Events

---

# Managed Data

MemoryCache quyidagilar bilan ishlaydi:

• Runtime Snapshot

• Latest Candle

• Current Price

• Cache Metadata

• Cache Version

---

# Workflow

```text
MemoryStorage

↓

MemoryCache

↓

Update Cache

↓

MemoryReader

↓

GoldBot Core
```

---

# Golden Rules

1. MemoryCache Persistent Storage emas.

2. MemoryCache faqat Runtime ma'lumotlarni ushlab turadi.

3. MemoryStorage yagona Data Source hisoblanadi.

4. MemoryReader avval Cache'dan o'qishga harakat qiladi.

5. Cache mavjud bo'lmasa Storage ishlatiladi.

6. Cache avtomatik yangilanadi.

7. Cache Trading Logic bajarmaydi.

8. Cache ma'lumotni o'zgartirmaydi.

---

# Related Documents

```text
MemoryCache/

├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```

---

# Summary

MemoryCache — Market Memory modulining Canonical Runtime Cache komponentidir.

Uning vazifasi:

• Runtime Market Data'ni RAM'da saqlash;

• Read Performance'ni oshirish;

• MemoryReader uchun tezkor ma'lumot taqdim etish;

• MemoryStorage bilan sinxron ishlash.

MemoryCache Market Memory Layer ichidagi yagona Canonical Runtime Cache moduli hisoblanadi.
