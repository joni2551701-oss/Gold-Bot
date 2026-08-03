# Market Calendar

Status: CANONICAL

---

# Purpose

MarketCalendar — Live Data modulining bozor holatini (Market Status) boshqaruvchi komponentidir.

Uning asosiy vazifasi qaysi bozorlarda savdo ochiq yoki yopiq ekanligini aniqlash va PriceStreamService'ga Live Stream'ni qachon boshlash yoki to'xtatish kerakligini bildiradi.

MarketCalendar narxlarni qabul qilmaydi, Candle yaratmaydi va Trading Decision qabul qilmaydi.

U faqat bozor vaqtini va sessiyalarni boshqaradi.

---

# Objective

MarketCalendar quyidagi vazifalarni bajaradi:

• Market Session Management

• Trading Hours Management

• Exchange Calendar Management

• Holiday Management

• Weekend Detection

• Market Open Detection

• Market Close Detection

• Session Status Publishing

---

# Layer Position

```text
Configuration Layer

↓

MarketCalendar

↓

PriceStreamService

↓

Live Providers

↓

CurrentPriceProvider

↓

StreamValidator

↓

CandleBuilder

↓

Market Memory

↓

GoldBot Core
```

---

# Responsibilities

MarketCalendar:

✓ Market Open aniqlash

✓ Market Close aniqlash

✓ Trading Session boshqarish

✓ Holiday tekshirish

✓ Weekend tekshirish

✓ Exchange Calendar boshqarish

✓ Session Status yaratish

✓ PriceStreamService'ga Market Status uzatish

---

# Not Responsible

MarketCalendar:

✗ Live Stream Management

✗ Provider Connection

✗ Current Price Management

✗ Tick Validation

✗ Candle Generation

✗ Historical Data

✗ Historical Database

✗ Market Memory

✗ Context Analysis

✗ Strategy

✗ Decision

✗ Risk

✗ Signal Generation

✗ AI Analysis

---

# Input

MarketCalendar quyidagilarni qabul qiladi:

• Current Date

• Current Time

• Time Zone

• Exchange Configuration

• Holiday Calendar

---

# Output

MarketCalendar quyidagilarni yaratadi:

• Market Status

• Session Status

• Trading Session

• Market Open Event

• Market Close Event

• Trading Schedule

---

# Managed Data

MarketCalendar quyidagi ma'lumotlarni boshqaradi:

• Trading Hours

• Trading Days

• Holidays

• Weekends

• Session Schedule

• Exchange Time Zone

• Market Status

---

# Workflow

```text
Current Time

↓

MarketCalendar

↓

Market Status

↓

PriceStreamService

↓

Live Providers

↓

Live Data Pipeline
```

---

# Golden Rules

1. MarketCalendar Live Data modulining yagona Market Schedule manbai hisoblanadi.

2. Live Stream faqat Market Open holatida ishlaydi.

3. Market Closed bo'lsa Live Provider ishga tushmaydi.

4. Holiday kunlari Market Closed hisoblanadi.

5. Weekend kunlari Market Closed hisoblanadi (bozor turiga qarab istisnolar konfiguratsiya orqali belgilanadi).

6. Session almashishi avtomatik aniqlanadi.

7. MarketCalendar narx ma'lumotlari bilan ishlamaydi.

8. MarketCalendar Trading Logic'dan mustaqil bo'lishi shart.

---

# Related Documents

```text
MarketCalendar/

├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```

---

# Summary

MarketCalendar — Live Data modulining bozor jadvali va sessiyalarini boshqaruvchi komponentidir.

Uning vazifasi:

• Market Open va Market Close holatini aniqlash;

• Trading Session'larni boshqarish;

• Holiday va Weekend'larni hisobga olish;

• PriceStreamService'ga Live Stream uchun ruxsat berish yoki to'xtatish.

MarketCalendar Live Data Pipeline ichidagi yagona Canonical Market Schedule moduli hisoblanadi.
