# Historical Providers Module Map

Status: CANONICAL

---

# Purpose

Ushbu hujjat Historical Providers modulining ichki arxitekturasini, komponentlari va boshqa modullar bilan bog'lanishini tavsiflaydi.

Bu Historical Providers modulining Canonical Architecture Blueprint hisoblanadi.

Bu implementatsiya emas.

---

# Module Position

```text
Configuration Layer

        │
        ▼
 Provider Factory

        │
        ▼
Historical Providers

        │
        ▼
HistoricalDataService

        │
        ▼
Historical Database

        │
        ▼
 Data Validation

        │
        ▼
 Market Memory
```

---

# Module Architecture

```text
                 Historical Providers
                          │
      ┌───────────────────┼────────────────────┐
      ▼                   ▼                    ▼
 Provider Manager   Authentication     Request Builder
      │                   │                    │
      └──────────────┬────┴────────────────────┘
                     ▼
              Historical Provider
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
 API Client     Response Parser  Error Handler
        │            │            │
        └────────────┼────────────┘
                     ▼
             Response Normalizer
                     │
                     ▼
          HistoricalDataService
```

---

# Internal Components

## Provider Manager

Historical Provider tanlash va boshqarish.

Masalan:

- Twelve Data
- Polygon
- CSV
- Future Providers

---

## Authentication

Provider bilan autentifikatsiyani boshqaradi.

Masalan:

- API Key

- Secret

- Token

---

## Request Builder

Provider uchun standart API so'rovini yaratadi.

Masalan:

- Symbol

- Timeframe

- Start Time

- End Time

- Candle Limit

---

## Historical Provider

Tashqi provider bilan bog'lanadi va tarixiy market ma'lumotlarini yuklaydi.

---

## API Client

HTTP yoki boshqa protokol orqali provider bilan aloqa qiladi.

---

## Response Parser

Provider javobini qabul qiladi va ichki obyektlarga ajratadi.

---

## Response Normalizer

Turli providerlardan kelgan ma'lumotlarni yagona GoldBot formatiga o'tkazadi.

---

## Error Handler

Quyidagilarni boshqaradi:

- Timeout

- Network Error

- Invalid Response

- Authentication Error

- Rate Limit

---

## HistoricalDataService

Normalize qilingan ma'lumotni qabul qiladi va keyingi bosqichga uzatadi.

---

# Dependency Map

```text
Configuration

↓

Provider Factory

↓

Historical Providers

↓

Authentication

↓

Request Builder

↓

Historical Provider

↓

API Client

↓

Response Parser

↓

Response Normalizer

↓

HistoricalDataService
```

---

# Allowed Dependencies

Historical Providers quyidagilar bilan ishlashi mumkin.

✓ Configuration Layer

✓ Provider Factory

✓ HistoricalDataService

✓ External Provider APIs

---

# Forbidden Dependencies

Historical Providers quyidagilar bilan ishlashi mumkin emas.

✗ Historical Database

✗ Data Validation

✗ Market Memory

✗ Live Data

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

---

# Input

Historical Providers qabul qiladi:

• Provider Configuration

• Symbol

• Timeframe

• Start Time

• End Time

• Candle Limit

---

# Output

Historical Providers qaytaradi:

• Historical Candles

• OHLC Data

• Volume

• Timestamp

• Provider Status

• Error Status

---

# Ownership

Historical Providers egalik qiladi:

✓ Provider Connection

✓ Authentication

✓ Request Building

✓ Response Parsing

✓ Response Normalization

✓ Provider Error Handling

Historical Providers egalik qilmaydi:

✗ Historical Database

✗ Data Validation

✗ Market Memory

✗ Bootstrap

✗ Recovery

✗ Trading Logic

✗ Analysis

✗ Strategy

✗ Decision

---

# Module Rules

1. Historical Providers faqat tashqi providerlar bilan ishlaydi.

2. Provider Factory yagona provider yaratish nuqtasi hisoblanadi.

3. Har bir provider Provider Interface talablariga mos bo'lishi shart.

4. Har bir javob Normalize qilinishi shart.

5. Historical Providers ma'lumotni saqlamaydi.

6. Historical Providers Validation bajarmaydi.

7. Historical Providers Market Memory bilan ishlamaydi.

8. Historical Providers faqat HistoricalDataService bilan bog'lanadi.

9. Circular Dependency qat'iyan taqiqlanadi.

---

# Summary

Historical Providers Module Map Historical Providers modulining ichki arxitekturasi va komponentlari orasidagi bog'lanishni belgilaydi.

Canonical Architecture:

Configuration

↓

Provider Factory

↓

Historical Providers

↓

Authentication

↓

Request Builder

↓

Historical Provider

↓

API Client

↓

Response Parser

↓

Response Normalizer

↓

HistoricalDataService

Historical Providers Data Layer ichidagi yagona tashqi tarixiy ma'lumot integratsiyasi moduli hisoblanadi.
