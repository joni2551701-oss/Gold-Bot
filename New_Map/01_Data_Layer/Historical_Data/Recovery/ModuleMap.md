# Recovery Module Map

Status: CANONICAL

---

# Purpose

Ushbu hujjat Recovery modulining ichki arxitekturasini, modullar orasidagi bog'lanishni va Data Layer ichidagi o'rnini tavsiflaydi.

Bu Recovery modulining Canonical Architecture Blueprint hisoblanadi.

Bu hujjat implementatsiya emas.

---

# Module Position

```text
HistoricalDataService

        │
        ▼
     Recovery

        │
        ▼
  Historical Provider

        │
        ▼
 Historical Database

        │
        ▼
  Data Validation

        │
        ▼
   Market Memory

        │
        ▼
     Event Bus
```

---

# Recovery Architecture

```text
                    Recovery
                        │
     ┌──────────────────┼──────────────────┐
     ▼                  ▼                  ▼
 Gap Detector     Recovery Planner     Retry Manager
     │                  │                  │
     └──────────────┬───┴──────────────────┘
                    ▼
            Historical Provider
                    │
                    ▼
          Historical Database
                    │
                    ▼
            Data Validation
                    │
                    ▼
             Market Memory
                    │
                    ▼
               Event Bus
```

---

# Internal Components

## Gap Detector

Historical Database va Market Memory holatini tekshiradi.

Yetishmayotgan:

- Candle
- Timeframe
- Symbol
- Time Range

ni aniqlaydi.

---

## Recovery Planner

Qaysi ma'lumotlarni qayta yuklash kerakligini rejalashtiradi.

Masalan:

- Symbol
- Timeframe
- Start Time
- End Time

---

## Retry Manager

Provider javob bermasa qayta urinishlarni boshqaradi.

Retry Policy.

Timeout.

Backoff Strategy.

---

## Historical Provider

Missing ma'lumotlarni tashqi providerlardan yuklaydi.

---

## Historical Database

Recovery qilingan ma'lumotlarni saqlaydi.

---

## Data Validation

Recovery qilingan ma'lumotlarni tekshiradi.

---

## Market Memory

Validation'dan o'tgan ma'lumotlarni yangilaydi.

---

## Event Bus

Recovery tugagandan keyin Event yuboradi.

Masalan:

- RecoveryCompleted
- RecoveryFailed

---

# Dependency Map

```text
Recovery

↓

Gap Detector

↓

Recovery Planner

↓

Historical Provider

↓

Historical Database

↓

Data Validation

↓

Market Memory

↓

Event Bus
```

---

# Allowed Dependencies

Recovery quyidagilar bilan ishlashi mumkin.

✓ HistoricalDataService

✓ Historical Provider

✓ Historical Database

✓ Data Validation

✓ Market Memory

✓ Event Bus

✓ Configuration Layer

---

# Forbidden Dependencies

Recovery quyidagilar bilan ishlashi mumkin emas.

✗ Live_Data

✗ CurrentPriceProvider

✗ CandleBuilder

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

Recovery qabul qiladi:

• Recovery Request

• Missing Range

• Symbol

• Timeframe

• Historical Provider

---

# Output

Recovery yaratadi:

• Recovered Historical Data

• Recovery Status

• Updated Historical Database

• Updated Market Memory

• Recovery Events

---

# Ownership

Recovery egalik qiladi:

✓ Gap Detection

✓ Missing Data Recovery

✓ Recovery Planning

✓ Retry Management

Recovery egalik qilmaydi:

✗ Bootstrap

✗ Live Streaming

✗ Current Price

✗ Market Analysis

✗ Strategy

✗ Decision

✗ Risk

✗ Signal

---

# Module Rules

1. Recovery faqat HistoricalDataService tomonidan boshqariladi.

2. Recovery faqat yetishmayotgan ma'lumotlarni tiklaydi.

3. Recovery Provider orqali ishlaydi.

4. Validation majburiy.

5. Validation'dan o'tmagan ma'lumot Market Memory'ga yozilmaydi.

6. Recovery tugagandan keyin Event Bus hodisa yuboradi.

7. Recovery Bootstrap jarayonini takrorlamaydi.

8. Circular Dependency qat'iyan taqiqlanadi.

---

# Summary

Recovery Module Map Recovery modulining ichki arxitekturasi va bog'lanishlarini belgilaydi.

Recovery quyidagi asosiy oqim bo'yicha ishlaydi:

Recovery

↓

Gap Detection

↓

Recovery Planning

↓

Historical Provider

↓

Historical Database

↓

Data Validation

↓

Market Memory

↓

Event Bus

Recovery Data Layer ichidagi mustaqil modul bo'lib, faqat tarixiy ma'lumotlarni tiklash uchun javobgardir.
