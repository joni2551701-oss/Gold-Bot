# TwelveData

Status: CANONICAL

---

# Purpose

TwelveData — Providers bo'limidagi tarixiy (Historical) market ma'lumotlarini taqdim etuvchi provider hisoblanadi.

Uning asosiy vazifasi Bootstrap va Recovery uchun tarixiy Candle va OHLC ma'lumotlarini ProviderInterface orqali yetkazishdir.

TwelveData marketni tahlil qilmaydi.

---

# Objective

TwelveData quyidagi vazifalarni bajaradi:

• Bootstrap uchun tarixiy ma'lumot yetkazish
• Recovery uchun yetishmayotgan ma'lumotni yetkazish
• Historical Candle taqdim etish
• Historical OHLC taqdim etish

---

# Layer Position

```text
ProviderFactory

        │
        ▼
TwelveData (ProviderInterface orqali)

        │
        ▼
HistoricalProviders
```

---

# Responsibilities

TwelveData:

✓ Tarixiy Candle yetkazadi
✓ Tarixiy OHLC yetkazadi
✓ Bootstrap so'rovlariga javob beradi
✓ Recovery so'rovlariga javob beradi

---

# Not Responsible

TwelveData:

✗ Live Data
✗ Ma'lumotni tekshirish
✗ Ma'lumotni saqlash
✗ Market Analysis

---

# Input

TwelveData qabul qiladi:

• Symbol
• Timeframe
• Sana Oralig'i

---

# Output

TwelveData yaratadi:

• Historical Candle
• Historical OHLC

---

# Golden Rules

1. TwelveData faqat ProviderInterface orqali chaqiriladi.
2. TwelveData faqat Historical ma'lumot beradi.
3. TwelveData marketni tahlil qilmaydi.

---

# Related Documents

```text
TwelveData/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```

---

# Summary

TwelveData Providers bo'limidagi Historical Data uchun tashqi ma'lumot manbai bo'lib, Bootstrap va Recovery jarayonlarini ta'minlaydi.
