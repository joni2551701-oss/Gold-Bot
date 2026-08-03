# Historical Data Layer Contracts

Status: CANONICAL

---

# Purpose

Ushbu hujjat Historical Data bo'limi uchun rasmiy Architecture Contract hisoblanadi.

---

# Layer Responsibility

Historical Data quyidagilar uchun javobgar.

✓ Historical Data Orchestration (HistoricalDataService)
✓ Initial Historical Loading (Bootstrap)
✓ Historical Gap Recovery (Recovery)
✓ Historical Provider Coordination (HistoricalProviders)
✓ Historical Data Storage (HistoricalDatabase)

---

# Layer Does NOT

✗ Live Data Streaming
✗ Current Price
✗ Candle Building (Real-Time)
✗ Market Analysis
✗ Strategy
✗ Decision
✗ Risk
✗ AI

---

# Input Contract

Historical Data qabul qiladi.

• Configuration
• Symbols
• Timeframes
• External Historical Provider ma'lumotlari

---

# Output Contract

Historical Data yaratadi.

• Historical Candle
• Historical OHLC
• Bootstrap Status
• Recovery Status

---

# Allowed Dependencies

✓ Configuration
✓ HistoricalProviders
✓ HistoricalDatabase
✓ Data Validation

---

# Forbidden Dependencies

✗ Live Data
✗ Context
✗ Strategy
✗ Decision
✗ Risk
✗ AI
✗ Platform Layer

---

# Runtime Contract

1. Bootstrap faqat tizim birinchi marta ishga tushganda ishlaydi.
2. Recovery faqat Data Gap aniqlanganda ishga tushadi.
3. Bootstrap va Recovery bir-birini o'rnini bosmaydi.
4. Har bir ma'lumot HistoricalDatabase'ga yozilishidan oldin va keyin Data Validation'dan o'tadi.
5. Market Memory faqat tekshirilgan ma'lumot bilan yangilanadi.
6. Historical Data Live Data bilan to'g'ridan-to'g'ri bog'lanmaydi.
7. Circular Dependency qat'iyan taqiqlanadi.

---

# Acceptance Criteria

✓ Bootstrap ishlaydi.
✓ Recovery ishlaydi.
✓ HistoricalProviders orqali ma'lumot olinadi.
✓ HistoricalDatabase'da saqlanadi.
✓ Data Validation'dan o'tadi.
✓ Market Memory yangilanadi.
✓ Architecture Boundary buzilmaydi.

---

# Summary

Historical Data Layer Contract GoldBot'ning tarixiy market ma'lumotlarini yuklash, saqlash va tiklash jarayonlarini, shuningdek ushbu bo'limning boshqa Layer'lardan mustaqilligini belgilovchi rasmiy Architecture Contract hisoblanadi.
