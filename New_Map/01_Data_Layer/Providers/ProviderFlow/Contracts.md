# Provider Flow Contracts

Status: CANONICAL

---

# Purpose

Ushbu hujjat ProviderFlow modulining rasmiy Architecture Contract hujjati hisoblanadi.

---

# Module Responsibility

ProviderFlow quyidagilar uchun javobgar.

✓ Historical va Live ma'lumot oqimlarini ajratish
✓ Har bir oqimni to'g'ri manzilga yo'naltirish

ProviderFlow bajarmaydi.

✗ Ma'lumot yuklash
✗ Ma'lumotni tekshirish
✗ Ma'lumotni saqlash

---

# Module Boundary

```text
ProviderInterface
↓
ProviderFlow
↓
Historical_Data / Live_Data
```

---

# Input Contract

• TwelveData chiqishi
• Bitget chiqishi

---

# Output Contract

• Historical_Data'ga yo'naltirilgan oqim
• Live_Data'ga yo'naltirilgan oqim

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
✗ Decision
✗ AI

---

# Runtime Contract

1. Historical va Live oqim hech qachon aralashtirilmaydi.
2. Har bir oqim ProviderInterface Contract'iga mos bo'lishi shart.
3. ProviderFlow marketni tahlil qilmaydi.

---

# Acceptance Criteria

✓ Historical oqim to'g'ri yo'naltiriladi.
✓ Live oqim to'g'ri yo'naltiriladi.
✓ Architecture Boundary buzilmaydi.

---

# Summary

ProviderFlow Contract Providers bo'limi ichidagi Historical va Live ma'lumot oqimlarini to'g'ri yo'naltirish bo'yicha rasmiy Canonical Architecture Contract hisoblanadi.
