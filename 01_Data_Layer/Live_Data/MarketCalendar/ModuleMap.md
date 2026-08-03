# MarketCalendar Module Map

Status: CANONICAL

---

# Purpose

Ushbu hujjat MarketCalendar modulining ichki arxitekturasini, komponentlarini va boshqa modullar bilan bog'lanishini tavsiflaydi.

MarketCalendar Live Data modulidagi yagona Canonical Market Schedule va Trading Session Management komponenti hisoblanadi.

Bu implementatsiya emas.

Bu MarketCalendar modulining Canonical Architecture Blueprint hisoblanadi.

---

# Module Position

```text
                 Configuration Layer
                          │
                          ▼
                  MarketCalendar
                          │
                          ▼
                PriceStreamService
                          │
                          ▼
                  Live Providers
                          │
                          ▼
              CurrentPriceProvider
                          │
                          ▼
                 StreamValidator
                          │
                          ▼
                  CandleBuilder
                          │
                          ▼
                  Market Memory
                          │
                          ▼
                  Memory Reader
                          │
                          ▼
                     GoldBot Core
```

---

# Module Architecture

```text
                  MarketCalendar
                         │
      ┌──────────────────┼──────────────────┐
      ▼                  ▼                  ▼
 Calendar Manager   Session Manager   State Manager
      │                  │                  │
      └──────────────────┼──────────────────┘
                         ▼
               Trading Hours Manager
                         │
                         ▼
                 Holiday Manager
                         │
                         ▼
                 Weekend Manager
                         │
                         ▼
                 TimeZone Manager
                         │
                         ▼
               Market Status Manager
                         │
                         ▼
                 Event Publisher
                         │
                         ▼
                PriceStreamService
```

---

# Internal Components

## Calendar Manager

Trading Calendar'ni boshqaradi.

Mas'ul:

- Trading Days

- Trading Sessions

- Calendar Loading

---

## Session Manager

Bozor sessiyalarini boshqaradi.

Mas'ul:

- Session Start

- Session End

- Session Switching

Masalan:

- Asia

- London

- New York

---

## State Manager

MarketCalendar holatini boshqaradi.

Holatlar:

- Initializing

- Market Open

- Market Closed

- Holiday

- Weekend

- Maintenance

---

## Trading Hours Manager

Bozorning ish vaqtlarini boshqaradi.

Tekshiradi:

- Open Time

- Close Time

- Trading Window

---

## Holiday Manager

Rasmiy dam olish kunlarini boshqaradi.

Tekshiradi:

- Public Holiday

- Exchange Holiday

- Emergency Closure

---

## Weekend Manager

Dam olish kunlarini boshqaradi.

Tekshiradi:

- Saturday

- Sunday

- Custom Weekend

---

## TimeZone Manager

Barcha vaqtlarni standart Time Zone'ga moslashtiradi.

Mas'ul:

- UTC Conversion

- Exchange Time

- Session Time

---

## Market Status Manager

Joriy Market Status'ni yaratadi.

Statuslar:

- Open

- Closed

- Holiday

- Weekend

- Maintenance

---

## Event Publisher

Market Status hodisalarini e'lon qiladi.

Masalan:

- Market Open

- Market Close

- Session Changed

- Holiday Started

---

# Dependency Map

```text
Configuration Layer

↓

MarketCalendar

↓

Calendar Manager

↓

Session Manager

↓

Trading Hours Manager

↓

Holiday Manager

↓

Weekend Manager

↓

TimeZone Manager

↓

Market Status Manager

↓

Event Publisher

↓

PriceStreamService

↓

Live Data Pipeline
```

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

# Input

MarketCalendar qabul qiladi:

• Current Date

• Current Time

• Time Zone

• Exchange Calendar

• Holiday Calendar

• Trading Schedule

---

# Output

MarketCalendar yaratadi:

• Market Status

• Trading Session

• Session Status

• Market Open Event

• Market Close Event

• Holiday Event

• Session Change Event

---

# Ownership

MarketCalendar egalik qiladi:

✓ Trading Calendar

✓ Trading Sessions

✓ Market Status

✓ Holiday Rules

✓ Weekend Rules

✓ Time Zone Rules

✓ Trading Schedule

✓ Market Events

MarketCalendar egalik qilmaydi:

✗ Live Stream

✗ Current Price

✗ Tick

✗ Candle

✗ Market Memory

✗ Trading Logic

✗ Strategy

✗ Decision

---

# Module Rules

1. MarketCalendar Market Status uchun yagona Canonical modul hisoblanadi.

2. Trading Session faqat MarketCalendar tomonidan boshqariladi.

3. Holiday va Weekend qoidalari shu modulda aniqlanadi.

4. Time Zone konvertatsiyasi har doim bajariladi.

5. PriceStreamService faqat Market Status'dan foydalanadi.

6. MarketCalendar Live Market Data bilan ishlamaydi.

7. MarketCalendar narxlarni qayta ishlamaydi.

8. MarketCalendar Trading Decision chiqarmaydi.

9. Circular Dependency qat'iyan taqiqlanadi.

---

# Summary

MarketCalendar Module Map Live Data modulidagi Trading Schedule va Market Status komponentining ichki arxitekturasini belgilaydi.

Canonical Module Flow:

Configuration Layer

↓

MarketCalendar

↓

Calendar Manager

↓

Session Manager

↓

Trading Hours Manager

↓

Holiday Manager

↓

Weekend Manager

↓

TimeZone Manager

↓

Market Status Manager

↓

Event Publisher

↓

PriceStreamService

↓

Live Data Pipeline

MarketCalendar Live Data Pipeline ichidagi yagona Canonical Market Schedule va Trading Session Management moduli hisoblanadi.
