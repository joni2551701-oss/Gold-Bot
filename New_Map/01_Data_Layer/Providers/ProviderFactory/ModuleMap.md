# Provider Factory Module Map

Status: CANONICAL

---

# Purpose

Ushbu hujjat ProviderFactory modulining ichki arxitekturasini tavsiflaydi.

---

# Module Position

```text
Configuration
↓
ProviderFactory
↓
ProviderInterface
```

---

# Module Architecture

```text
ProviderFactory
        │
        ├── Configuration Reader
        ├── Provider Selector
        ├── Provider Registry
        └── Instance Builder
```

---

# Internal Components

## Configuration Reader
Configuration'dan kerakli provider sozlamalarini o'qiydi.

---

## Provider Selector
Historical yoki Live provider turini aniqlaydi.

---

## Provider Registry
Yaratilgan provider'larni ro'yxatga oladi.

---

## Instance Builder
ProviderInterface'ga mos provider Instance yaratadi.

---

# Allowed Dependencies

✓ ProviderInterface
✓ TwelveData
✓ Bitget

---

# Forbidden Dependencies

✗ Data_Validation
✗ Market_Memory
✗ Historical_Data (to'g'ridan-to'g'ri)
✗ Live_Data (to'g'ridan-to'g'ri)

---

# Summary

ProviderFactory Providers bo'limi ichidagi provider yaratish va ro'yxatga olish jarayonlarini boshqaruvchi Canonical modul hisoblanadi.
