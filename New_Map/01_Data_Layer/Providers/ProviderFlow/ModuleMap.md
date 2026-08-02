# Provider Flow Module Map

Status: CANONICAL

---

# Purpose

Ushbu hujjat ProviderFlow modulining ichki tuzilishini tavsiflaydi.

---

# Module Position

```text
ProviderInterface
↓
ProviderFlow
↓
Historical_Data / Live_Data
```

---

# Module Architecture

```text
ProviderFlow
        │
        ├── Historical Route
        └── Live Route
```

---

# Internal Components

## Historical Route
TwelveData'dan kelgan ma'lumotni Historical_Data'ga yo'naltiradi.

---

## Live Route
Bitget'dan kelgan ma'lumotni Live_Data'ga yo'naltiradi.

---

# Allowed Dependencies

✓ ProviderInterface
✓ TwelveData
✓ Bitget

---

# Forbidden Dependencies

✗ Data_Validation
✗ Market_Memory
✗ Context
✗ Strategy

---

# Summary

ProviderFlow Providers bo'limi ichidagi Historical va Live ma'lumot yo'nalishlarini ajratuvchi Canonical modul hisoblanadi.
