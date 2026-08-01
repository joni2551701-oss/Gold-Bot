# CurrentPriceProvider Contracts

Status: CANONICAL

---

# Purpose

Ushbu hujjat CurrentPriceProvider modulining rasmiy Architecture Contract hujjati hisoblanadi.

CurrentPriceProvider Live Data modulining yagona Canonical Current Price Provider hisoblanadi.

Live Provider'dan kelgan barcha Tick ma'lumotlari aynan ushbu modul orqali Current Price ko'rinishiga o'tkaziladi.

Har qanday implementatsiya ushbu Contract talablariga to'liq mos bo'lishi shart.

---

# Module Responsibility

CurrentPriceProvider quyidagi vazifalar uchun javobgar.

✓ Live Tick qabul qilish

✓ Current Price yaratish

✓ Bid Price boshqaruvi

✓ Ask Price boshqaruvi

✓ Mid Price hisoblash (agar yoqilgan bo'lsa)

✓ Current Price Cache

✓ Latest Tick saqlash

✓ Price Publish

CurrentPriceProvider quyidagi vazifalarni bajarmaydi.

✗ Live Stream Management

✗ Provider Connection

✗ Candle Building

✗ Stream Validation

✗ Market Calendar

✗ Historical Data

✗ Historical Storage

✗ Strategy

✗ Decision

✗ Risk

✗ Signal Generation

✗ AI Analysis

---

# Module Boundary

Live Provider

↓

PriceStreamService

↓

CurrentPriceProvider

↓

Stream Validator

↓

Boundary End

---

# Input Contract

CurrentPriceProvider quyidagilarni qabul qiladi.

• Live Tick

• Bid Price

• Ask Price

• Timestamp

• Symbol

• Provider Metadata

---

# Output Contract

CurrentPriceProvider quyidagilarni yaratadi.

• Current Price

• Bid Price

• Ask Price

• Mid Price

• Latest Tick

• Current Price Event

---

# Read Contract

CurrentPriceProvider quyidagilarni o'qishi mumkin.

✓ Live Tick

✓ Provider Status

✓ Configuration

✓ Current Cache

---

# Write Contract

CurrentPriceProvider quyidagilarga yozishi mumkin.

✓ Current Price Cache

✓ Stream Validator

✓ Event Bus

Boshqa modullarga yozish taqiqlanadi.

---

# Allowed Dependencies

CurrentPriceProvider quyidagilar bilan ishlashi mumkin.

✓ PriceStreamService

✓ Live Providers

✓ Stream Validator

✓ Event Bus

✓ Configuration Layer

---

# Forbidden Dependencies

CurrentPriceProvider quyidagilar bilan ishlashi mumkin emas.

✗ Historical Data

✗ HistoricalDataService

✗ Historical Database

✗ Bootstrap

✗ Recovery

✗ Candle Builder

✗ Market Memory

✗ Memory Reader

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

CurrentPriceProvider egalik qiladi.

✓ Current Price

✓ Bid Price

✓ Ask Price

✓ Mid Price

✓ Latest Tick

✓ Latest Timestamp

✓ Current Price Cache

✓ Price Publishing

CurrentPriceProvider egalik qilmaydi.

✗ Live Stream

✗ Candle

✗ Validation

✗ Market Memory

✗ Trading Logic

✗ Strategy

✗ Decision

---

# State Contract

CurrentPriceProvider quyidagi holatlarda bo'lishi mumkin.

• Idle

• Waiting Tick

• Receiving Tick

• Updating Price

• Publishing

• Completed

• Failed

---

# Error Contract

CurrentPriceProvider quyidagi xatolarni qaytarishi mumkin.

• Invalid Tick

• Invalid Symbol

• Invalid Timestamp

• Invalid Price

• Missing Bid

• Missing Ask

• Cache Error

• Publish Failed

• Unknown Price Error

Har qanday xato PriceStreamService tomonidan boshqariladi.

---

# Runtime Contract

1. CurrentPriceProvider faqat PriceStreamService tomonidan boshqariladi.

2. Har bir Tick ketma-ket qayta ishlanishi shart.

3. Current Price har bir Tick kelganda yangilanadi.

4. Current Price Cache faqat eng oxirgi narxni saqlaydi.

5. CurrentPriceProvider Validation bajarmaydi.

6. Validation Stream Validator tomonidan bajariladi.

7. CurrentPriceProvider Candle yaratmaydi.

8. CurrentPriceProvider Market Memory bilan bevosita ishlamaydi.

9. CurrentPriceProvider Live Provider bilan to'g'ridan-to'g'ri ishlamaydi.

10. Tick tartibi buzilmasligi shart.

---

# Architecture Rules

CurrentPriceProvider:

✓ Current Price yaratadi.

✓ Bid va Ask narxlarini boshqaradi.

✓ Latest Tick'ni saqlaydi.

✓ Price Update hodisasini yaratadi.

✓ Stream Validator'ga uzatadi.

CurrentPriceProvider:

✗ Live Stream boshqarmaydi.

✗ Provider ulanishini boshqarmaydi.

✗ Candle yaratmaydi.

✗ Validation bajarmaydi.

✗ Market Memory'ga yozmaydi.

✗ Trading qilmaydi.

✗ Strategy hisoblamaydi.

✗ Signal yaratmaydi.

✗ Decision chiqarmaydi.

---

# Contract Violations

Quyidagilar Architecture Violation hisoblanadi.

• CurrentPriceProvider → Historical Data import

• CurrentPriceProvider → CandleBuilder import

• CurrentPriceProvider → Market Memory import

• CurrentPriceProvider → Context Engine import

• CurrentPriceProvider → Strategy Engine import

• CurrentPriceProvider → Decision Engine import

• CurrentPriceProvider → AI Layer import

• CurrentPriceProvider → Business Layer import

• Validation bajarish

• Candle yaratish

• Market Memory'ga to'g'ridan-to'g'ri yozish

• Circular Dependency

---

# Acceptance Criteria

CurrentPriceProvider to'g'ri ishlaydi agar:

✓ Har bir Live Tick qabul qilinsa.

✓ Current Price to'g'ri yangilansa.

✓ Bid va Ask narxlari saqlansa.

✓ Mid Price (agar yoqilgan bo'lsa) hisoblangan bo'lsa.

✓ Current Price Cache yangilansa.

✓ Stream Validator'ga narx uzatilsa.

✓ Tick tartibi saqlansa.

✓ Boshqa modullarning vazifasi takrorlanmasa.

---

# Summary

CurrentPriceProvider Contract Live Data modulidagi Current Price komponentining rasmiy arxitektura shartnomasi hisoblanadi.

CurrentPriceProvider Live Market'dan kelgan barcha Tick ma'lumotlarini yagona Canonical Current Price formatiga o'tkazuvchi modul hisoblanadi.

U faqat joriy narxni boshqaradi va uni Stream Validator'ga uzatadi. Ushbu hujjatda belgilangan Boundary, Dependency, Runtime va Ownership qoidalaridan chetga chiqadigan har qanday implementatsiya GoldBot Architecture Violation hisoblanadi.
