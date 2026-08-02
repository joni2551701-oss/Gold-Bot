# Providers Layer Data Flow

Status: CANONICAL

---

# Purpose

Ushbu hujjat Providers bo'limi ichidagi barcha Runtime Data Flow'ni tavsiflaydi.

Providers bo'limi tashqi market ma'lumotlari manbalarini (TwelveData, Bitget) boshqaradi va standart interfeys orqali Historical_Data hamda Live_Data modullariga ma'lumot yetkazadi.

Bu implementatsiya emas.

Bu Providers bo'limining Canonical Runtime Data Flow hujjati hisoblanadi.

---

# Layer Position

```text
Configuration Layer

        │
        ▼
Providers

        │
        ▼
Historical_Data / Live_Data
```

---

# Complete Data Flow

```text
Configuration

        │
        ▼
ProviderFactory

        │
        ▼
ProviderInterface

        │
        ▼
TwelveData / Bitget

        │
        ▼
ProviderFlow

        │
        ▼
Historical_Data / Live_Data
```

---

# Pipeline Flow

```text
Configuration

↓

ProviderFactory Provider Turini Aniqlaydi

↓

ProviderInterface Orqali Provider Yaratiladi

↓

ProviderLifecycle Ulanishni Boshqaradi

↓

TwelveData / Bitget Ma'lumot Beradi

↓

ProviderFlow Yo'naltiradi

↓

Historical_Data / Live_Data
```

---

# Runtime Rules

1. Pipeline har doim ProviderFactory bilan boshlanadi.
2. Har bir provider ProviderInterface'ga mos bo'lishi shart.
3. ProviderLifecycle barcha provider ulanishlarini boshqaradi.
4. ProviderFlow Historical va Live oqimlarni aralashtirmaydi.
5. Circular Data Flow qat'iyan taqiqlanadi.

---

# Layer Boundaries

Providers qabul qiladi:

• Configuration
• External Provider ma'lumotlari

Providers uzatadi:

• Historical Candle / OHLC (TwelveData orqali)
• Live Tick / Current Price (Bitget orqali)

---

# Summary

Providers Layer Data Flow hujjati Providers bo'limi ichidagi barcha Runtime ma'lumot oqimini belgilaydi.

Canonical Layer Flow:

ProviderFactory

↓

ProviderInterface

↓

TwelveData / Bitget

↓

ProviderFlow

↓

Historical_Data / Live_Data

Ushbu Data Flow GoldBot Providers bo'limi uchun yagona Canonical Runtime Pipeline hisoblanadi.
