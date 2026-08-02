# Bitget

Status: CANONICAL

---

# Purpose

Bitget — Providers bo'limidagi jonli (Live) market ma'lumotlarini taqdim etuvchi provider hisoblanadi.

Uning asosiy vazifasi WebSocket orqali Tick Stream va Current Price ma'lumotlarini ProviderInterface orqali Live_Data moduliga yetkazishdir.

Bitget marketni tahlil qilmaydi.

---

# Objective

Bitget quyidagi vazifalarni bajaradi:

• Tick Stream yetkazish
• Current Price yetkazish
• Live Candle uchun xom ma'lumot yetkazish
• WebSocket ulanishini boshqarish

---

# Layer Position

```text
ProviderFactory

        │
        ▼
Bitget (ProviderInterface orqali)

        │
        ▼
LiveProviders
```

---

# Responsibilities

Bitget:

✓ Tick Stream'ga ulanadi
✓ Current Price yetkazadi
✓ WebSocket orqali real vaqt ma'lumot beradi

---

# Not Responsible

Bitget:

✗ Historical Data
✗ Candle Building
✗ Ma'lumotni tekshirish
✗ Market Analysis

---

# Input

Bitget qabul qiladi:

• Symbol
• Subscription so'rovi

---

# Output

Bitget yaratadi:

• Live Tick
• Current Price

---

# Golden Rules

1. Bitget faqat ProviderInterface orqali chaqiriladi.
2. Bitget faqat Live ma'lumot beradi.
3. Bitget marketni tahlil qilmaydi.

---

# Related Documents

```text
Bitget/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```

---

# Summary

Bitget Providers bo'limidagi Live Data uchun tashqi ma'lumot manbai bo'lib, real vaqt Tick Stream va Current Price'ni ta'minlaydi.
