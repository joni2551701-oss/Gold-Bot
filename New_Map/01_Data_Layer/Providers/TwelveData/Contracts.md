# TwelveData Contracts

Status: CANONICAL

---

# Purpose

Ushbu hujjat TwelveData modulining rasmiy Architecture Contract hujjati hisoblanadi.

---

# Module Responsibility

TwelveData quyidagilar uchun javobgar.

✓ Historical Candle yetkazish
✓ Historical OHLC yetkazish
✓ Bootstrap va Recovery so'rovlariga javob berish

TwelveData bajarmaydi.

✗ Live Data
✗ Ma'lumotni tekshirish
✗ Ma'lumotni saqlash
✗ Market Analysis

---

# Module Boundary

```text
HistoricalProviders
↓
ProviderInterface
↓
TwelveData
```

---

# Input Contract

• Symbol
• Timeframe
• Sana Oralig'i

---

# Output Contract

• Historical Candle
• Historical OHLC

---

# Allowed Dependencies

✓ ProviderInterface

---

# Forbidden Dependencies

✗ Data_Validation
✗ Market_Memory
✗ Live_Data
✗ Context
✗ Strategy
✗ Decision
✗ AI

---

# Runtime Contract

1. TwelveData faqat ProviderInterface orqali chaqiriladi.
2. Har bir so'rov Symbol va Timeframe bilan birga bo'lishi shart.
3. Xato holatida ProviderLifecycle Retry siyosatini qo'llaydi.
4. TwelveData Data Validation bosqichini o'tkazib yubormaydi.

---

# Acceptance Criteria

✓ Historical Candle qaytariladi.
✓ Historical OHLC qaytariladi.
✓ ProviderInterface Contract'iga mos javob beriladi.
✓ Architecture Boundary buzilmaydi.

---

# Summary

TwelveData Contract Providers bo'limidagi Historical Data uchun tashqi integratsiyaning rasmiy shartnomasi hisoblanadi.
