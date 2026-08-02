# Bitget Contracts

Status: CANONICAL

---

# Purpose

Ushbu hujjat Bitget modulining rasmiy Architecture Contract hujjati hisoblanadi.

---

# Module Responsibility

Bitget quyidagilar uchun javobgar.

✓ Tick Stream yetkazish
✓ Current Price yetkazish
✓ WebSocket ulanishini boshqarish

Bitget bajarmaydi.

✗ Historical Data
✗ Candle Building
✗ Ma'lumotni tekshirish
✗ Market Analysis

---

# Module Boundary

```text
LiveProviders
↓
ProviderInterface
↓
Bitget
```

---

# Input Contract

• Symbol
• Subscription so'rovi

---

# Output Contract

• Live Tick
• Current Price

---

# Allowed Dependencies

✓ ProviderInterface

---

# Forbidden Dependencies

✗ Data_Validation
✗ Market_Memory
✗ Historical_Data
✗ Context
✗ Strategy
✗ Decision
✗ AI

---

# Runtime Contract

1. Bitget faqat ProviderInterface orqali chaqiriladi.
2. Har bir Subscription Symbol bilan birga bo'lishi shart.
3. Ulanish uzilganda ProviderLifecycle Reconnect siyosatini qo'llaydi.
4. Bitget Data Validation bosqichini o'tkazib yubormaydi.

---

# Acceptance Criteria

✓ Live Tick qaytariladi.
✓ Current Price qaytariladi.
✓ ProviderInterface Contract'iga mos javob beriladi.
✓ Architecture Boundary buzilmaydi.

---

# Summary

Bitget Contract Providers bo'limidagi Live Data uchun tashqi integratsiyaning rasmiy shartnomasi hisoblanadi.
