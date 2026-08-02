# Providers Layer Sequence Diagram

Status: CANONICAL

---

# Purpose

Ushbu hujjat Providers bo'limi ishga tushganda modullar qanday ketma-ketlikda ishlashini ko'rsatadi.

Bu Runtime Sequence bo'lib, implementatsiya emas.

---

# Startup Sequence

```text
GoldBot Start
      │
      ▼
Configuration Layer
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
ProviderLifecycle (Health Check)
      │
      ▼
ProviderFlow
      │
      ▼
Historical_Data / Live_Data
```

---

# Module Interaction

```text
ProviderFactory
        │
        ▼
ProviderInterface
        │
        ▼
TwelveData / Bitget
        │
        ▼
ProviderLifecycle
        │
        ▼
ProviderFlow
```

---

# Failure Sequence

```text
Provider Error
↓
ProviderLifecycle Aniqlaydi
↓
Reconnect / Retry
↓
Muvaffaqiyatli bo'lsa — Streaming davom etadi
↓
Muvaffaqiyatsiz bo'lsa — Health Report Xato Holatini Qayd Etadi
```

---

# Runtime Rules

1. ProviderFactory har doim jarayonni boshlaydi.
2. Har bir provider ProviderInterface orqali ishlaydi.
3. ProviderLifecycle barcha ulanish holatlarini kuzatadi.
4. ProviderFlow Historical va Live oqimlarni ajratadi.

---

# Summary

ProviderFactory

↓

ProviderInterface

↓

TwelveData / Bitget

↓

ProviderFlow

↓

Historical_Data / Live_Data
