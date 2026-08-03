# MarketCalendar Contracts

Status: CANONICAL

---

# Purpose

Ushbu hujjat MarketCalendar modulining rasmiy Architecture Contract hujjati hisoblanadi.

MarketCalendar Live Data modulining yagona Canonical Market Schedule va Trading Session Management komponentidir.

Bozorning ochilishi, yopilishi, sessiyalar, dam olish kunlari va Holiday qoidalari aynan ushbu modul tomonidan boshqariladi.

Har qanday implementatsiya ushbu Contract talablariga to'liq mos bo'lishi shart.

---

# Module Responsibility

MarketCalendar quyidagi vazifalar uchun javobgar.

✓ Trading Session Management

✓ Market Open Detection

✓ Market Close Detection

✓ Trading Hours Management

✓ Holiday Management

✓ Weekend Detection

✓ Time Zone Management

✓ Market Status Publishing

✓ Session Change Events

MarketCalendar quyidagi vazifalarni bajarmaydi.

✗ Live Stream Management

✗ Provider Connection

✗ Current Price Management

✗ Tick Validation

✗ Candle Generation

✗ Historical Data

✗ Historical Storage

✗ Market Memory Storage

✗ Context Analysis

✗ Strategy

✗ Decision

✗ Risk

✗ Signal Generation

✗ AI Analysis

---

# Module Boundary

Configuration Layer

↓

MarketCalendar

↓

PriceStreamService

↓

Boundary End

---

# Input Contract

MarketCalendar quyidagilarni qabul qiladi.

• Current Date

• Current Time

• Time Zone

• Exchange Calendar

• Holiday Calendar

• Trading Schedule

• Exchange Configuration

---

# Output Contract

MarketCalendar quyidagilarni yaratadi.

• Market Status

• Trading Session

• Session Status

• Market Open Event

• Market Close Event

• Session Changed Event

• Holiday Event

• Weekend Event

---

# Read Contract

MarketCalendar quyidagilarni o'qishi mumkin.

✓ Configuration Layer

✓ Exchange Calendar

✓ Holiday Calendar

✓ Time Service

✓ Time Zone Configuration

---

# Write Contract

MarketCalendar quyidagilarga yozishi mumkin.

✓ PriceStreamService

✓ Event Bus

Boshqa modullarga yozish taqiqlanadi.

---

# Allowed Dependencies

MarketCalendar quyidagilar bilan ishlashi mumkin.

✓ Configuration Layer

✓ Time Service

✓ Exchange Calendar

✓ Holiday Calendar

✓ PriceStreamService

✓ Event Bus

---

# Forbidden Dependencies

MarketCalendar quyidagilar bilan ishlashi mumkin emas.

✗ Historical Data

✗ HistoricalDatabase

✗ HistoricalDataService

✗ Live Providers

✗ CurrentPriceProvider

✗ StreamValidator

✗ CandleBuilder

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

MarketCalendar egalik qiladi.

✓ Trading Calendar

✓ Trading Sessions

✓ Trading Hours

✓ Market Status

✓ Holiday Rules

✓ Weekend Rules

✓ Time Zone Rules

✓ Session Events

✓ Market Events

MarketCalendar egalik qilmaydi.

✗ Live Stream

✗ Current Price

✗ Tick

✗ Candle

✗ Market Memory

✗ Trading Logic

✗ Strategy

✗ Decision

---

# State Contract

MarketCalendar quyidagi holatlarda bo'lishi mumkin.

• Initializing

• Market Open

• Market Closed

• Holiday

• Weekend

• Maintenance

• Session Changing

• Waiting

• Failed

---

# Error Contract

MarketCalendar quyidagi xatolarni qaytarishi mumkin.

• InvalidTimeZone

• InvalidTradingSchedule

• CalendarUnavailable

• HolidayCalendarError

• ExchangeCalendarError

• SessionCalculationFailed

• InvalidMarketStatus

• ConfigurationError

• UnknownCalendarError

Har qanday xato PriceStreamService tomonidan boshqariladi va Event Bus orqali e'lon qilinadi.

---

# Runtime Contract

1. MarketCalendar Market Status uchun yagona Canonical modul hisoblanadi.

2. Live Stream faqat Market Open holatida ishlashi mumkin.

3. Market Closed holatida Live Stream ishga tushirilmaydi.

4. Holiday kunlari Market Closed hisoblanadi.

5. Weekend kunlari Market Closed hisoblanadi (konfiguratsiyaga bog'liq istisnolar bundan mustasno).

6. Session almashishi avtomatik aniqlanadi.

7. Time Zone konvertatsiyasi har doim bajarilishi shart.

8. Market Status o'zgarganda Event yaratilishi shart.

9. PriceStreamService faqat MarketCalendar yaratgan Status'dan foydalanadi.

10. MarketCalendar Trading Decision qabul qilmaydi.

---

# Architecture Rules

MarketCalendar:

✓ Trading Calendar'ni boshqaradi.

✓ Trading Session'larni boshqaradi.

✓ Market Status yaratadi.

✓ Holiday va Weekend qoidalarini boshqaradi.

✓ Time Zone'ni boshqaradi.

✓ Session Event'larni yaratadi.

MarketCalendar:

✗ Live Stream boshqarmaydi.

✗ Tick yaratmaydi.

✗ Current Price yaratmaydi.

✗ Candle yaratmaydi.

✗ Market Memory'ga yozmaydi.

✗ Trading qilmaydi.

✗ Strategy hisoblamaydi.

✗ Signal yaratmaydi.

✗ Decision chiqarmaydi.

✗ AI ishlatmaydi.

---

# Contract Violations

Quyidagilar Architecture Violation hisoblanadi.

• MarketCalendar → Historical Data import

• MarketCalendar → Live Providers import

• MarketCalendar → CurrentPriceProvider import

• MarketCalendar → StreamValidator import

• MarketCalendar → CandleBuilder import

• MarketCalendar → Market Memory import

• MarketCalendar → Context Engine import

• MarketCalendar → Strategy Engine import

• MarketCalendar → Decision Engine import

• MarketCalendar → AI Layer import

• MarketCalendar → Business Layer import

• Current Price hisoblash

• Candle yaratish

• Trading Decision chiqarish

• Circular Dependency

---

# Acceptance Criteria

MarketCalendar to'g'ri ishlaydi agar:

✓ Market Open va Market Close holati to'g'ri aniqlansa.

✓ Trading Session'lar to'g'ri boshqarilsa.

✓ Holiday va Weekend qoidalari ishlasa.

✓ Time Zone konvertatsiyasi to'g'ri bajarilsa.

✓ Market Status Event'lari yaratilsa.

✓ PriceStreamService to'g'ri boshqarilsa.

✓ Arxitektura chegaralari buzilmasa.

---

# Summary

MarketCalendar Contract Live Data modulidagi Market Schedule va Trading Session Management komponentining rasmiy arxitektura shartnomasi hisoblanadi.

MarketCalendar bozorning ish vaqtlari, sessiyalari va Market Status'ini boshqaruvchi yagona Canonical modul hisoblanadi.

Ushbu hujjatda belgilangan Boundary, Dependency, Runtime va Ownership qoidalaridan chetga chiqadigan har qanday implementatsiya **GoldBot Architecture Violation** hisoblanadi.
