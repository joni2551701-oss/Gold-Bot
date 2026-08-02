# Provider Factory Contracts

Status: CANONICAL

---

# Purpose

Ushbu hujjat ProviderFactory modulining rasmiy Architecture Contract hujjati hisoblanadi.

---

# Module Responsibility

ProviderFactory quyidagilar uchun javobgar.

✓ Provider Instantiation
✓ Provider Configuration
✓ Provider Registry Boshqaruvi

ProviderFactory bajarmaydi.

✗ Ma'lumot yuklash
✗ Ma'lumotni tekshirish
✗ Ma'lumotni saqlash
✗ Market Analysis

---

# Module Boundary

```text
Configuration
↓
ProviderFactory
↓
ProviderInterface
```

---

# Input Contract

• Configuration
• Provider turi (Historical / Live)

---

# Output Contract

• Provider Instance

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

1. Har bir provider ProviderInterface'ga mos yaratilishi shart.
2. Bitta provider turi uchun bitta Instance Registry'da bo'lishi shart.
3. ProviderFactory Historical va Live provider'larni aralashtirmaydi.
4. Circular Dependency qat'iyan taqiqlanadi.

---

# Acceptance Criteria

✓ Configuration to'g'ri o'qiladi.
✓ To'g'ri provider turi tanlanadi.
✓ Provider Instance yaratiladi.
✓ Registry yangilanadi.
✓ Architecture Boundary buzilmaydi.

---

# Summary

ProviderFactory Contract Providers bo'limining yagona provider yaratish nuqtasi sifatida ishlashini belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
