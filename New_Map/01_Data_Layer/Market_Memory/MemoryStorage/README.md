# Memory Storage

Status: CANONICAL

---

# Purpose

MemoryStorage — Market Memory modulining doimiy (Persistent) va vaqtinchalik (Runtime) market ma'lumotlarini saqlovchi komponentidir.

Uning asosiy vazifasi Live Data Layer'dan kelgan tayyor va tasdiqlangan (Validated) market ma'lumotlarini xavfsiz saqlash hamda MemoryReader orqali GoldBot Core foydalanishi uchun tayyor holatda ushlab turishdir.

MemoryStorage hech qanday Market Analysis, Strategy yoki Decision Logic bajarmaydi.

U faqat Market Memory ma'lumotlarini boshqaradi.

---

# Objective

MemoryStorage quyidagi vazifalarni bajaradi:

• Candle Storage

• Tick Storage

• Current Price Storage

• Runtime Memory Storage

• Cache Synchronization

• Memory Persistence

• Memory Recovery Support

• Data Integrity

---

# Layer Position

```text
Live Data Layer

↓

MemoryWriter

↓

MemoryStorage

↓

MemoryReader

↓

GoldBot Core
```

---

# Responsibilities

MemoryStorage:

✓ Validated Candle saqlash

✓ Current Price saqlash

✓ Runtime Memory saqlash

✓ Memory Version boshqarish

✓ Memory Consistency saqlash

✓ Recovery uchun Memory tayyorlash

✓ Cache bilan sinxronlash

---

# Not Responsible

MemoryStorage:

✗ Live Tick qabul qilish

✗ Tick Validation

✗ Candle Generation

✗ Market Analysis

✗ Context Analysis

✗ Strategy

✗ Decision

✗ Risk

✗ Signal Generation

✗ AI Analysis

---

# Input

MemoryStorage quyidagilarni qabul qiladi:

• Validated Candle

• Current Price

• Runtime Snapshot

• Memory Update Request

• Recovery Request

---

# Output

MemoryStorage quyidagilarni yaratadi:

• Stored Memory

• Runtime Snapshot

• Memory State

• Recovery Snapshot

• Storage Events

---

# Managed Data

MemoryStorage quyidagi ma'lumotlarni boshqaradi:

• OHLC Candles

• Current Price

• Runtime State

• Market Snapshot

• Memory Version

• Storage Metadata

---

# Workflow

```text
Live Data Layer

↓

MemoryWriter

↓

MemoryStorage

↓

Persist Memory

↓

Update Cache

↓

MemoryReader

↓

GoldBot Core
```

---

# Golden Rules

1. MemoryStorage faqat tasdiqlangan (Validated) ma'lumotlarni saqlaydi.

2. MemoryStorage hech qachon Candle yaratmaydi.

3. MemoryStorage hech qachon Tick Validation bajarmaydi.

4. MemoryStorage faqat MemoryWriter orqali yozuv qabul qiladi.

5. GoldBot Core MemoryStorage bilan bevosita ishlamaydi.

6. MemoryReader yagona o'qish interfeysi hisoblanadi.

7. Har bir yozuv Data Integrity tekshiruvidan o'tishi kerak.

8. MemoryStorage Trading Logic bajarmaydi.

---

# Related Documents

```text
MemoryStorage/

├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```

---

# Summary

MemoryStorage — Market Memory modulining markaziy saqlash komponentidir.

Uning vazifasi:

• Validated Market Data saqlash;

• Runtime Memory boshqarish;

• Recovery uchun Snapshot yaratish;

• MemoryReader orqali GoldBot Core'ga ma'lumot yetkazish.

MemoryStorage Market Memory Layer ichidagi yagona Canonical Storage komponenti hisoblanadi.
