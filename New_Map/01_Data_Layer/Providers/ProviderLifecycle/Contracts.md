# Provider Lifecycle Contracts

Status: CANONICAL

---

# Purpose

Ushbu hujjat ProviderLifecycle modulining rasmiy Architecture Contract hujjati hisoblanadi.

---

# Module Responsibility

ProviderLifecycle quyidagilar uchun javobgar.

✓ Provider Startup
✓ Provider Reconnect
✓ Provider Shutdown
✓ Provider Health Check

ProviderLifecycle bajarmaydi.

✗ Ma'lumot yuklash
✗ Ma'lumotni tekshirish
✗ Ma'lumotni saqlash

---

# Module Boundary

```text
ProviderFactory
↓
ProviderLifecycle
↓
TwelveData / Bitget
```

---

# Input Contract

• Provider Instance
• Lifecycle Event (Start, Stop, Reconnect)

---

# Output Contract

• Provider Status
• Health Report

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

1. Har bir Provider Startup Health Check bilan yakunlanishi shart.
2. Ulanish uzilishi avtomatik Reconnect'ni ishga tushirishi shart.
3. Provider nosozligi GoldBot Core ishlashini to'xtatmasligi kerak.
4. Shutdown har doim to'liq Disconnect bilan yakunlanishi shart.

---

# Acceptance Criteria

✓ Provider muvaffaqiyatli ishga tushadi.
✓ Ulanish uzilganda Reconnect ishlaydi.
✓ Health Check muntazam bajariladi.
✓ Architecture Boundary buzilmaydi.

---

# Summary

ProviderLifecycle Contract Providers bo'limidagi barcha provider'larning hayotiy siklini boshqarish bo'yicha rasmiy Canonical Architecture Contract hisoblanadi.
