# Provider Interface Contracts

Status: CANONICAL

---

# Purpose

Ushbu hujjat ProviderInterface modulining rasmiy Architecture Contract hujjati hisoblanadi.

---

# Module Responsibility

ProviderInterface quyidagilar uchun javobgar.

✓ Standart Provider Contract'ni belgilash
✓ Har bir provider uchun majburiy metodlarni belgilash

ProviderInterface bajarmaydi.

✗ Ma'lumot yuklash
✗ Ulanishni amalga oshirish
✗ Ma'lumotni saqlash

---

# Module Boundary

```text
ProviderFactory
↓
ProviderInterface
↓
TwelveData / Bitget
```

---

# Input Contract

ProviderInterface o'zi Runtime Input qabul qilmaydi — u Contract ta'riflaydi.

---

# Output Contract

ProviderInterface o'zi Output yaratmaydi — implementatsiya (TwelveData/Bitget) natija qaytaradi.

---

# Allowed Dependencies

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

1. Har bir provider ProviderInterface'ning barcha metodlarini implement qilishi shart.
2. ProviderInterface'siz provider ProviderFactory tomonidan yaratilmaydi.
3. Interface metodlari o'zgarganda barcha provider'lar mos yangilanishi shart.

---

# Acceptance Criteria

✓ Barcha provider'lar Interface'ga mos.
✓ Yangi provider qo'shilganda mavjud Interface o'zgarmaydi.
✓ Architecture Boundary buzilmaydi.

---

# Summary

ProviderInterface Contract Providers bo'limidagi barcha provider'lar uchun yagona, majburiy standart hisoblanadi.
