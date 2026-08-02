# Provider Flow

Status: CANONICAL

---

# Purpose

ProviderFlow — Providers bo'limi ichidagi ma'lumot oqimini (Data Flow) tavsiflovchi hujjat-modul hisoblanadi.

Uning asosiy vazifasi tashqi provider'lardan (TwelveData, Bitget) kelgan ma'lumot Historical_Data va Live_Data modullariga qanday yetib borishini standartlashtirishdir.

Bu implementatsiya emas — bu Providers bo'limining Canonical Data Flow Blueprint komponenti.

---

# Objective

ProviderFlow quyidagi jarayonlarni tavsiflaydi:

• External Provider'dan ma'lumot olish
• ProviderInterface orqali standartlashtirish
• Historical_Data / Live_Data'ga uzatish

---

# Layer Position

```text
External Provider

        │
        ▼
ProviderFactory

        │
        ▼
ProviderInterface

        │
        ▼
ProviderFlow

        │
        ▼
Historical_Data / Live_Data
```

---

# Responsibilities

ProviderFlow:

✓ Provider'dan kelgan ma'lumotning yo'nalishini belgilaydi
✓ Historical va Live oqimlarni ajratadi

---

# Not Responsible

ProviderFlow:

✗ Ma'lumot yuklash
✗ Ma'lumotni tekshirish
✗ Ma'lumotni saqlash

---

# Input

ProviderFlow qabul qiladi (hujjat darajasida tavsiflaydi):

• TwelveData chiqishi
• Bitget chiqishi

---

# Output

ProviderFlow yo'naltiradi:

• Historical_Data'ga (TwelveData orqali)
• Live_Data'ga (Bitget orqali)

---

# Golden Rules

1. Historical va Live oqimlar bir-birini kesib o'tmaydi.
2. Har bir oqim ProviderInterface orqali standartlashtiriladi.
3. ProviderFlow marketni tahlil qilmaydi.

---

# Related Documents

```text
ProviderFlow/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```

---

# Summary

ProviderFlow Providers bo'limi ichidagi ma'lumot oqimini — tashqi provider'lardan Historical_Data va Live_Data'gacha — belgilovchi Canonical modul hisoblanadi.
