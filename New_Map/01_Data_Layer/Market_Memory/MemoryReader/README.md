# Memory Reader

Status: CANONICAL

---

# Purpose

MemoryReader — Market Memory modulining Market Memory ma'lumotlarini o'qish uchun mo'ljallangan komponentidir.

Uning asosiy vazifasi MemoryStorage ichida saqlanayotgan Runtime Market Data'ni xavfsiz va izchil tarzda GoldBot Core hamda ruxsat etilgan modullarga taqdim etishdir.

MemoryReader hech qachon Memory'ga yozmaydi.

U faqat Memory'dan o'qiydi.

---

# Objective

MemoryReader quyidagi vazifalarni bajaradi:

• Runtime Memory Reading

• Current Market Snapshot Reading

• Current Price Reading

• Candle Reading

• Memory Version Reading

• Snapshot Reading

• Read Consistency

• Read Optimization

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

MemoryReader:

✓ Runtime Memory o'qish

✓ Current Candle o'qish

✓ Current Price o'qish

✓ Market Snapshot o'qish

✓ Memory Version o'qish

✓ Snapshot o'qish

✓ Read Consistency ta'minlash

---

# Not Responsible

MemoryReader:

✗ Memory Writing

✗ Memory Update

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

MemoryReader quyidagilarni qabul qiladi:

• Read Request

• Snapshot Request

• Current Market Request

• Runtime Request

• Version Request

---

# Output

MemoryReader quyidagilarni yaratadi:

• Current Market Snapshot

• Current Candle

• Current Price

• Runtime Memory

• Memory Version

• Read Response

---

# Managed Data

MemoryReader quyidagi ma'lumotlar bilan ishlaydi:

• Runtime Memory

• Current Candle

• Current Price

• Market Snapshot

• Memory Version

• Storage Metadata

---

# Workflow

```text
GoldBot Core

↓

MemoryReader

↓

MemoryStorage

↓

Load Runtime Memory

↓

Return Snapshot

↓

GoldBot Core
```

---

# Golden Rules

1. MemoryReader faqat MemoryStorage'dan o'qiydi.

2. MemoryReader hech qachon Memory'ga yozmaydi.

3. Har bir Read Request izchil (Consistent) ma'lumot qaytarishi kerak.

4. MemoryStorage yagona Data Source hisoblanadi.

5. GoldBot Core MemoryStorage bilan bevosita ishlamaydi.

6. MemoryReader Trading Logic bajarmaydi.

7. MemoryReader ma'lumotni o'zgartirmaydi.

8. MemoryReader faqat o'qish interfeysi hisoblanadi.

---

# Related Documents

```text
MemoryReader/

├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```

---

# Summary

MemoryReader — Market Memory modulining Canonical Read Interface komponentidir.

Uning vazifasi:

• Runtime Market Memory'ni o'qish;

• Current Candle va Current Price'ni taqdim etish;

• Snapshot va Memory Version'ni qaytarish;

• GoldBot Core uchun xavfsiz Read Interface ta'minlash.

MemoryReader Market Memory Layer ichidagi yagona Canonical Read komponenti hisoblanadi.
