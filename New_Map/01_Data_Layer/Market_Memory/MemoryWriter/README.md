# Memory Writer

Status: CANONICAL

---

# Purpose

MemoryWriter — Market Memory modulining Market Memory'ga yozish (Write) uchun mo'ljallangan komponentidir.

Uning asosiy vazifasi Live Data Layer'dan kelayotgan tasdiqlangan (Validated) market ma'lumotlarini qabul qilish, ularni tekshirish va MemoryStorage'ga xavfsiz tarzda yozishdir.

MemoryWriter hech qachon Memory'dan o'qimaydi.

U faqat MemoryStorage'ga yozadi.

---

# Objective

MemoryWriter quyidagi vazifalarni bajaradi:

• Memory Write Management

• Runtime Memory Update

• Candle Writing

• Current Price Writing

• Snapshot Writing

• Version Update Request

• Storage Synchronization

• Write Consistency

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

MemoryWriter:

✓ Validated Candle yozish

✓ Current Price yozish

✓ Runtime Memory yangilash

✓ Snapshot yozish

✓ Memory Update Request yaratish

✓ Storage Synchronization boshlash

✓ Write Consistency ta'minlash

---

# Not Responsible

MemoryWriter:

✗ Memory Reading

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

MemoryWriter quyidagilarni qabul qiladi:

• Validated Candle

• Current Price

• Runtime Update

• Snapshot Request

• Memory Update Request

---

# Output

MemoryWriter quyidagilarni yaratadi:

• Storage Write Request

• Runtime Update

• Snapshot Update

• Write Event

• Storage Response

---

# Managed Data

MemoryWriter quyidagi ma'lumotlar bilan ishlaydi:

• Validated Candle

• Current Price

• Runtime Memory

• Snapshot

• Memory Version Request

• Write Metadata

---

# Workflow

```text
Live Data Layer

↓

MemoryWriter

↓

Validate Write Request

↓

MemoryStorage

↓

Persist Memory

↓

Storage Response
```

---

# Golden Rules

1. MemoryWriter MemoryStorage'ga yozuvchi yagona Canonical komponent hisoblanadi.

2. MemoryWriter faqat Validated ma'lumotlarni qabul qiladi.

3. MemoryWriter hech qachon Memory'dan o'qimaydi.

4. MemoryStorage yagona Storage komponenti hisoblanadi.

5. Har bir Write Request izchil bo'lishi shart.

6. GoldBot Core MemoryWriter bilan bevosita ishlamaydi.

7. MemoryWriter Trading Logic bajarmaydi.

8. MemoryWriter ma'lumotni tahlil qilmaydi.

---

# Related Documents

```text
MemoryWriter/

├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```

---

# Summary

MemoryWriter — Market Memory modulining Canonical Write Interface komponentidir.

Uning vazifasi:

• Validated Market Data'ni qabul qilish;

• MemoryStorage'ga xavfsiz yozish;

• Runtime Memory yangilanishini boshqarish;

• Snapshot va Version Update jarayonlarini boshlash.

MemoryWriter Market Memory Layer ichidagi yagona Canonical Write komponenti hisoblanadi.
