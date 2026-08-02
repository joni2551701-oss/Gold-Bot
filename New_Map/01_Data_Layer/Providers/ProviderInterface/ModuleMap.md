# Provider Interface Module Map

Status: CANONICAL

---

# Purpose

Ushbu hujjat ProviderInterface modulining ichki tuzilishini tavsiflaydi.

---

# Module Position

```text
ProviderFactory
↓
ProviderInterface
↓
TwelveData / Bitget
```

---

# Module Architecture

```text
ProviderInterface
        │
        ├── connect()
        ├── disconnect()
        ├── fetchHistorical()
        ├── subscribeLive()
        └── healthCheck()
```

---

# Internal Components

## connect()
Providerga ulanishni belgilaydi.

---

## disconnect()
Providerdan uzilishni belgilaydi.

---

## fetchHistorical()
Tarixiy ma'lumot so'rovini belgilaydi (Historical provider'lar uchun).

---

## subscribeLive()
Live oqimga obuna bo'lishni belgilaydi (Live provider'lar uchun).

---

## healthCheck()
Provider holatini tekshirishni belgilaydi.

---

# Allowed Dependencies

✓ TwelveData (implement qiladi)
✓ Bitget (implement qiladi)

---

# Forbidden Dependencies

✗ Data_Validation
✗ Market_Memory
✗ Historical_Data
✗ Live_Data

---

# Summary

ProviderInterface Providers bo'limidagi barcha provider'lar uchun majburiy standart Contract'ni belgilovchi Canonical modul hisoblanadi.
