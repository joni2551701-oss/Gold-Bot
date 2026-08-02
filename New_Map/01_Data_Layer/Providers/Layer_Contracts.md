# Providers Layer Contracts

Status: CANONICAL

---

# Purpose

Ushbu hujjat Providers bo'limi uchun rasmiy Architecture Contract hisoblanadi.

---

# Layer Responsibility

Providers quyidagilar uchun javobgar.

✓ Provider Instantiation (ProviderFactory)
✓ Standard Provider Interface (ProviderInterface)
✓ Historical Provider Integration (TwelveData)
✓ Live Provider Integration (Bitget)
✓ Provider Lifecycle Management (ProviderLifecycle)
✓ Provider Data Routing (ProviderFlow)

---

# Layer Does NOT

✗ Market Analysis
✗ Data Validation
✗ Data Storage
✗ Strategy
✗ Decision
✗ Risk
✗ AI

---

# Input Contract

Providers qabul qiladi.

• Configuration
• External Provider ma'lumotlari (TwelveData API, Bitget WebSocket)

---

# Output Contract

Providers yaratadi.

• Historical Candle / OHLC
• Live Tick / Current Price
• Provider Health Report

---

# Allowed Dependencies

✓ Configuration
✓ Historical_Data (Output sifatida)
✓ Live_Data (Output sifatida)

---

# Forbidden Dependencies

✗ Core
✗ Application Services
✗ Business Layer
✗ Data_Validation (to'g'ridan-to'g'ri)
✗ Market_Memory (to'g'ridan-to'g'ri)
✗ Context
✗ Strategy
✗ Decision
✗ AI

---

# Runtime Contract

1. Barcha provider'lar ProviderInterface orqali ishlaydi.
2. Providerlar bir-biridan mustaqil bo'lishi kerak.
3. Provider almashtirish GoldBot Core'ga ta'sir qilmasligi kerak.
4. Historical va Live providerlar alohida boshqariladi.
5. Provider Factory yagona provider yaratish nuqtasi hisoblanadi.
6. Providerlar faqat Data Layer bilan ishlaydi.
7. Providerlar marketni tahlil qilmaydi.
8. Providerlardan kelgan barcha ma'lumot Validation'dan o'tadi.
9. Provider nosozligi GoldBot Core ishlashini to'xtatmasligi kerak.
10. Yangi provider qo'shish mavjud arxitekturani buzmasligi kerak.

---

# Acceptance Criteria

✓ ProviderFactory provider'ni to'g'ri yaratadi.
✓ Barcha provider'lar ProviderInterface'ga mos.
✓ ProviderLifecycle ulanishni boshqaradi.
✓ ProviderFlow Historical va Live oqimlarni to'g'ri yo'naltiradi.
✓ Architecture Boundary buzilmaydi.

---

# Summary

Providers Layer Contract Data Layer ichidagi tashqi market ma'lumotlari bilan integratsiyani, Provider Instantiation, Lifecycle va Data Routing jarayonlarini belgilovchi rasmiy Canonical Architecture Contract hisoblanadi.
