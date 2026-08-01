# CandleBuilder Contracts

Status: CANONICAL

---

# Purpose

Ushbu hujjat CandleBuilder modulining rasmiy Architecture Contract hujjati hisoblanadi.

CandleBuilder Live Data modulining yagona Canonical OHLC Candle Generation komponenti hisoblanadi.

Validation'dan o'tgan Tick ma'lumotlarini Timeframe bo'yicha OHLC Candle'ga aylantirish faqat ushbu modul orqali amalga oshiriladi.

Har qanday implementatsiya ushbu Contract talablariga to'liq mos bo'lishi shart.

---

# Module Responsibility

CandleBuilder quyidagi vazifalar uchun javobgar.

✓ OHLC Candle Generation

✓ Active Candle Management

✓ Candle Update

✓ Candle Close

✓ New Candle Creation

✓ Multi-Timeframe Candle Building

✓ Candle Lifecycle Management

✓ Candle Publishing

CandleBuilder quyidagi vazifalarni bajarmaydi.

✗ Live Stream Management

✗ Provider Connection

✗ Current Price Management

✗ Tick Validation

✗ Historical Data

✗ Market Calendar

✗ Context Analysis

✗ Strategy

✗ Decision

✗ Risk

✗ Signal Generation

✗ AI Analysis

---

# Module Boundary

PriceStreamService

↓

CurrentPriceProvider

↓

Stream Validator

↓

CandleBuilder

↓

Market Memory

↓

Boundary End

---

# Input Contract

CandleBuilder quyidagilarni qabul qiladi.

• Validated Tick

• Current Price

• Timestamp

• Symbol

• Timeframe

• Volume (agar mavjud bo'lsa)

---

# Output Contract

CandleBuilder quyidagilarni yaratadi.

• Active Candle

• Closed Candle

• New Candle

• OHLC Data

• Candle Event

• Candle Status

---

# Read Contract

CandleBuilder quyidagilarni o'qishi mumkin.

✓ Current Price

✓ Validated Tick

✓ Timeframe Configuration

✓ Active Candle

✓ Candle State

---

# Write Contract

CandleBuilder quyidagilarga yozishi mumkin.

✓ Market Memory

✓ Event Bus

Boshqa modullarga yozish taqiqlanadi.

---

# Allowed Dependencies

CandleBuilder quyidagilar bilan ishlashi mumkin.

✓ PriceStreamService

✓ CurrentPriceProvider

✓ StreamValidator

✓ MarketMemory

✓ Event Bus

✓ Configuration Layer

---

# Forbidden Dependencies

CandleBuilder quyidagilar bilan ishlashi mumkin emas.

✗ Historical Data

✗ HistoricalDatabase

✗ HistoricalDataService

✗ Live Providers

✗ Market Calendar

✗ Context Engine

✗ Analysis Engine

✗ Strategy Engine

✗ Confluence Engine

✗ Decision Engine

✗ Risk Engine

✗ Signal Engine

✗ AI Layer

✗ Platform Layer

✗ User Experience Layer

✗ Business Layer

✗ Learning Layer

✗ Media Layer

✗ Future Expansion Layer

---

# Ownership

CandleBuilder egalik qiladi.

✓ Active Candle

✓ Closed Candle

✓ OHLC Values

✓ Candle Lifecycle

✓ Timeframe Candles

✓ Candle State

✓ Candle Events

CandleBuilder egalik qilmaydi.

✗ Live Stream

✗ Current Price

✗ Validation Logic

✗ Market Memory

✗ Trading Logic

✗ Strategy

✗ Decision

---

# State Contract

CandleBuilder quyidagi holatlarda bo'lishi mumkin.

• Idle

• Waiting Tick

• Updating Candle

• Closing Candle

• Opening New Candle

• Publishing

• Completed

• Failed

---

# Error Contract

CandleBuilder quyidagi xatolarni qaytarishi mumkin.

• Invalid Tick

• Invalid Timeframe

• Invalid Timestamp

• Missing Current Price

• Candle Build Failed

• Candle Publish Failed

• State Error

• Unknown Candle Error

Har qanday xato PriceStreamService tomonidan boshqariladi va Event Bus orqali e'lon qilinadi.

---

# Runtime Contract

1. CandleBuilder faqat Validation'dan o'tgan Tick bilan ishlaydi.

2. Har bir Tick faqat bitta faol Candle'ni yangilaydi.

3. Open narxi Candle ochilganda faqat bir marta belgilanadi.

4. High narxi faqat yuqoriga yangilanadi.

5. Low narxi faqat pastga yangilanadi.

6. Close narxi har bir Tick bilan yangilanadi.

7. Candle yopilgandan keyin qayta o'zgartirilmaydi.

8. Har bir Timeframe mustaqil Candle Lifecycle'ga ega.

9. CandleBuilder faqat tayyor Candle'ni Market Memory'ga uzatadi.

10. CandleBuilder Trading Logic bajarmaydi.

---

# Architecture Rules

CandleBuilder:

✓ OHLC Candle yaratadi.

✓ Active Candle'ni boshqaradi.

✓ Candle Lifecycle'ni boshqaradi.

✓ Multi-Timeframe Candle yaratadi.

✓ Candle Event yaratadi.

✓ Market Memory'ga tayyor Candle uzatadi.

CandleBuilder:

✗ Tick Validation bajarmaydi.

✗ Current Price yaratmaydi.

✗ Live Stream boshqarmaydi.

✗ Trading qilmaydi.

✗ Strategy hisoblamaydi.

✗ Signal yaratmaydi.

✗ Decision chiqarmaydi.

✗ AI ishlatmaydi.

---

# Contract Violations

Quyidagilar Architecture Violation hisoblanadi.

• CandleBuilder → Historical Data import

• CandleBuilder → HistoricalDatabase import

• CandleBuilder → Live Providers import

• CandleBuilder → Context Engine import

• CandleBuilder → Strategy Engine import

• CandleBuilder → Decision Engine import

• CandleBuilder → AI Layer import

• CandleBuilder → Business Layer import

• Validation bajarish

• Current Price yaratish

• Market Memory'ni chetlab o'tish

• Yopilgan Candle'ni qayta o'zgartirish

• Circular Dependency

---

# Acceptance Criteria

CandleBuilder to'g'ri ishlaydi agar:

✓ Har bir Validated Tick qabul qilinsa.

✓ OHLC qiymatlari to'g'ri shakllansa.

✓ Candle Timeframe bo'yicha yopilsa.

✓ Yangi Candle avtomatik ochilsa.

✓ Multi-Timeframe Candle'lar mustaqil ishlasa.

✓ Market Memory yangilansa.

✓ Candle Lifecycle to'liq boshqarilsa.

✓ Arxitektura chegaralari buzilmasa.

---

# Summary

CandleBuilder Contract Live Data modulidagi OHLC Candle Generation komponentining rasmiy arxitektura shartnomasi hisoblanadi.

CandleBuilder Validation'dan o'tgan Tick ma'lumotlarini Canonical OHLC Candle formatiga aylantiruvchi yagona modul hisoblanadi.

Ushbu hujjatda belgilangan Boundary, Dependency, Runtime va Ownership qoidalaridan chetga chiqadigan har qanday implementatsiya **GoldBot Architecture Violation** hisoblanadi.
