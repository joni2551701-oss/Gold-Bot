# Provider Lifecycle Module Map

Status: CANONICAL

---

# Purpose

Ushbu hujjat ProviderLifecycle modulining ichki tuzilishini tavsiflaydi.

---

# Module Position

```text
ProviderFactory
↓
ProviderLifecycle
↓
TwelveData / Bitget
```

---

# Module Architecture

```text
ProviderLifecycle
        │
        ├── Startup Manager
        ├── Reconnect Manager
        ├── Shutdown Manager
        └── Health Monitor
```

---

# Internal Components

## Startup Manager
Provider'ni ishga tushiradi va boshlang'ich ulanishni o'rnatadi.

---

## Reconnect Manager
Ulanish uzilganda qayta ulanishni boshqaradi.

---

## Shutdown Manager
Provider'ni xavfsiz to'xtatadi.

---

## Health Monitor
Provider holatini muntazam tekshiradi.

---

# Allowed Dependencies

✓ TwelveData
✓ Bitget

---

# Forbidden Dependencies

✗ Data_Validation
✗ Market_Memory
✗ Historical_Data
✗ Live_Data (to'g'ridan-to'g'ri)

---

# Summary

ProviderLifecycle Providers bo'limidagi barcha provider'larning ishga tushirish, qayta ulanish va to'xtatish jarayonlarini boshqaruvchi Canonical modul hisoblanadi.
